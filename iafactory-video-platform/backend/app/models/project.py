"""
Modèle Project - Projet vidéo principal
"""
from sqlalchemy import Column, String, Text, Enum, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
import enum


class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    SCRIPTING = "scripting"
    GENERATING = "generating"
    EDITING = "editing"
    REVIEW = "review"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Project(Base):
    """Projet vidéo - conteneur principal"""
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Infos de base
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Prompt NLP initial de l'utilisateur
    user_prompt = Column(Text, nullable=False)

    # Configuration du projet
    target_duration = Column(String(50), default="60s")  # 15s, 30s, 60s, 3min, 10min
    aspect_ratio = Column(String(20), default="16:9")  # 16:9, 9:16, 1:1, 4:5
    style = Column(String(100), nullable=True)  # cinematic, corporate, fun, etc.
    language = Column(String(10), default="fr")

    # Plateformes cibles
    target_platforms = Column(JSON, default=list)  # ["youtube", "tiktok", "instagram"]

    # Status
    status = Column(Enum(ProjectStatus), default=ProjectStatus.DRAFT)
    progress = Column(JSON, default=dict)  # {"scripting": 100, "images": 50, ...}

    # Métadonnées
    metadata = Column(JSON, default=dict)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Project {self.title} ({self.status})>"
