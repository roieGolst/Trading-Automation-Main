from abc import ABC, abstractmethod

import app.service.grpc.proto.dist_worker.ActivationTask_pb2 as Activation
import app.service.grpc.proto.dist_worker.DeactivationTask_pb2 as Deactivation
import app.service.grpc.proto.dist_worker.TransactionTask_pb2 as Transaction


# TODO: TBD: If one more models level is needed to represents the input or just export it from the __init__ file
class ITradingStub(ABC):
    @abstractmethod
    def activation(self, task: Activation.Task) -> Activation.Response:
        pass

    @abstractmethod
    def deactivation(self, task: Deactivation.Task) -> Deactivation.Response:
        pass

    @abstractmethod
    def transaction(self, task: Transaction.Task) -> Transaction.Response:
        pass
