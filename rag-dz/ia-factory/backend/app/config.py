"""
IA Factory - Configuration
Environment and application settings
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment"""
    
    # App
    app_name: str = Field(default="IA Factory")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    environment: str = Field(default="development")
    
    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    workers: int = Field(default=4)
    
    # MongoDB
    mongodb_url: str = Field(default="mongodb://localhost:27017")
    db_name: str = Field(default="iafactory")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379")
    
    # Anthropic Claude
    anthropic_api_key: str = Field(default="")
    claude_model: str = Field(default="claude-3-5-sonnet-20241022")
    
    # VEO 3 (Video Generation)
    veo3_api_key: str = Field(default="")
    veo3_base_url: str = Field(default="https://api.veo.co/v1")
    
    # Replicate (Alternative Video)
    replicate_api_token: str = Field(default="")
    
    # Whisper (Speech-to-Text)
    whisper_model: str = Field(default="base")
    
    # Storage
    upload_dir: str = Field(default="/opt/ia-factory/uploads")
    output_dir: str = Field(default="/opt/ia-factory/outputs")
    max_file_size_mb: int = Field(default=500)
    
    # Platform APIs
    instagram_token: Optional[str] = Field(None)
    instagram_account_id: Optional[str] = Field(None)
    tiktok_client_key: Optional[str] = Field(None)
    tiktok_client_secret: Optional[str] = Field(None)
    youtube_api_key: Optional[str] = Field(None)
    linkedin_client_id: Optional[str] = Field(None)
    linkedin_client_secret: Optional[str] = Field(None)
    
    # Security
    secret_key: str = Field(default="change-me-in-production")
    jwt_algorithm: str = Field(default="HS256")
    jwt_expiry_hours: int = Field(default=24)
    
    # CORS
    cors_origins: List[str] = Field(default=["*"])
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=100)
    rate_limit_period: int = Field(default=60)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()
