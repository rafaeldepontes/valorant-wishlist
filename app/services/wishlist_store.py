from app.utils.time import now_iso
import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List


class WishlistStore:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.data: Dict[str, List[dict[str, Any]]] = {}
        self.lock = asyncio.Lock()

    async def load(self) -> None:
        if not self.file_path.exists():
            return

        raw = json.loads(self.file_path.read_text(encoding="utf-8"))

        for user, items in raw.items():
            if items and isinstance(items[0], str):
                raw[user] = [
                    {
                        "item_id": item,
                        "notes": None,
                        "priority": 1,
                        "notify_on_sale": False,
                        "status": "active",
                        "created_at": now_iso(),
                        "updated_at": now_iso(),
                    }
                    for item in items
                ]

        self.data = raw

    async def save(self) -> None:
        tmp_path = self.file_path.with_suffix(".tmp")
        tmp_path.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp_path.replace(self.file_path)

    async def add(
        self,
        user: str,
        item_id: str,
        notes: str | None = None,
        priority: int = 1,
        notify_on_sale: bool = False,
    ) -> dict[str, Any]:
        async with self.lock:
            items = self.data.setdefault(user, [])

            for item in items:
                if item["item_id"] == item_id:
                    return item

            now = now_iso()
            record = {
                "item_id": item_id,
                "notes": notes,
                "priority": priority,
                "notify_on_sale": notify_on_sale,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            }
            items.append(record)
            await self.save()
            return record

    async def update(
        self,
        user: str,
        item_id: str,
        updates: dict[str, Any],
    ) -> dict[str, Any]:
        async with self.lock:
            if user not in self.data:
                raise KeyError("user not found")

            for item in self.data[user]:
                if item["item_id"] == item_id:
                    for key, value in updates.items():
                        if value is not None:
                            item[key] = value

                    item["updated_at"] = now_iso()
                    await self.save()
                    return item

            raise KeyError("item not found")

    async def get(self, user: str) -> List[dict[str, Any]]:
        return self.data.get(user, [])

    async def remove(self, user: str, item_id: str) -> None:
        async with self.lock:
            if user not in self.data:
                raise KeyError("user not found")

            before = len(self.data[user])
            self.data[user] = [item for item in self.data[user] if item["item_id"] != item_id]

            if len(self.data[user]) == before:
                raise KeyError("item not found")

            await self.save()