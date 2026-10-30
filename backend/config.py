"""Application configuration loaded from environment variables."""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "National Resilience Intelligence Backbone"
    app_env: str = "development"
    debug: bool = False
    database_url: str = "sqlite:///./resilience.db"
    # Shared API key for protected endpoints. Must be set via environment.
    api_key: str = ""
    cors_origins: List[str] = ["http://localhost:3000"]
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
