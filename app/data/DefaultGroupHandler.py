import threading

from dataclasses import dataclass
from app.data.IGroupHandler import IGroupHandler
from app.db.IDatabase import IDatabase
from app.service.grpc.ITradingStub import ITradingStub


@dataclass
class DefaultGroupHandlerParams:
    db: IDatabase


class DefaultGroupHandler(IGroupHandler):
    __db: IDatabase
    __new_group_task_queue: list[str]
    __group_dist: dict[str, ITradingStub]

    __instance = None
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            with cls.__lock:
                if not cls.__instance:
                    cls.__instance = super(DefaultGroupHandler, cls).__new__(cls)
        return cls.__instance

    def __init__(self, params: DefaultGroupHandlerParams):
        self.__db = params.db
        self.__new_group_task_queue = list()
        self.__group_dist = dict()

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            with cls.__lock:
                if not cls.__instance:
                    raise Exception("Instance not initiate yet")
        return cls.__instance

    def create_group(self, group_name: str):
        self.__new_group_task_queue.append(group_name)

    def get_group(self, group_name: str) -> ITradingStub:
        group = self.__group_dist.get(group_name, None)

        if not group:
            # TODO: return no client
            raise "Group not created yet... :<("

        return group

    def get_groups(self) -> [ITradingStub]:
        return self.__group_dist.values()

    def _set_group(self, group_name: str, stub: ITradingStub):
        self.__group_dist[group_name] = stub
        self.__db.create_group(group_name)

    def on_new_client(self, stub: ITradingStub) -> None:
        if not self.__new_group_task_queue:
            return None

        group_name = self.__new_group_task_queue.pop(0)
        print(f"Group consumer: {group_name}")
        self._set_group(group_name, stub)
        self.__db.create_group(group_name)

