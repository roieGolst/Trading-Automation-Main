"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'ActivationTask.proto')
_sym_db = _symbol_database.Default()
from . import types_pb2 as types__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14ActivationTask.proto\x12\x0fTask.Activation\x1a\x0btypes.proto"\x95\x04\n\x0fActivationCreds\x12\x15\n\x08USERNAME\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x15\n\x08PASSWORD\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x12\n\x05EMAIL\x18\x03 \x01(\tH\x02\x88\x01\x01\x12\x19\n\x0cACCESS_TOKEN\x18\x04 \x01(\tH\x03\x88\x01\x01\x12\x1e\n\x11TOTP_SECRET_OR_NA\x18\x05 \x01(\tH\x04\x88\x01\x01\x12\x17\n\nTOTP_OR_NA\x18\x06 \x01(\tH\x05\x88\x01\x01\x12\x18\n\x0bTOTP_SECRET\x18\x07 \x01(\tH\x06\x88\x01\x01\x12\x10\n\x03OTP\x18\x08 \x01(\tH\x07\x88\x01\x01\x12!\n\x14CELL_PHONE_LAST_FOUR\x18\t \x01(\tH\x08\x88\x01\x01\x12\x1c\n\x0fPHONE_LAST_FOUR\x18\n \x01(\tH\t\x88\x01\x01\x12\x12\n\x05DEBUG\x18\x0b \x01(\tH\n\x88\x01\x01\x12\x10\n\x03DID\x18\x0c \x01(\tH\x0b\x88\x01\x01\x12\x18\n\x0bTRADING_PIN\x18\r \x01(\tH\x0c\x88\x01\x01B\x0b\n\t_USERNAMEB\x0b\n\t_PASSWORDB\x08\n\x06_EMAILB\x0f\n\r_ACCESS_TOKENB\x14\n\x12_TOTP_SECRET_OR_NAB\r\n\x0b_TOTP_OR_NAB\x0e\n\x0c_TOTP_SECRETB\x06\n\x04_OTPB\x17\n\x15_CELL_PHONE_LAST_FOURB\x12\n\x10_PHONE_LAST_FOURB\x08\n\x06_DEBUGB\x06\n\x04_DIDB\x0e\n\x0c_TRADING_PIN"\x94\x01\n\x04Task\x12"\n\tbase_task\x18\x01 \x01(\x0b2\x0f.Types.BaseTask\x12-\n\tbrokerage\x18\x02 \x01(\x0e2\x1a.Task.Activation.Brokerage\x129\n\x0faccount_details\x18\x03 \x01(\x0b2 .Task.Activation.ActivationCreds"\x80\x01\n\x08Response\x12\x1d\n\x06status\x18\x01 \x01(\x0e2\r.Types.Status\x12$\n\naccount_id\x18\x02 \x01(\x0b2\x0b.Types.UUIDH\x00\x88\x01\x01\x12\x14\n\x07message\x18\x03 \x01(\tH\x01\x88\x01\x01B\r\n\x0b_account_idB\n\n\x08_message*\xd9\x01\n\tBrokerage\x12\x08\n\x04BBAE\x10\x00\x12\t\n\x05Chase\x10\x01\x12\t\n\x05DSPAC\x10\x02\x12\n\n\x06Fennel\x10\x03\x12\x0c\n\x08Fidelity\x10\x04\x12\r\n\tFirstrade\x10\x05\x12\n\n\x06Public\x10\x06\x12\r\n\tRobinhood\x10\x07\x12\n\n\x06Schwab\x10\x08\x12\x08\n\x04SoFi\x10\t\x12\x0b\n\x07Tornado\x10\n\x12\x0b\n\x07Tradier\x10\x0b\x12\x0e\n\nTastytrade\x10\x0c\x12\n\n\x06Webull\x10\r\x12\x0c\n\x08Vanguard\x10\x0e\x12\x0e\n\nWellsFargo\x10\x0fb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ActivationTask_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_BROKERAGE']._serialized_start = 873
    _globals['_BROKERAGE']._serialized_end = 1090
    _globals['_ACTIVATIONCREDS']._serialized_start = 55
    _globals['_ACTIVATIONCREDS']._serialized_end = 588
    _globals['_TASK']._serialized_start = 591
    _globals['_TASK']._serialized_end = 739
    _globals['_RESPONSE']._serialized_start = 742
    _globals['_RESPONSE']._serialized_end = 870