from abc import ABC, abstractmethod

from app.common.Response import Response
from app.service.grpc.model.types import Brokerage


class IDatabase(ABC):
    @abstractmethod
    def create_group(self, group_name: str) -> bool:
        """
        Creates an empty group if it does not exist in memory or in Redis.

        :param group_name: Name of the created group
        :return: bool
        """
        pass

    @abstractmethod
    def get_all_groups(self) -> list[str]:
        """
        Returns all existing groups by scanning keys that match Group:*.

        :return: List of all groups
        """
        pass

    @abstractmethod
    def get_group_accounts(self, group_name: str) -> set[str]:
        """
        Returns all account names belonging to the group.
        If group was created but never persisted (still empty), returns empty set.

        :param group_name: Name of the dedicated group
        :return: set of accounts keys
        """
        pass

    @abstractmethod
    def add_account(
            self,
            group_name: str,
            account_name: str,
            brokerage: Brokerage,
            account_details: dict
    ) -> bool:
        """
        Creates an account and associates it with a group. Also creates account details.

        :param group_name: Name of the dedicated group
        :param account_name: Account name
        :param brokerage: The associated account broker
        :param account_details: Account login details dictionary
        :return: bool
        """
        pass

    @abstractmethod
    def get_account(self, account_name: str) -> dict:
        """
        Returns account hash as a dictionary.

        :param account_name: Account name
        :return: dict
        """
        pass

    @abstractmethod
    def get_account_details(self, account_name: str) -> dict:
        """
        Retrieve all details of the account.

        :param account_name: Account name
        :return: dict
        """
        pass

    @abstractmethod
    def deactivate_account(self, account_name: str) -> bool:
        """
        Deactivate account by name

        :param account_name: Account name
        :return: bool
        """
        pass
