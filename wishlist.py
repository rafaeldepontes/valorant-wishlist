from pathlib import Path
import asyncio
import json
from typing import Dict, List

from pydantic import BaseModel


class WishlistItem(BaseModel):
    user: str
    skin_id: str


class WishlistStore:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.data: Dict[str, List[str]] = {}
        self.lock = asyncio.Lock()

    async def load(self) -> None:
        if self.file_path.exists():
            self.data = json.loads(self.file_path.read_text(encoding="utf-8"))

    async def save(self) -> None:
        tmp_path = self.file_path.with_suffix(".tmp")
        tmp_path.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp_path.replace(self.file_path)

    async def add(self, user: str, skin_id: str) -> None:
        async with self.lock:
            skins = self.data.setdefault(user, [])
            if skin_id not in skins:
                skins.append(skin_id)
                await self.save()

    async def get(self, user: str) -> List[str]:
        return self.data.get(user, [])

    async def remove(self, user: str, skin_id: str) -> None:
        async with self.lock:
            if user not in self.data:
                raise KeyError("user not found")

            before = len(self.data[user])
            self.data[user] = [s for s in self.data[user] if s != skin_id]

            if len(self.data[user]) == before:
                raise KeyError("skin not found")

            await self.save()
