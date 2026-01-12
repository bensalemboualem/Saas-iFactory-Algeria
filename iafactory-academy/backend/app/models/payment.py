"""
Payment and Certificate models.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Numeric, DateTime, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class PaymentStatus(str, enum.Enum):
    """Payment status."""
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(str, enum.Enum):
    """Payment method."""
    STRIPE = "stripe"
    CCP = "ccp"
    BARIDIMOB = "baridimob"
    BANK_TRANSFER = "bank_transfer"

class Payment(Base):
    """Payment transaction model."""
    
    __tablename__ = "payments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    enrollment_id = Column(UUID(as_uuid=True), ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False)
    payment_method = Column(SQLEnum(PaymentMethod), default=PaymentMethod.STRIPE, nullable=False)
    stripe_payment_id = Column(String(255), unique=True, nullable=True, index=True)
    stripe_session_id = Column(String(255), nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="CHF", nullable=False)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    payment_metadata = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    succeeded_at = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="payments")
    enrollment = relationship("Enrollment", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment {self.amount} {self.currency} ({self.status})>"

class Certificate(Base):
    """Course completion certificate model."""
    
    __tablename__ = "certificates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    enrollment_id = Column(UUID(as_uuid=True), ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False)
    certificate_number = Column(String(50), unique=True, nullable=False, index=True)
    pdf_url = Column(String(500), nullable=True)
    verification_code = Column(String(100), unique=True, nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="certificates")
    course = relationship("Course")
    enrollment = relationship("Enrollment", back_populates="certificates")
    
    def __repr__(self):
        return f"<Certificate {self.certificate_number}>"