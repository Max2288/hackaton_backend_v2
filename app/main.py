from fastapi import FastAPI
from loguru import logger

from app.api import api
from app.core.config import Config
from app.version import VERSION

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.on_startup.redis import start_redis

from app.api.minio import consumer, client

logger.add(
    "./logs/sirius.log",
    rotation="50 MB",
    retention=5,
)


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await start_redis()
    logger.info("START APP")
    yield
    await consumer.stop()
    await client.stop()
    logger.info("END APP")


def create_app() -> FastAPI:
    app = FastAPI(
        title=Config.SERVICE_NAME,
        debug=Config.DEBUG,
        description=Config.DESCRIPTION,
        version=VERSION,
        lifespan=lifespan,
    )
    setup_middleware(app)
    PATH_PREFIX = "/stenagrafist" + Config.API_V1_STR
    app.include_router(api.router, prefix=PATH_PREFIX)
    return app


app = create_app()
