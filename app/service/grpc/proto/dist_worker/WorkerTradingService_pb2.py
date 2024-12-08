"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'WorkerTradingService.proto')
_sym_db = _symbol_database.Default()
from . import ActivationTask_pb2 as ActivationTask__pb2
from . import DeactivationTask_pb2 as DeactivationTask__pb2
from . import TransactionTask_pb2 as TransactionTask__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1aWorkerTradingService.proto\x12\x0eTradingService\x1a\x14ActivationTask.proto\x1a\x16DeactivationTask.proto\x1a\x15TransactionTask.proto2\xdf\x01\n\x14WorkerTradingService\x12>\n\nActivation\x12\x15.Task.Activation.Task\x1a\x19.Task.Activation.Response\x12D\n\x0cDeactivation\x12\x17.Task.Deactivation.Task\x1a\x1b.Task.Deactivation.Response\x12A\n\x0bTransaction\x12\x16.Task.Transaction.Task\x1a\x1a.Task.Transaction.Responseb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'WorkerTradingService_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_WORKERTRADINGSERVICE']._serialized_start = 116
    _globals['_WORKERTRADINGSERVICE']._serialized_end = 339