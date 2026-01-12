"""
Module and Lesson models for course content structure.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class LessonType(str, enum.Enum):
    """Lesson content type."""
    VIDEO = "video"
    TEXT = "text"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    LIVE = "live"


class Module(Base):
    """Course module (chapter) model."""
    
    __tablename__ = "modules"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Course reference
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    
    # Basic info
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Ordering
    order_index = Column(Integer, nullable=False, default=0)
    
    # Metadata
    duration_minutes = Column(Integer, default=0, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan", order_by="Lesson.order_index")
    
    def __repr__(self):
        return f"<Module {self.title}>"


class Lesson(Base):
    """Course lesson model."""
    
    __tablename__ = "lessons"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Module reference
    module_id = Column(UUID(as_uuid=True), ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    
    # Basic info
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)  # Text content or markdown
    
    # Content type
    type = Column(SQLEnum(LessonType), default=LessonType.VIDEO, nullable=False)
    
    # Media
    video_url = Column(String(500), nullable=True)
    video_duration = Column(Integer, nullable=True)  # seconds
    transcript = Column(Text, nullable=True)
    
    # Resources
    resources = Column(JSON, nullable=True)  # [{name, url, type}]
    
    # Ordering
    order_index = Column(Integer, nullable=False, default=0)
    
    # Metadata
    duration_minutes = Column(Integer, default=0, nullable=False)
    is_preview = Column(Boolean, default=False, nullable=False)  # Free preview
    is_published = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    module = relationship("Module", back_populates="lessons")
    progress = relationship("Progress", back_populates="lesson", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Lesson {self.title} ({self.type})>"
