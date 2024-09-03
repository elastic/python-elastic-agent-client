#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License 2.0;
# you may not use this file except in compliance with the Elastic License 2.0.
#
# !/usr/bin/env python3
import asyncio
import functools
import signal
import sys
from typing import Optional

from elasticsearch import AsyncElasticsearch

from elastic_agent_client.client import V2, V2Options, VersionInfo
from elastic_agent_client.generated import elastic_agent_client_pb2 as proto
from elastic_agent_client.handler.action import BaseActionHandler
from elastic_agent_client.handler.checkin import BaseCheckinHandler
from elastic_agent_client.reader import new_v2_from_reader
from elastic_agent_client.service.actions import ActionsService
from elastic_agent_client.service.checkin import CheckinV2Service
from elastic_agent_client.util.async_tools import (
    BaseService,
    MultiService,
    get_event_loop,
    sleeps_for_retryable,
)
from elastic_agent_client.util.logger import logger

FAKE = "fake"


class FakeActionHandler(BaseActionHandler):
    async def handle_action(self, action: proto.ActionRequest):
        msg = f"This fake component can't handle action requests. Received: {action}"
        raise NotImplementedError(msg)


class FakeOutputService(BaseService):
    name = FAKE

    def __init__(self, agent_client: V2):
        super().__init__(agent_client, self.name)
        self.agent_client: V2 = agent_client
        self.es_client: Optional[AsyncElasticsearch] = None

    async def _run(self):
        await asyncio.sleep(0)
        while self.es_client is None:
            logger.info("Waiting to receive Elasticsearch output configuration...")
            await asyncio.sleep(5)

        await self.es_client.perform_request(
            "PUT",
            "/test-fake/_doc/1",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            body={"message": "Hello, Fake World!"},
        )
        logger.info("Successfully wrote 'hello world' to Elasticsearch")

    def create_es_client(self, hosts, username, password):
        options = {
            "hosts": hosts,
            "request_timeout": 120,
            "retry_on_timeout": True,
        }
        auth = username, password
        options["basic_auth"] = auth
        options["headers"] = {}
        options["headers"]["user-agent"] = "py-es-agent-client/fake"
        options["headers"]["X-elastic-product-origin"] = "py-es-agent-client"
        self.es_client = AsyncElasticsearch(**options)


class FakeCheckinHandler(BaseCheckinHandler):
    def __init__(self, client: V2, output_service: FakeOutputService):
        super().__init__(client)
        self.output_service = output_service

    async def apply_from_client(self):
        logger.info("There's new information for the components/units!")
        if self.client.units:
            outputs = [
                unit
                for unit in self.client.units
                if unit.unit_type == proto.UnitType.OUTPUT
            ]
            if len(outputs) > 0 and outputs[0].config:
                source = outputs[0].config.source
                if (
                    source.fields.get("hosts")
                    and source.fields.get("username")
                    and source.fields.get("password")
                ):
                    logger.info("instantiating ES client")
                    self.output_service.create_es_client(
                        source["hosts"], source["username"], source["password"]
                    )


def main():
    try:
        logger.info("Hello, this is the Fake Component - Py")
        run()
    except Exception as e:
        logger.exception(e)
        return 1
    return 0


def run():
    ver = VersionInfo(name=FAKE, meta={"input": FAKE})
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
    output_service = FakeOutputService(client)
    action_handler = FakeActionHandler()
    checkin_handler = FakeCheckinHandler(client, output_service)
    multi_service = MultiService(
        CheckinV2Service(client, checkin_handler),
        ActionsService(client, action_handler),
        output_service,
    )

    def _shutdown(signal_name):
        sleeps_for_retryable.cancel(signal_name)
        multi_service.shutdown(signal_name)

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, functools.partial(_shutdown, sig.name))

    return await multi_service.run()


if __name__ == "__main__":
    sys.exit(main())
