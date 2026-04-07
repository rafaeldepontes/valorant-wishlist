from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.deps import skin_cache_singleton, wishlist_store_singleton


@asynccontextmanager
async def lifespan(app: FastAPI):
    await wishlist_store_singleton.load()
    await skin_cache_singleton.load()
    yield
    await wishlist_store_singleton.save()