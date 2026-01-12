"""
Enrollment and Progress schemas.
"""
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal
from pydantic import Field, ConfigDict
from uuid import UUID

from app.schemas.base import BaseSchema, TimestampSchema, FilterParams
from app.models.enrollment import EnrollmentStatus, ProgressStatus

if TYPE_CHECKING:
    from app.schemas.course import CourseListItem
    from app.schemas.content import LessonListItem


class EnrollmentCreate(BaseSchema):
    """Schema for creating enrollment (internal use)."""
    
    course_id: UUID = Field(..., description="Course ID to enroll in")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "course_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    )


class EnrollmentResponse(TimestampSchema):
    """Schema for enrollment response."""
    
    id: UUID = Field(..., description="Enrollment ID")
    user_id: UUID = Field(..., description="User ID")
    course_id: UUID = Field(..., description="Course ID")
    status: EnrollmentStatus = Field(..., description="Enrollment status")
    progress_percentage: Decimal = Field(..., description="Progress percentage")
    completed_lessons: int = Field(..., description="Number of completed lessons")
    total_time_spent: int = Field(..., description="Total time spent in seconds")
    enrolled_at: datetime = Field(..., description="Enrollment timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")
    last_accessed_at: Optional[datetime] = Field(None, description="Last access timestamp")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "660e8400-e29b-41d4-a716-446655440001",
                "course_id": "770e8400-e29b-41d4-a716-446655440002",
                "status": "active",
                "progress_percentage": 45.50,
                "completed_lessons": 55,
                "total_time_spent": 36000,
                "enrolled_at": "2024-01-15T00:00:00Z",
                "completed_at": None,
                "expires_at": None,
                "last_accessed_at": "2024-12-10T10:00:00Z",
                "created_at": "2024-01-15T00:00:00Z",
                "updated_at": "2024-12-10T10:00:00Z"
            }
        }
    )


class EnrollmentWithCourse(EnrollmentResponse):
    """Enrollment response with course details."""

    course: "CourseListItem" = Field(..., description="Course details")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "660e8400-e29b-41d4-a716-446655440001",
                "course_id": "770e8400-e29b-41d4-a716-446655440002",
                "status": "active",
                "progress_percentage": 45.50,
                "completed_lessons": 55,
                "course": {
                    "id": "770e8400-e29b-41d4-a716-446655440002",
                    "title": "Python Programming Masterclass",
                    "slug": "python-programming-masterclass",
                    "price": 299.00,
                    "currency": "CHF",
                    "level": "beginner"
                }
            }
        }
    )


class EnrollmentFilterParams(FilterParams):
    """Filter parameters for enrollments."""
    
    status: Optional[EnrollmentStatus] = Field(None, description="Filter by enrollment status")
    course_id: Optional[UUID] = Field(None, description="Filter by course")
    user_id: Optional[UUID] = Field(None, description="Filter by user")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "active",
                "course_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    )


class ProgressCreate(BaseSchema):
    """Schema for creating progress entry."""
    
    lesson_id: UUID = Field(..., description="Lesson ID")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "lesson_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    )


class ProgressUpdate(BaseSchema):
    """Schema for updating progress."""
    
    status: Optional[ProgressStatus] = Field(None, description="Progress status")
    time_spent_seconds: Optional[int] = Field(None, ge=0, description="Time spent in seconds")
    video_progress_seconds: Optional[int] = Field(None, ge=0, description="Video progress in seconds")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "completed",
                "time_spent_seconds": 650,
                "video_progress_seconds": 600
            }
        }
    )


class ProgressResponse(TimestampSchema):
    """Schema for progress response."""
    
    id: UUID = Field(..., description="Progress ID")
    user_id: UUID = Field(..., description="User ID")
    lesson_id: UUID = Field(..., description="Lesson ID")
    status: ProgressStatus = Field(..., description="Progress status")
    time_spent_seconds: int = Field(..., description="Time spent in seconds")
    video_progress_seconds: Optional[int] = Field(None, description="Video progress in seconds")
    started_at: Optional[datetime] = Field(None, description="Start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    last_accessed_at: datetime = Field(..., description="Last access timestamp")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "660e8400-e29b-41d4-a716-446655440001",
                "lesson_id": "770e8400-e29b-41d4-a716-446655440002",
                "status": "completed",
                "time_spent_seconds": 650,
                "video_progress_seconds": 600,
                "started_at": "2024-12-10T09:00:00Z",
                "completed_at": "2024-12-10T09:11:00Z",
                "last_accessed_at": "2024-12-10T09:11:00Z",
                "created_at": "2024-12-10T09:00:00Z",
                "updated_at": "2024-12-10T09:11:00Z"
            }
        }
    )


class ProgressWithLesson(ProgressResponse):
    """Progress response with lesson details."""

    lesson: "LessonListItem" = Field(..., description="Lesson details")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "660e8400-e29b-41d4-a716-446655440001",
                "lesson_id": "770e8400-e29b-41d4-a716-446655440002",
                "status": "completed",
                "time_spent_seconds": 650,
                "lesson": {
                    "id": "770e8400-e29b-41d4-a716-446655440002",
                    "title": "Your First Python Program",
                    "type": "video",
                    "duration_minutes": 10,
                    "is_preview": False,
                    "is_published": True,
                    "order_index": 0
                }
            }
        }
    )


class CourseProgress(BaseSchema):
    """Course progress overview."""
    
    course_id: UUID = Field(..., description="Course ID")
    total_lessons: int = Field(..., description="Total lessons in course")
    completed_lessons: int = Field(..., description="Completed lessons")
    in_progress_lessons: int = Field(..., description="Lessons in progress")
    not_started_lessons: int = Field(..., description="Lessons not started")
    progress_percentage: Decimal = Field(..., description="Progress percentage")
    total_time_spent: int = Field(..., description="Total time spent in seconds")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "course_id": "550e8400-e29b-41d4-a716-446655440000",
                "total_lessons": 120,
                "completed_lessons": 55,
                "in_progress_lessons": 3,
                "not_started_lessons": 62,
                "progress_percentage": 45.83,
                "total_time_spent": 36000
            }
        }
    )


class LearningStats(BaseSchema):
    """User learning statistics."""
    
    total_courses_enrolled: int = Field(..., description="Total courses enrolled")
    active_courses: int = Field(..., description="Active courses")
    completed_courses: int = Field(..., description="Completed courses")
    total_lessons_completed: int = Field(..., description="Total lessons completed")
    total_time_spent: int = Field(..., description="Total time spent in seconds")
    average_progress: Decimal = Field(..., description="Average progress percentage")
    current_streak_days: int = Field(..., description="Current learning streak in days")
    longest_streak_days: int = Field(..., description="Longest learning streak in days")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_courses_enrolled": 12,
                "active_courses": 7,
                "completed_courses": 5,
                "total_lessons_completed": 450,
                "total_time_spent": 216000,
                "average_progress": 58.33,
                "current_streak_days": 15,
                "longest_streak_days": 45
            }
        }
    )
