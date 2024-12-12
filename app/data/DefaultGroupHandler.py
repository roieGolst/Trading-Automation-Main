import threading

from dataclasses import dataclass
from logging import Logger
from typing import Optional

from typing_extensions import Self

from app.data.IGroupHandler import IGroupHandler
from app.db.IDatabase import IDatabase
from app.service.grpc.stub.ITradingStub import ITradingStub
from app.service.grpc.stub.IStubHandler import IStubHandler, StubFactory
import app.service.grpc as grpc


@dataclass
class DefaultGroupHandlerParams:
    db: IDatabase
    logger: Logger


class DefaultGroupHandler(IGroupHandler, IStubHandler):
    _db: IDatabase
    _logger: Logger
    _new_group_task_queue: set[str]
    _group_dist: dict[str, ITradingStub]

    __instance = None
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            with cls.__lock:
                if not cls.__instance:
                    cls.__instance = super(DefaultGroupHandler, cls).__new__(cls)
        return cls.__instance

    def __init__(self, params: DefaultGroupHandlerParams):
        self._db = params.db
        self._logger = params.logger
        self._new_group_task_queue = set()
        self._group_dist = dict()

    @classmethod
    def get_instance(cls) -> Self:
        if not cls.__instance:
            with cls.__lock:
                if not cls.__instance:
                    raise Exception("Instance not initiate yet")
        return cls.__instance

    def create_group(self, group_name: str):
        self._new_group_task_queue.add(group_name)

    def get_group(self, group_name: str) -> Optional[ITradingStub]:
        group = self._group_dist.get(group_name)

        if not group:
            return None

        return group

    def get_groups(self) -> [ITradingStub]:
        return self._group_dist.values()

    def _set_group(self, group_name: str, stub: ITradingStub):
        self._group_dist[group_name] = stub
        self._db.create_group(group_name)

    def on_new_client(self, stub_factory: StubFactory) -> None:
        if not self._new_group_task_queue:
            return None

        group_name = self._new_group_task_queue.pop()
        stub = stub_factory(group_name)

        self._logger.debug(f"Waiting group consumed: {group_name}")
        self._set_group(group_name, stub)
        self._db.create_group(group_name)

    def on_client_close(self, client_id: str):
        self.__build_group_queue_task()

    def __build_group_queue_task(self):
        # TODO: Implement!!!!!!
        self._logger.info("!!!!!! Method not implemented yet !!!!!!")
