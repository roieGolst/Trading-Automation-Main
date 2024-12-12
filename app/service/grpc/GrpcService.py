from concurrent import futures
from dataclasses import dataclass, field
from logging import Logger

import grpc
from grpc import Channel
from grpc._server import _Server

from app.service.grpc.stub.IStubHandler import IStubHandler
from .IGrpcService import IGrpcService
from ._MainTradingServiceServicer import _MainTradingServiceServicer
from .proto.dist_main.MainTradingService_pb2_grpc import add_MainTradingServiceServicer_to_server
from .stub._Stub import _Stub


@dataclass
class GrpcOptions:
    """
    gRPC channel options data class.

    Parameters:
    - ping_ms_interval (int): Time interval for pinging the channel (in milliseconds).
      Default is 10000 (10 seconds).
    - timeout_ms (int): Timeout for the channel (in milliseconds).
      Default is 5000 (5 seconds).
    """
    ping_ms_interval: int = field(default=10000)
    timeout_ms: int = field(default=5000)


@dataclass
class GrpcConnectionParams:
    host: str
    port: int
    stub_handler: IStubHandler
    logger: Logger
    grpc_options: GrpcOptions = GrpcOptions()


class GrpcService(IGrpcService):
    _host: str
    _port: int
    _options: GrpcOptions
    _stub_handler: IStubHandler
    _logger: Logger
    _server: _Server

    def __init__(self, params: GrpcConnectionParams):
        self._host = params.host
        self._port = params.port
        self._options = params.grpc_options
        self._stub_handler = params.stub_handler
        self._logger = params.logger
        self._create_group_queue = []

    def start(self):
        self._logger.debug("Staring gRPC server for Ping/Pong communication on: "
                           "f'{self.host}:{self.port}'")
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
        add_MainTradingServiceServicer_to_server(
            servicer=_MainTradingServiceServicer(
                self._run_client,
                self._logger
            ),
            server=self._server
        )

        self._server.add_insecure_port(f'{self._host}:{self._port}')
        self._server.start()
        self._logger.info("gRPC server is listening for Ping/Pong communication on: "
                          "f'{self.host}:{self.port}...'")

    def _run_client(self, host: str):
        self._logger.info(f"Trying to crate gRPC connection on: {host}")
        channel: Channel = grpc.insecure_channel(
            host,
            options=[
                ('grpc.keepalive_time_ms', self._options.ping_ms_interval),
                ('grpc.keepalive_timeout_ms', self._options.timeout_ms),
                ('grpc.keepalive_permit_without_calls', True),
            ]
        )

        self._stub_handler.on_new_client(
            lambda stub_id: _Stub(
                stub_id,
                channel,
                self._stub_handler.on_client_close
            )
        )

        self._logger.info(f"Successfully connect to client in {host}")
