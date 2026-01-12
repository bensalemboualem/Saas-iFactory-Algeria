"""
Core configuration for iafactory AI Tools
"""
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "iafactory AI Tools"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    
    # Server
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8001
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    # Database
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # AI Providers
    OPENAI_API_KEY: str
    OPENAI_ORG_ID: str = ""
    ANTHROPIC_API_KEY: str = ""
    STABILITY_API_KEY: str = ""
    REPLICATE_API_TOKEN: str = ""
    DEEPL_API_KEY: str = ""
    
    # Storage
    S3_ENDPOINT_URL: str = ""
    S3_ACCESS_KEY_ID: str = ""
    S3_SECRET_ACCESS_KEY: str = ""
    S3_BUCKET_NAME: str = "iafactory-ai-outputs"
    S3_REGION: str = "fr-par"
    LOCAL_STORAGE_PATH: str = "/tmp/iafactory-uploads"
    
    # Rate Limiting
    RATE_LIMIT_TRANSLATOR: int = 60
    RATE_LIMIT_SPEECH_TO_TEXT: int = 10
    RATE_LIMIT_TEXT_GENERATOR: int = 30
    RATE_LIMIT_IMAGE_GENERATOR: int = 20
    RATE_LIMIT_BACKGROUND_REMOVER: int = 30
    RATE_LIMIT_IMAGE_UPSCALER: int = 20
    RATE_LIMIT_IMAGE_TRANSFORMER: int = 20
    
    # File Upload
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_AUDIO_FORMATS: str = "mp3,wav,m4a,flac,ogg"
    ALLOWED_IMAGE_FORMATS: str = "jpg,jpeg,png,webp,gif"
    
    # Models
    DEFAULT_TEXT_MODEL: str = "gpt-4o-mini"
    MAX_TOKENS_TEXT: int = 4000
    DEFAULT_TRANSLATION_MODEL: str = "gpt-4o-mini"
    SUPPORTED_LANGUAGES: str = "fr,ar,en,es,de,it"
    WHISPER_MODEL: str = "whisper-1"
    DEFAULT_IMAGE_MODEL: str = "dall-e-3"
    IMAGE_SIZE: str = "1024x1024"
    
    # Cache
    CACHE_TTL_TRANSLATION: int = 3600
    CACHE_TTL_TEXT_GENERATION: int = 1800
    ENABLE_CACHE: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    SENTRY_DSN: str = ""
    
    # Multi-tenancy
    TENANT_RAG_DZ_ID: str = "rag-dz"
    TENANT_HELVETIA_ID: str = "helvetia"
    TENANT_STORAGE_ENABLED: bool = True
    
    # Feature Flags
    ENABLE_TRANSLATOR: bool = True
    ENABLE_SPEECH_TO_TEXT: bool = True
    ENABLE_TEXT_GENERATOR: bool = True
    ENABLE_IMAGE_GENERATOR: bool = True
    ENABLE_BACKGROUND_REMOVER: bool = True
    ENABLE_IMAGE_UPSCALER: bool = True
    ENABLE_IMAGE_TRANSFORMER: bool = True
    
    USE_LOCAL_WHISPER: bool = False
    USE_LOCAL_STABLE_DIFFUSION: bool = False
    USE_LOCAL_REMBG: bool = True
    
    # JWT
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    @property
    def supported_languages_list(self) -> List[str]:
        return [lang.strip() for lang in self.SUPPORTED_LANGUAGES.split(",")]
    
    @property
    def allowed_audio_formats_list(self) -> List[str]:
        return [fmt.strip() for fmt in self.ALLOWED_AUDIO_FORMATS.split(",")]
    
    @property
    def allowed_image_formats_list(self) -> List[str]:
        return [fmt.strip() for fmt in self.ALLOWED_IMAGE_FORMATS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
