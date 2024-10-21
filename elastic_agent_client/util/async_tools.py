#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License 2.0;
# you may not use this file except in compliance with the Elastic License 2.0.
#
import asyncio
import time

from elastic_agent_client.util.logger import logger


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


def _get_uvloop():
    import uvloop

    return uvloop


def get_event_loop():
    # activate uvloop if lib is present
    try:
        asyncio.set_event_loop_policy(_get_uvloop().EventLoopPolicy())
    except Exception as e:
        logger.warning(f"Unable to enable uvloop: {e}. Running with default event loop")
        pass
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop_policy().get_event_loop()
        if loop is None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    return loop


class BaseService:
    """Base class for creating a service.

    Any class deriving from this class will get added to the registry,
    given its `name` class attribute (unless it's not set).

    A concrete service class needs to implement `_run`.
    """

    name: str

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
            logger.exception(
                f"Exception found for task {task.get_name()}: {task.exception()}",
                exc_info=task.exception(),
            )


class MultiService:
    """Wrapper class to run multiple services against the same client."""

    def __init__(self, *services):
        self._services = services

    async def run(self):
        """Runs every service in a task and wait for all tasks."""
        tasks = [
            asyncio.create_task(service.run(), name=service.name)
            for service in self._services
        ]

        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

        exception = None
        for task in done:
            if task.done() and not task.cancelled():
                if task.exception():
                    logger.exception(
                        f"Exception found for task {task.get_name()}: {task.exception()}",
                        exc_info=task.exception(),
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
        try:
            item = await self.queue.get()
        except Exception as e:
            raise StopAsyncIteration() from e
        else:
            return item


class AsyncIterator:
    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration as ex:
            raise StopAsyncIteration from ex
