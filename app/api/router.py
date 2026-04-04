from fastapi import APIRouter
from app.api.routers.skins import router as skins_router
from app.api.routers.users import router as users_router
from app.api.routers.wishlist import router as wishlist_router
from app.api.routers.reviews import router as reviews_router
from app.api.routers.health import router as health_check

api_router = APIRouter()
api_router.include_router(skins_router)
api_router.include_router(users_router)
api_router.include_router(wishlist_router)
api_router.include_router(reviews_router)
api_router.include_router(health_check)