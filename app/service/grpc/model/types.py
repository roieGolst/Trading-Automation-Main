import uuid
from abc import ABC
from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Any
from uuid import UUID


class TaskType(Enum):
    Activation = "activation"
    Deactivation = "deactivation"
    Transaction = "transaction"


class TransactionMethod(IntEnum):
    Sell = 0
    Buy = 1


class Brokerage(IntEnum):
    BBAE = 0
    Chase = 1
    DSPAC = 2
    Fennel = 3
    Fidelity = 4
    Firstrade = 5
    Public = 6
    Robinhood = 7
    Schwab = 8
    SoFi = 9
    Tornado = 10
    Tradier = 11
    Tastytrade = 12
    Webull = 13
    Vanguard = 14
    WellsFargo = 15


class Task(ABC):
    task_type: TaskType
    task_id: UUID

    def __init__(self, task_type: TaskType, task_id: UUID):
        self.task_type = task_type
        self.task_id = task_id

    @staticmethod
    def Activation(account_name: str, brokerage: Brokerage, creds: Any):
        return _ActivationTask(account_name,brokerage, creds)

    @staticmethod
    def Deactivation(account_id: UUID):
        return _DeactivationTask(account_id)

    @staticmethod
    def Transaction(method: TransactionMethod, amount: int, ticker: str):
        return _TransactionTask(method, amount, ticker)


class _ActivationTask(Task):
    account_name: str
    brokerage: Brokerage
    cred: any

    def __init__(self, account_name: str, brokerage: Brokerage, creds: dict):
        super().__init__(task_type=TaskType.Activation, task_id=uuid.uuid4())
        self.account_name = account_name
        self.brokerage = brokerage
        self.cred = self.parse_creds(creds)

    def parse_creds(self, creds: Any):
        parsed_creds = {}
        if creds.get("USERNAME"):
            parsed_creds["USERNAME"] = creds["USERNAME"]

        if creds.get("PASSWORD"):
            parsed_creds["PASSWORD"] = creds["PASSWORD"]

        if creds.get("EMAIL"):
            parsed_creds["EMAIL"] = creds["EMAIL"]

        if creds.get("ACCESS_TOKEN"):
            parsed_creds["ACCESS_TOKEN"] = creds["ACCESS_TOKEN"]

        if creds.get("TOTP_SECRET_OR_NA"):
            parsed_creds["TOTP_SECRET_OR_NA"] = creds["TOTP_SECRET_OR_NA"]

        if creds.get("TOTP_OR_NA"):
            parsed_creds["TOTP_OR_NA"] = creds["TOTP_OR_NA"]

        if creds.get("TOTP_SECRET"):
            parsed_creds["TOTP_SECRET"] = creds["TOTP_SECRET"]

        if creds.get("OTP"):
            parsed_creds["OTP"] = creds["OTP"]

        if creds.get("PHONE_LAST_FOUR"):
            parsed_creds["PHONE_LAST_FOUR"] = creds["PHONE_LAST_FOUR"]

        if creds.get("DEBUG"):
            parsed_creds["DEBUG"] = creds["DEBUG"]

        if creds.get("DID"):
            parsed_creds["DID"] = creds["DID"]

        if creds.get("TRADING_PIN"):
            parsed_creds["TRADING_PIN"] = creds["TRADING_PIN"]

        return parsed_creds


class _DeactivationTask(Task):
    account_name: str

    def __init__(self, account_name: str):
        super().__init__(task_type=TaskType.Deactivation, task_id=uuid.uuid4())
        self.account_name = account_name


class _TransactionTask(Task):
    transaction_method: TransactionMethod
    amount: int
    ticker: str

    def __init__(self, method: TransactionMethod, amount: int, ticker: str):
        super().__init__(task_type=TaskType.Transaction, task_id=uuid.uuid4())
        self.transaction_method = method
        self.amount = amount
        self.ticker = ticker


ActivationTask = _ActivationTask
DeactivationTask = _DeactivationTask
TransactionTask = _TransactionTask


@dataclass
class ActivationResponse:
    success: bool


@dataclass
class DeactivationResponse:
    # Added if needed
    pass


@dataclass
class TransactionResponse:
    stdout: str

