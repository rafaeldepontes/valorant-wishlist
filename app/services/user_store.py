import uuid
from typing import Any
from app.utils.time import now_iso


class UserStore:
    def __init__(self):
        self.data: dict[str, dict[str, Any]] = {}

    def create(self, body: dict[str, Any]) -> dict[str, Any]:
        if self.get_by_username(body["username"]):
            raise ValueError("invalid username and/or password")
        if self.get_by_email(body["email"]):
            raise ValueError("invalid email and/or password")

        user_id = str(uuid.uuid4())

        now = now_iso()
        record = {
            **body,
            "user_id": user_id,
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

    def get_by_username(self, username: str) -> dict[str, Any] | None:
        for user in self.data.values():
            if user["username"] == username:
                return user
        return None

    def get_by_email(self, email: str) -> dict[str, Any] | None:
        for user in self.data.values():
            if user["email"] == email:
                return user
        return None
