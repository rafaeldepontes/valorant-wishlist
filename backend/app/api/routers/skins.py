from fastapi import APIRouter, Depends, Request

from app.api.deps import get_skin_cache, get_current_user
from app.services.skin_cache import SkinCache

router = APIRouter(prefix="/skins", tags=["Skins"])

@router.get("")
async def read_skins(
    request: Request,
    skin_cache: SkinCache = Depends(get_skin_cache),
    current_user: dict = Depends(get_current_user),
):
    if skin_cache.len() == 0:
        await skin_cache.load()
    return skin_cache.list
