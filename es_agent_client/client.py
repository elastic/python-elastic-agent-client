from typing import Optional

import es_agent_client.generated.elastic_agent_client_pb2 as proto
from es_agent_client.generated.elastic_agent_client_future_pb2_grpc import (
    ElasticAgentArtifact,
    ElasticAgentLog,
    ElasticAgentStore,
)
from es_agent_client.generated.elastic_agent_client_pb2_grpc import ElasticAgentStub


class VersionInfo:
    def __init__(
        self, name: str, meta: Optional[dict] = None, build_hash: Optional[str] = None
    ):
        self.name = name
        self.meta = meta
        self.build_hash = build_hash


class V2Options:
    def __init__(
        self,
        max_message_size: Optional[int] = None,
        chunking_allowed: Optional[bool] = None,
        agent_info: Optional[proto.AgentInfo] = None,
    ):
        self.max_message_size = max_message_size
        self.chunking_allowed = chunking_allowed
        self.agent_info = agent_info
        self.credentials = None


class Unit:
    def __init__(self, id=None):
        self.id: Optional[str] = id
        self.unit_type: Optional[proto.UnitType] = None
        self.expected_state: Optional[proto.State] = None
        self.log_level: Optional[proto.UnitLogLevel] = None
        self.config: Optional[proto.UnitExpectedConfig] = None
        self.config_idx: Optional[int] = None
        self.features: Optional[proto.Features] = None
        self.features_idx: Optional[int] = None
        self.apm: Optional[proto.APMConfig] = None
        self.state: Optional[proto.State] = None
        self.state_msg: Optional[str] = None
        self.state_payload: Optional[dict] = None
        self.actions: Optional[dict] = None
        self.client: Optional[V2] = None
        self.diag_hooks: Optional[dict] = None

    def to_observed(self) -> proto.UnitObserved:
        return proto.UnitObserved(
            id=self.id,
            type=self.unit_type,
            config_state_idx=self.config_idx,
            state=self.state,
            message=self.state_msg,
            payload=self.state_payload,
        )


class V2:
    def __init__(self):
        self.target: Optional[str] = None
        self.opts: Optional[V2Options] = None
        self.token: Optional[str] = None
        self.agent_info: Optional[proto.AgentInfo] = None
        self.version_info: Optional[VersionInfo] = None
        self.version_info_sent: Optional[bool] = None
        self.client: Optional[ElasticAgentStub] = None
        self.store_client: Optional[ElasticAgentStore] = None
        self.artifact_client: Optional[ElasticAgentArtifact] = None
        self.log_client: Optional[ElasticAgentLog] = None
        self.units: Optional[list[Unit]] = None
        self.features_idx: Optional[int] = None
        self.component_idx: Optional[int] = None
        self.component_config: Optional[proto.Component] = None
        self.apm_config: Optional[proto.APMConfig] = None

    def __str__(self):
        if self.agent_info and self.version_info:
            return f"V2 Client: (agent id: {self.agent_info.id}, agent version: {self.agent_info.version}, name: {self.version_info.name}, target: {self.target})"
        else:
            return "Uninitialized V2 Client"

    def sync_component(self, checkin: proto.CheckinExpected):
        self.component_config = checkin.component
        self.component_idx = checkin.component_idx

    def sync_units(self, checkin: proto.CheckinExpected):
        if checkin.component:
            self.apm_config = checkin.component.apm_config
        units = []
        for expected_unit in checkin.units:
            unit = Unit()
            unit.id = expected_unit.id
            unit.unit_type = expected_unit.type
            unit.expected_state = expected_unit.state
            unit.log_level = expected_unit.log_level
            unit.config = expected_unit.config
            unit.config_idx = expected_unit.config_state_idx
            unit.features = None  # TODO?
            unit.features_idx = 0  # TODO?
            unit.apm = None  # TODO?
            unit.state = expected_unit.state
            unit.state_msg = ""  # TODO?
            unit.state_payload = None  # TODO?
            unit.actions = None  # TODO?
            unit.client = self
            unit.diag_hooks = {}  # TODO?
            units.append(unit)
        self.units = units
