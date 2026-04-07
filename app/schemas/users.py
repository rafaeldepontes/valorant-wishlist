from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    user_id: str
    username: str
    email: EmailStr
    display_name: str | None = None
    favorite_weapon: str | None = None
    bio: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    display_name: str | None = None
    favorite_weapon: str | None = None
    bio: str


class UserOut(BaseModel):
    user_id: str
    username: str
    email: EmailStr
    display_name: str | None = None
    favorite_weapon: str | None = None
    wishlist_count: int
    status: str
    created_at: str
    updated_at: str
    bio: str