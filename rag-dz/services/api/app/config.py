"""
Configuration management avec variables d'environnement
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuration centralisée de l'application"""

    # Database - REQUIRED in production
    postgres_url: str = ""  # Must be set via POSTGRES_URL env var
    postgres_user: str = "postgres"
    postgres_password: str = ""  # Must be set via POSTGRES_PASSWORD env var
    postgres_db: str = "iafactory_dz"

    # Redis
    redis_url: str = "redis://iafactory-redis:6379/0"
    redis_password: str = ""

    # Qdrant
    qdrant_host: str = "iafactory-qdrant"
    qdrant_port: int = 6333
    qdrant_api_key: str = ""

    # Cloud LLM
    llm_provider: str = "openai"  # openai, anthropic, groq
    llm_model: str = "gpt-3.5-turbo"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    enable_llm: bool = True

    # Security - REQUIRED in production
    api_secret_key: str = ""  # Must be set via API_SECRET_KEY env var
    allowed_origins: str = "http://localhost:3000,http://localhost:5173,http://localhost:8180"
    hash_algorithm: str = "sha256"

    # Rate Limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    rate_limit_burst: int = 10
    enable_rate_limiting: bool = True

    # Embeddings
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    embedding_device: str = "cpu"
    embedding_batch_size: int = 32

    # Service
    service_name: str = "rag-dz-api"
    service_version: str = "1.0.0"
    log_level: str = "INFO"
    environment: str = "development"

    # Features
    enable_cors: bool = True
    enable_metrics: bool = True
    enable_api_key_auth: bool = True
    metrics_port: int = 9090

    # Nouvelles variables Archon
    supabase_url: str = ""
    supabase_service_key: str = ""
    use_reranking: bool = True
    reranking_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    reranking_top_k: int = 10
    use_pgvector: bool = True
    meili_url: str = "http://meilisearch:7700"
    meili_master_key: str = ""  # Must be set via MEILI_MASTER_KEY env var

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"  # Permet les champs supplémentaires

    def validate_production_config(self) -> None:
        """Validate required settings in production"""
        if self.environment == "production":
            required = {
                "POSTGRES_PASSWORD": self.postgres_password,
                "POSTGRES_URL": self.postgres_url,
                "API_SECRET_KEY": self.api_secret_key,
            }
            missing = [k for k, v in required.items() if not v]
            if missing:
                raise ValueError(f"Missing required env vars for production: {', '.join(missing)}")

    def get_allowed_origins(self) -> List[str]:
        """Parse allowed origins from comma-separated string"""
        if self.environment == "development":
            return ["*"]
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
