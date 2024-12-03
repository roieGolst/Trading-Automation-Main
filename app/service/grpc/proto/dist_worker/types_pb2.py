"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'types.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0btypes.proto\x12\x05Types"(\n\x08BaseTask\x12\x1c\n\x07task_id\x18\x02 \x01(\x0b2\x0b.Types.UUID"\x15\n\x04UUID\x12\r\n\x05value\x18\x01 \x01(\t*"\n\x06Status\x12\x0b\n\x07Success\x10\x00\x12\x0b\n\x07Failure\x10\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'types_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_STATUS']._serialized_start = 87
    _globals['_STATUS']._serialized_end = 121
    _globals['_BASETASK']._serialized_start = 22
    _globals['_BASETASK']._serialized_end = 62
    _globals['_UUID']._serialized_start = 64
    _globals['_UUID']._serialized_end = 85