import asyncio
import queue
import functools
import json

import es_agent_client.generated.elastic_agent_client_pb2 as proto
from es_agent_client.generated.elastic_agent_client_pb2_grpc import ElasticAgentStub
from es_agent_client.generated.elastic_agent_client_future_pb2_grpc import ElasticAgentStore, ElasticAgentArtifact, ElasticAgentLog

from es_agent_client.util.logger import logger
from es_agent_client.util.async_tools import BaseService
from asyncio import sleep
from google.protobuf.json_format import MessageToJson


class VersionInfo:
    def __init__(self, name, meta, build_hash=None):
        self.name = name
        self.meta = meta
        self.build_hash = build_hash


class V2Options:
    def __init__(self, max_message_size=None, chunking_allowed=None, agent_info: proto.AgentInfo = None):
        self.max_message_size = max_message_size
        self.chunking_allowed = chunking_allowed
        self.agent_info = agent_info
        self.credentials = None


class Unit:
    def __init__(self):
        self.id: str = None
        self.unit_type: proto.UnitType = None
        self.expected_state: proto.State = None
        self.log_level: proto.UnitLogLevel = None
        self.config: proto.UnitExpectedConfig = None
        self.config_idx: int = None
        self.features: proto.Features = None
        self.features_idx: int = None
        self.apm: proto.APMConfig = None
        self.state: proto.State = None
        self.state_msg: str = None
        self.state_payload: dict = None
        self.actions: dict = None
        self.client: V2 = None
        self.diag_hooks: dict = None

    def to_observed(self) -> proto.UnitObserved:
        return proto.UnitObserved(
            id=self.id,
            type=proto.UnitType(self.unit_type),
            config_state_idx=self.config_idx,
            state=proto.State(self.state),
            message=self.state_msg,
            payload=self.state_payload
        )



class V2:
    def __init__(self):
        self.target: str = None
        self.opts: V2Options = None
        self.token: str = None
        self.agent_info: proto.AgentInfo = None
        self.version_info: VersionInfo = None
        self.version_info_sent: bool = None
        self.client: ElasticAgentStub = None
        self.store_client: ElasticAgentStore = None
        self.artifact_client: ElasticAgentArtifact = None
        self.log_client: ElasticAgentLog = None
        self.units: list[Unit] = None
        self.features_idx: int = None
        self.component_idx: int = None
        self.component_config: proto.Component = None

    def __str__(self):
        return f"V2 Client: (agent id: {self.agent_info.id}, agent version: {self.agent_info.version}, name: {self.version_info.name}, target: {self.target})"

    def sync_component(self, checkin: proto.CheckinExpected):
        pass # TODO

    def sync_units(self, checkin: proto.CheckinExpected):
        pass # TODO


class CheckinV2Service(BaseService):
    name = "checkinV2"
    CHECKIN_INTERVAL = 5

    def __init__(self, client: V2):
        super().__init__(client, "checkinV2")
        logger.info("Initializing the checkin service")
        self.client = client

    async def _run(self):
        logger.info("_run called on checkin service")
        send_queue = queue.SimpleQueue()
        checkin_stream = self.client.client.CheckinV2(iter(send_queue.get, None))

        send_checkins_task = asyncio.create_task(self.send_checkins(send_queue), name="Checkin Writer")
        receive_checkins_task = asyncio.create_task(self.receive_checkins(checkin_stream), name="Checkin Reader")
        send_checkins_task.add_done_callback(functools.partial(self._callback))
        receive_checkins_task.add_done_callback(functools.partial(self._callback))

        try:
            logger.info("awaiting gathered tasks...")
            await asyncio.wait([send_checkins_task, receive_checkins_task])
        except Exception:
            send_checkins_task.cancel()
            receive_checkins_task.cancel()
            raise

    async def send_checkins(self, send_queue):
        logger.info("Inside send_checkins()")
        while self.running:
            self.do_checkin(send_queue)
            await sleep(self.CHECKIN_INTERVAL)

    async def receive_checkins(self, checkin_stream):
        current_checkin: proto.CheckinExpected = None
        checkin: proto.CheckinExpected
        logger.info("Listening for checkin events...")
        for checkin in checkin_stream:
            checkin_str = json.dumps(json.loads(MessageToJson(checkin))) # TODO, this is super inefficient and should be removed
            logger.info(f"received a checkin event from CheckinV2: {checkin_str}")
            if current_checkin is None:
                current_checkin = checkin
            elif checkin.units_timestamp != current_checkin.units_timestamp:
                current_checkin = checkin
            if len(checkin.units) == 0:
                self.apply_expected(current_checkin)
            if current_checkin != checkin:
                current_checkin.units.extend(checkin.units)
            await sleep(10)

    def apply_expected(self, checkin: proto.CheckinExpected):
        self.client.agent_info = proto.AgentInfo(
            id=checkin.agent_info.id,
            version=checkin.agent_info.version,
            snapshot=checkin.agent_info.snapshot
        )
        self.client.sync_component(checkin)
        self.client.sync_units(checkin)

    def do_checkin(self, send_queue):
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
        send_queue.put(msg)
