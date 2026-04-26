import uuid
from typing import Any, List
from sqlmodel import select, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.review import Review
from app.utils.time import now_iso
from app.core.errors import ErrorMessages


class ReviewStore:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, body: dict[str, Any]) -> dict[str, Any]:
        record = Review(
            user_id=user_id,
            **body
        )
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record.model_dump()

    async def get_by_id(self, review_uuid: str) -> dict[str, Any]:
        statement = select(Review).where(Review.uuid == uuid.UUID(review_uuid))
        results = await self.session.exec(statement)
        record = results.first()
        if not record:
            raise KeyError(ErrorMessages.REVIEW_NOT_FOUND)
        return record.model_dump()

    async def get_by_skin(self, item_id: str, requester_id: int) -> List[dict[str, Any]]:
        statement = select(Review).where(
            Review.item_id == item_id,
            or_(Review.is_anonymous == False, Review.user_id == requester_id)
        )
        results = await self.session.exec(statement)
        return [r.model_dump() for r in results.all()]

    async def get_by_user(self, user_id: int, requester_id: int) -> List[dict[str, Any]]:
        statement = select(Review).where(Review.user_id == user_id)
        if user_id != requester_id:
            statement = statement.where(Review.is_anonymous == False)

        results = await self.session.exec(statement)
        return [r.model_dump() for r in results.all()]

    async def update(self, review_uuid: str, requester_id: int, patch: dict[str, Any]) -> dict[str, Any]:
        statement = select(Review).where(Review.uuid == uuid.UUID(review_uuid))
        results = await self.session.exec(statement)
        record = results.first()
        if not record:
            raise KeyError(ErrorMessages.REVIEW_NOT_FOUND)

        if record.user_id != requester_id:
            raise PermissionError(ErrorMessages.NOT_ENOUGH_PERMISSIONS)

        if record.is_anonymous:
            raise PermissionError(ErrorMessages.NOT_ENOUGH_PERMISSIONS)

        for key, value in patch.items():
            setattr(record, key, value)

        record.updated_at = now_iso()
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record.model_dump()

    async def delete(self, review_uuid: str, requester_id: int) -> None:
        statement = select(Review).where(Review.uuid == uuid.UUID(review_uuid))
        results = await self.session.exec(statement)
        record = results.first()
        if not record:
            raise KeyError(ErrorMessages.REVIEW_NOT_FOUND)

        if record.user_id != requester_id:
            raise PermissionError(ErrorMessages.NOT_ENOUGH_PERMISSIONS)

        if record.is_anonymous:
            raise PermissionError(ErrorMessages.NOT_ENOUGH_PERMISSIONS)

        await self.session.delete(record)
        await self.session.commit()

    async def list_all(self) -> List[dict[str, Any]]:
        statement = select(Review).where(Review.is_anonymous == False)
        results = await self.session.exec(statement)
        return [r.model_dump() for r in results.all()]
