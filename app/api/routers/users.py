from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.api.deps import get_user_store, get_wishlist_store, get_current_user
from app.schemas.users import UserCreate, UserOut, UserUpdate, UserList
from app.services.user_store import UserStore
from app.services.wishlist_store import WishlistStore
from app.core.errors import ErrorMessages

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=list[UserList])
async def list_users(
    user_store: UserStore = Depends(get_user_store),
    current_user: dict = Depends(get_current_user),
):
    users = await user_store.list_all()
    return [{"user_id": str(u["uuid"]), "username": u["username"]} for u in users]

@router.get("/me", response_model=UserOut)
async def get_users_me(
    current_user: dict = Depends(get_current_user),
    wishlist_store: WishlistStore = Depends(get_wishlist_store),
):
    internal_id = current_user["id"]
    wishlist_items = await wishlist_store.get(internal_id)

    return {
        **current_user,
        "user_id": str(current_user["uuid"]),
        "wishlist_count": len(wishlist_items),
    }

@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: str,
    user_store: UserStore = Depends(get_user_store),
    wishlist_store: WishlistStore = Depends(get_wishlist_store),
    current_user: dict = Depends(get_current_user),
):
    try:
        user_data = await user_store.get(user_id)
        internal_id = user_data["id"]
        wishlist_items = await wishlist_store.get(internal_id)

        return {
            **user_data,
            "user_id": str(user_data["uuid"]),
            "wishlist_count": len(wishlist_items),
        }
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

@router.patch("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: str,
    body: UserUpdate,
    user_store: UserStore = Depends(get_user_store),
    wishlist_store: WishlistStore = Depends(get_wishlist_store),
    current_user: dict = Depends(get_current_user),
):
    if str(current_user["uuid"]) != user_id:
         raise HTTPException(status_code=403, detail=ErrorMessages.NOT_ENOUGH_PERMISSIONS)

    try:
        updated_user = await user_store.update(user_id, body.model_dump(exclude_none=True))
        internal_id = updated_user["id"]
        wishlist_items = await wishlist_store.get(internal_id)

        return {
            **updated_user,
            "user_id": str(updated_user["uuid"]),
            "wishlist_count": len(wishlist_items),
        }
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
