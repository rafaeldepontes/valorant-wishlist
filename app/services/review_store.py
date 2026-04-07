import uuid
from typing import Any, Dict, List
from app.utils.time import now_iso


class ReviewStore:
    def __init__(self):
        self.data: Dict[str, dict[str, Any]] = {}

    def create(self, body: dict[str, Any]) -> dict[str, Any]:
        review_id = str(uuid.uuid4())
        now = now_iso()
        
        record = {
            "review_id": review_id,
            **body,
            "created_at": now,
            "updated_at": now,
        }
        self.data[review_id] = record
        return record

    def get_by_id(self, review_id: str) -> dict[str, Any]:
        if review_id not in self.data:
            raise KeyError("review not found")
        return self.data[review_id]

    def get_by_skin(self, item_id: str) -> List[dict[str, Any]]:
        return [r for r in self.data.values() if r["item_id"] == item_id]

    def get_by_user(self, user_id: str) -> List[dict[str, Any]]:
        return [r for r in self.data.values() if r["user_id"] == user_id]

    def update(self, review_id: str, patch: dict[str, Any]) -> dict[str, Any]:
        if review_id not in self.data:
            raise KeyError("review not found")

        self.data[review_id].update(patch)
        self.data[review_id]["updated_at"] = now_iso()
        return self.data[review_id]

    def delete(self, review_id: str) -> None:
        if review_id not in self.data:
            raise KeyError("review not found")
        del self.data[review_id]

    def list_all(self) -> List[dict[str, Any]]:
        return list(self.data.values())
