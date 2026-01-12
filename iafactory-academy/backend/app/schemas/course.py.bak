"""
Course schemas for course management.
"""
from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal
from pydantic import Field, field_validator, ConfigDict
from uuid import UUID
from slugify import slugify

from app.schemas.base import BaseSchema, TimestampSchema, FilterParams
from app.models.course import CourseLevel, CourseStatus

if TYPE_CHECKING:
    from app.schemas.user import UserPublicResponse


class CourseCreate(BaseSchema):
    """Schema for creating a new course."""
    
    title: str = Field(..., min_length=3, max_length=255, description="Course title")
    description: str = Field(..., min_length=10, description="Course description")
    short_description: Optional[str] = Field(None, max_length=500, description="Short description")
    price: Decimal = Field(..., ge=0, description="Course price")
    currency: str = Field("CHF", min_length=3, max_length=3, description="Currency code")
    level: CourseLevel = Field(CourseLevel.BEGINNER, description="Course difficulty level")
    thumbnail_url: Optional[str] = Field(None, max_length=500, description="Thumbnail image URL")
    trailer_url: Optional[str] = Field(None, max_length=500, description="Trailer video URL")
    
    @field_validator('currency')
    @classmethod
    def currency_to_uppercase(cls, v: str) -> str:
        """Convert currency to uppercase."""
        return v.upper()
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Python Programming Masterclass",
                "description": "Learn Python from beginner to advanced level with hands-on projects",
                "short_description": "Master Python programming with practical examples",
                "price": 299.00,
                "currency": "CHF",
                "level": "beginner",
                "thumbnail_url": "https://example.com/thumbnail.jpg",
                "trailer_url": "https://example.com/trailer.mp4"
            }
        }
    )


class CourseUpdate(BaseSchema):
    """Schema for updating a course."""
    
    title: Optional[str] = Field(None, min_length=3, max_length=255, description="Course title")
    description: Optional[str] = Field(None, min_length=10, description="Course description")
    short_description: Optional[str] = Field(None, max_length=500, description="Short description")
    price: Optional[Decimal] = Field(None, ge=0, description="Course price")
    currency: Optional[str] = Field(None, min_length=3, max_length=3, description="Currency code")
    level: Optional[CourseLevel] = Field(None, description="Course difficulty level")
    thumbnail_url: Optional[str] = Field(None, max_length=500, description="Thumbnail image URL")
    trailer_url: Optional[str] = Field(None, max_length=500, description="Trailer video URL")
    
    @field_validator('currency')
    @classmethod
    def currency_to_uppercase(cls, v: Optional[str]) -> Optional[str]:
        """Convert currency to uppercase."""
        return v.upper() if v else v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Python Programming Masterclass 2024",
                "price": 349.00,
                "level": "intermediate"
            }
        }
    )


class CourseResponse(TimestampSchema):
    """Schema for course response."""
    
    id: UUID = Field(..., description="Course ID")
    instructor_id: UUID = Field(..., description="Instructor ID")
    title: str = Field(..., description="Course title")
    slug: str = Field(..., description="Course slug")
    description: str = Field(..., description="Course description")
    short_description: Optional[str] = Field(None, description="Short description")
    price: Decimal = Field(..., description="Course price")
    currency: str = Field(..., description="Currency code")
    level: CourseLevel = Field(..., description="Course difficulty level")
    status: CourseStatus = Field(..., description="Course status")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail image URL")
    trailer_url: Optional[str] = Field(None, description="Trailer video URL")
    duration_hours: int = Field(..., description="Total course duration in hours")
    total_lessons: int = Field(..., description="Total number of lessons")
    total_students: int = Field(..., description="Total enrolled students")
    average_rating: Decimal = Field(..., description="Average course rating")
    total_reviews: int = Field(..., description="Total number of reviews")
    has_certificate: bool = Field(..., description="Whether course provides certificate")
    has_lifetime_access: bool = Field(..., description="Whether course has lifetime access")
    published_at: Optional[datetime] = Field(None, description="Publication timestamp")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "instructor_id": "660e8400-e29b-41d4-a716-446655440001",
                "title": "Python Programming Masterclass",
                "slug": "python-programming-masterclass",
                "description": "Comprehensive Python course",
                "short_description": "Learn Python from scratch",
                "price": 299.00,
                "currency": "CHF",
                "level": "beginner",
                "status": "published",
                "thumbnail_url": "https://example.com/thumbnail.jpg",
                "trailer_url": "https://example.com/trailer.mp4",
                "duration_hours": 40,
                "total_lessons": 120,
                "total_students": 1500,
                "average_rating": 4.7,
                "total_reviews": 450,
                "has_certificate": True,
                "has_lifetime_access": True,
                "published_at": "2024-01-15T00:00:00Z",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-12-10T00:00:00Z"
            }
        }
    )


