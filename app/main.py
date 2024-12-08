from fastapi import FastAPI

import app.api.app as apiRouter
from .bootstarp import bootstrap, BootstrapParams

app = bootstrap(
    BootstrapParams(
        db_host="localhost",
        db_port=6379,
        gprc_host="0.0.0.0",
        gprc_port=50052
    )
)

app.include_router(router=apiRouter.router)