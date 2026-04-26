import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from fastapi.responses import RedirectResponse
from slowapi.errors import RateLimitExceeded

from app.api.router import api_router
from app.api.deps import skin_cache_singleton
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.limiter import limiter

app = FastAPI(
    lifespan=lifespan,
    title="Valorant Wishlist API",
    swagger_ui_parameters={"persistAuthorization": True}
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    max_age=300,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_headers=["Accept", "Content-Type", "Authorization"],
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
)

app.include_router(api_router)

@app.get("/")
async def redirect_typer():
    return RedirectResponse(settings.url_api + "/docs")
