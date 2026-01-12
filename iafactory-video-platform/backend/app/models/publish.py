"""
Modèle PublishJob - Publication sur les plateformes
"""
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, JSON, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
import enum


class Platform(str, enum.Enum):
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM_REELS = "instagram_reels"
    INSTAGRAM_POST = "instagram_post"
    INSTAGRAM_STORY = "instagram_story"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    PINTEREST = "pinterest"
    SNAPCHAT = "snapchat"
    TWITCH = "twitch"


class PublishStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    PENDING = "pending"
    UPLOADING = "uploading"
    PROCESSING = "processing"
    PUBLISHED = "published"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PublishJob(Base):
    """Job de publication sur une plateforme"""
    __tablename__ = "publish_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_id = Column(UUID(as_uuid=True), ForeignKey("videos.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)

    # Plateforme cible
    platform = Column(Enum(Platform), nullable=False)

    # Contenu optimisé par plateforme
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=list)  # hashtags
    thumbnail_url = Column(String(500), nullable=True)

    # Paramètres spécifiques à la plateforme
    platform_settings = Column(JSON, default=dict)
    """
    Exemples:
    YouTube: {"privacy": "public", "category": "22", "playlist_id": "..."}
    TikTok: {"allow_duet": true, "allow_stitch": true}
    Instagram: {"share_to_feed": true, "location": "..."}
    """

    # Planification
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    is_scheduled = Column(Boolean, default=False)

    # Status
    status = Column(Enum(PublishStatus), default=PublishStatus.PENDING)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)

    # Résultat
    platform_post_id = Column(String(255), nullable=True)  # ID sur la plateforme
    platform_url = Column(String(500), nullable=True)  # URL de la publication

    # Analytics (mise à jour périodique)
    analytics = Column(JSON, default=dict)
    """
    {
        "views": 1000,
        "likes": 50,
        "comments": 10,
        "shares": 5,
        "last_updated": "2024-01-01T00:00:00Z"
    }
    """

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<PublishJob {self.platform.value} ({self.status})>"
