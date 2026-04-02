from typing import Any
from app.utils.time import now_iso


class UserStore:
    def __init__(self):
        self.data: dict[str, dict[str, Any]] = {}

    def create(self, body: dict[str, Any]) -> dict[str, Any]:
        user_id = body["user_id"]
        if user_id in self.data:
            raise ValueError("user already exists")

        now = now_iso()
        record = {
            **body,
            "wishlist_count": 0,
            "status": "active",
            "created_at": now,
            "updated_at": now,
        }
        self.data[user_id] = record
        return record

    def update(self, user_id: str, patch: dict[str, Any]) -> dict[str, Any]:
        if user_id not in self.data:
            raise KeyError("user not found")

        self.data[user_id].update(patch)
        self.data[user_id]["updated_at"] = now_iso()
        return self.data[user_id]


    def get(self, user_id: str) -> dict[str, Any]:
        if user_id not in self.data:
            raise KeyError("user not found")
        return self.data[user_id]