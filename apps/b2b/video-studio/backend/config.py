"""
IAFactory Video Studio Pro - Configuration Centralisée
"""

from typing import Dict, List, Literal, Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuration principale de l'application."""
    
    # Application
    APP_NAME: str = "IAFactory Video Studio Pro"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = Field(default="dev-secret-key-change-in-production", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = Field(default="sqlite:///./video_studio.db", env="DATABASE_URL")
    DATABASE_POOL_SIZE: int = 20
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # Celery
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/1")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/2")
    
    # Storage (S3/MinIO)
    S3_ENDPOINT: str = Field(default="http://localhost:9000")
    S3_ACCESS_KEY: str = Field(default="minioadmin", env="S3_ACCESS_KEY")
    S3_SECRET_KEY: str = Field(default="minioadmin", env="S3_SECRET_KEY")
    S3_BUCKET_NAME: str = "iafactory-video-studio"
    S3_REGION: str = "us-east-1"
    
    # ============================================
    # SERVICES IA EXTERNES
    # ============================================
    
    # Anthropic (Claude)
    ANTHROPIC_API_KEY: str = Field(default="", env="ANTHROPIC_API_KEY")
    CLAUDE_MODEL_OPUS: str = "claude-opus-4-20250514"
    CLAUDE_MODEL_SONNET: str = "claude-sonnet-4-20250514"
    
    # MiniMax (Hailuo AI) - Génération Vidéo
    MINIMAX_API_KEY: str = Field(default="", env="MINIMAX_API_KEY")
    MINIMAX_API_BASE: str = "https://api.minimaxi.chat/v1"
    MINIMAX_GROUP_ID: str = Field(default="", env="MINIMAX_GROUP_ID")
    
    # Luma Dream Machine - Alternative Vidéo
    LUMA_API_KEY: str = Field(default="", env="LUMA_API_KEY")
    LUMA_API_BASE: str = "https://api.lumalabs.ai/dream-machine/v1"
    
    # Fal.ai - Pipeline IA Rapide
    FAL_API_KEY: str = Field(default="", env="FAL_API_KEY")
    FAL_API_BASE: str = "https://fal.run"
    
    # ElevenLabs - Text-to-Speech
    ELEVENLABS_API_KEY: str = Field(default="", env="ELEVENLABS_API_KEY")
    ELEVENLABS_API_BASE: str = "https://api.elevenlabs.io/v1"
    ELEVENLABS_VOICE_FR_MALE: str = ""
    ELEVENLABS_VOICE_FR_FEMALE: str = ""
    ELEVENLABS_VOICE_AR_MALE: str = ""
    ELEVENLABS_VOICE_DARIJA: str = ""
    
    # Suno AI - Génération Musicale
    SUNO_API_KEY: str = Field(default="", env="SUNO_API_KEY")
    SUNO_API_BASE: str = "https://api.suno.ai/v1"
    
    # Grok (xAI) - Agent Growth Hacker
    GROK_API_KEY: str = Field(default="", env="GROK_API_KEY")
    GROK_API_BASE: str = "https://api.x.ai/v1"
    
    # n8n - Automatisation
    N8N_URL: str = Field(default="http://localhost:5678")
    N8N_API_KEY: str = Field(default="", env="N8N_API_KEY")
    
    # ============================================
    # CONFIGURATION MEDIA
    # ============================================
    
    # FFmpeg
    FFMPEG_PATH: str = "/usr/bin/ffmpeg"
    FFPROBE_PATH: str = "/usr/bin/ffprobe"
    
    # Formats de sortie
    OUTPUT_FORMATS: Dict = {
        "youtube": {"width": 1920, "height": 1080, "fps": 30, "bitrate": "8M"},
        "tiktok": {"width": 1080, "height": 1920, "fps": 30, "bitrate": "6M"},
        "instagram": {"width": 1080, "height": 1920, "fps": 30, "bitrate": "6M"},
        "square": {"width": 1080, "height": 1080, "fps": 30, "bitrate": "5M"},
    }
    
    # Limites
    MAX_VIDEO_DURATION_FREE: int = 60  # secondes
    MAX_VIDEO_DURATION_PRO: int = 600
    MAX_VIDEO_DURATION_ENTERPRISE: int = 3600
    MAX_UPLOAD_SIZE_MB: int = 500
    
    # ============================================
    # SYSTÈME IAF-TOKENS
    # ============================================
    
    TOKEN_COSTS: Dict = {
        "script_claude_opus": 50,      # par 1000 mots
        "script_claude_sonnet": 25,    # par 1000 mots
        "video_minimax_30s": 200,
        "video_luma_30s": 180,
        "video_fal_30s": 150,
        "voice_elevenlabs_1min": 30,
        "voice_local_1min": 5,
        "music_suno_30s": 50,
        "montage_complete": 100,
        "publish_youtube": 10,
        "publish_tiktok": 10,
        "publish_instagram": 10,
    }
    
    # Plans tarifaires
    PLANS: Dict = {
        "free": {
            "monthly_tokens": 100,
            "max_video_duration": 60,
            "platforms": ["youtube"],
            "priority": "low"
        },
        "pro": {
            "monthly_tokens": 1000,
            "max_video_duration": 600,
            "platforms": ["youtube", "tiktok", "instagram"],
            "priority": "medium"
        },
        "enterprise": {
            "monthly_tokens": -1,  # illimité
            "max_video_duration": 3600,
            "platforms": ["youtube", "tiktok", "instagram", "linkedin"],
            "priority": "high",
            "api_access": True
        }
    }
    
    # ============================================
    # LANGUES SUPPORTÉES
    # ============================================
    
    SUPPORTED_LANGUAGES: List[str] = [
        "fr",      # Français
        "ar",      # Arabe standard
        "darija",  # Dialecte algérien
        "en",      # Anglais
        "de",      # Allemand
        "it",      # Italien
    ]
    
    LANGUAGE_CONFIG: Dict = {
        "fr": {"name": "Français", "rtl": False, "font": "Arial"},
        "ar": {"name": "العربية", "rtl": True, "font": "Noto Sans Arabic"},
        "darija": {"name": "الدارجة", "rtl": True, "font": "Noto Sans Arabic"},
        "en": {"name": "English", "rtl": False, "font": "Arial"},
        "de": {"name": "Deutsch", "rtl": False, "font": "Arial"},
        "it": {"name": "Italiano", "rtl": False, "font": "Arial"},
    }
    
    # ============================================
    # CORS & SÉCURITÉ
    # ============================================
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://iafactory.ai",
        "https://studio.iafactory.ai",
    ]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 500
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Retourne l'instance singleton des settings."""
    return Settings()


# Configurations spécifiques par agent
class AgentConfigs:
    """Configurations des agents IA."""
    
    SCRIPTWRITER = {
        "model": "claude-opus-4-20250514",
        "temperature": 0.8,
        "max_tokens": 8000,
        "retry_attempts": 3,
        "timeout": 120,
    }
    
    STORYBOARDER = {
        "model": "claude-sonnet-4-20250514",
        "temperature": 0.6,
        "max_tokens": 4000,
        "image_model": "fal-ai/flux/schnell",
        "video_model": "minimax",
    }
    
    DIRECTOR = {
        "ffmpeg_preset": "medium",
        "video_codec": "libx264",
        "audio_codec": "aac",
        "subtitle_burn": True,
    }
    
    GROWTH_HACKER = {
        "model": "grok-4.1-fast",
        "temperature": 0.4,
        "max_tokens": 2000,
        "ab_variations": 5,
    }
    
    DISTRIBUTOR = {
        "max_retries": 3,
        "retry_delay": 30,
        "parallel_uploads": 3,
    }


# Export
settings = get_settings()
agent_configs = AgentConfigs()
