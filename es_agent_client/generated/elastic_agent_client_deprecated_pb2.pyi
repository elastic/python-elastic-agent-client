from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StateObserved(_message.Message):
    __slots__ = ("token", "config_state_idx", "status", "message", "payload")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STARTING: _ClassVar[StateObserved.Status]
        CONFIGURING: _ClassVar[StateObserved.Status]
        HEALTHY: _ClassVar[StateObserved.Status]
        DEGRADED: _ClassVar[StateObserved.Status]
        FAILED: _ClassVar[StateObserved.Status]
        STOPPING: _ClassVar[StateObserved.Status]
    STARTING: StateObserved.Status
    CONFIGURING: StateObserved.Status
    HEALTHY: StateObserved.Status
    DEGRADED: StateObserved.Status
    FAILED: StateObserved.Status
    STOPPING: StateObserved.Status
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    CONFIG_STATE_IDX_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    token: str
    config_state_idx: int
    status: StateObserved.Status
    message: str
    payload: str
    def __init__(self, token: _Optional[str] = ..., config_state_idx: _Optional[int] = ..., status: _Optional[_Union[StateObserved.Status, str]] = ..., message: _Optional[str] = ..., payload: _Optional[str] = ...) -> None: ...

class StateExpected(_message.Message):
    __slots__ = ("state", "config_state_idx", "config")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        RUNNING: _ClassVar[StateExpected.State]
        STOPPING: _ClassVar[StateExpected.State]
    RUNNING: StateExpected.State
    STOPPING: StateExpected.State
    STATE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_STATE_IDX_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    state: StateExpected.State
    config_state_idx: int
    config: str
    def __init__(self, state: _Optional[_Union[StateExpected.State, str]] = ..., config_state_idx: _Optional[int] = ..., config: _Optional[str] = ...) -> None: ...
