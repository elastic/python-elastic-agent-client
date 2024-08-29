from google.protobuf import empty_pb2 as _empty_pb2
import elastic_agent_client_pb2 as _elastic_agent_client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StoreTxType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    READ_ONLY: _ClassVar[StoreTxType]
    READ_WRITE: _ClassVar[StoreTxType]
READ_ONLY: StoreTxType
READ_WRITE: StoreTxType

class StoreBeginTxRequest(_message.Message):
    __slots__ = ("token", "unit_id", "unit_type", "type")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    UNIT_ID_FIELD_NUMBER: _ClassVar[int]
    UNIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    token: str
    unit_id: str
    unit_type: _elastic_agent_client_pb2.UnitType
    type: StoreTxType
    def __init__(self, token: _Optional[str] = ..., unit_id: _Optional[str] = ..., unit_type: _Optional[_Union[_elastic_agent_client_pb2.UnitType, str]] = ..., type: _Optional[_Union[StoreTxType, str]] = ...) -> None: ...

class StoreBeginTxResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class StoreGetKeyRequest(_message.Message):
    __slots__ = ("token", "tx_id", "name")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    TX_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    token: str
    tx_id: str
    name: str
    def __init__(self, token: _Optional[str] = ..., tx_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class StoreGetKeyResponse(_message.Message):
    __slots__ = ("status", "value")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FOUND: _ClassVar[StoreGetKeyResponse.Status]
        NOT_FOUND: _ClassVar[StoreGetKeyResponse.Status]
    FOUND: StoreGetKeyResponse.Status
    NOT_FOUND: StoreGetKeyResponse.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    status: StoreGetKeyResponse.Status
    value: bytes
    def __init__(self, status: _Optional[_Union[StoreGetKeyResponse.Status, str]] = ..., value: _Optional[bytes] = ...) -> None: ...

class StoreSetKeyRequest(_message.Message):
    __slots__ = ("token", "tx_id", "name", "value", "ttl")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    TX_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    token: str
    tx_id: str
    name: str
    value: bytes
    ttl: int
    def __init__(self, token: _Optional[str] = ..., tx_id: _Optional[str] = ..., name: _Optional[str] = ..., value: _Optional[bytes] = ..., ttl: _Optional[int] = ...) -> None: ...

class StoreSetKeyResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StoreDeleteKeyRequest(_message.Message):
    __slots__ = ("token", "tx_id", "name")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    TX_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    token: str
    tx_id: str
    name: str
    def __init__(self, token: _Optional[str] = ..., tx_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class StoreDeleteKeyResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StoreCommitTxRequest(_message.Message):
    __slots__ = ("token", "tx_id")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    TX_ID_FIELD_NUMBER: _ClassVar[int]
    token: str
    tx_id: str
    def __init__(self, token: _Optional[str] = ..., tx_id: _Optional[str] = ...) -> None: ...

class StoreCommitTxResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StoreDiscardTxRequest(_message.Message):
    __slots__ = ("token", "tx_id")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    TX_ID_FIELD_NUMBER: _ClassVar[int]
    token: str
    tx_id: str
    def __init__(self, token: _Optional[str] = ..., tx_id: _Optional[str] = ...) -> None: ...

class StoreDiscardTxResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ArtifactFetchRequest(_message.Message):
    __slots__ = ("token", "id", "sha256")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SHA256_FIELD_NUMBER: _ClassVar[int]
    token: str
    id: str
    sha256: str
    def __init__(self, token: _Optional[str] = ..., id: _Optional[str] = ..., sha256: _Optional[str] = ...) -> None: ...

class ArtifactFetchResponse(_message.Message):
    __slots__ = ("content", "eof")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    EOF_FIELD_NUMBER: _ClassVar[int]
    content: bytes
    eof: _empty_pb2.Empty
    def __init__(self, content: _Optional[bytes] = ..., eof: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ...) -> None: ...

class LogMessage(_message.Message):
    __slots__ = ("unit_id", "unit_type", "message")
    UNIT_ID_FIELD_NUMBER: _ClassVar[int]
    UNIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    unit_id: str
    unit_type: _elastic_agent_client_pb2.UnitType
    message: bytes
    def __init__(self, unit_id: _Optional[str] = ..., unit_type: _Optional[_Union[_elastic_agent_client_pb2.UnitType, str]] = ..., message: _Optional[bytes] = ...) -> None: ...

class LogMessageRequest(_message.Message):
    __slots__ = ("token", "messages")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    token: str
    messages: _containers.RepeatedCompositeFieldContainer[LogMessage]
    def __init__(self, token: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[LogMessage, _Mapping]]] = ...) -> None: ...

class LogMessageResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
