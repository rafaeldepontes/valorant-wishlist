import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.config import settings
from app.core.db import get_async_session
from app.services.skin_cache import SkinCache
from app.services.user_store import UserStore
from app.services.wishlist_store import WishlistStore
from app.services.review_store import ReviewStore
from app.services.auth import AuthService
from app.core.errors import ErrorMessages

security = HTTPBearer()

def get_skin_cache() -> SkinCache:
    return skin_cache_singleton

async def get_user_store(session: AsyncSession = Depends(get_async_session)) -> UserStore:
    return UserStore(session)

async def get_wishlist_store(session: AsyncSession = Depends(get_async_session)) -> WishlistStore:
    return WishlistStore(session)

async def get_review_store(session: AsyncSession = Depends(get_async_session)) -> ReviewStore:
    return ReviewStore(session)

def get_auth_service() -> AuthService:
    return auth_service_singleton

async def get_current_user(
    auth: HTTPAuthorizationCredentials = Depends(security),
    user_store: UserStore = Depends(get_user_store),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ErrorMessages.INVALID_TOKEN,
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = auth.credentials
    try:
        payload = auth_service.decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = await user_store.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user

skin_cache_singleton = SkinCache(ttl=settings.skins_cache_ttl)
auth_service_singleton = AuthService()
