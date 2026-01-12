"""
Payment and Certificate schemas.
"""
from __future__ import annotations
from typing import Optional, Dict, Any, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal
from pydantic import Field, ConfigDict
from uuid import UUID

from app.schemas.base import BaseSchema, TimestampSchema, FilterParams
from app.models.payment import PaymentStatus, PaymentMethod

if TYPE_CHECKING:
    from app.schemas.course import CourseListItem
    from app.schemas.user import UserPublicResponse


class PaymentCreate(BaseSchema):
    """Schema for creating payment (internal use)."""
    
    enrollment_id: UUID = Field(..., description="Enrollment ID")
    amount: Decimal = Field(..., ge=0, description="Payment amount")
    currency: str = Field("CHF", min_length=3, max_length=3, description="Currency code")
    payment_method: PaymentMethod = Field(PaymentMethod.STRIPE, description="Payment method")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "enrollment_id": "550e8400-e29b-41d4-a716-446655440000",
                "amount": 299.00,
                "currency": "CHF",
                "payment_method": "stripe"
            }
        }
    )


class PaymentResponse(TimestampSchema):
    """Schema for payment response."""
    
    id: UUID = Field(..., description="Payment ID")
    user_id: UUID = Field(..., description="User ID")
    enrollment_id: UUID = Field(..., description="Enrollment ID")
    payment_method: PaymentMethod = Field(..., description="Payment method")
    stripe_payment_id: Optional[str] = Field(None, description="Stripe payment ID")
    stripe_session_id: Optional[str] = Field(None, description="Stripe session ID")
    amount: Decimal = Field(..., description="Payment amount")
    currency: str = Field(..., description="Currency code")
    status: PaymentStatus = Field(..., description="Payment status")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    succeeded_at: Optional[datetime] = Field(None, description="Success timestamp")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "660e8400-e29b-41d4-a716-446655440001",
                "enrollment_id": "770e8400-e29b-41d4-a716-446655440002",
                "payment_method": "stripe",
                "stripe_payment_id": "pi_1234567890",
                "stripe_session_id": "cs_1234567890",
                "amount": 299.00,
                "currency": "CHF",
                "status": "succeeded",
                "metadata": {"course_title": "Python Masterclass"},
                "error_message": None,
                "succeeded_at": "2024-01-15T10:30:00Z",
                "created_at": "2024-01-15T10:25:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }
    )


class PaymentWithCourse(PaymentResponse):
    """Payment response with course details."""

    course: "CourseListItem" = Field(..., description="Course details")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "amount": 299.00,
                "currency": "CHF",
                "status": "succeeded",
                "course": {
                    "id": "770e8400-e29b-41d4-a716-446655440002",
                    "title": "Python Programming Masterclass",
                    "slug": "python-programming-masterclass"
                }
            }
        }
    )


class StripeCheckoutSession(BaseSchema):
    """Stripe checkout session response."""
    
    session_id: str = Field(..., description="Stripe session ID")
    checkout_url: str = Field(..., description="Stripe checkout URL")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "cs_test_1234567890",
                "checkout_url": "https://checkout.stripe.com/pay/cs_test_1234567890"
            }
        }
    )


class PaymentRefund(BaseSchema):
    """Schema for refunding payment."""
    
    reason: Optional[str] = Field(None, max_length=500, description="Refund reason")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "reason": "Customer request"
            }
        }
    )


class PaymentFilterParams(FilterParams):
    """Filter parameters for payments."""
    
    status: Optional[PaymentStatus] = Field(None, description="Filter by payment status")
    payment_method: Optional[PaymentMethod] = Field(None, description="Filter by payment method")
    user_id: Optional[UUID] = Field(None, description="Filter by user")
    min_amount: Optional[Decimal] = Field(None, ge=0, description="Minimum amount")
    max_amount: Optional[Decimal] = Field(None, ge=0, description="Maximum amount")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "succeeded",
                "payment_method": "stripe",
                "min_amount": 100.00,
                "max_amount": 1000.00
            }
        }
    )


class PaymentStats(BaseSchema):
    """Payment statistics."""
    
    total_payments: int = Field(..., description="Total number of payments")
    total_revenue: Decimal = Field(..., description="Total revenue")
    successful_payments: int = Field(..., description="Number of successful payments")
    failed_payments: int = Field(..., description="Number of failed payments")
    refunded_payments: int = Field(..., description="Number of refunded payments")
    average_payment: Decimal = Field(..., description="Average payment amount")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_payments": 1500,
                "total_revenue": 448500.00,
                "successful_payments": 1425,
                "failed_payments": 50,
                "refunded_payments": 25,
                "average_payment": 299.00
            }
        }
    )


