from contextlib import asynccontextmanager
from dataclasses import dataclass
from logging import Logger

from fastapi import FastAPI

from app.data.DefaultGroupHandler import DefaultGroupHandler, DefaultGroupHandlerParams
from app.db.RedisDB import RedisDB, RedisConnectionParams
from app.service.grpc.GrpcService import GrpcService, GrpcConnectionParams


@dataclass
class BootstrapParams:
    db_host: str
    db_port: int
    gprc_host: str
    gprc_port: int
    logger: Logger


def bootstrap(params: BootstrapParams):
    RedisDB(
        connection_params=RedisConnectionParams(
            host=params.db_host,
            port=params.db_port
        )
    )

    DefaultGroupHandler(
        params=DefaultGroupHandlerParams(
            db=RedisDB.get_instance(),
            logger=params.logger
        )
    )

    DefaultGroupHandler.get_instance().create_group("Roie")

    global grpc_service
    grpc_service = GrpcService(
        params=GrpcConnectionParams(
            host=params.gprc_host,
            port=params.gprc_port,
            stub_handler=DefaultGroupHandler.get_instance(),
            logger=params.logger
        )
    )

    return FastAPI(lifespan=lifespan)


@asynccontextmanager
async def lifespan(_: FastAPI):
    RedisDB.get_instance().init()
    grpc_service.start()
    yield
    # TODO: Add logger!!!
    print("Bye..")
