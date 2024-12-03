from abc import ABC, abstractmethod
from typing import Union

from service.grpc.ITradingStub import ITradingStub


class IGroupHandler(ABC):
    @abstractmethod
    def create_group(self, group_name: str):
        pass

    @abstractmethod
    def get_group(self, group_name: str) -> Union[ITradingStub, None]:
        pass

    def on_new_client(self, client: ITradingStub) -> None:
        pass
