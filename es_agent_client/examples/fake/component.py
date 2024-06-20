#!/usr/bin/env python3
import sys
import asyncio
import signal
import functools


from es_agent_client.util.logger import logger
from es_agent_client.client import VersionInfo, V2Options
from es_agent_client.service.checkin import CheckinV2Service
from es_agent_client.service.actions import ActionsService
from es_agent_client.reader import new_v2_from_reader
from es_agent_client.util.async_tools import get_event_loop, sleeps_for_retryable, MultiService

FAKE = "fake"


def main(args=None):
    try:
        logger.info("Hello, this is the Fake Component - Py")
        run()
    except Exception as e:
        logger.exception(e)
        return 1
    return 0


def run():
    ver = VersionInfo(
        name=FAKE,
        meta={
            "input": FAKE
        }
    )
    opts = V2Options()
    run_loop(sys.stdin.buffer, ver, opts)


def run_loop(buffer, ver, opts):
    loop = get_event_loop()
    coro = _start_service(loop, buffer, ver, opts)

    try:
        return loop.run_until_complete(coro)
    except asyncio.CancelledError:
        return 0
    finally:
        logger.info("Bye")


async def _start_service(loop, buffer, ver, opts):
    client = new_v2_from_reader(buffer, ver, opts)
    multi_service = MultiService(CheckinV2Service(client), ActionsService(client, handle_action))

    def _shutdown(signal_name):
        sleeps_for_retryable.cancel(signal_name)
        multi_service.shutdown(signal_name)

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, functools.partial(_shutdown, sig.name))

    return await multi_service.run()


def handle_action(action):
    raise NotImplementedError(f"This fake component can't handle action requests. Received: {action}")


if __name__ == "__main__":
    sys.exit(main())
