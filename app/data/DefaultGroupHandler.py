import threading

from dataclasses import dataclass
from logging import Logger
from typing import Optional

from typing_extensions import Self

from app.data.IGroupHandler import IGroupHandler
from app.db.IDatabase import IDatabase
from app.service.grpc.model.types import ActivationTask, Brokerage
from app.service.grpc.stub.ITradingStub import ITradingStub
from app.service.grpc.stub.IStubHandler import IStubHandler, StubFactory


@dataclass
class DefaultGroupHandlerParams:
    db: IDatabase
    logger: Logger


class DefaultGroupHandler(IGroupHandler, IStubHandler):
    _db: IDatabase
    _logger: Logger
    _new_group_task_queue: set[str]
    _pending_closed_groups: list[tuple[str, list[ActivationTask]]]
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
        self._pending_closed_groups = list()
        self._group_dist = dict()

    @classmethod
    def get_instance(cls) -> Self:
        if not cls.__instance:
            with cls.__lock:
                if not cls.__instance:
                    raise Exception("Instance not initiate yet")
        return cls.__instance

    def create_group(self, group_name: str) -> bool:
        if group_name in self._new_group_task_queue:
            return False

        self._logger.debug(f"Creating new group named: {group_name}")
        self._new_group_task_queue.add(group_name)
        return True

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

    def on_new_client(self, stub_factory: StubFactory) -> bool:
        if not self._new_group_task_queue and not self._pending_closed_groups:
            return False

        if self._pending_closed_groups:
            group_name, task_queue = self._pending_closed_groups.pop(0)
            stub = stub_factory(group_name)
            self._logger.debug(f"Pending group consumed: {group_name}")
            self._set_group(group_name, stub)

            for task in task_queue:
                try:
                    stub.activation(task)
                except Exception:
                    self._logger.exception("Stub Error!!!!")
                    return False
            return True

        group_name = self._new_group_task_queue.pop()
        stub = stub_factory(group_name)

        self._logger.debug(f"Waiting group consumed: {group_name}")
        self._set_group(group_name, stub)
        self._db.create_group(group_name)

        return True

    def on_client_close(self, id: str):
        self._logger.info(f"Stub: {id} closed. build pending task queue!")
        task_queue = self.__build_group_queue_task(id)
        self._group_dist.pop(id)
        self._pending_closed_groups.append((id, task_queue))

    def __build_group_queue_task(self, group_name: str) -> list[ActivationTask]:
        group_accounts = self._db.get_group_accounts(group_name)

        if not group_accounts:
            return []

        queue: list[ActivationTask] = []
        for account_id in group_accounts:
            account = self._db.get_account(account_id)
            if not account or not account.get("status"):
                continue

            account_details = self._db.get_account_details(account_id)
            account_name = account.get("account_name")
            account_brokerage = account.get("brokerage")

            if not account_details or not account_brokerage or not account_name:
                continue

            activation_task = ActivationTask(
                account_name=account_name,
                brokerage=Brokerage(int(account_brokerage)),
                creds=account_details
            )

            queue.append(activation_task)

        return queue
