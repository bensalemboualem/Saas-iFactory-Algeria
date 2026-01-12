"""
User schemas for authentication and profile management.
"""
from typing import Optional
from datetime import datetime
from pydantic import EmailStr, Field, field_validator, ConfigDict
from uuid import UUID

from app.schemas.base import BaseSchema, TimestampSchema
from app.models.user import UserRole


class UserCreate(BaseSchema):
    """Schema for creating a new user."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=100, description="User password")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    role: UserRole = Field(UserRole.STUDENT, description="User role")

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

    @field_validator('email')
    @classmethod
    def email_to_lowercase(cls, v: str) -> str:
        """Convert email to lowercase."""
        return v.lower()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123",
                "first_name": "John",
                "last_name": "Doe",
                "role": "student"
            }
        }
    )


class UserRegister(BaseSchema):
    """Schema for user registration (public)."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=100, description="User password")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

    @field_validator('email')
    @classmethod
    def email_to_lowercase(cls, v: str) -> str:
        """Convert email to lowercase."""
        return v.lower()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "jane.smith@example.com",
                "password": "SecurePass456",
                "first_name": "Jane",
                "last_name": "Smith"
            }
        }
    )


class UserLogin(BaseSchema):
    """Schema for user login."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

    @field_validator('email')
    @classmethod
    def email_to_lowercase(cls, v: str) -> str:
        """Convert email to lowercase."""
        return v.lower()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123"
            }
        }
    )


class UserUpdate(BaseSchema):
    """Schema for updating user profile."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=100, description="First name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Last name")
    bio: Optional[str] = Field(None, max_length=1000, description="User bio")
    avatar_url: Optional[str] = Field(None, max_length=500, description="Avatar URL")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "bio": "Passionate learner and developer",
                "avatar_url": "https://example.com/avatar.jpg"
            }
        }
    )


class UserPasswordChange(BaseSchema):
    """Schema for changing user password."""

    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")

    @field_validator('new_password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "current_password": "OldPass123",
                "new_password": "NewSecurePass456"
            }
        }
    )


class UserPasswordReset(BaseSchema):
    """Schema for requesting password reset."""

    email: EmailStr = Field(..., description="User email address")

    @field_validator('email')
    @classmethod
    def email_to_lowercase(cls, v: str) -> str:
        """Convert email to lowercase."""
        return v.lower()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john.doe@example.com"
            }
        }
    )


class UserPasswordResetConfirm(BaseSchema):
    """Schema for confirming password reset."""

    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")

    @field_validator('new_password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "new_password": "NewSecurePass789"
            }
        }
    )


class UserResponse(TimestampSchema):
    """Schema for user response."""

    id: UUID = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    role: UserRole = Field(..., description="User role")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    bio: Optional[str] = Field(None, description="User bio")
    is_active: bool = Field(..., description="Is user active")
    email_verified: bool = Field(..., description="Is email verified")
    last_login_at: Optional[datetime] = Field(None, description="Last login timestamp")

    @property
    def full_name(self) -> str:
        """Get full name."""
        return f"{self.first_name} {self.last_name}"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "role": "student",
                "avatar_url": "https://example.com/avatar.jpg",
                "bio": "Passionate learner",
                "is_active": True,
                "email_verified": True,
                "last_login_at": "2024-12-10T10:00:00Z",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-12-10T10:00:00Z"
            }
        }
    )


class UserPublicResponse(BaseSchema):
    """Public user profile (limited info)."""

    id: UUID = Field(..., description="User ID")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    bio: Optional[str] = Field(None, description="User bio")
    role: UserRole = Field(..., description="User role")

    @property
    def full_name(self) -> str:
        """Get full name."""
        return f"{self.first_name} {self.last_name}"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "first_name": "John",
                "last_name": "Doe",
                "avatar_url": "https://example.com/avatar.jpg",
                "bio": "Experienced instructor",
                "role": "instructor"
            }
        }
    )


class UserListResponse(BaseSchema):
    """Minimal user info for lists."""

    id: UUID = Field(..., description="User ID")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    email: EmailStr = Field(..., description="User email address")
    role: UserRole = Field(..., description="User role")
    is_active: bool = Field(..., description="Is user active")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "role": "student",
                "is_active": True
            }
        }
    )


class TokenResponse(BaseSchema):
    """JWT token response."""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 900
            }
        }
    )


class TokenRefresh(BaseSchema):
    """Schema for refreshing access token."""

    refresh_token: str = Field(..., description="JWT refresh token")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
    )


class EmailVerification(BaseSchema):
    """Schema for email verification."""
    
    token: str = Field(..., description="Email verification token")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
    )


class PasswordResetRequest(BaseSchema):
    """Schema for password reset request."""
    
    email: EmailStr = Field(..., description="User email address")
    
    @field_validator('email')
    @classmethod
    def email_to_lowercase(cls, v: str) -> str:
        """Convert email to lowercase."""
        return v.lower()
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john.doe@example.com"
            }
        }
    )


class PasswordReset(BaseSchema):
    """Schema for password reset."""
    
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")
    
    @field_validator('new_password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "new_password": "NewSecurePass123"
            }
        }
    )


class UserStats(BaseSchema):
    """User statistics."""

    total_enrollments: int = Field(..., description="Total course enrollments")
    completed_courses: int = Field(..., description="Completed courses")
    in_progress_courses: int = Field(..., description="Courses in progress")
    total_certificates: int = Field(..., description="Total certificates earned")
    total_time_spent: int = Field(..., description="Total time spent learning (seconds)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_enrollments": 12,
                "completed_courses": 5,
                "in_progress_courses": 7,
                "total_certificates": 5,
                "total_time_spent": 86400
            }
        }
    )