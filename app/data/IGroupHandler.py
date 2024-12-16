from abc import ABC, abstractmethod
from typing import Union

from app.service.grpc.stub.ITradingStub import ITradingStub


# TODO: Reconsidering if this class should return ITradingStub instances or wrap them
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
