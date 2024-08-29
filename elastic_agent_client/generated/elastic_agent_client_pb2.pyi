from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import elastic_agent_client_deprecated_pb2 as _elastic_agent_client_deprecated_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectionSupports(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CheckinChunking: _ClassVar[ConnectionSupports]

class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STARTING: _ClassVar[State]
    CONFIGURING: _ClassVar[State]
    HEALTHY: _ClassVar[State]
    DEGRADED: _ClassVar[State]
    FAILED: _ClassVar[State]
    STOPPING: _ClassVar[State]
    STOPPED: _ClassVar[State]

class UnitType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INPUT: _ClassVar[UnitType]
    OUTPUT: _ClassVar[UnitType]

class UnitLogLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR: _ClassVar[UnitLogLevel]
    WARN: _ClassVar[UnitLogLevel]
    INFO: _ClassVar[UnitLogLevel]
    DEBUG: _ClassVar[UnitLogLevel]
    TRACE: _ClassVar[UnitLogLevel]

class AgentManagedMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MANAGED: _ClassVar[AgentManagedMode]
    STANDALONE: _ClassVar[AgentManagedMode]

class ConnInfoServices(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Checkin: _ClassVar[ConnInfoServices]
    CheckinV2: _ClassVar[ConnInfoServices]
    Store: _ClassVar[ConnInfoServices]
    Artifact: _ClassVar[ConnInfoServices]
    Log: _ClassVar[ConnInfoServices]
CheckinChunking: ConnectionSupports
STARTING: State
CONFIGURING: State
HEALTHY: State
DEGRADED: State
FAILED: State
STOPPING: State
STOPPED: State
INPUT: UnitType
OUTPUT: UnitType
ERROR: UnitLogLevel
WARN: UnitLogLevel
INFO: UnitLogLevel
DEBUG: UnitLogLevel
TRACE: UnitLogLevel
MANAGED: AgentManagedMode
STANDALONE: AgentManagedMode
Checkin: ConnInfoServices
CheckinV2: ConnInfoServices
Store: ConnInfoServices
Artifact: ConnInfoServices
Log: ConnInfoServices

class Package(_message.Message):
    __slots__ = ("source", "name", "version")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    source: _struct_pb2.Struct
    name: str
    version: str
    def __init__(self, source: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., name: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class Meta(_message.Message):
    __slots__ = ("source", "package")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    source: _struct_pb2.Struct
    package: Package
    def __init__(self, source: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., package: _Optional[_Union[Package, _Mapping]] = ...) -> None: ...

class DataStream(_message.Message):
    __slots__ = ("source", "dataset", "type", "namespace")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    DATASET_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    source: _struct_pb2.Struct
    dataset: str
    type: str
    namespace: str
    def __init__(self, source: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., dataset: _Optional[str] = ..., type: _Optional[str] = ..., namespace: _Optional[str] = ...) -> None: ...

class Stream(_message.Message):
    __slots__ = ("source", "id", "data_stream")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DATA_STREAM_FIELD_NUMBER: _ClassVar[int]
    source: _struct_pb2.Struct
    id: str
    data_stream: DataStream
    def __init__(self, source: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., id: _Optional[str] = ..., data_stream: _Optional[_Union[DataStream, _Mapping]] = ...) -> None: ...

class UnitExpectedConfig(_message.Message):
    __slots__ = ("source", "id", "type", "name", "revision", "meta", "data_stream", "streams")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    DATA_STREAM_FIELD_NUMBER: _ClassVar[int]
    STREAMS_FIELD_NUMBER: _ClassVar[int]
    source: _struct_pb2.Struct
    id: str
    type: str
    name: str
    revision: int
    meta: Meta
    data_stream: DataStream
    streams: _containers.RepeatedCompositeFieldContainer[Stream]
    def __init__(self, source: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., id: _Optional[str] = ..., type: _Optional[str] = ..., name: _Optional[str] = ..., revision: _Optional[int] = ..., meta: _Optional[_Union[Meta, _Mapping]] = ..., data_stream: _Optional[_Union[DataStream, _Mapping]] = ..., streams: _Optional[_Iterable[_Union[Stream, _Mapping]]] = ...) -> None: ...

class UnitExpected(_message.Message):
    __slots__ = ("id", "type", "state", "config_state_idx", "config", "log_level")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_STATE_IDX_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    LOG_LEVEL_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: UnitType
    state: State
    config_state_idx: int
    config: UnitExpectedConfig
    log_level: UnitLogLevel
    def __init__(self, id: _Optional[str] = ..., type: _Optional[_Union[UnitType, str]] = ..., state: _Optional[_Union[State, str]] = ..., config_state_idx: _Optional[int] = ..., config: _Optional[_Union[UnitExpectedConfig, _Mapping]] = ..., log_level: _Optional[_Union[UnitLogLevel, str]] = ...) -> None: ...

class AgentInfo(_message.Message):
    __slots__ = ("id", "version", "snapshot", "mode", "Unprivileged")
    ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    UNPRIVILEGED_FIELD_NUMBER: _ClassVar[int]
    id: str
    version: str
    snapshot: bool
    mode: AgentManagedMode
    Unprivileged: bool
    def __init__(self, id: _Optional[str] = ..., version: _Optional[str] = ..., snapshot: bool = ..., mode: _Optional[_Union[AgentManagedMode, str]] = ..., Unprivileged: bool = ...) -> None: ...

class Features(_message.Message):
    __slots__ = ("source", "fqdn")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    FQDN_FIELD_NUMBER: _ClassVar[int]
    source: _struct_pb2.Struct
    fqdn: FQDNFeature
    def __init__(self, source: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., fqdn: _Optional[_Union[FQDNFeature, _Mapping]] = ...) -> None: ...

class FQDNFeature(_message.Message):
    __slots__ = ("enabled",)
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    def __init__(self, enabled: bool = ...) -> None: ...

class ElasticAPMTLS(_message.Message):
    __slots__ = ("skip_verify", "server_cert", "server_ca")
    SKIP_VERIFY_FIELD_NUMBER: _ClassVar[int]
    SERVER_CERT_FIELD_NUMBER: _ClassVar[int]
    SERVER_CA_FIELD_NUMBER: _ClassVar[int]
    skip_verify: bool
    server_cert: str
    server_ca: str
    def __init__(self, skip_verify: bool = ..., server_cert: _Optional[str] = ..., server_ca: _Optional[str] = ...) -> None: ...

class ElasticAPM(_message.Message):
    __slots__ = ("tls", "environment", "api_key", "secret_token", "hosts", "global_labels")
    TLS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    SECRET_TOKEN_FIELD_NUMBER: _ClassVar[int]
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_LABELS_FIELD_NUMBER: _ClassVar[int]
    tls: ElasticAPMTLS
    environment: str
    api_key: str
    secret_token: str
    hosts: _containers.RepeatedScalarFieldContainer[str]
    global_labels: str
    def __init__(self, tls: _Optional[_Union[ElasticAPMTLS, _Mapping]] = ..., environment: _Optional[str] = ..., api_key: _Optional[str] = ..., secret_token: _Optional[str] = ..., hosts: _Optional[_Iterable[str]] = ..., global_labels: _Optional[str] = ...) -> None: ...

class APMConfig(_message.Message):
    __slots__ = ("elastic",)
    ELASTIC_FIELD_NUMBER: _ClassVar[int]
    elastic: ElasticAPM
    def __init__(self, elastic: _Optional[_Union[ElasticAPM, _Mapping]] = ...) -> None: ...

class Component(_message.Message):
    __slots__ = ("limits", "apm_config")
    LIMITS_FIELD_NUMBER: _ClassVar[int]
    APM_CONFIG_FIELD_NUMBER: _ClassVar[int]
    limits: ComponentLimits
    apm_config: APMConfig
    def __init__(self, limits: _Optional[_Union[ComponentLimits, _Mapping]] = ..., apm_config: _Optional[_Union[APMConfig, _Mapping]] = ...) -> None: ...

class ComponentLimits(_message.Message):
    __slots__ = ("source", "go_max_procs")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    GO_MAX_PROCS_FIELD_NUMBER: _ClassVar[int]
    source: _struct_pb2.Struct
    go_max_procs: int
    def __init__(self, source: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., go_max_procs: _Optional[int] = ...) -> None: ...

class CheckinExpected(_message.Message):
    __slots__ = ("units", "agent_info", "features", "features_idx", "component", "component_idx", "units_timestamp")
    UNITS_FIELD_NUMBER: _ClassVar[int]
    AGENT_INFO_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    FEATURES_IDX_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_IDX_FIELD_NUMBER: _ClassVar[int]
    UNITS_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    units: _containers.RepeatedCompositeFieldContainer[UnitExpected]
    agent_info: AgentInfo
    features: Features
    features_idx: int
    component: Component
    component_idx: int
    units_timestamp: _timestamp_pb2.Timestamp
    def __init__(self, units: _Optional[_Iterable[_Union[UnitExpected, _Mapping]]] = ..., agent_info: _Optional[_Union[AgentInfo, _Mapping]] = ..., features: _Optional[_Union[Features, _Mapping]] = ..., features_idx: _Optional[int] = ..., component: _Optional[_Union[Component, _Mapping]] = ..., component_idx: _Optional[int] = ..., units_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UnitObserved(_message.Message):
    __slots__ = ("id", "type", "config_state_idx", "state", "message", "payload")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_STATE_IDX_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: UnitType
    config_state_idx: int
    state: State
    message: str
    payload: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., type: _Optional[_Union[UnitType, str]] = ..., config_state_idx: _Optional[int] = ..., state: _Optional[_Union[State, str]] = ..., message: _Optional[str] = ..., payload: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class CheckinObservedVersionInfo(_message.Message):
    __slots__ = ("name", "meta", "build_hash")
    class MetaEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    BUILD_HASH_FIELD_NUMBER: _ClassVar[int]
    name: str
    meta: _containers.ScalarMap[str, str]
    build_hash: str
    def __init__(self, name: _Optional[str] = ..., meta: _Optional[_Mapping[str, str]] = ..., build_hash: _Optional[str] = ...) -> None: ...

class CheckinObserved(_message.Message):
    __slots__ = ("token", "units", "version_info", "features_idx", "component_idx", "units_timestamp", "supports", "pid")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    VERSION_INFO_FIELD_NUMBER: _ClassVar[int]
    FEATURES_IDX_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_IDX_FIELD_NUMBER: _ClassVar[int]
    UNITS_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    token: str
    units: _containers.RepeatedCompositeFieldContainer[UnitObserved]
    version_info: CheckinObservedVersionInfo
    features_idx: int
    component_idx: int
    units_timestamp: _timestamp_pb2.Timestamp
    supports: _containers.RepeatedScalarFieldContainer[ConnectionSupports]
    pid: int
    def __init__(self, token: _Optional[str] = ..., units: _Optional[_Iterable[_Union[UnitObserved, _Mapping]]] = ..., version_info: _Optional[_Union[CheckinObservedVersionInfo, _Mapping]] = ..., features_idx: _Optional[int] = ..., component_idx: _Optional[int] = ..., units_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., supports: _Optional[_Iterable[_Union[ConnectionSupports, str]]] = ..., pid: _Optional[int] = ...) -> None: ...

class ActionRequest(_message.Message):
    __slots__ = ("id", "name", "params", "unit_id", "unit_type", "type", "level")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CUSTOM: _ClassVar[ActionRequest.Type]
        DIAGNOSTICS: _ClassVar[ActionRequest.Type]
    CUSTOM: ActionRequest.Type
    DIAGNOSTICS: ActionRequest.Type
    class Level(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ALL: _ClassVar[ActionRequest.Level]
        COMPONENT: _ClassVar[ActionRequest.Level]
        UNIT: _ClassVar[ActionRequest.Level]
    ALL: ActionRequest.Level
    COMPONENT: ActionRequest.Level
    UNIT: ActionRequest.Level
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    UNIT_ID_FIELD_NUMBER: _ClassVar[int]
    UNIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    params: bytes
    unit_id: str
    unit_type: UnitType
    type: ActionRequest.Type
    level: ActionRequest.Level
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., params: _Optional[bytes] = ..., unit_id: _Optional[str] = ..., unit_type: _Optional[_Union[UnitType, str]] = ..., type: _Optional[_Union[ActionRequest.Type, str]] = ..., level: _Optional[_Union[ActionRequest.Level, str]] = ...) -> None: ...

class ActionDiagnosticUnitResult(_message.Message):
    __slots__ = ("name", "filename", "description", "content_type", "content", "generated")
    NAME_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    GENERATED_FIELD_NUMBER: _ClassVar[int]
    name: str
    filename: str
    description: str
    content_type: str
    content: bytes
    generated: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., filename: _Optional[str] = ..., description: _Optional[str] = ..., content_type: _Optional[str] = ..., content: _Optional[bytes] = ..., generated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ActionResponse(_message.Message):
    __slots__ = ("token", "id", "status", "result", "diagnostic")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[ActionResponse.Status]
        FAILED: _ClassVar[ActionResponse.Status]
    SUCCESS: ActionResponse.Status
    FAILED: ActionResponse.Status
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTIC_FIELD_NUMBER: _ClassVar[int]
    token: str
    id: str
    status: ActionResponse.Status
    result: bytes
    diagnostic: _containers.RepeatedCompositeFieldContainer[ActionDiagnosticUnitResult]
    def __init__(self, token: _Optional[str] = ..., id: _Optional[str] = ..., status: _Optional[_Union[ActionResponse.Status, str]] = ..., result: _Optional[bytes] = ..., diagnostic: _Optional[_Iterable[_Union[ActionDiagnosticUnitResult, _Mapping]]] = ...) -> None: ...

class StartUpInfo(_message.Message):
    __slots__ = ("addr", "server_name", "token", "ca_cert", "peer_cert", "peer_key", "services", "supports", "max_message_size", "agent_info")
    ADDR_FIELD_NUMBER: _ClassVar[int]
    SERVER_NAME_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    CA_CERT_FIELD_NUMBER: _ClassVar[int]
    PEER_CERT_FIELD_NUMBER: _ClassVar[int]
    PEER_KEY_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_FIELD_NUMBER: _ClassVar[int]
    MAX_MESSAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    AGENT_INFO_FIELD_NUMBER: _ClassVar[int]
    addr: str
    server_name: str
    token: str
    ca_cert: bytes
    peer_cert: bytes
    peer_key: bytes
    services: _containers.RepeatedScalarFieldContainer[ConnInfoServices]
    supports: _containers.RepeatedScalarFieldContainer[ConnectionSupports]
    max_message_size: int
    agent_info: AgentInfo
    def __init__(self, addr: _Optional[str] = ..., server_name: _Optional[str] = ..., token: _Optional[str] = ..., ca_cert: _Optional[bytes] = ..., peer_cert: _Optional[bytes] = ..., peer_key: _Optional[bytes] = ..., services: _Optional[_Iterable[_Union[ConnInfoServices, str]]] = ..., supports: _Optional[_Iterable[_Union[ConnectionSupports, str]]] = ..., max_message_size: _Optional[int] = ..., agent_info: _Optional[_Union[AgentInfo, _Mapping]] = ...) -> None: ...
