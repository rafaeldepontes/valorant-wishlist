import httpx
import time

class SkinCache:
    def __init__(self):
        self.data = {}
        self.list = []
        self.last_update = 0
        self.ttl = 3600         # 1 hour cache

    async def load(self):
        await self.refresh()

    async def refresh(self):
        print("[INFO] saving payload in cache")
        async with httpx.AsyncClient() as client:
            res = await client.get("https://valorant-api.com/v1/weapons")
            payload = res.json()

        skins_map = {}
        skins_list = []

        for weapon in payload["data"]:
            weapon_name = weapon["displayName"]

            for skin in weapon.get("skins", []):
                skin_id = skin["uuid"]

                obj = {
                    "weapon_name": weapon_name,
                    "skin_id": skin_id,
                    "skin_name": skin["displayName"],
                    "image": skin.get("displayIcon"),
                }

                skins_map[skin_id] = obj
                skins_list.append(obj)

        skins_list = sorted(
            skins_list,
            key=lambda x: (x["weapon_name"], x["skin_name"].lower())
        )

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
        data = self.data
        return len(data)