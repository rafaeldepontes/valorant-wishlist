from app.core.config import settings
from app.services.skin_cache import SkinCache
from app.services.user_store import UserStore
from app.services.wishlist_store import WishlistStore
from app.services.review_store import ReviewStore

def get_skin_cache() -> SkinCache:
    return skin_cache_singleton

def get_wishlist_store() -> WishlistStore:
    return wishlist_store_singleton

def get_user_store() -> UserStore:
    return user_store_singleton

def get_review_store() -> ReviewStore:
    return review_store_singleton

skin_cache_singleton = SkinCache(ttl=settings.skins_cache_ttl)
wishlist_store_singleton = WishlistStore(settings.wishlist_path)
user_store_singleton = UserStore()
review_store_singleton = ReviewStore()