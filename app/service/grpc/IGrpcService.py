from abc import ABC, abstractmethod


class IGrpcService(ABC):
    @abstractmethod
    def start(self):
        pass
