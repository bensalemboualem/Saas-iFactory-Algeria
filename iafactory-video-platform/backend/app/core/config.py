"""
Configuration centralisée pour IAFactory Video Platform
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    """Configuration principale de l'application"""

    # === APPLICATION ===
    APP_NAME: str = "IAFactory Video Platform"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me-in-production"

    # === API ===
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://localhost:8001"

    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse ALLOWED_ORIGINS as comma-separated string"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    # === DATABASE ===
    DATABASE_URL: str = "postgresql://iafactory:password@localhost:5432/video_platform"
    REDIS_URL: str = "redis://localhost:6379/0"

    # === STORAGE ===
    STORAGE_PROVIDER: str = "local"  # local, s3, r2, minio
    STORAGE_PATH: str = "./storage"
    S3_BUCKET: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    S3_REGION: Optional[str] = None
    S3_ENDPOINT: Optional[str] = None

    # === LLM PROVIDERS ===
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-turbo-preview"

    # Anthropic
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-opus-20240229"

    # Groq
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # DeepSeek
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_MODEL: str = "deepseek-chat"

    # Google
    GOOGLE_API_KEY: Optional[str] = None
    GOOGLE_MODEL: str = "gemini-pro"

    # Mistral
    MISTRAL_API_KEY: Optional[str] = None
    MISTRAL_MODEL: str = "mistral-large-latest"

    # Default LLM
    DEFAULT_LLM_PROVIDER: str = "groq"

    # === IMAGE GENERATION ===
    # DALL-E
    DALLE_MODEL: str = "dall-e-3"

    # Stability AI
    STABILITY_API_KEY: Optional[str] = None

    # Leonardo AI
    LEONARDO_API_KEY: Optional[str] = None

    # Replicate (Flux, SDXL)
    REPLICATE_API_TOKEN: Optional[str] = None

    # Ideogram
    IDEOGRAM_API_KEY: Optional[str] = None

    # FAL AI
    FAL_KEY: Optional[str] = None

    # Default Image Provider
    DEFAULT_IMAGE_PROVIDER: str = "dalle"

    # === VIDEO GENERATION ===
    # Runway ML
    RUNWAY_API_KEY: Optional[str] = None

    # Pika Labs
    PIKA_API_KEY: Optional[str] = None

    # Luma AI
    LUMA_API_KEY: Optional[str] = None

    # Kling AI
    KLING_ACCESS_KEY: Optional[str] = None
    KLING_SECRET_KEY: Optional[str] = None

    # MiniMax
    MINIMAX_API_KEY: Optional[str] = None

    # Default Video Provider
    DEFAULT_VIDEO_PROVIDER: str = "fal"

    # === AVATAR GENERATION ===
    # HeyGen
    HEYGEN_API_KEY: Optional[str] = None

    # D-ID
    DID_API_KEY: Optional[str] = None

    # Synthesia
    SYNTHESIA_API_KEY: Optional[str] = None

    # Default Avatar Provider
    DEFAULT_AVATAR_PROVIDER: str = "heygen"

    # === AUDIO/VOICE ===
    # ElevenLabs
    ELEVENLABS_API_KEY: Optional[str] = None

    # OpenAI TTS/Whisper (uses OPENAI_API_KEY)

    # Default Audio Provider
    DEFAULT_TTS_PROVIDER: str = "elevenlabs"
    DEFAULT_STT_PROVIDER: str = "whisper"

    # === MUSIC GENERATION ===
    # Suno AI
    SUNO_API_KEY: Optional[str] = None

    # Udio
    UDIO_API_KEY: Optional[str] = None

    # === SOCIAL PLATFORMS ===
    # YouTube
    YOUTUBE_CLIENT_ID: Optional[str] = None
    YOUTUBE_CLIENT_SECRET: Optional[str] = None

    # TikTok
    TIKTOK_CLIENT_KEY: Optional[str] = None
    TIKTOK_CLIENT_SECRET: Optional[str] = None

    # Instagram
    INSTAGRAM_APP_ID: Optional[str] = None
    INSTAGRAM_APP_SECRET: Optional[str] = None

    # LinkedIn
    LINKEDIN_CLIENT_ID: Optional[str] = None
    LINKEDIN_CLIENT_SECRET: Optional[str] = None

    # Twitter/X
    TWITTER_API_KEY: Optional[str] = None
    TWITTER_API_SECRET: Optional[str] = None

    # Facebook
    FACEBOOK_APP_ID: Optional[str] = None
    FACEBOOK_APP_SECRET: Optional[str] = None

    # === PROCESSING ===
    MAX_VIDEO_DURATION_SECONDS: int = 600  # 10 minutes
    MAX_UPLOAD_SIZE_MB: int = 500
    FFMPEG_PATH: str = "ffmpeg"

    # === QUEUE ===
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Retourne les settings en cache"""
    return Settings()


settings = get_settings()
