from fastapi import APIRouter, Depends, Request

from app.api.deps import get_skin_cache
from app.services.skin_cache import SkinCache

router = APIRouter(prefix="/skins", tags=["skins"])

@router.get("")
async def read_skins(
    request: Request,
    skin_cache: SkinCache = Depends(get_skin_cache),
):
    if skin_cache.len() == 0:
        await skin_cache.load()
    return skin_cache.list