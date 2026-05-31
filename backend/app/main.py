import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1 import router as v1_router
from app.core.config import settings
from app.models.base import engine, Base
from app.utils.redis import redis_client
from app.utils.queue import rabbitmq_client

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await redis_client.ping()
    await rabbitmq_client.connect()
    logger.info("Application started")
    yield
    # Shutdown
    await engine.dispose()
    await redis_client.close()
    await rabbitmq_client.close()
    logger.info("Application stopped")

app = FastAPI(
    title="AI Ops Dashboard API",
    version="1.0.0",
    lifespan=lifespan,
)

Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok"}