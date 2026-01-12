"""
Resource library and bookmark models.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class ResourceType(str, enum.Enum):
    """Resource content type."""
    VIDEO = "video"
    DOCUMENT = "document"
    EBOOK = "ebook"
    SLIDES = "slides"
    CODE = "code"
    TOOL = "tool"
    LINK = "link"


class Resource(Base):
    """Resource library model for downloadable content."""
    
    __tablename__ = "resources"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic info
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Type and file
    type = Column(SQLEnum(ResourceType), default=ResourceType.DOCUMENT, nullable=False)
    file_url = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)  # bytes
    
    # External link
    external_url = Column(String(500), nullable=True)
    
    # Metadata
    thumbnail_url = Column(String(500), nullable=True)
    downloads_count = Column(Integer, default=0, nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)
    
    # Tags for search
    tags = Column(String(500), nullable=True)  # Comma-separated
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    bookmarks = relationship("Bookmark", back_populates="resource", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Resource {self.title} ({self.type})>"


class Bookmark(Base):
    """User bookmarks for resources."""
    
    __tablename__ = "bookmarks"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # References
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    resource_id = Column(UUID(as_uuid=True), ForeignKey("resources.id", ondelete="CASCADE"), nullable=False)
    
    # Metadata
    notes = Column(Text, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="bookmarks")
    resource = relationship("Resource", back_populates="bookmarks")
    
    def __repr__(self):
        return f"<Bookmark User {self.user_id} Resource {self.resource_id}>"
