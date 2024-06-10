import queue

import es_agent_client.generated.elastic_agent_client_pb2 as proto
from es_agent_client.generated.elastic_agent_client_pb2_grpc import ElasticAgentStub
from es_agent_client.generated.elastic_agent_client_future_pb2_grpc import ElasticAgentStore, ElasticAgentArtifact, ElasticAgentLog

from es_agent_client.util.logger import logger
from es_agent_client.util.async_tools import BaseService
from asyncio import sleep


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
        return f"""
        V2 Client
          agent id: {self.agent_info.id}
          agent version: {self.agent_info.version}
          name: {self.version_info.name}
          target: {self.target}
        """

    def sync_component(self, checkin: proto.CheckinExpected):
        pass # TODO

    def sync_units(self, checkin: proto.CheckinExpected):
        pass # TODO


class CheckinV2Service(BaseService):
    name = "checkinV2"

    def __init__(self, client: V2):
        super().__init__(client, "checkinV2")
        self.client = client

    async def _run(self):
        while self.running:
            send_queue = queue.SimpleQueue()
            await sleep(0)
            checkin_stream = self.client.client.CheckinV2(iter(send_queue.get, None))
            current_checkin: proto.CheckinExpected = None
            checkin: proto.CheckinExpected
            for checkin in checkin_stream:
                logger.info(f"received a checkin event from CheckinV2: {checkin}")
                if current_checkin is None:
                    current_checkin = checkin
                elif checkin.units_timestamp != current_checkin.units_timestamp:
                    current_checkin = checkin
                if len(checkin.units) == 0:
                    self.apply_expected(current_checkin)
                    self.do_checkin(send_queue)
                if current_checkin != checkin:
                    current_checkin.units.extend(checkin.units)
                logger.info("Waiting for a bit...")
                await sleep(10)

    def apply_expected(self, checkin: proto.CheckinExpected):
        self.client.agent_info = proto.AgentInfo(id=checkin.agent_info.id, version=checkin.agent_info.version, snapshot=checkin.agent_info.snapshot)
        self.client.sync_component(checkin)
        self.client.sync_units(checkin)

    def do_checkin(self, send_queue):
        logger.info("Checking in....")
        units_observed = [unit.to_observed() for unit in self.client.units]
        msg = proto.CheckinObserved(
            token=self.client.token,
            units=units_observed,
            version_info=None,
            features_idx=self.client.features_idx,
            component_idx=self.client.component_idx,
        )
        if not self.client.version_info_sent:
            msg.version_info = self.client.version_info
            if self.client.opts.chunking_allowed:
                msg.supports = proto.ConnectionSupports(proto.CheckinChunking)
        send_queue.put(msg)
