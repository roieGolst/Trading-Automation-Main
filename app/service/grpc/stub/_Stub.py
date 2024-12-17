from typing import Callable

import grpc
from grpc import Channel
from grpc import ChannelConnectivity

from app.common.Response import Response
from app.service.grpc.model.types import ActivationTask, ActivationResponse, Brokerage, DeactivationTask, \
    DeactivationResponse, TransactionTask, TransactionResponse
from app.service.grpc.proto.dist_worker import ActivationTask_pb2 as Activation, DeactivationTask_pb2 as Deactivation, \
    TransactionTask_pb2 as Transaction
from app.service.grpc.proto.dist_worker.ActivationTask_pb2 import Brokerage as GrpcBrokerage, ActivationCreds
from app.service.grpc.proto.dist_worker.WorkerTradingService_pb2_grpc import WorkerTradingServiceStub
from app.service.grpc.proto.dist_worker.types_pb2 import Status, BaseTask, UUID
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

    def activation(self, task: ActivationTask) -> Response[ActivationResponse]:
        try:
            activation_task = Activation.Task(
                base_task=BaseTask(task_id=UUID(value=str(task.task_id))),
                account_name=task.account_name,
                brokerage=task.brokerage,
                account_details=self._cast_creds(task.brokerage.name, task.cred)
            )

            result: Activation.Response = self.Activation(activation_task)
            status = True if result.status == Status.Success else False

            return Response[ActivationResponse](
                success=True,
                value=ActivationResponse(success=status)
            )
        except grpc.RpcError:
            return Response(
                success=False,
                error="Stub error"
            )

    def _cast_brokerage(self, brokerage: Brokerage) -> GrpcBrokerage:
        casting_map = {
            Brokerage.BBAE: GrpcBrokerage.BBAE,
            Brokerage.Chase: GrpcBrokerage.Chase,
            Brokerage.DSPAC: GrpcBrokerage.DSPAC,
            Brokerage.Fennel: GrpcBrokerage.Fennel,
            Brokerage.Fidelity: GrpcBrokerage.Fidelity,
            Brokerage.Firstrade: GrpcBrokerage.Firstrade,
            Brokerage.Public: GrpcBrokerage.Public,
            Brokerage.Robinhood: GrpcBrokerage.Robinhood,
            Brokerage.Schwab: GrpcBrokerage.Schwab,
            Brokerage.SoFi: GrpcBrokerage.SoFi,
            Brokerage.Tornado: GrpcBrokerage.Tornado,
            Brokerage.Tradier: GrpcBrokerage.Tradier,
            Brokerage.Tastytrade: GrpcBrokerage.Tastytrade,
            Brokerage.Webull: GrpcBrokerage.Webull,
            Brokerage.Vanguard: GrpcBrokerage.Vanguard,
            Brokerage.WellsFargo: GrpcBrokerage.WellsFargo,
        }

        return casting_map[brokerage]

    def _cast_creds(self, broker_name: str, account_details: dict[str, any]) -> ActivationCreds:
        broker_fields = {
            'BBAE': ['USERNAME', 'PASSWORD'],
            'Chase': ['USERNAME', 'PASSWORD', 'PHONE_LAST_FOUR', 'DEBUG'],
            'DSPAC': ['USERNAME', 'PASSWORD'],
            'Fennel': ['EMAIL'],
            'Fidelity': ['USERNAME', 'PASSWORD', 'TOTP_SECRET_OR_NA'],
            'Firstrade': ['USERNAME', 'PASSWORD', 'OTP'],
            'Public': ['USERNAME', 'PASSWORD'],
            'Robinhood': ['USERNAME', 'PASSWORD', 'TOTP_OR_NA'],
            'Schwab': ['USERNAME', 'PASSWORD', 'TOTP_SECRET_OR_NA'],
            'SoFi': ['USERNAME', 'PASSWORD', 'TOTP_SECRET'],
            'Tastytrade': ['USERNAME', 'PASSWORD'],
            'Tornado': ['EMAIL', 'PASSWORD'],
            'Tradier': ['ACCESS_TOKEN'],
            'Vanguard': ['USERNAME', 'PASSWORD', 'PHONE_LAST_FOUR', 'DEBUG'],
            'Webull': ['USERNAME', 'PASSWORD', 'DID', 'TRADING_PIN'],
            'WellsFargo': ['USERNAME', 'PASSWORD', 'PHONE_LAST_FOUR'],
        }

        fields = broker_fields.get(broker_name)
        if not fields:
            raise ValueError(f"Broker '{broker_name}' is not supported for serialization.")

        details_fields = {}
        for field in fields:
            value = account_details.get(field)
            if value is None:
                raise ValueError(f"Missing field '{field}' for broker '{broker_name}'.")

            details_fields[field] = value

        return ActivationCreds(**details_fields)

    def deactivation(self, task: DeactivationTask) -> DeactivationResponse:
        try:
            deactivation_task = Deactivation.Task(
                base_task=BaseTask(task_id=UUID(value=str(task.task_id))),
                account_id=UUID(value=str(task.account_id))
            )
            result = self.Deactivation(deactivation_task)
            return result
        except grpc.RpcError:
            return Deactivation.Response(
                status=Status.Failure,
                message="Stub error"
            )

    def transaction(self, task: TransactionTask) -> TransactionResponse:
        try:
            transaction_task = Transaction.Task(
                base_task=BaseTask(task_id=UUID(value=str(task.task_id))),
                method=task.transaction_method,
                amount=task.amount,
                ticker=task.ticker
            )

            result = self.Transaction(transaction_task)
            return result
        except grpc.RpcError:
            return Transaction.Response(
                status=Status.Failure,
                message="Stub error"
            )
