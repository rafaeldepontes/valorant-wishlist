from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from app.utils.time import now_iso

class Review(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, unique=True, index=True)
    user_id: int = Field(foreign_key="user.id")
    item_id: str = Field(index=True)
    rating: int
    comment: str
    is_anonymous: bool = False
    created_at: str = Field(default_factory=now_iso)
    updated_at: str = Field(default_factory=now_iso)
