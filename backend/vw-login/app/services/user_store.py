from typing import Any
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.user import User
from app.services.id_cache import id_cache
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
