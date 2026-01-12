"""
Modèle Script - Script généré par l'IA
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class Script(Base):
    """Script vidéo avec timeline et scènes"""
    __tablename__ = "scripts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)

    # Contenu
    title = Column(String(255), nullable=False)
    synopsis = Column(Text, nullable=True)

    # Structure du script
    scenes = Column(JSON, nullable=False, default=list)
    """
    Format des scènes:
    [
        {
            "scene_id": "scene_001",
            "order": 1,
            "duration": 5.0,
            "type": "intro|content|transition|outro",
            "narration": "Texte de la voix off",
            "visual_prompt": "Description visuelle pour génération",
            "music_mood": "upbeat|calm|dramatic",
            "text_overlay": "Texte affiché à l'écran",
            "speaker": "narrator|avatar_1",
            "camera_movement": "static|pan_left|zoom_in",
            "assets": ["asset_id_1", "asset_id_2"]
        }
    ]
    """

    # Timeline calculée
    total_duration = Column(Integer, default=0)  # en secondes

    # Version actuelle
    version = Column(Integer, default=1)
    is_approved = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Script {self.title} v{self.version}>"


class ScriptVersion(Base):
    """Historique des versions de script"""
    __tablename__ = "script_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    script_id = Column(UUID(as_uuid=True), ForeignKey("scripts.id"), nullable=False)

    version = Column(Integer, nullable=False)
    scenes = Column(JSON, nullable=False)

    # Raison du changement
    change_reason = Column(Text, nullable=True)
    changed_by = Column(String(50), default="user")  # user, ai_correction, ai_optimization

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ScriptVersion {self.script_id} v{self.version}>"
