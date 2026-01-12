"""
Modèle Video - Vidéo finale montée
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
import enum


class VideoStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    RENDERING = "rendering"
    COMPLETED = "completed"
    FAILED = "failed"


class Video(Base):
    """Vidéo finale montée"""
    __tablename__ = "videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    script_id = Column(UUID(as_uuid=True), ForeignKey("scripts.id"), nullable=False)

    # Fichier
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_url = Column(String(500), nullable=True)

    # Specs vidéo
    duration = Column(Integer, nullable=False)  # en secondes
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    fps = Column(Integer, default=30)
    bitrate = Column(Integer, nullable=True)
    codec = Column(String(50), default="h264")
    file_size = Column(Integer, nullable=True)  # en bytes

    # Format et version
    format = Column(String(20), default="mp4")
    version = Column(Integer, default=1)
    variant = Column(String(50), nullable=True)  # youtube_16x9, tiktok_9x16, etc.

    # Timeline utilisée
    timeline = Column(JSON, default=dict)
    """
    Format timeline:
    {
        "tracks": [
            {"type": "video", "clips": [{"asset_id": "...", "start": 0, "end": 5}]},
            {"type": "audio", "clips": [...]},
            {"type": "music", "clips": [...]},
            {"type": "text", "clips": [...]}
        ],
        "effects": [...],
        "transitions": [...]
    }
    """

    # Status
    status = Column(Enum(VideoStatus), default=VideoStatus.PENDING)
    progress = Column(Integer, default=0)  # 0-100
    error_message = Column(Text, nullable=True)

    # Métadonnées
    metadata = Column(JSON, default=dict)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Video {self.filename} ({self.status})>"
