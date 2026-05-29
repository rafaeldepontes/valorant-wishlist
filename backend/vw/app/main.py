import os

from fastapi import FastAPI, Request
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

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    # Content-Security-Policy: default-src 'self'; img-src 'self' https://media.valorantapi.com;
    response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' data: https://media.valorantapi.com; style-src 'self' 'unsafe-inline';"
    return response

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
