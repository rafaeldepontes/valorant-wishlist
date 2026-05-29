from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from app.core.db import get_async_session
from app.services.user_store import UserStore
from app.services.auth import AuthService

async def get_user_store(session: AsyncSession = Depends(get_async_session)) -> UserStore:
    return UserStore(session)

def get_auth_service() -> AuthService:
    return auth_service_singleton

auth_service_singleton = AuthService()
