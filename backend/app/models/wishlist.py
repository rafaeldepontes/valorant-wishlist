from sqlmodel import SQLModel, Field
from app.utils.time import now_iso

class WishlistItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    item_id: str = Field(index=True)
    notes: str | None = None
    priority: int = 1
    notify_on_sale: bool = False
    status: str = Field(default="active")
    created_at: str = Field(default_factory=now_iso)
    updated_at: str = Field(default_factory=now_iso)
