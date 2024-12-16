import threading
from dataclasses import dataclass
import redis
from typing_extensions import Self
from app.db.IDatabase import IDatabase
from app.service.grpc.model.types import Brokerage


@dataclass
class RedisConnectionParams:
    host: str
    port: int


class RedisDB(IDatabase):
    __GROUP_PREFIX: str = "Group"
    __ACCOUNT_PREFIX: str = "Account"
    __DETAILS_PREFIX: str = f"{__ACCOUNT_PREFIX}:Details"

    __connection_params: RedisConnectionParams
    __redis: redis.Redis
    _empty_group_set: set[str]
    __instance = None
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            with cls.__lock:
                if not cls.__instance:
                    cls.__instance = super(RedisDB, cls).__new__(cls)
        return cls.__instance

    def __init__(self, connection_params: RedisConnectionParams):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.__connection_params = connection_params
            self._empty_group_set = set()

    @classmethod
    def get_instance(cls) -> Self:
        if not cls.__instance:
            with cls.__lock:
                if not cls.__instance:
                    raise Exception("Instance not initiated yet")
        return cls.__instance

    def init(self):
        try:
            self.__redis = redis.Redis(
                host=self.__connection_params.host,
                port=self.__connection_params.port,
                decode_responses=True
            )
        except redis.RedisError as err:
            raise RuntimeError(f"Redis Connection Error: {err}")

    # ---------------------
    # Helper Key Generators
    # ---------------------
    def __get_group_key(self, group_name: str) -> str:
        return f"{self.__GROUP_PREFIX}:{group_name}"

    def __get_account_key(self, account_name: str) -> str:
        return f"{self.__ACCOUNT_PREFIX}:{account_name}"

    def __get_account_details_key(self, account_name: str) -> str:
        return f"{self.__DETAILS_PREFIX}:{account_name}"

    # ---------------------
    # Group CRUD Operations
    # ---------------------
    def create_group(self, group_name: str) -> bool:
        group_key = self.__get_group_key(group_name)
        if group_key in self._empty_group_set or self.__redis.exists(group_key):
            return False

        self._empty_group_set.add(group_key)
        return True

    def get_all_groups(self) -> list[str]:
        groups = []
        cursor = 0
        while True:
            cursor, keys = self.__redis.scan(cursor=cursor, match=f"{self.__GROUP_PREFIX}:*", count=100)
            for key in keys:
                group_name = key.split(":", 1)[1]
                groups.append(group_name)
            if cursor == 0:
                break

        for g_key in self._empty_group_set:
            group_name = g_key.split(":", 1)[1]
            if group_name not in groups:
                groups.append(group_name)

        return groups

    def get_group_accounts(self, group_name: str) -> set[str]:
        group_key = self.__get_group_key(group_name)

        if group_key in self._empty_group_set:
            return set()

        if not self.__redis.exists(group_key):
            return set()

        return self.__redis.smembers(group_key)

    # ----------------------
    # Account CRUD Operations
    # ----------------------
    def add_account(
            self,
            group_name: str,
            account_name: str,
            brokerage: Brokerage,
            account_details: dict
    ) -> bool:
        group_key = self.__get_group_key(group_name)
        if not self.__redis.exists(group_key) and group_key not in self._empty_group_set:
            return False

        if group_key in self._empty_group_set:
            self._empty_group_set.remove(group_key)
            self.__redis.sadd(group_key, "")  # Add dummy to create the set
            self.__redis.srem(group_key, "")  # Remove dummy

        account_key = self.__get_account_key(account_name)
        details_key = self.__get_account_details_key(account_name)

        if self.__redis.exists(account_key):
            return False

        self.__redis.hset(account_key, mapping={
            "account_name": account_name,
            "brokerage": brokerage.value,
            "status": "1"
        })
        if account_details:
            self.__redis.hset(details_key, mapping=account_details)

        self.__redis.sadd(group_key, account_name)
        return True

    def get_account(self, account_name: str) -> dict:
        account_key = self.__get_account_key(account_name)
        account_info = self.__redis.hgetall(account_key)
        return account_info

    def deactivate_account(self, account_name: str) -> bool:
        account_key = self.__get_account_key(account_name)

        if not self.__redis.exists(account_key):
            return False

        account_mapping = self.__redis.hgetall(account_key)
        account_mapping["status"] = 0

        self.__redis.hset(account_key, mapping=account_mapping)
        return True

    # ----------------------------
    # Account Details CRUD Methods
    # ----------------------------
    def get_account_details(self, account_name: str) -> dict:
        details_key = self.__get_account_details_key(account_name)
        return self.__redis.hgetall(details_key)
