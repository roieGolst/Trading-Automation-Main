import re
from logging import Logger
from typing import Callable
from urllib import parse

import grpc
from app.service.grpc.proto.dist_main.MainTradingService_pb2 import Ping, Pong
from app.service.grpc.proto.dist_main.MainTradingService_pb2_grpc import MainTradingServiceServicer


def extract_ip(encoded_str):
    try:
        decoded_str = parse.unquote(encoded_str)
        pattern = re.compile(r'ipv6:\[(.*?)]:\d+|ipv4:([\d.]+):\d+')

        match = pattern.match(decoded_str)
        if match:
            if match.group(1):
                return f'[{match.group(1)}]'
            else:
                return match.group(2)
        return None
    except Exception:
        return None


class _MainTradingServiceServicer(MainTradingServiceServicer):
    _new_client_cb: Callable[[str], None]
    _logger: Logger

    def __init__(self, create_client_cb: Callable[[str], None], logger: Logger):
        super().__init__()
        self._new_client_cb = create_client_cb
        self._logger = logger

    def ping(self, request: Ping, context: grpc.ServicerContext):
        worker_ip = extract_ip(context.peer())

        if not worker_ip:
            self._logger.error(f"Invalid clint IP: {context.peer()}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Ip validation failed!")
            return

        try:
            self._logger.debug(f"Ping Request from: {worker_ip}:{request.return_to_port}")
            self._new_client_cb(f"{worker_ip}:{request.return_to_port}")
        except grpc.RpcError as err:
            self._logger.exception(f"Failed occurred when creating connection to: {worker_ip}:{request.return_to_port}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to connect client server!")
            return

        return Pong()
