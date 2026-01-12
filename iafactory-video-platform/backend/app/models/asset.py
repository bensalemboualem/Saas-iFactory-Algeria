"""
Modèle Asset - Images, vidéos, sons générés ou uploadés
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
import enum


class AssetType(str, enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    VOICE = "voice"
    MUSIC = "music"
    AVATAR = "avatar"
    SUBTITLE = "subtitle"


class Asset(Base):
    """Asset média généré ou uploadé"""
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)

    # Type et source
    type = Column(Enum(AssetType), nullable=False)
    source = Column(String(50), nullable=False)  # dalle, runway, elevenlabs, upload, etc.

    # Fichier
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_url = Column(String(500), nullable=True)  # URL publique si hébergé
    mime_type = Column(String(100), nullable=True)
    file_size = Column(Integer, nullable=True)  # en bytes

    # Métadonnées spécifiques au type
    duration = Column(Integer, nullable=True)  # en millisecondes pour audio/video
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)

    # Prompt utilisé pour la génération
    generation_prompt = Column(Text, nullable=True)
    generation_params = Column(JSON, default=dict)  # paramètres utilisés

    # Pour les voix/avatars
    voice_id = Column(String(100), nullable=True)
    avatar_id = Column(String(100), nullable=True)

    # Référence à la scène
    scene_id = Column(String(50), nullable=True)

    # Qualité et statut
    quality_score = Column(Integer, nullable=True)  # 0-100
    is_selected = Column(Integer, default=0)  # 0=non, 1=oui (pour les alternatives)

    # Coûts
    generation_cost = Column(Integer, default=0)  # en centimes

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Asset {self.type.value}: {self.filename}>"
