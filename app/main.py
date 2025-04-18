from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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

# Подключаем роутеры и статический html
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(health.router, tags=["Health"])
app.include_router(aggregate.router, tags=["Aggregator"])


@app.get("/")
async def read_index():
    from fastapi.responses import FileResponse

    return FileResponse("static/index.html")
