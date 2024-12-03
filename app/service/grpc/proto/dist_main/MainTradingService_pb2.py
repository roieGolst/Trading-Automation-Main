"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'MainTradingService.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18MainTradingService.proto\x12\x0eTradingService"\x1e\n\x04Ping\x12\x16\n\x0ereturn_to_port\x18\x01 \x01(\x05"\x06\n\x04Pong2H\n\x12MainTradingService\x122\n\x04ping\x12\x14.TradingService.Ping\x1a\x14.TradingService.Pongb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'MainTradingService_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_PING']._serialized_start = 44
    _globals['_PING']._serialized_end = 74
    _globals['_PONG']._serialized_start = 76
    _globals['_PONG']._serialized_end = 82
    _globals['_MAINTRADINGSERVICE']._serialized_start = 84
    _globals['_MAINTRADINGSERVICE']._serialized_end = 156