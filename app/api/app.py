from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.model.Activation import ActivationRequest, StringBrokerage
from app.common.Response import Response
from app.data.DefaultGroupHandler import DefaultGroupHandler
from app.db.RedisDB import RedisDB
from app.service.grpc.stub.ITradingStub import ITradingStub
from app.service.grpc.model.types import ActivationTask, ActivationResponse, Brokerage, DeactivationTask, \
    DeactivationResponse, TransactionTask, TransactionMethod, TransactionResponse

router = APIRouter()


def cast_string_brokerage(brokerage: StringBrokerage) -> Brokerage:
    return {
        StringBrokerage.BBAE: Brokerage.BBAE,
        StringBrokerage.Chase: Brokerage.Chase,
        StringBrokerage.DSPAC: Brokerage.DSPAC,
        StringBrokerage.Fennel: Brokerage.Fennel,
        StringBrokerage.Fidelity: Brokerage.Fidelity,
        StringBrokerage.Firstrade: Brokerage.Firstrade,
        StringBrokerage.Public: Brokerage.Public,
        StringBrokerage.Robinhood: Brokerage.Robinhood,
        StringBrokerage.Schwab: Brokerage.Schwab,
        StringBrokerage.SoFi: Brokerage.SoFi,
        StringBrokerage.Tornado: Brokerage.Tornado,
        StringBrokerage.Tradier: Brokerage.Tradier,
        StringBrokerage.Tastytrade: Brokerage.Tastytrade,
        StringBrokerage.Webull: Brokerage.Webull,
        StringBrokerage.Vanguard: Brokerage.Vanguard,
        StringBrokerage.WellsFargo: Brokerage.WellsFargo
    }[brokerage]


@router.post("/createGroup")
def create_group(group_name: str):
    res = DefaultGroupHandler.get_instance().create_group(group_name)

    if not res:
        return JSONResponse(
            status_code=400,
            content="Group already exists"
        )

    return "Group created"


@router.post(path="/activate")
def activate_user(activate_request: ActivationRequest):
    # TODO: Replace with use cases
    group_stub: ITradingStub = DefaultGroupHandler.get_instance().get_group(activate_request.group_name)

    if not group_stub:
        return JSONResponse(
            status_code=400,
            content="Group dose not exists"
        )
    try:
        broker = cast_string_brokerage(activate_request.brokerage)
        response: Response[ActivationResponse] = group_stub.activation(
            task=ActivationTask(
                brokerage=broker,
                creds=activate_request.cred
            )
        )

    except Exception as err:
        # TODO: Replace with error handling
        print(f"Invalid stub: {err}")
        return JSONResponse(
            status_code=500,
            content=f"Stub error: {err}"
        )

    if not response.success:
        return JSONResponse(
            status_code=500,
            content=response.error
        )

    RedisDB.get_instance().add_account(
        group_name=activate_request.group_name,
        account_name=activate_request.account_name,
        brokerage=broker,
        account_details=activate_request.cred
    )
    return {"accountId": response.value.account_id}


# TODO: Add endpoint models
@router.post("/deactivate")
def deactivate_task(group_name: str, account_id: str):
    groups_stub = DefaultGroupHandler.get_instance().get_group(group_name)

    deactivation_task = DeactivationTask(
        account_id=UUID(account_id)
    )

    response: Response[DeactivationResponse] = groups_stub.deactivation(deactivation_task)
    return {
        "status": response.success,
        "message": response.error
    }


# TODO: Add endpoint models
@router.post("/transaction")
def transaction(group_name: str):
    groups_stub = DefaultGroupHandler.get_instance().get_group(group_name)

    transaction_task = TransactionTask(
        method=TransactionMethod.Buy,
        amount=1,
        ticker="AAPL"
    )

    transaction_task_response: Response[TransactionResponse] = groups_stub.transaction(transaction_task)

    return {
        "status": transaction_task_response.success,
        "message": transaction_task_response.value.stdout
    }
