from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from datetime import datetime
from app.utils.time import now_iso

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, unique=True, index=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password: str
    display_name: str | None = None
    favorite_weapon: str | None = None
    bio: str | None = None
    status: str = Field(default="active")
    created_at: str = Field(default_factory=now_iso)
    updated_at: str = Field(default_factory=now_iso)
