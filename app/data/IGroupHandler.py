from abc import ABC, abstractmethod
from typing import Union

from app.service.grpc.ITradingStub import ITradingStub


class IGroupHandler(ABC):

    @classmethod
    @abstractmethod
    def get_instance(cls):
        pass

    @abstractmethod
    def create_group(self, group_name: str):
        pass

    @abstractmethod
    def get_group(self, group_name: str) -> Union[ITradingStub, None]:
        pass

    def on_new_client(self, client: ITradingStub) -> None:
        pass
