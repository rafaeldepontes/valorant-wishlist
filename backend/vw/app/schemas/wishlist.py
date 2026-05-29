from pydantic import BaseModel


class WishlistCreate(BaseModel):
    user_id: str
    item_id: str
    notes: str | None = None
    priority: int = 1
    notify_on_sale: bool = False


class WishlistUpdate(BaseModel):
    notes: str | None = None
    favorite: bool | None = None
    status: str | None = None
    notify_on_sale: bool | None = None
    priority: int | None = None


class WishlistOut(BaseModel):
    user_id: str
    item_id: str
    notes: str | None = None
    priority: int
    notify_on_sale: bool
    status: str
    created_at: str
    updated_at: str
    weapon_name: str
    skin_name: str
    image: str | None