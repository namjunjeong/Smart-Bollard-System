from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Req(_message.Message):
    __slots__ = ["request"]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: int
    def __init__(self, request: _Optional[int] = ...) -> None: ...

class Res(_message.Message):
    __slots__ = ["response"]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: bool
    def __init__(self, response: bool = ...) -> None: ...

class OptVal(_message.Message):
    __slots__ = ["manual_flag", "manual", "letsgo_flag", "letsgo"]
    MANUAL_FLAG_FIELD_NUMBER: _ClassVar[int]
    MANUAL_FIELD_NUMBER: _ClassVar[int]
    LETSGO_FLAG_FIELD_NUMBER: _ClassVar[int]
    LETSGO_FIELD_NUMBER: _ClassVar[int]
    manual_flag: bool
    manual: bool
    letsgo_flag: bool
    letsgo: bool
    def __init__(self, manual_flag: bool = ..., manual: bool = ..., letsgo_flag: bool = ..., letsgo: bool = ...) -> None: ...
