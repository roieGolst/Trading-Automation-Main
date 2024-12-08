from app.service.grpc.ITradingStub import ITradingStub
# from app.service.grpc.proto.dist_worker.types_pb2 import Status
# from app.service.grpc.proto.dist_worker.ActivationTask_pb2 import Task as ActivationTask
# from app.service.grpc.proto.dist_worker.ActivationTask_pb2 import Response as ActivationResponse
# from app.service.grpc.proto.dist_worker.DeactivationTask_pb2 import Task as DeactivationTask
# from app.service.grpc.proto.dist_worker.TransactionTask_pb2 import Task as TransactionTask
from app.service.grpc.proto.dist_worker.WorkerTradingService_pb2_grpc import WorkerTradingServiceStub

from app.service.grpc.proto.dist_worker.ActivationTask_pb2 import Task as ActivationTask
from app.service.grpc.proto.dist_worker.DeactivationTask_pb2 import Task as DeactivationTask
from app.service.grpc.proto.dist_worker.TransactionTask_pb2 import Task as TransactionTask
import grpc


class MyTradingStub(ITradingStub, WorkerTradingServiceStub):
    def __init__(self, channel):
        # Initialize the WorkerTradingServiceStub with the provided channel
        WorkerTradingServiceStub.__init__(self, channel)

    def activation(self, activation_task: ActivationTask):
        # Call the gRPC Activation method
        response = self.Activation(activation_task)
        return response

    def deactivation(self, deactivation_task: DeactivationTask):
        # Call the gRPC Deactivation method
        response = self.Deactivation(deactivation_task)
        return response

    def transaction(self, transaction_task: TransactionTask):
        # Call the gRPC Transaction method
        response = self.Transaction(transaction_task)
        return response