class CourseListItem(BaseSchema):
    """Minimal course info for lists."""
    
    id: UUID = Field(..., description="Course ID")
    title: str = Field(..., description="Course title")
    slug: str = Field(..., description="Course slug")
    short_description: Optional[str] = Field(None, description="Short description")
    price: Decimal = Field(..., description="Course price")
    currency: str = Field(..., description="Currency code")
    level: CourseLevel = Field(..., description="Course difficulty level")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail image URL")
    duration_hours: int = Field(..., description="Total course duration in hours")
    total_students: int = Field(..., description="Total enrolled students")
    average_rating: Decimal = Field(..., description="Average course rating")
    total_reviews: int = Field(..., description="Total number of reviews")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Python Programming Masterclass",
                "slug": "python-programming-masterclass",
                "short_description": "Learn Python from scratch",
                "price": 299.00,
                "currency": "CHF",
                "level": "beginner",
                "thumbnail_url": "https://example.com/thumbnail.jpg",
                "duration_hours": 40,
                "total_students": 1500,
                "average_rating": 4.7,
                "total_reviews": 450
            }
        }
    )


class CourseDetailResponse(CourseResponse):
    """Detailed course response with instructor info."""

    instructor: "UserPublicResponse" = Field(..., description="Instructor information")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "instructor_id": "660e8400-e29b-41d4-a716-446655440001",
                "title": "Python Programming Masterclass",
                "slug": "python-programming-masterclass",
                "description": "Comprehensive Python course",
                "price": 299.00,
                "currency": "CHF",
                "level": "beginner",
                "status": "published",
                "instructor": {
                    "id": "660e8400-e29b-41d4-a716-446655440001",
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "role": "instructor"
                }
            }
        }
    )


class CoursePublish(BaseSchema):
    """Schema for publishing a course."""
    
    publish: bool = Field(..., description="Whether to publish or unpublish")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "publish": True
            }
        }
    )


class CourseFilterParams(FilterParams):
    """Filter parameters for courses."""
    
    level: Optional[CourseLevel] = Field(None, description="Filter by course level")
    status: Optional[CourseStatus] = Field(None, description="Filter by course status")
    instructor_id: Optional[UUID] = Field(None, description="Filter by instructor")
    min_price: Optional[Decimal] = Field(None, ge=0, description="Minimum price")
    max_price: Optional[Decimal] = Field(None, ge=0, description="Maximum price")
    has_certificate: Optional[bool] = Field(None, description="Filter by certificate availability")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "level": "beginner",
                "status": "published",
                "min_price": 0,
                "max_price": 500,
                "has_certificate": True
            }
        }
    )


class CourseStats(BaseSchema):
    """Course statistics."""
    
    total_enrollments: int = Field(..., description="Total enrollments")
    active_students: int = Field(..., description="Active students")
    completed_students: int = Field(..., description="Students who completed")
    completion_rate: Decimal = Field(..., description="Completion rate percentage")
    average_rating: Decimal = Field(..., description="Average rating")
    total_reviews: int = Field(..., description="Total reviews")
    total_revenue: Decimal = Field(..., description="Total revenue")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_enrollments": 1500,
                "active_students": 850,
                "completed_students": 650,
                "completion_rate": 43.33,
                "average_rating": 4.7,
                "total_reviews": 450,
                "total_revenue": 448500.00
            }
        }
    )
