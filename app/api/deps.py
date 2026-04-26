import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.services.skin_cache import SkinCache
from app.services.user_store import UserStore
from app.services.wishlist_store import WishlistStore
from app.services.review_store import ReviewStore
from app.services.auth import AuthService
from app.schemas.auth import TokenData

bearer_scheme = HTTPBearer()

def get_skin_cache() -> SkinCache:
    return skin_cache_singleton

def get_wishlist_store() -> WishlistStore:
    return wishlist_store_singleton

def get_user_store() -> UserStore:
    return user_store_singleton

def get_review_store() -> ReviewStore:
    return review_store_singleton

def get_auth_service() -> AuthService:
    return auth_service_singleton

async def get_current_user(
    auth: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthService = Depends(get_auth_service),
    user_store: UserStore = Depends(get_user_store)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = auth.credentials

    try:
        payload = auth_service.decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception

    user = user_store.get_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user

skin_cache_singleton = SkinCache(ttl=settings.skins_cache_ttl)
wishlist_store_singleton = WishlistStore(settings.wishlist_path)
user_store_singleton = UserStore()
review_store_singleton = ReviewStore()
auth_service_singleton = AuthService()
