from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from service.grpc.proto.dist_worker.ActivationTask_pb2 import Task as ActivationTask
from service.grpc.proto.dist_worker.DeactivationTask_pb2 import Task as DeactivationTask
from service.grpc.proto.dist_worker.TransactionTask_pb2 import Task as TransactionTask


# TODO: TBD: If one more models level is needed to represents the input or just export it from the __init__ file
class ITradingStub(ABC):
    @abstractmethod
    def activation(self, activation_task: ActivationTask):
        pass

    @abstractmethod
    def deactivation(self, deactivation_task: DeactivationTask):
        pass

    @abstractmethod
    def transaction(self, transaction_task: TransactionTask):
        pass
