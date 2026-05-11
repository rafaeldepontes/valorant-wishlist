import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    skins_cache_ttl: int = 3600
    cors_origins: list[str] = [os.environ.get("FRONTEND_URL", "http://localhost:5173")]
    rate_limit: str = "20/minute"
    url_api: str = os.environ.get("API_URL", "http://localhost:8000")
    database_url: str = os.environ.get("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost:5432/valorant_wishlist")

    auth_secret_key: str = os.environ.get("AUTH_SECRET_KEY", "keep-it-secret-keep-it-safe")
    auth_algorithm: str = os.environ.get("AUTH_ALGORITHM", "HS256")
    auth_token_expire_minutes: int = 30
    auth_cookie_name: str = "access_token"
    auth_cookie_secure: bool = os.environ.get("AUTH_COOKIE_SECURE", "False").lower() == "true"
    auth_cookie_samesite: str = "lax"

settings = Settings()
