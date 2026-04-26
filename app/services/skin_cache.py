import os
import time
from typing import Any

import httpx


class SkinCache:
    def __init__(self, ttl: int = 3600):
        self.data: dict[str, dict[str, Any]] = {}
        self.list: list[dict[str, Any]] = []
        self.last_update: float = 0.0
        self.ttl = ttl

    async def load(self) -> None:
        await self.refresh()

    async def refresh(self) -> None:
        async with httpx.AsyncClient(timeout=20) as client:
            res = await client.get(os.environ.get("VALORANT_API_URL", "https://valorant-api.com/v1/weapons"))
            res.raise_for_status()
            payload = res.json()

        skins_map: dict[str, dict[str, Any]] = {}
        skins_list: list[dict[str, Any]] = []

        for weapon in payload.get("data", []):
            weapon_name = weapon.get("displayName", "")

            for skin in weapon.get("skins", []):
                skin_id = skin.get("uuid")
                if not skin_id:
                    continue

                obj = {
                    "weapon_name": weapon_name,
                    "skin_id": skin_id,
                    "skin_name": skin.get("displayName", ""),
                    "image": skin.get("displayIcon"),
                }

                skins_map[skin_id] = obj
                skins_list.append(obj)

        skins_list.sort(key=lambda x: (x["weapon_name"], x["skin_name"].lower()))

        self.data = skins_map
        self.list = skins_list
        self.last_update = time.time()

    async def get(self, skin_id: str):
        if time.time() - self.last_update > self.ttl:
            await self.refresh()
        return self.data.get(skin_id)

    async def exists(self, skin_id: str) -> bool:
        return await self.get(skin_id) is not None

    def len(self) -> int:
        return len(self.data)