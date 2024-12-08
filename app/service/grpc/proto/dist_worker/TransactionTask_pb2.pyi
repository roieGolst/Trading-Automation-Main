"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
from . import types_pb2
import typing
if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _TransactionMethod:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _TransactionMethodEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_TransactionMethod.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    Sell: _TransactionMethod.ValueType
    Buy: _TransactionMethod.ValueType

class TransactionMethod(_TransactionMethod, metaclass=_TransactionMethodEnumTypeWrapper):
    ...
Sell: TransactionMethod.ValueType
Buy: TransactionMethod.ValueType
global___TransactionMethod = TransactionMethod

@typing.final
class Task(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    BASE_TASK_FIELD_NUMBER: builtins.int
    METHOD_FIELD_NUMBER: builtins.int
    AMOUNT_FIELD_NUMBER: builtins.int
    TICKER_FIELD_NUMBER: builtins.int
    method: global___TransactionMethod.ValueType
    amount: builtins.int
    ticker: builtins.str

    @property
    def base_task(self) -> types_pb2.BaseTask:
        ...

    def __init__(self, *, base_task: types_pb2.BaseTask | None=..., method: global___TransactionMethod.ValueType=..., amount: builtins.int=..., ticker: builtins.str=...) -> None:
        ...

    def HasField(self, field_name: typing.Literal['base_task', b'base_task']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing.Literal['amount', b'amount', 'base_task', b'base_task', 'method', b'method', 'ticker', b'ticker']) -> None:
        ...
global___Task = Task

@typing.final
class Response(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    STATUS_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    status: types_pb2.Status.ValueType
    message: builtins.str

    def __init__(self, *, status: types_pb2.Status.ValueType=..., message: builtins.str | None=...) -> None:
        ...

    def HasField(self, field_name: typing.Literal['_message', b'_message', 'message', b'message']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing.Literal['_message', b'_message', 'message', b'message', 'status', b'status']) -> None:
        ...

    def WhichOneof(self, oneof_group: typing.Literal['_message', b'_message']) -> typing.Literal['message'] | None:
        ...
global___Response = Response