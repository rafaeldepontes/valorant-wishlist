from typing import Any, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.wishlist import WishlistItem
from app.utils.time import now_iso
from app.core.errors import ErrorMessages


class WishlistStore:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(
        self,
        user_id: int,
        item_id: str,
        notes: str | None = None,
        priority: int = 1,
        notify_on_sale: bool = False,
    ) -> dict[str, Any]:
        statement = select(WishlistItem).where(
            WishlistItem.user_id == user_id, 
            WishlistItem.item_id == item_id
        )
        results = await self.session.exec(statement)
        item = results.first()
        
        if item:
            return item.model_dump()

        record = WishlistItem(
            user_id=user_id,
            item_id=item_id,
            notes=notes,
            priority=priority,
            notify_on_sale=notify_on_sale,
        )
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record.model_dump()

    async def update(
        self,
        user_id: int,
        item_id: str,
        updates: dict[str, Any],
    ) -> dict[str, Any]:
        statement = select(WishlistItem).where(
            WishlistItem.user_id == user_id, 
            WishlistItem.item_id == item_id
        )
        results = await self.session.exec(statement)
        item = results.first()

        if not item:
            raise KeyError(ErrorMessages.ITEM_NOT_FOUND)

        for key, value in updates.items():
            setattr(item, key, value)

        item.updated_at = now_iso()
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item.model_dump()

    async def get(self, user_id: int) -> List[dict[str, Any]]:
        statement = select(WishlistItem).where(WishlistItem.user_id == user_id)
        results = await self.session.exec(statement)
        return [r.model_dump() for r in results.all()]

    async def remove(self, user_id: int, item_id: str) -> None:
        statement = select(WishlistItem).where(
            WishlistItem.user_id == user_id, 
            WishlistItem.item_id == item_id
        )
        results = await self.session.exec(statement)
        item = results.first()

        if not item:
            raise KeyError(ErrorMessages.ITEM_NOT_FOUND)

        await self.session.delete(item)
        await self.session.commit()
