import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Disaster Resilience Platform"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./disaster_resilience.db")

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "change-me-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # CORS
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:8080"]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
