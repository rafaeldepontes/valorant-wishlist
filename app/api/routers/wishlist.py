from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.api.deps import get_skin_cache, get_wishlist_store
from app.schemas.wishlist import WishlistCreate, WishlistOut, WishlistUpdate
from app.services.skin_cache import SkinCache
from app.services.wishlist_store import WishlistStore

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.post("", response_model=WishlistOut, status_code=status.HTTP_201_CREATED)
async def add_wishlist(
    request: Request,
    body: WishlistCreate,
    skin_cache: SkinCache = Depends(get_skin_cache),
    store: WishlistStore = Depends(get_wishlist_store),
):
    skin = await skin_cache.get(body.item_id)
    if not skin:
        raise HTTPException(status_code=404, detail="skin not found")

    record = await store.add(
        body.user_id,
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


@router.get("/{user_id}", response_model=list[WishlistOut])
async def get_wishlist(
    request: Request,
    user_id: str,
    skin_cache: SkinCache = Depends(get_skin_cache),
    store: WishlistStore = Depends(get_wishlist_store),
):
    items = await store.get(user_id)
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


@router.patch("/{user_id}/{item_id}", response_model=WishlistOut)
async def update_wishlist(
    user_id: str,
    item_id: str,
    body: WishlistUpdate,
    skin_cache: SkinCache = Depends(get_skin_cache),
    store: WishlistStore = Depends(get_wishlist_store),
):
    updates = body.model_dump(exclude_none=True)

    try:
        record = await store.update(user_id, item_id, updates)
    except KeyError:
        raise HTTPException(status_code=404, detail="item not found")

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
):
    try:
        await store.remove(user_id, item_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="item not found")