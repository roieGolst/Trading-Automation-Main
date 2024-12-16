from abc import ABC, abstractmethod

from app.common.Response import Response
from app.service.grpc.model.types import ActivationTask, ActivationResponse, DeactivationResponse, DeactivationTask, \
    TransactionTask, TransactionResponse


# TODO: TBD: If one more models level is needed to represents the input or just export it from the __init__ file
class ITradingStub(ABC):
    @abstractmethod
    def activation(self, task: ActivationTask) -> Response[ActivationResponse]:
        pass

    @abstractmethod
    def deactivation(self, task: DeactivationTask) -> Response[DeactivationResponse]:
        pass

    @abstractmethod
    def transaction(self, task: TransactionTask) -> Response[TransactionResponse]:
        pass
