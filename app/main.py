from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.router import api_router
from app.api.deps import skin_cache_singleton
from app.core.config import settings
from app.core.lifespan import lifespan

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.rate_limit]
)

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    max_age=300,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_headers=["Accept", "Content-Type"],
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
)

app.include_router(api_router)