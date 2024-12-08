"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'DeactivationTask.proto')
_sym_db = _symbol_database.Default()
from . import types_pb2 as types__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16DeactivationTask.proto\x12\x11Task.Deactivation\x1a\x0btypes.proto"K\n\x04Task\x12"\n\tbase_task\x18\x01 \x01(\x0b2\x0f.Types.BaseTask\x12\x1f\n\naccount_id\x18\x02 \x01(\x0b2\x0b.Types.UUID"K\n\x08Response\x12\x1d\n\x06status\x18\x01 \x01(\x0e2\r.Types.Status\x12\x14\n\x07message\x18\x02 \x01(\tH\x00\x88\x01\x01B\n\n\x08_messageb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'DeactivationTask_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_TASK']._serialized_start = 58
    _globals['_TASK']._serialized_end = 133
    _globals['_RESPONSE']._serialized_start = 135
    _globals['_RESPONSE']._serialized_end = 210