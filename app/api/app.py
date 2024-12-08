from fastapi import APIRouter, Response

from app.data.DefaultGroupHandler import DefaultGroupHandler
from app.db.RedisDB import RedisDB
from app.service.grpc.ITradingStub import ITradingStub
from app.service.grpc.proto.dist_worker.types_pb2 import BaseTask, UUID
import app.service.grpc.proto.dist_worker.ActivationTask_pb2 as Activation
import app.service.grpc.proto.dist_worker.DeactivationTask_pb2 as Deactivation
import app.service.grpc.proto.dist_worker.TransactionTask_pb2 as Transaction

router = APIRouter()


# TODO: Add endpoint models
@router.post(path="/activate")
def activate_user(group_name: str):
    group_stub: ITradingStub = DefaultGroupHandler.get_instance().get_group(group_name)
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

    RedisDB.get_instance().add_account(
        group_name=group_name,
        account_name="roieBBAE",
        account_id=account_id.account_id.value,
        account_details={
            "USERNAME": "roieUsername123",
            "PASSWORD": "roieBestPasswordEver"
        }
    )
    return {"accountId": account_id.account_id.value}


# TODO: Add endpoint models
@router.post("/deactivate")
def deactivate_task(group_name: str, account_id: str):
    groups_stub = DefaultGroupHandler.get_instance().get_group(group_name)

    deactivation_task = Deactivation.Task(
        base_task=BaseTask(task_id=UUID(value="3d757fb9-1c33-4cbe-ae0e-bf4d8cdd45b1")),
        account_id=UUID(value=account_id)
    )

    response: Deactivation.Response = groups_stub.deactivation(deactivation_task)
    return {
        "status": response.status,
        "message": response.message
    }


# TODO: Add endpoint models
@router.post("/transaction")
def transaction(group_name: str):
    groups_stub = DefaultGroupHandler.get_instance().get_group(group_name)

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
