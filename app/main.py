import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi import Response

from app.data.DefaultGroupHandler import DefaultGroupHandler, DefaultGroupHandlerParams
from app.db.RedisDB import RedisDB, RedisConnectionParams
from app.service.grpc.GrpcService import GrpcService, GrpcConnectionParams
import app.service.grpc.proto.dist_worker.ActivationTask_pb2 as Activation
import app.service.grpc.proto.dist_worker.DeactivationTask_pb2 as Deactivation
import app.service.grpc.proto.dist_worker.TransactionTask_pb2 as Transaction
from app.service.grpc.proto.dist_worker.types_pb2 import BaseTask, UUID

from app.service.grpc.proto.dist_worker.WorkerTradingService_pb2_grpc import WorkerTradingServiceStub

GROUP_NAME = "Roie"
db = RedisDB(
    connection_params=RedisConnectionParams(
        host="localhost",
        port=6379
    )
)

# print(f"Thread id: {threading.get_ident()}")

group_handler = DefaultGroupHandler(
    params=DefaultGroupHandlerParams(
        db=RedisDB.get_instance()
    )
)

@asynccontextmanager
async def lifespan(_: FastAPI):
    RedisDB.get_instance().init()
    group_handler.create_group(GROUP_NAME)
    group_handler.create_group("Yakir")

    grpc_service = GrpcService(
        params=GrpcConnectionParams(
            "0.0.0.0",
            50052,
            on_new_client=group_handler.on_new_client
        )
    )

    # grpc_thread = threading.Thread(target=grpc_service.start, args=())
    # grpc_thread.start()
    grpc_service.start()
    yield
    print("Bye..")

app = FastAPI(lifespan=lifespan)
@app.post(
    path="/activate",
)
def activate_user(group_name: str):
    group_stub: WorkerTradingServiceStub = group_handler.get_group(group_name)
    try:
        account_id: Activation.Response = group_stub.activation(
            activation_task=Activation.Task(
                base_task=BaseTask(task_id=UUID(value="2f3667fe-a9ff-4254-b24a-95c83d66f500")),
                brokerage=Activation.Brokerage.BBAE,
                account_details=Activation.ActivationCreds(
                    USERNAME="roieUsername123",
                    PASSWORD="roieBestPasswordEver"
                )
            )
        )

    except Exception as err:
        # TODO: Replace with error handling
        print(f"Invalid stub: {err}")
        return Response(
            status_code=500
        )

    db.add_account(
        group_name=group_name,
        account_name="roieBBAE",
        account_id=account_id.account_id.value,
        account_details={
            "USERNAME": "roieUsername123",
            "PASSWORD": "roieBestPasswordEver"
        }
    )
    return {"accountId": account_id.account_id.value}

@app.post("/deactivate")
def deactivate_task(group_name: str, account_id: str):
    groups_stub = group_handler.get_group(group_name)

    deactivation_task = Deactivation.Task(
        base_task=BaseTask(task_id=UUID(value="3d757fb9-1c33-4cbe-ae0e-bf4d8cdd45b1")),
        account_id=UUID(value=account_id)
    )

    response: Deactivation.Response = groups_stub.deactivation(deactivation_task)
    return {
        "status": response.status,
        "message": response.message
    }

@app.post("/transaction")
def transaction(group_name: str):
    groups_stub = group_handler.get_group(group_name)

    transaction_task = Transaction.Task(
        base_task=BaseTask(task_id=UUID(value="a9327d24-826b-427c-9e98-fa3ba914bbda")),
        method=Transaction.TransactionMethod.Buy,
        amount=1,
        ticker="AAPL"
    )

    transaction_task_response: Transaction.Response = groups_stub.transaction(transaction_task)

    return {
        "status": transaction_task_response.status,
        "message": transaction_task_response.message
    }