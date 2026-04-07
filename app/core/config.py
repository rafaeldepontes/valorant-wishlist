import os

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    wishlist_path: Path = Path(os.environ.get("WISHLIST_PATH", "./wishlist.json"))
    skins_cache_ttl: int = 3600
    cors_origins: list[str] = ["*"]
    rate_limit: str = "20/minute"
    url_api: str = os.environ.get("API_URL", "http://localhost:8000")

settings = Settings()
