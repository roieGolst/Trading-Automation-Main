import re
from typing import Callable, Coroutine
from urllib import parse

import grpc
from service.grpc.proto.dist_main.MainTradingService_pb2 import Ping, Pong
from service.grpc.proto.dist_main.MainTradingService_pb2_grpc import MainTradingServiceServicer


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
        # TODO: Replace with error handling
        return None


class MyMainTradingServiceServicer(MainTradingServiceServicer):
    new_client_cb: Callable[[str], Coroutine]

    def __init__(self, create_client_cb: Callable[[str], Coroutine]):
        super().__init__()
        self.new_client_cb = create_client_cb

    def ping(self, request: Ping, context: grpc.ServicerContext):
        worker_ip = extract_ip(context.peer())

        if not worker_ip:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Ip validation failed!")
            return

        try:
            self.new_client_cb(f"{worker_ip}:{request.return_to_port}")
        except grpc.RpcError as err:
            # TODO: Add logger
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to connect client server!")
            return

        return Pong()