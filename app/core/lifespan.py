from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.deps import skin_cache_singleton
from app.core.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    await skin_cache_singleton.load()

    yield
