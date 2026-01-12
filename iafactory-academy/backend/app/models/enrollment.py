"""
Enrollment and Progress tracking models.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Numeric, Integer, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class EnrollmentStatus(str, enum.Enum):
    """Enrollment status."""
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class ProgressStatus(str, enum.Enum):
    """Lesson progress status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Enrollment(Base):
    """Course enrollment model."""
    
    __tablename__ = "enrollments"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # References
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    
    # Status
    status = Column(SQLEnum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE, nullable=False)
    
    # Progress
    progress_percentage = Column(Numeric(5, 2), default=0, nullable=False)
    completed_lessons = Column(Integer, default=0, nullable=False)
    total_time_spent = Column(Integer, default=0, nullable=False)  # seconds
    
    # Timestamps
    enrolled_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    last_accessed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    payments = relationship("Payment", back_populates="enrollment", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="enrollment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Enrollment User {self.user_id} in Course {self.course_id}>"


class Progress(Base):
    """Lesson progress tracking model."""
    
    __tablename__ = "progress"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # References
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    
    # Status
    status = Column(SQLEnum(ProgressStatus), default=ProgressStatus.NOT_STARTED, nullable=False)
    
    # Time tracking
    time_spent_seconds = Column(Integer, default=0, nullable=False)
    video_progress_seconds = Column(Integer, default=0, nullable=True)
    
    # Timestamps
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    last_accessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress")
    
    def __repr__(self):
        return f"<Progress User {self.user_id} Lesson {self.lesson_id} ({self.status})>"
