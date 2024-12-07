from abc import ABC, abstractmethod
from concurrent import futures
from dataclasses import dataclass
from typing_extensions import Callable

import grpc
from grpc._server import _Server

from .ITradingStub import ITradingStub
from .MyMainTradingServiceServicer import MyMainTradingServiceServicer
from .MyTradingStub import MyTradingStub
from .proto.dist_main.MainTradingService_pb2_grpc import add_MainTradingServiceServicer_to_server
# from service.grpc.proto.dist_worker.ActivationTask_pb2 import Task, Brokerage, ActivationCreds
# from service.grpc.proto.dist_worker.types_pb2 import BaseTask, UUID
# from service.grpc.proto.dist_worker.WorkerTradingService_pb2_grpc import WorkerTradingServiceStub


# # def run_client(host: str):
# #     with grpc.insecure_channel(f'{host}') as channel:
# #         stub = WorkerTradingServiceStub(channel)
# #
# #         activation_task = ActivationTask.Task(
# #             base_task=BaseTask(task_id=UUID(value="123e4567-e89b-12d3-a456-426614174000")),
# #             brokerage=ActivationTask.Brokerage.Tastytrade,
# #             account_details=ActivationTask.ActivationCreds(
# #                 USERNAME="LironGolst",
# #                 PASSWORD="liron12312312312321"
# #             )
# #         )
# #
# #         response: ActivationTask.Response = stub.Activation(activation_task)
# #         print(f"Account Id: {response.account_id}")
# #
# #         activation_task2 = ActivationTask.Task(
# #             base_task=BaseTask(task_id=UUID(value="3d757fb9-1c33-4cbe-ae0e-bf4d8cdd45b1")),
# #             brokerage=ActivationTask.Brokerage.BBAE,
# #             account_details=ActivationTask.ActivationCreds(
# #                 USERNAME="RoieGoolst ",
# #                 PASSWORD="sdaspassw12313"
# #             )
# #         )
# #
# #         account_id: ActivationTask.Response = stub.Activation(activation_task2)
# #         print(f"Account Id: {account_id.account_id}")
# #
# #         # deactivation_task = DeactivationTask.Task(
# #         #     base_task=BaseTask(task_id=UUID(value="3d757fb9-1c33-4cbe-ae0e-bf4d8cdd45b1")),
# #         #     account_id=UUID(value=account_id.account_id.value)
# #         # )
# #         #
# #         # try:
# #         #     deactivation_response = stub.Deactivation(deactivation_task)
# #         # except Exception as err:
# #         #     print(err)
# #         #     return
# #         # #
# #         # if deactivation_response.status != Status.Success:
# #         #     raise "Not working"
# #         #
# #         # print(f"Deactivate account id: {account_id}")
# #
# #         transaction_task = TransactionTask.Task(
# #             base_task=BaseTask(task_id=UUID(value="a9327d24-826b-427c-9e98-fa3ba914bbda")),
# #             method=TransactionTask.TransactionMethod.Buy,
# #             amount=1,
# #             ticker="AAPL"
# #         )
# #
# #         transaction_task_response: TransactionTask.Response = stub.Transaction(transaction_task)
# #
# #         if transaction_task_response.status != Status.Failure:
# #             print(f"Container response: {transaction_task}")
#
@dataclass
class GrpcConnectionParams:
    host: str
    port: int
    on_new_client: Callable[[ITradingStub], None]
#     TODO: Add Logger to class



# TODO: Reconsidering the Vitality
class IGrpcService(ABC):
    @abstractmethod
    def start(self):
        pass

class GrpcService(IGrpcService):
    _connection_params: GrpcConnectionParams
    _server: _Server

    def __init__(self, params: GrpcConnectionParams):
        self._connection_params = params
        self._create_group_queue = []

    def start(self):
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
        add_MainTradingServiceServicer_to_server(MyMainTradingServiceServicer(self._run_client), self._server)

        self._server.add_insecure_port(f'{self._connection_params.host}:{self._connection_params.port}')
        self._server.start()
        # TODO: Think about the thread block with server in background
        # self._server.wait_for_termination()

    def _run_client(self, host: str):
        try:
            channel = grpc.insecure_channel(f'{host}')
            print(f"Successfully connect to client in {host}")
            stub = MyTradingStub(channel)
            self._connection_params.on_new_client(stub)

        except grpc.RpcError as err:
            # TODO: Add logger
            raise f"Grpc Error: {err}"

