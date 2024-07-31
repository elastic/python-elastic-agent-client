#!/usr/bin/env python3
import asyncio
import functools
import signal
import sys

from es_agent_client.client import V2, V2Options, VersionInfo
from es_agent_client.generated import elastic_agent_client_pb2 as proto
from es_agent_client.handler.action import BaseActionHandler
from es_agent_client.handler.checkin import BaseCheckinHandler
from es_agent_client.reader import new_v2_from_reader
from es_agent_client.service.actions import ActionsService
from es_agent_client.service.checkin import CheckinV2Service
from es_agent_client.util.async_tools import (
    BaseService,
    MultiService,
    get_event_loop,
    sleeps_for_retryable,
)
from es_agent_client.util.logger import logger

sys.path.append("/Users/jedr/connectors-python")

from connectors import service_cli

CONNECTOR_SERVICE = "connector-service"


class ConnectorActionHandler(BaseActionHandler):
    async def handle_action(self, action: proto.ActionRequest):
        msg = (
            f"This connector component can't handle action requests. Received: {action}"
        )
        raise NotImplementedError(msg)


class ConnectorServiceManager(BaseService):

    name = "connector-serivce-manager"

    def __init__(self, client, initial_config):
        super().__init__(client, "connector-service-manager")
        self.config = initial_config
        self.connector_services = []
        self._multi_service = None

    async def _run(self):
        try:
            await self.setup_connectors()
            if self._multi_service:
                await self._multi_service.run()
        except Exception as e:
            logger.exception(f"Error in ConnectorServiceManager: {e}")
            raise

    async def setup_connectors(self):
        try:
            self.connector_services = service_cli.get_connector_services(
                self.config, log_level="INFO"
            )
            self._multi_service = MultiService(*self.connector_services)
        except Exception as e:
            logger.exception(f"Error setting up connectors: {e}")
            raise

    def stop(self):
        super().stop()
        for connector in self.connector_services:
            connector.stop()

    async def update_config(self, new_config):
        try:
            self.config.update(new_config)
            self.stop()
            self.connector_services.clear()
            await self.setup_connectors()
            asyncio.create_task(self.run())
        except Exception as e:
            logger.exception(f"Error updating config: {e}")
            raise


class ConnectorCheckinHandler(BaseCheckinHandler):
    def __init__(
        self,
        client: V2,
        connector_service_manager: ConnectorServiceManager,
    ):
        super().__init__(client)
        self.connector_service_manager = connector_service_manager

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
                # if (
                #     source.fields.get("hosts")
                #     and source.fields.get("username")
                #     and source.fields.get("password")
                # ):
                #     logger.info("instantiating ES client")
                #     self.output_service.create_es_client(
                #         source["hosts"], source["username"], source["password"]
                #     )
                if source.fields.get("hosts") and (
                    source.fields.get("api_key")
                    or source.fields.get("username")
                    and source.fields.get("password")
                ):
                    logger.info("updating connector service manager config")

                    es_creds = {
                        "host": source["hosts"][0],
                    }

                    if source.fields.get("api_key"):
                        es_creds["api_key"] = source["api_key"]
                    elif source.fields.get("username") and source.fields.get(
                        "password"
                    ):
                        es_creds["username"] = source["username"]
                        es_creds["password"] = source["password"]
                    else:
                        raise ValueError("Invalid Elasticsearch credentials")

                    new_config = {"elasticsearch": es_creds}

                    # This assumes the connector service offers "native" experience
                    # If adding specigic connecptor you need to hardcode here
                    # new_config["connectors"] = [{"connector_id": ...., "service_type": ..., "api_key": ....}]

                    # this restarts all connector services
                    # this should happen only when user changes the target elasticsearch output
                    # in agent policy
                    await self.connector_service_manager.update_config(new_config)


def main():
    try:
        logger.info("Hello, this is the Connector Component - Py")
        run()
    except Exception as e:
        logger.exception(e)
        return 1
    return 0


def run():
    ver = VersionInfo(name=CONNECTOR_SERVICE, meta={"input": CONNECTOR_SERVICE})
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
    action_handler = ConnectorActionHandler()
    connector_service_manager = ConnectorServiceManager(client, {})
    checkin_handler = ConnectorCheckinHandler(client, connector_service_manager)
    multi_service = MultiService(
        CheckinV2Service(client, checkin_handler),
        ActionsService(client, action_handler),
        connector_service_manager,
    )

    def _shutdown(signal_name):
        sleeps_for_retryable.cancel(signal_name)
        multi_service.shutdown(signal_name)

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, functools.partial(_shutdown, sig.name))

    return await multi_service.run()


if __name__ == "__main__":
    sys.exit(main())