class CertificateResponse(TimestampSchema):
    """Schema for certificate response."""
    
    id: UUID = Field(..., description="Certificate ID")
    user_id: UUID = Field(..., description="User ID")
    course_id: UUID = Field(..., description="Course ID")
    enrollment_id: UUID = Field(..., description="Enrollment ID")
    certificate_number: str = Field(..., description="Certificate number")
    pdf_url: Optional[str] = Field(None, description="Certificate PDF URL")
    verification_code: str = Field(..., description="Verification code")
    issued_at: datetime = Field(..., description="Issuance timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "660e8400-e29b-41d4-a716-446655440001",
                "course_id": "770e8400-e29b-41d4-a716-446655440002",
                "enrollment_id": "880e8400-e29b-41d4-a716-446655440003",
                "certificate_number": "CERT-2024-001234",
                "pdf_url": "https://example.com/certificates/cert-001234.pdf",
                "verification_code": "ABCD1234EFGH5678",
                "issued_at": "2024-06-15T00:00:00Z",
                "expires_at": None,
                "created_at": "2024-06-15T00:00:00Z",
                "updated_at": "2024-06-15T00:00:00Z"
            }
        }
    )


class CertificateWithCourse(CertificateResponse):
    """Certificate response with course and user details."""

    course: "CourseListItem" = Field(..., description="Course details")
    user: "UserPublicResponse" = Field(..., description="User details")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "certificate_number": "CERT-2024-001234",
                "issued_at": "2024-06-15T00:00:00Z",
                "course": {
                    "id": "770e8400-e29b-41d4-a716-446655440002",
                    "title": "Python Programming Masterclass",
                    "slug": "python-programming-masterclass"
                },
                "user": {
                    "id": "660e8400-e29b-41d4-a716-446655440001",
                    "first_name": "John",
                    "last_name": "Doe",
                    "role": "student"
                }
            }
        }
    )


class CertificateVerify(BaseSchema):
    """Schema for verifying certificate."""
    
    certificate_number: str = Field(..., description="Certificate number to verify")
    verification_code: str = Field(..., description="Verification code")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "certificate_number": "CERT-2024-001234",
                "verification_code": "ABCD1234EFGH5678"
            }
        }
    )


class CertificateVerifyResponse(BaseSchema):
    """Certificate verification response."""
    
    valid: bool = Field(..., description="Whether certificate is valid")
    certificate: Optional[CertificateWithCourse] = Field(None, description="Certificate details if valid")
    message: str = Field(..., description="Verification message")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "valid": True,
                "certificate": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "certificate_number": "CERT-2024-001234",
                    "issued_at": "2024-06-15T00:00:00Z"
                },
                "message": "Certificate is valid"
            }
        }
    )


class CertificateFilterParams(FilterParams):
    """Filter parameters for certificates."""
    
    user_id: Optional[UUID] = Field(None, description="Filter by user")
    course_id: Optional[UUID] = Field(None, description="Filter by course")
    issued_after: Optional[datetime] = Field(None, description="Issued after date")
    issued_before: Optional[datetime] = Field(None, description="Issued before date")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "660e8400-e29b-41d4-a716-446655440001",
                "issued_after": "2024-01-01T00:00:00Z"
            }
        }
    )


class CheckoutSessionCreate(BaseSchema):
    """Schema for creating a checkout session."""

    course_id: UUID = Field(..., description="Course ID to purchase")
    success_url: Optional[str] = Field(None, description="URL to redirect on success")
    cancel_url: Optional[str] = Field(None, description="URL to redirect on cancel")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "course_id": "550e8400-e29b-41d4-a716-446655440000",
                "success_url": "https://example.com/success",
                "cancel_url": "https://example.com/cancel"
            }
        }
    )


class CheckoutSessionResponse(BaseSchema):
    """Schema for checkout session response."""

    session_id: str = Field(..., description="Stripe checkout session ID")
    checkout_url: str = Field(..., description="URL to redirect user for payment")
    expires_at: Optional[datetime] = Field(None, description="Session expiration time")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "cs_test_a1b2c3d4e5f6g7h8i9j0",
                "checkout_url": "https://checkout.stripe.com/c/pay/cs_test_...",
                "expires_at": "2024-12-29T12:00:00Z"
            }
        }
    )
