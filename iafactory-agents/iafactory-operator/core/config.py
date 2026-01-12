"""
IA Factory Operator - Core Configuration
Centralized configuration management with environment variables
"""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # === Environment ===
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # === API ===
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8090, env="API_PORT")
    api_workers: int = Field(default=4, env="API_WORKERS")
    
    # === Database ===
    database_url: str = Field(
        default="sqlite:///./iafactory_operator.db",
        env="DATABASE_URL"
    )
    
    # === Redis ===
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # === LLM / Claude ===
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(default="claude-sonnet-4-20250514", env="ANTHROPIC_MODEL")
    
    # === OpenAI (Whisper) ===
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    whisper_model: str = Field(default="whisper-1", env="WHISPER_MODEL")
    
    # === Storage (S3) ===
    s3_endpoint_url: Optional[str] = Field(default=None, env="S3_ENDPOINT_URL")
    s3_bucket: str = Field(default="iafactory-operator", env="S3_BUCKET")
    s3_access_key: str = Field(default="", env="S3_ACCESS_KEY")
    s3_secret_key: str = Field(default="", env="S3_SECRET_KEY")
    s3_region: str = Field(default="eu-central-1", env="S3_REGION")
    
    # === Public URL ===
    public_url_base: str = Field(
        default="https://iafactoryalgeria.com/outputs",
        env="PUBLIC_URL_BASE"
    )
    
    # === Webhook ===
    webhook_secret: str = Field(default="", env="WEBHOOK_SECRET")
    
    # === FFmpeg ===
    ffmpeg_path: str = Field(default="ffmpeg", env="FFMPEG_PATH")
    ffprobe_path: str = Field(default="ffprobe", env="FFPROBE_PATH")
    
    # === Directories ===
    temp_dir: str = Field(default="/tmp/iafactory_operator", env="TEMP_DIR")
    output_dir: str = Field(
        default="/opt/iafactory-rag-dz/outputs/operator",
        env="OUTPUT_DIR"
    )
    
    # === Limits ===
    max_video_duration: int = Field(default=600, env="MAX_VIDEO_DURATION")  # 10 min
    max_file_size: int = Field(default=500 * 1024 * 1024, env="MAX_FILE_SIZE")  # 500MB
    max_concurrent_jobs: int = Field(default=5, env="MAX_CONCURRENT_JOBS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()


# Create directories on import
os.makedirs(settings.temp_dir, exist_ok=True)
os.makedirs(settings.output_dir, exist_ok=True)
