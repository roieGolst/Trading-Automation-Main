from abc import ABC, abstractmethod

from app.common.Response import Response


class IDatabase(ABC):
    @abstractmethod
    def create_group(self, group_name: str) -> Response[str]:
        pass

    @abstractmethod
    def add_account(self, group_name: str, account_name: str, account_id: str, account_details: dict) -> Response[str]:
        pass

    @abstractmethod
    def deactivate_account_from_group(self, group_name: str, account_name: str) -> Response[str]:
        pass
