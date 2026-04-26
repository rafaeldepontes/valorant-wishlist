from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.api.deps import get_skin_cache, get_wishlist_store, get_user_store, get_current_user
from app.schemas.wishlist import WishlistCreate, WishlistOut, WishlistUpdate
from app.services.skin_cache import SkinCache
from app.services.wishlist_store import WishlistStore
from app.services.user_store import UserStore
from app.core.errors import ErrorMessages

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.get("/{user_id}", response_model=list[WishlistOut])
async def get_wishlist(
    request: Request,
    user_id: str,
    skin_cache: SkinCache = Depends(get_skin_cache),
    store: WishlistStore = Depends(get_wishlist_store),
    user_store: UserStore = Depends(get_user_store),
    current_user: dict = Depends(get_current_user),
):
    try:
        internal_user_id = await user_store.get_internal_id(user_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=ErrorMessages.USER_NOT_FOUND)

    items = await store.get(internal_user_id)
    result = []

    for item in items:
        skin = await skin_cache.get(item["item_id"])
        if not skin:
            continue

        result.append({
            "user_id": user_id,
            "item_id": item["item_id"],
            "notes": item.get("notes"),
            "priority": item.get("priority", 1),
            "notify_on_sale": item.get("notify_on_sale", False),
            "status": item["status"],
            "created_at": item["created_at"],
            "updated_at": item["updated_at"],
            "weapon_name": skin["weapon_name"],
            "skin_name": skin["skin_name"],
            "image": skin.get("image"),
        })

    return result


@router.post("", response_model=WishlistOut, status_code=status.HTTP_201_CREATED)
async def add_wishlist(
    request: Request,
    body: WishlistCreate,
    skin_cache: SkinCache = Depends(get_skin_cache),
    store: WishlistStore = Depends(get_wishlist_store),
    user_store: UserStore = Depends(get_user_store),
    current_user: dict = Depends(get_current_user),
):
    if str(current_user["uuid"]) != body.user_id:
        raise HTTPException(status_code=403, detail=ErrorMessages.NOT_ENOUGH_PERMISSIONS)

    skin = await skin_cache.get(body.item_id)
    if not skin:
        raise HTTPException(status_code=404, detail=ErrorMessages.SKIN_NOT_FOUND)

    try:
        internal_user_id = await user_store.get_internal_id(body.user_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=ErrorMessages.USER_NOT_FOUND)

    record = await store.add(
        internal_user_id,
        body.item_id,
        body.notes,
        body.priority,
        body.notify_on_sale,
    )

    return {
        "user_id": body.user_id,
        "item_id": body.item_id,
        "notes": record["notes"],
        "priority": record["priority"],
        "notify_on_sale": record["notify_on_sale"],
        "status": record["status"],
        "created_at": record["created_at"],
        "updated_at": record["updated_at"],
        "weapon_name": skin["weapon_name"],
        "skin_name": skin["skin_name"],
        "image": skin.get("image"),
    }


@router.patch("/{user_id}/{item_id}", response_model=WishlistOut)
async def update_wishlist(
    user_id: str,
    item_id: str,
    body: WishlistUpdate,
    skin_cache: SkinCache = Depends(get_skin_cache),
    store: WishlistStore = Depends(get_wishlist_store),
    user_store: UserStore = Depends(get_user_store),
    current_user: dict = Depends(get_current_user),
):
    if str(current_user["uuid"]) != user_id:
        raise HTTPException(status_code=403, detail=ErrorMessages.NOT_ENOUGH_PERMISSIONS)

    try:
        internal_user_id = await user_store.get_internal_id(user_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=ErrorMessages.USER_NOT_FOUND)

    updates = body.model_dump(exclude_none=True)

    try:
        record = await store.update(internal_user_id, item_id, updates)
    except KeyError:
        raise HTTPException(status_code=404, detail=ErrorMessages.ITEM_NOT_FOUND)

    skin = await skin_cache.get(item_id)

    return {
        "user_id": user_id,
        "item_id": item_id,
        "notes": record.get("notes"),
        "priority": record.get("priority"),
        "notify_on_sale": record.get("notify_on_sale"),
        "status": record.get("status"),
        "created_at": record.get("created_at"),
        "updated_at": record.get("updated_at"),
        "weapon_name": skin["weapon_name"],
        "skin_name": skin["skin_name"],
        "image": skin.get("image"),
    }

@router.delete("/{user_id}/{item_id}", status_code=204)
async def delete_wishlist(
    user_id: str,
    item_id: str,
    store: WishlistStore = Depends(get_wishlist_store),
    user_store: UserStore = Depends(get_user_store),
    current_user: dict = Depends(get_current_user),
):
    if str(current_user["uuid"]) != user_id:
        raise HTTPException(status_code=403, detail=ErrorMessages.NOT_ENOUGH_PERMISSIONS)

    try:
        internal_user_id = await user_store.get_internal_id(user_id)
        await store.remove(internal_user_id, item_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
