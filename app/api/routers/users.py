from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.api.deps import get_user_store, get_wishlist_store
from app.schemas.users import UserCreate, UserOut, UserUpdate
from app.services.user_store import UserStore
from app.services.wishlist_store import WishlistStore

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: Request,
    body: UserCreate,
    user_store: UserStore = Depends(get_user_store),
):
    try:
        return user_store.create(body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    request: Request,
    user_id: str,
    user_store: UserStore = Depends(get_user_store),
    wishlist_store: WishlistStore = Depends(get_wishlist_store),
):
    try:
        user = user_store.get(user_id)
        wishlist_items = await wishlist_store.get(user_id)

        return {
            **user,
            "wishlist_count": len(wishlist_items),
        }
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.patch("/{user_id}", response_model=UserOut)
async def update_user(
    request: Request,
    user_id: str,
    body: UserUpdate,
    user_store: UserStore = Depends(get_user_store),
    wishlist_store: WishlistStore = Depends(get_wishlist_store),
):
    try:
        updated_user = user_store.update(user_id, body.model_dump(exclude_none=True))
        wishlist_items = await wishlist_store.get(user_id)

        return {
            **updated_user,
            "wishlist_count": len(wishlist_items),
        }
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e