"""
Application configuration using Pydantic Settings.
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Application
    APP_NAME: str = "IAFactory Academy"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False  # SECURITY: Default to False, must be explicitly enabled
    SECRET_KEY: str
    API_VERSION: str = "v1"
    API_PREFIX: str = "/api/v1"

    @validator("DEBUG", pre=True, always=True)
    def validate_debug_mode(cls, v, values):
        """SECURITY: Fail fast if DEBUG is True in production environment."""
        env = values.get("ENVIRONMENT", "development")
        if env == "production" and v is True:
            raise ValueError(
                "SECURITY ERROR: DEBUG=True is not allowed in production environment. "
                "Set DEBUG=False or change ENVIRONMENT."
            )
        return v
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 0
    DB_ECHO: bool = False
    
    # Redis
    REDIS_URL: str
    REDIS_CACHE_DB: int = 0
    REDIS_SESSION_DB: int = 1
    
    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    CELERY_TASK_ALWAYS_EAGER: bool = False
    
    # JWT Authentication
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Password Hashing
    BCRYPT_ROUNDS: int = 12
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    # Stripe Payment
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISHABLE_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    STRIPE_CURRENCY: str = "chf"
    STRIPE_SUCCESS_URL: str = "http://localhost:3000/payment/success"
    STRIPE_CANCEL_URL: str = "http://localhost:3000/payment/cancel"
    
    # SendGrid Email
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str
    SENDGRID_FROM_NAME: str = "IAFactory Academy"
    SENDGRID_TEMPLATE_WELCOME: Optional[str] = None
    SENDGRID_TEMPLATE_RESET_PASSWORD: Optional[str] = None
    SENDGRID_TEMPLATE_ENROLLMENT: Optional[str] = None
    SENDGRID_TEMPLATE_CERTIFICATE: Optional[str] = None
    
    # AWS S3
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "eu-central-1"
    AWS_S3_BUCKET: str
    AWS_S3_URL: str
    AWS_CLOUDFRONT_URL: Optional[str] = None
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 104857600  # 100MB
    ALLOWED_VIDEO_EXTENSIONS: str = "mp4,mov,avi,mkv"
    ALLOWED_DOCUMENT_EXTENSIONS: str = "pdf,doc,docx,ppt,pptx"
    ALLOWED_IMAGE_EXTENSIONS: str = "jpg,jpeg,png,gif,webp"
    
    @property
    def allowed_video_exts(self) -> List[str]:
        return self.ALLOWED_VIDEO_EXTENSIONS.split(",")
    
    @property
    def allowed_document_exts(self) -> List[str]:
        return self.ALLOWED_DOCUMENT_EXTENSIONS.split(",")
    
    @property
    def allowed_image_exts(self) -> List[str]:
        return self.ALLOWED_IMAGE_EXTENSIONS.split(",")
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 100
    
    # Sentry Monitoring
    SENTRY_DSN: Optional[str] = None
    SENTRY_TRACES_SAMPLE_RATE: float = 0.1
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_MAX_BYTES: int = 10485760  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # Admin User
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    ADMIN_FIRST_NAME: str = "Admin"
    ADMIN_LAST_NAME: str = "User"
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Cache TTL (seconds)
    CACHE_USER_TTL: int = 300
    CACHE_COURSE_TTL: int = 3600
    CACHE_LESSON_TTL: int = 1800
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
