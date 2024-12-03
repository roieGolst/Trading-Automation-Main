import time

from data.DefaultGroupHandler import DefaultGroupHandler, DefaultGroupHandlerParams
from db.RedisDB import RedisDB, RedisConnectionParams
from service.grpc.GrpcService import GrpcService, GrpcConnectionParams
from service.grpc.proto.dist_worker.ActivationTask_pb2 import Task, Brokerage, ActivationCreds
from service.grpc.proto.dist_worker.types_pb2 import BaseTask, UUID

import threading


def main():
    GROUP_NAME = "Roie"

    db = RedisDB(
        connection_params=RedisConnectionParams(
            host="localhost",
            port=6379
        )
    )
    db.init()

    group_handler = DefaultGroupHandler(
        params=DefaultGroupHandlerParams(
            db=db
        )
    )
    group_handler.create_group(GROUP_NAME)

    grpc_service = GrpcService(
        params=GrpcConnectionParams(
            "[::]",
            50052,
            on_new_client=group_handler.on_new_client
        )
    )

    grpc_thread = threading.Thread(target=grpc_service.start, args=())
    grpc_thread.start()

    time.sleep(5)

    group_stub = group_handler.get_group(GROUP_NAME)
    account_id = group_stub.activation(
        activation_task=Task(
            base_task=BaseTask(task_id=UUID(value="2f3667fe-a9ff-4254-b24a-95c83d66f500")),
            brokerage=Brokerage.BBAE,
            account_details=ActivationCreds(
                USERNAME="roieUsername123",
                PASSWORD="roieBestPasswordEver"
            )
        )
    )

    print(account_id)

if __name__ == '__main__':
    main()
