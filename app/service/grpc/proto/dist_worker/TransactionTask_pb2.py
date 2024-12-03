"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'TransactionTask.proto')
_sym_db = _symbol_database.Default()
from . import types_pb2 as types__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15TransactionTask.proto\x12\x10Task.Transaction\x1a\x0btypes.proto"\x7f\n\x04Task\x12"\n\tbase_task\x18\x01 \x01(\x0b2\x0f.Types.BaseTask\x123\n\x06method\x18\x02 \x01(\x0e2#.Task.Transaction.TransactionMethod\x12\x0e\n\x06amount\x18\x03 \x01(\x05\x12\x0e\n\x06ticker\x18\x04 \x01(\t"K\n\x08Response\x12\x1d\n\x06status\x18\x01 \x01(\x0e2\r.Types.Status\x12\x14\n\x07message\x18\x02 \x01(\tH\x00\x88\x01\x01B\n\n\x08_message*&\n\x11TransactionMethod\x12\x08\n\x04Sell\x10\x00\x12\x07\n\x03Buy\x10\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'TransactionTask_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_TRANSACTIONMETHOD']._serialized_start = 262
    _globals['_TRANSACTIONMETHOD']._serialized_end = 300
    _globals['_TASK']._serialized_start = 56
    _globals['_TASK']._serialized_end = 183
    _globals['_RESPONSE']._serialized_start = 185
    _globals['_RESPONSE']._serialized_end = 260