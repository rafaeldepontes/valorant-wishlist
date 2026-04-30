from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=1)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    display_name: str | None = None
    favorite_weapon: str | None = None
    bio: str | None = None


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
    bio: str | None = None

class UserList(BaseModel):
    user_id: str
    username: str
