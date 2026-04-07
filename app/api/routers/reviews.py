from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.api.deps import get_review_store, get_skin_cache, get_user_store
from app.schemas.reviews import ReviewCreate, ReviewOut, ReviewUpdate
from app.services.review_store import ReviewStore
from app.services.skin_cache import SkinCache
from app.services.user_store import UserStore

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
    if not review.get("is_anonymous"):
        try:
            user = user_store.get(review["user_id"])
            username = user["username"]
        except KeyError:
            username = "Unknown User"

    return {
        **review,
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
):
    # Verify user exists
    try:
        user_store.get(body.user_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="user not found")

    # Verify skin exists
    if not await skin_cache.exists(body.item_id):
        raise HTTPException(status_code=404, detail="skin not found")

    review = review_store.create(body.model_dump())
    return await _enrich_review(review, skin_cache, user_store)


@router.get("/skin/{item_id}", response_model=List[ReviewOut])
async def get_skin_reviews(
    item_id: str,
    review_store: ReviewStore = Depends(get_review_store),
    skin_cache: SkinCache = Depends(get_skin_cache),
    user_store: UserStore = Depends(get_user_store),
):
    reviews = review_store.get_by_skin(item_id)
    return [await _enrich_review(r, skin_cache, user_store) for r in reviews]


@router.get("/user/{user_id}", response_model=List[ReviewOut])
async def get_user_reviews(
    user_id: str,
    review_store: ReviewStore = Depends(get_review_store),
    skin_cache: SkinCache = Depends(get_skin_cache),
    user_store: UserStore = Depends(get_user_store),
):
    reviews = review_store.get_by_user(user_id)
    return [await _enrich_review(r, skin_cache, user_store) for r in reviews]


@router.patch("/{review_id}", response_model=ReviewOut)
async def update_review(
    review_id: str,
    body: ReviewUpdate,
    review_store: ReviewStore = Depends(get_review_store),
    skin_cache: SkinCache = Depends(get_skin_cache),
    user_store: UserStore = Depends(get_user_store),
):
    try:
        review = review_store.update(review_id, body.model_dump(exclude_none=True))
        return await _enrich_review(review, skin_cache, user_store)
    except KeyError:
        raise HTTPException(status_code=404, detail="review not found")


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: str,
    review_store: ReviewStore = Depends(get_review_store),
):
    try:
        review_store.delete(review_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="review not found")
