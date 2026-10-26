import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "DisasterOps API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-production")

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./disasterops.db"
    )

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8080", "http://localhost:8000", "http://127.0.0.1:8000", "*"]

    # JWT
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
