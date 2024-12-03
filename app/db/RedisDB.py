from dataclasses import dataclass

import redis

from db.IDatabase import IDatabase


@dataclass
class RedisConnectionParams:
    # TODO: Add logger
    host: str
    port: int
    # TODO: Added more if needed


class RedisDB(IDatabase):
    __GROUP_PREFIX: str = "Group"
    __ACCOUNT_PREFIX: str = "Account"
    __DETAILS_SUFFIX: str = "Details"

    __connection_params: RedisConnectionParams
    __redis: redis.Redis
    __empty_group_set = set[str]

    def __init__(self, connection_params: RedisConnectionParams):
        self.__connection_params = connection_params
        self.__empty_group_set = set()

    def init(self):
        try:
            self.__redis = redis.Redis(host=self.__connection_params.host, port=self.__connection_params.port)
        except redis.RedisError as err:
            # TODO: Add to logger
            raise f"Redis Connection Error: {err}"

    def create_group(self, group_name: str) -> bool:
        # TODO: TBD: If empty set is needed or do nothing
        group_key = self.__get_group_key(group_name)
        if group_key in self.__empty_group_set:
            return False

        self.__empty_group_set.add(group_key)
        return True

    def add_account(self, group_name: str, account_name: str, account_id: str, account_details: dict) -> bool:
        group_key = self.__get_group_key(group_name)
        group = self.__redis.smembers(group_key)

        if not group or group_key not in self.__empty_group_set:
            return False

        self.__empty_group_set.remove(group_key)
        account_key = self.__get_account_key(account_name)
        account_details_key = self.__get_account_details_key(account_name)

        self.__redis.sadd(group_key, account_name)

        # TODO: Replace with builder
        self.__redis.hset(account_key, mapping={
            "account_id": account_id,
            "status": "true",
        })
        self.__redis.hset(account_details_key, mapping=account_details)
        return True

    def deactivate_account_from_group(self, group_name: str, account_name: str) -> bool:
        group_key = self.__get_group_key(group_name)
        group_accounts = self.__redis.smembers(group_key)

        if not group_accounts:
            return False

        if account_name not in group_accounts:
            return False

        account_key = self.__get_account_key(account_name)
        account_info = self.__redis.hgetall(account_key)
        account_status = account_info.get("status", None)

        if not account_info or not account_status:
            return False

        account_info["status"] = "false"
        self.__redis.hset(account_key, mapping=account_info)

        return True

    def __get_group_key(self, group_name: str):
        return f"{self.__GROUP_PREFIX}:{group_name}"

    def __get_account_key(self, group_name: str, account_name: str):
        return f"{self.__get_group_key(group_name)}:{self.__ACCOUNT_PREFIX}:{account_name}"

    def __get_account_details_key(self, group_name: str, account_name: str):
        return f"{self.__get_account_key(group_name, account_name)}:{self.__DETAILS_SUFFIX}"