from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    user_id: str
    item_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: str
    is_anonymous: bool = False


class ReviewUpdate(BaseModel):
    rating: int | None = Field(None, ge=1, le=5)
    comment: str | None = None
    is_anonymous: bool | None = None


class ReviewOut(BaseModel):
    review_id: str
    user_id: str | None
    username: str | None
    item_id: str
    weapon_name: str
    skin_name: str
    rating: int
    comment: str
    is_anonymous: bool
    created_at: str
    updated_at: str
