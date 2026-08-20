from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Rural Healthcare Diagnostic Hub"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    DATABASE_URL: str
    SECRET_KEY: str
    
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
