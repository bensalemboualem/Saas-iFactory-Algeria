from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List
import os


class Settings(BaseSettings):
    # App
    APP_NAME: str = "IA Factory Video Studio"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "https://video.iafactory.dz"]
    
    # Auth
    JWT_SECRET: str = "change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/iafactory_video"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # AI APIs
    FAL_KEY: str = ""
    REPLICATE_API_TOKEN: str = ""
    ELEVENLABS_API_KEY: str = ""
    
    # Storage (S3/R2)
    S3_BUCKET: str = "iafactory-videos"
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_ENDPOINT: str = ""
    S3_REGION: str = "auto"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
