"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing
if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _Status:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _StatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_Status.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    Success: _Status.ValueType
    Failure: _Status.ValueType

class Status(_Status, metaclass=_StatusEnumTypeWrapper):
    ...
Success: Status.ValueType
Failure: Status.ValueType
global___Status = Status

@typing.final
class BaseTask(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TASK_ID_FIELD_NUMBER: builtins.int

    @property
    def task_id(self) -> global___UUID:
        ...

    def __init__(self, *, task_id: global___UUID | None=...) -> None:
        ...

    def HasField(self, field_name: typing.Literal['task_id', b'task_id']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing.Literal['task_id', b'task_id']) -> None:
        ...
global___BaseTask = BaseTask

@typing.final
class UUID(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    VALUE_FIELD_NUMBER: builtins.int
    value: builtins.str

    def __init__(self, *, value: builtins.str=...) -> None:
        ...

    def ClearField(self, field_name: typing.Literal['value', b'value']) -> None:
        ...
global___UUID = UUID