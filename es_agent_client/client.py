from dataclasses import dataclass
from typing import List
from es_agent_client.generated.elastic_agent_client_pb2 import AgentInfo
from es_agent_client.generated.elastic_agent_client_pb2_grpc import ElasticAgentStub
from es_agent_client.generated.elastic_agent_client_future_pb2_grpc import ElasticAgentStore, ElasticAgentArtifact, ElasticAgentLog


class VersionInfo:
    def __init__(self, name, meta, build_hash=None):
        self.name = name
        self.meta = meta
        self.build_hash = build_hash


class V2Options:
    def __init__(self, max_message_size=None, chunking_allowed=None, agent_info: AgentInfo = None):
        self.max_message_size = max_message_size
        self.chunking_allowed = chunking_allowed
        self.agent_info = agent_info
        self.credentials = None


class V2:
    def __init__(self):
        self.target: str = None
        self.opts: V2Options = None
        self.token: str = None
        self.agent_info: AgentInfo = None
        self.version_info: VersionInfo = None
        self.version_info_sent: bool = None
        self.client: ElasticAgentStub = None
        self.store_client: ElasticAgentStore = None
        self.artifact_client: ElasticAgentArtifact = None
        self.log_client: ElasticAgentLog = None

    def __str__(self):
        return f"""
        V2 Client
          agent id: {self.agent_info.id}
          agent version: {self.agent_info.version}
          name: {self.version_info.name}
          target: {self.target}
        """


