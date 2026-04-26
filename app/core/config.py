import os

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    skins_cache_ttl: int = 3600
    cors_origins: list[str] = ["*"]
    rate_limit: str = "20/minute"
    url_api: str = os.environ.get("API_URL", "http://localhost:8000")
    database_url: str = os.environ.get("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/valorant_wishlist")

    auth_secret_key: str = os.environ.get("AUTH_SECRET_KEY", "keep-it-secret-keep-it-safe")
    auth_algorithm: str = os.environ.get("AUTH_ALGORITHM", "HS256")
    auth_token_expire_minutes: int = 30

settings = Settings()
