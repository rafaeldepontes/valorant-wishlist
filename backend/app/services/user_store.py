import uuid
from typing import Any
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.user import User
from app.services.id_cache import id_cache
from app.utils.time import now_iso
from uuid import UUID
from app.core.errors import ErrorMessages


class UserStore:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, body: dict[str, Any]) -> dict[str, Any]:
        if await self.get_by_username(body.get("username")):
            raise ValueError(ErrorMessages.USER_ALREADY_EXISTS)
        if await self.get_by_email(body.get("email")):
            raise ValueError(ErrorMessages.USER_ALREADY_EXISTS)

        user = User(**body)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        id_cache.set(str(user.uuid), user.id)

        return user.model_dump()

    async def update(self, user_uuid: str, patch: dict[str, Any]) -> dict[str, Any]:
        user = await self._get_model_by_uuid(user_uuid)
        if not user:
            raise KeyError(ErrorMessages.USER_NOT_FOUND)

        for key, value in patch.items():
            setattr(user, key, value)

        user.updated_at = now_iso()
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user.model_dump()

    async def get(self, user_uuid: str) -> dict[str, Any]:
        user = await self._get_model_by_uuid(user_uuid)
        if not user:
            raise KeyError(ErrorMessages.USER_NOT_FOUND)
        return user.model_dump()

    async def get_by_username(self, username: str) -> dict[str, Any] | None:
        statement = select(User).where(User.username == username)
        results = await self.session.exec(statement)
        user = results.first()
        return user.model_dump() if user else None

    async def get_by_email(self, email: str) -> dict[str, Any] | None:
        statement = select(User).where(User.email == email)
        results = await self.session.exec(statement)
        user = results.first()
        return user.model_dump() if user else None

    async def _get_model_by_uuid(self, user_uuid: str) -> User | None:
        internal_id = id_cache.get(user_uuid)
        if internal_id:
            user = await self.session.get(User, internal_id)
            if user:
                return user

        try:
            uuid_obj = UUID(user_uuid)
        except ValueError:
            return None

        statement = select(User).where(User.uuid == uuid_obj)
        results = await self.session.exec(statement)
        user = results.first()

        if user:
            id_cache.set(user_uuid, user.id)

        return user

    async def get_internal_id(self, user_uuid: str) -> int:
        user = await self._get_model_by_uuid(user_uuid)
        if not user:
            raise KeyError(ErrorMessages.USER_NOT_FOUND)
        return user.id

    async def list_all(self) -> list[dict[str, Any]]:
        statement = select(User)
        results = await self.session.exec(statement)
        return [user.model_dump() for user in results.all()]
