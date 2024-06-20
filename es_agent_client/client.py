import es_agent_client.generated.elastic_agent_client_pb2 as proto
from es_agent_client.generated.elastic_agent_client_pb2_grpc import ElasticAgentStub
from es_agent_client.generated.elastic_agent_client_future_pb2_grpc import ElasticAgentStore, ElasticAgentArtifact, ElasticAgentLog


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



