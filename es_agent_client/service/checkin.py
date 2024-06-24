import asyncio
import functools
import json

import es_agent_client.generated.elastic_agent_client_pb2 as proto
from es_agent_client.util.async_tools import AsyncQueueIterator, BaseService
from es_agent_client.handler.checkin import BaseCheckinHandler
from es_agent_client.client import V2
from es_agent_client.util.logger import logger
from asyncio import sleep
from google.protobuf.json_format import MessageToJson


class CheckinV2Service(BaseService):
    name = "checkinV2"
    CHECKIN_INTERVAL = 5

    def __init__(self, client: V2, checkin_handler: BaseCheckinHandler):
        super().__init__(client, "checkinV2")
        logger.info("Initializing the checkin service")
        self.client = client
        self.checkin_handler = checkin_handler

    async def _run(self):
        send_queue = asyncio.Queue()
        checkin_stream = self.client.client.CheckinV2(AsyncQueueIterator(send_queue))

        send_checkins_task = asyncio.create_task(self.send_checkins(send_queue), name="Checkin Writer")
        receive_checkins_task = asyncio.create_task(self.receive_checkins(checkin_stream), name="Checkin Reader")
        send_checkins_task.add_done_callback(functools.partial(self._callback))
        receive_checkins_task.add_done_callback(functools.partial(self._callback))

        try:
            await asyncio.wait([send_checkins_task, receive_checkins_task])
        except Exception:
            send_checkins_task.cancel()
            receive_checkins_task.cancel()
            raise

    async def send_checkins(self, send_queue):
        while self.running:
            if send_queue.empty():
                await self.do_checkin(send_queue)
            await sleep(self.CHECKIN_INTERVAL)

    async def receive_checkins(self, checkin_stream):
        checkin: proto.CheckinExpected
        logger.info("Listening for checkin events...")
        async for checkin in checkin_stream:
            logger.info("Received a checkin event from CheckinV2")
            logger.info(f"ExpectedCheckin is: {json.dumps(json.loads(MessageToJson(checkin)))}")
            await self.apply_expected(checkin)
            await sleep(0)

    async def apply_expected(self, checkin: proto.CheckinExpected):
        logger.info("applying CheckinExpected")
        self.client.agent_info = proto.AgentInfo(
            id=checkin.agent_info.id,
            version=checkin.agent_info.version,
            snapshot=checkin.agent_info.snapshot
        )
        self.client.sync_component(checkin)
        self.client.sync_units(checkin)
        await self.checkin_handler.apply_from_client()

    async def do_checkin(self, send_queue):
        logger.info("Checking in....")
        units_observed = [unit.to_observed() for unit in self.client.units]

        if not self.client.version_info_sent:
            version_info = proto.CheckinObservedVersionInfo(
                name=self.client.version_info.name,
                meta=self.client.version_info.meta,
                build_hash=self.client.version_info.build_hash
            )
            if self.client.opts.chunking_allowed:
                supports = [proto.ConnectionSupports.CheckinChunking]
            else:
                supports = []

        else:
            version_info = None
            supports = []
        msg = proto.CheckinObserved(
            token=self.client.token,
            units=units_observed,
            version_info=version_info,
            features_idx=self.client.features_idx,
            component_idx=self.client.component_idx,
            supports=supports
        )
        await send_queue.put(msg)
