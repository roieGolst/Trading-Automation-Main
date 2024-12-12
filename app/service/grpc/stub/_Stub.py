from typing import Callable

import grpc
from grpc import Channel
from grpc import ChannelConnectivity

from app.service.grpc.proto.dist_worker import ActivationTask_pb2 as Activation, DeactivationTask_pb2 as Deactivation, \
    TransactionTask_pb2 as Transaction
from app.service.grpc.proto.dist_worker.WorkerTradingService_pb2_grpc import WorkerTradingServiceStub
from app.service.grpc.proto.dist_worker.types_pb2 import Status
from app.service.grpc.stub.ITradingStub import ITradingStub


OnCloseCB = Callable[[str], None]


class _Stub(ITradingStub, WorkerTradingServiceStub):
    _id: str
    _channel: Channel
    _on_close_function: OnCloseCB
    _channel_idle_state_counter: int = 0

    def __init__(self, id: str, channel: Channel, on_close_cb: OnCloseCB):
        WorkerTradingServiceStub.__init__(self, channel)
        self._id = id
        self._channel = channel
        self._on_close_function = on_close_cb
        self._channel.subscribe(self._channel_state_callback, try_to_connect=True)

    def _channel_state_callback(self, state: ChannelConnectivity):
        """
        Callback function triggered on gRPC channel connectivity state changes.

        Behavior:
        ---------
        - If the channel enters the `IDLE` state twice:
            - This is treated as a lost connection. The channel is closed, and a
              callback (`self._on_close_function`) is triggered to handle reconnection.

        - If the channel transitions to `TRANSIENT_FAILURE` or `SHUTDOWN`:
            - The channel is immediately closed, and the callback is invoked.

        Parameters:
        -----------
        state : ChannelConnectivity
            The current connectivity state of the gRPC channel. Common states include:
            - `IDLE`: Channel is not actively connected but can reconnect.
            - `TRANSIENT_FAILURE`: Transient connection error, attempting to reconnect.
            - `SHUTDOWN`: Channel is closed and cannot be reused.

        Callback:
        ---------
        - `self._on_close_function(self._id)`:
            Invoked when the channel is deemed unusable to initiate reconnection.

        """
        if state == ChannelConnectivity.IDLE:
            self._channel_idle_state_counter += 1

        if self._channel_idle_state_counter > 1:
            self._channel.close()
            self._on_close_function(self._id)

        if state in [ChannelConnectivity.TRANSIENT_FAILURE, ChannelConnectivity.SHUTDOWN]:
            self._channel.close()
            self._on_close_function(self._id)

    def health_check(self):
        try:
            self.HealthCheck()
        except grpc.RpcError as err:
            print(err.code())

    def activation(self, task: Activation.Task) -> Activation.Response:
        try:
            result = self.Activation(task)
            return result
        except grpc.RpcError:
            return Activation.Response(
                status=Status.Failure,
                message="Stub error"
            )

    def deactivation(self, task: Deactivation.Task) -> Deactivation.Response:
        try:
            result = self.Deactivation(task)
            return result
        except grpc.RpcError:
            return Deactivation.Response(
                status=Status.Failure,
                message="Stub error"
            )

    def transaction(self, task: Transaction.Task) -> Transaction.Response:
        try:
            result = self.Transaction(task)
            return result
        except grpc.RpcError:
            return Transaction.Response(
                status=Status.Failure,
                message="Stub error"
            )
