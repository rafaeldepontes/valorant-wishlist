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

# =========================
# imports adicionais
# =========================
from pydantic import BaseModel
from datetime import datetime


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
This has a rate limit of 20 request per
minute and this should be or default value
through the application.
'''
@app.get("/skins")
@limiter.limit("20/minute")
async def read_root(request: Request):
    if skin_cache.len() == 0:
        await skin_cache.load()
    return skin_cache.list


# =========================
# modelos
# =========================

class UserCreate(BaseModel):
    user_id: str
    username: str
    email: str
    created_at: str
    wishlist_count: int


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    wishlist_count: int | None = None
    updated_at: str | None = None
    status: str | None = None


class WishlistCreate(BaseModel):
    user_id: str
    item_id: str
    weapon: str
    skin_name: str
    rarity: str
    image: str


class WishlistUpdate(BaseModel):
    user_id: str
    item_id: str
    skin_name: str
    rarity: str
    updated_at: str
    notes: str


# =========================
# usuário na memória
# =========================
users = {}


# =========================
# users
# =========================

@app.post("/users")
@limiter.limit("20/minute")
async def create_user(request: Request, body: UserCreate):
    if body.user_id in users:
        return {"error": "user already exists"}

    users[body.user_id] = body.dict()
    return {"message": "user created", "user": body}


@app.patch("/users/{user_id}")
@limiter.limit("20/minute")
async def update_user(request: Request, user_id: str, body: UserUpdate):
    if user_id not in users:
        return {"error": "user not found"}

    user = users[user_id]

    for key, value in body.dict(exclude_none=True).items():
        user[key] = value

    return {"message": "user updated", "user": user}


# =========================
# wishlist
# =========================

@app.post("/wishlist")
@limiter.limit("20/minute")
async def add_wishlist(request: Request, body: WishlistCreate):
    if not await skin_cache.exists(body.item_id):
        return {"error": "skin not found"}

    await store.add(body.user_id, body.item_id)

    return {
        "message": "added to wishlist",
        "item": body
    }


@app.get("/wishlist/{user_id}")
@limiter.limit("20/minute")
async def get_wishlist(request: Request, user_id: str):
    skin_ids = await store.get(user_id)

    result = []

    for skin_id in skin_ids:
        skin = await skin_cache.get(skin_id)
        if skin:
            result.append(skin)

    return {
        "user_id": user_id,
        "wishlist": result
    }


@app.delete("/wishlist")
@limiter.limit("20/minute")
async def remove_wishlist(request: Request, user_id: str, item_id: str):
    try:
        await store.remove(user_id, item_id)
        return {"message": "removed from wishlist"}
    except KeyError as e:
        return {"error": str(e)}


@app.patch("/wishlist")
@limiter.limit("20/minute")
async def update_wishlist(request: Request, body: WishlistUpdate):
    # ⚠️ apenas simulação (wishlist.py não salva esses campos ainda)

    exists = await skin_cache.exists(body.item_id)

    if not exists:
        return {"error": "skin not found"}

    return {
        "message": "wishlist item updated (mock)",
        "data": body
    }
