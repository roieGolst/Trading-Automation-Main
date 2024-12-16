from abc import ABC, abstractmethod
from typing import Callable

from app.service.grpc.stub._Stub import _Stub

StubFactory = Callable[[str], _Stub]


class IStubHandler(ABC):
    @abstractmethod
    def on_new_client(self, stub_factory: StubFactory) -> bool:
        pass

    @abstractmethod
    def on_client_close(self, client_id: str):
        pass
