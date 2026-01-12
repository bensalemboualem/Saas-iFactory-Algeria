"""
IA FACTORY - Configuration Centralisée
"""

from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # ═══════════════════════════════════════════════════════════
    # API KEYS
    # ═══════════════════════════════════════════════════════════
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: Optional[str] = None
    
    # ═══════════════════════════════════════════════════════════
    # DATABASE
    # ═══════════════════════════════════════════════════════════
    DATABASE_URL_CH: str = "postgresql://iafactory:password@localhost:5432/iafactory_ch"
    DATABASE_URL_DZ: str = "postgresql://iafactory:password@localhost:5432/iafactory_dz"
    REDIS_URL: str = "redis://localhost:6379"
    QDRANT_URL: str = "http://localhost:6333"
    
    # Contacts
    EMAIL_CH: str = "contact@iafactory.ch"
    EMAIL_DZ: str = "contact@iafactoryalgeria.com"
    WEBSITE_CH: str = "www.iafactory.ch"
    WEBSITE_DZ: str = "www.iafactoryalgeria.com"
    BOUALEM_PHONE: Optional[str] = None
    
    # ═══════════════════════════════════════════════════════════
    # APP
    # ═══════════════════════════════════════════════════════════
    APP_NAME: str = "IA Factory"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
