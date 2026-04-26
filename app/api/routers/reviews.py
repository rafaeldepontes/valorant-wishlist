from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.api.deps import get_review_store, get_skin_cache, get_user_store, get_current_user
from app.schemas.reviews import ReviewCreate, ReviewOut, ReviewUpdate
from app.services.review_store import ReviewStore
from app.services.skin_cache import SkinCache
from app.services.user_store import UserStore
from app.core.errors import ErrorMessages

router = APIRouter(prefix="/reviews", tags=["Reviews"])


async def _enrich_review(
    review: dict,
    skin_cache: SkinCache,
    user_store: UserStore
) -> dict:
    skin = await skin_cache.get(review["item_id"])
    if not skin:
        weapon_name = "Unknown"
        skin_name = "Unknown"
    else:
        weapon_name = skin["weapon_name"]
        skin_name = skin["skin_name"]

    username = None
    user_uuid = None

    try:
        from sqlmodel import select
        from app.models.user import User
        statement = select(User).where(User.id == review["user_id"])
        results = await user_store.session.exec(statement)
        user = results.first()
        if user:
            user_uuid = str(user.uuid)
            if not review.get("is_anonymous"):
                username = user.username
        else:
            if not review.get("is_anonymous"):
                username = ErrorMessages.UNKNOWN_USER
    except Exception:
        if not review.get("is_anonymous"):
            username = ErrorMessages.UNKNOWN_USER

    res = {**review}
    if "user_id" in res:
        del res["user_id"]

    return {
        **res,
        "review_id": str(review["uuid"]),
        "user_id": user_uuid if not review.get("is_anonymous") else None,
        "weapon_name": weapon_name,
        "skin_name": skin_name,
        "username": username,
    }


@router.post("", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
async def create_review(
    body: ReviewCreate,
    review_store: ReviewStore = Depends(get_review_store),
    skin_cache: SkinCache = Depends(get_skin_cache),
    user_store: UserStore = Depends(get_user_store),
    current_user: dict = Depends(get_current_user),
):
    if str(current_user["uuid"]) != body.user_id:
        raise HTTPException(status_code=403, detail=ErrorMessages.NOT_ENOUGH_PERMISSIONS)

    try:
        user_data = await user_store.get(body.user_id)
        internal_user_id = user_data["id"]
    except KeyError:
        raise HTTPException(status_code=404, detail=ErrorMessages.USER_NOT_FOUND)

    if not await skin_cache.exists(body.item_id):
        raise HTTPException(status_code=404, detail=ErrorMessages.SKIN_NOT_FOUND)

    data = body.model_dump()
    if "user_id" in data:
        del data["user_id"]

    review = await review_store.create(internal_user_id, data)
    return await _enrich_review(review, skin_cache, user_store)


@router.get("/skin/{item_id}", response_model=List[ReviewOut])
async def get_skin_reviews(
    item_id: str,
    review_store: ReviewStore = Depends(get_review_store),
    skin_cache: SkinCache = Depends(get_skin_cache),
    user_store: UserStore = Depends(get_user_store),
    current_user: dict = Depends(get_current_user),
):
    reviews = await review_store.get_by_skin(item_id, current_user["id"])
    return [await _enrich_review(r, skin_cache, user_store) for r in reviews]


@router.get("/user/{user_id}", response_model=List[ReviewOut])
async def get_user_reviews(
    user_id: str,
    review_store: ReviewStore = Depends(get_review_store),
    skin_cache: SkinCache = Depends(get_skin_cache),
    user_store: UserStore = Depends(get_user_store),
    current_user: dict = Depends(get_current_user),
):
    try:
        user_data = await user_store.get(user_id)
        target_internal_id = user_data["id"]
    except KeyError:
        raise HTTPException(status_code=404, detail=ErrorMessages.USER_NOT_FOUND)

    reviews = await review_store.get_by_user(target_internal_id, current_user["id"])
    return [await _enrich_review(r, skin_cache, user_store) for r in reviews]


@router.patch("/{review_id}", response_model=ReviewOut)
async def update_review(
    review_id: str,
    body: ReviewUpdate,
    review_store: ReviewStore = Depends(get_review_store),
    skin_cache: SkinCache = Depends(get_skin_cache),
    user_store: UserStore = Depends(get_user_store),
    current_user: dict = Depends(get_current_user),
):
    try:
        review = await review_store.update(review_id, current_user["id"], body.model_dump(exclude_none=True))
        return await _enrich_review(review, skin_cache, user_store)
    except (KeyError, PermissionError) as e:
        status_code = 404 if isinstance(e, KeyError) else 403
        raise HTTPException(status_code=status_code, detail=str(e))


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: str,
    review_store: ReviewStore = Depends(get_review_store),
    current_user: dict = Depends(get_current_user),
):
    try:
        await review_store.delete(review_id, current_user["id"])
    except (KeyError, PermissionError) as e:
        status_code = 404 if isinstance(e, KeyError) else 403
        raise HTTPException(status_code=status_code, detail=str(e))
