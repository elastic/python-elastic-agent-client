import asyncio
from es_agent_client.util.logger import logger
import time


class CancellableSleeps:
    def __init__(self):
        self._sleeps = set()

    async def sleep(self, delay, result=None, *, loop=None):
        async def _sleep(delay, result=None, *, loop=None):
            coro = asyncio.sleep(delay, result=result)
            task = asyncio.ensure_future(coro)
            self._sleeps.add(task)
            try:
                return await task
            except asyncio.CancelledError:
                logger.debug("Sleep canceled")
                return result
            finally:
                self._sleeps.remove(task)

        await _sleep(delay, result=result, loop=loop)

    def cancel(self, sig=None):
        if sig:
            logger.debug(f"Caught {sig}. Cancelling sleeps...")
        else:
            logger.debug("Cancelling sleeps...")

        for task in self._sleeps:
            task.cancel()


sleeps_for_retryable = CancellableSleeps()

_SERVICES = {}


def get_event_loop():

    # activate uvloop if lib is present
    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except Exception as e:
        logger.warning(
            f"Unable to enable uvloop: {e}. Running with default event loop"
        )
        pass
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop_policy().get_event_loop()
        if loop is None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    return loop





def get_services(names, client):
    """Instantiates a list of services given their names and a client.

    returns a `MultiService` instance.
    """
    return MultiService(*[get_service(name, client) for name in names])


def get_service(name, client):
    """Instantiates a service object given a name and a client"""
    return _SERVICES[name](client)




class BaseService():
    """Base class for creating a service.

    Any class deriving from this class will get added to the registry,
    given its `name` class attribute (unless it's not set).

    A concrete service class needs to implement `_run`.
    """

    name = None  # using None here avoids registering this class

    def __init__(self, client, service_name):
        self.running = False
        self._sleeps = CancellableSleeps()
        self.errors = [0, time.time()]

    def stop(self):
        self.running = False
        self._sleeps.cancel()

    async def _run(self):
        raise NotImplementedError()

    async def run(self):
        """Runs the service"""
        if self.running:
            msg = f"{self.__class__.__name__} is already running."
            raise Exception(msg)

        self.running = True
        try:
            await self._run()
        finally:
            self.stop()

    def _callback(self, task):
        if task.cancelled():
            logger.error(
                f"Task {task.get_name()} was cancelled",
            )
        elif task.exception():
            logger.error(
                f"Exception found for task {task.get_name()}: {task.exception()}",
            )


class MultiService:
    """Wrapper class to run multiple services against the same client."""

    def __init__(self, *services):
        self._services = services

    async def run(self):
        """Runs every service in a task and wait for all tasks."""
        tasks = [asyncio.create_task(service.run(), name=service.name) for service in self._services]

        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

        exception = None
        for task in done:
            if task.done() and not task.cancelled():
                if task.exception():
                    logger.error(
                        f"Exception found for task {task.get_name()}: {task.exception()}",
                    )
                    exception = task.exception()

        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                logger.error("Service did not handle cancellation gracefully.")

        if exception:
            raise exception

    def shutdown(self, sig):
        logger.info(f"Caught {sig}. Graceful shutdown.")

        for service in self._services:
            logger.debug(f"Shutting down {service.__class__.__name__}...")
            service.stop()
            logger.debug(f"Done shutting down {service.__class__.__name__}...")


class AsyncQueueIterator:

    def __init__(self, queue):
        self.queue = queue

    def __aiter__(self):
        return self

    async def __anext__(self):
        while self.queue.empty():
            await asyncio.sleep(1) # TODO this seems wrong

        return self.queue.get()
