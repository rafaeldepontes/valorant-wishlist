import os

from pathlib import Path
from dotenv import load_dotenv
from wishlist import WishlistStore
from skins import SkinCache
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler

load_dotenv()

limiter = Limiter(key_func=get_remote_address)
store = WishlistStore(Path(os.environ.get("WISHLIST_PATH", "./wishlist.json")))
skin_cache = SkinCache()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await store.load() # startup
    yield
    await store.save() # shutdown

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter

origins = [
    "*",
]

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # type: ignore
app.add_middleware(
    CORSMiddleware,
    max_age=300,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["Accept", "Content-Type"],
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    )

'''
This has a rate limit of 20 requests per
minute, and this should be the default value
across the application.
'''
@app.get("/skins")
@limiter.limit("20/minute")
async def read_root(request: Request): #
    if skin_cache.len() == 0:
        await skin_cache.load()
    return skin_cache.list

'''
Other endpoints, this should contain the register
user, """"login"""" user, add N to wishlist, remove
from wishlist, update N items and list user wishlist.
'''

# TODO: Impl above description