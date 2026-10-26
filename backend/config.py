"""Application configuration loaded from environment variables."""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AegisFlow"
    debug: bool = False
    database_url: str = "sqlite:///./aegisflow.db"
    # Shared secret required in the X-API-Key header. Must be set in the environment.
    api_key: str
    cors_origins: List[str] = ["http://localhost:3000"]
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
