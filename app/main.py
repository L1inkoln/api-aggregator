from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import health, aggregate
import logging
from app.utils.client import client, close_client  # noqa: F401
from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_client()


app = FastAPI(title="API Aggregator", version="0.1.0", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(health.router, tags=["Health"])
app.include_router(aggregate.router, prefix="/api", tags=["Aggregator"])
