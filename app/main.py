import app.api.app as api_router
from .bootstarp import bootstrap, BootstrapParams
from .logger import logger_factory


# TODO: Replace with configs
app = bootstrap(
    BootstrapParams(
        db_host="redis",
        db_port=6379,
        gprc_host="0.0.0.0",
        gprc_port=50052,
        logger=logger_factory()
    )
)

app.include_router(router=api_router.router)
