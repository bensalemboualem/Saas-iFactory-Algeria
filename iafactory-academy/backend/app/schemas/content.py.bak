"""
Content schemas for modules and lessons.
"""
from typing import Optional, List, Dict, Any
from pydantic import Field, ConfigDict
from uuid import UUID

from app.schemas.base import BaseSchema, TimestampSchema
from app.models.content import LessonType


class ModuleCreate(BaseSchema):
    """Schema for creating a new module."""
    
    title: str = Field(..., min_length=3, max_length=255, description="Module title")
    description: Optional[str] = Field(None, description="Module description")
    order_index: int = Field(..., ge=0, description="Module order index")
    is_published: bool = Field(True, description="Whether module is published")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Introduction to Python",
                "description": "Learn the basics of Python programming",
                "order_index": 0,
                "is_published": True
            }
        }
    )


class ModuleUpdate(BaseSchema):
    """Schema for updating a module."""
    
    title: Optional[str] = Field(None, min_length=3, max_length=255, description="Module title")
    description: Optional[str] = Field(None, description="Module description")
    order_index: Optional[int] = Field(None, ge=0, description="Module order index")
    is_published: Optional[bool] = Field(None, description="Whether module is published")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Introduction to Python - Updated",
                "order_index": 1
            }
        }
    )


class ModuleResponse(TimestampSchema):
    """Schema for module response."""
    
    id: UUID = Field(..., description="Module ID")
    course_id: UUID = Field(..., description="Course ID")
    title: str = Field(..., description="Module title")
    description: Optional[str] = Field(None, description="Module description")
    order_index: int = Field(..., description="Module order index")
    duration_minutes: int = Field(..., description="Total module duration in minutes")
    is_published: bool = Field(..., description="Whether module is published")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "course_id": "660e8400-e29b-41d4-a716-446655440001",
                "title": "Introduction to Python",
                "description": "Learn the basics",
                "order_index": 0,
                "duration_minutes": 180,
                "is_published": True,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-12-10T00:00:00Z"
            }
        }
    )


class LessonCreate(BaseSchema):
    """Schema for creating a new lesson."""
    
    title: str = Field(..., min_length=3, max_length=255, description="Lesson title")
    description: Optional[str] = Field(None, description="Lesson description")
    content: Optional[str] = Field(None, description="Lesson text content")
    type: LessonType = Field(LessonType.VIDEO, description="Lesson content type")
    video_url: Optional[str] = Field(None, max_length=500, description="Video URL")
    video_duration: Optional[int] = Field(None, ge=0, description="Video duration in seconds")
    transcript: Optional[str] = Field(None, description="Video transcript")
    resources: Optional[List[Dict[str, Any]]] = Field(None, description="Lesson resources")
    order_index: int = Field(..., ge=0, description="Lesson order index")
    duration_minutes: int = Field(..., ge=0, description="Estimated duration in minutes")
    is_preview: bool = Field(False, description="Whether lesson is free preview")
    is_published: bool = Field(True, description="Whether lesson is published")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Your First Python Program",
                "description": "Learn how to write your first Python program",
                "content": "# Hello World\nprint('Hello, World!')",
                "type": "video",
                "video_url": "https://example.com/lesson1.mp4",
                "video_duration": 600,
                "order_index": 0,
                "duration_minutes": 10,
                "is_preview": True,
                "is_published": True
            }
        }
    )


class LessonUpdate(BaseSchema):
    """Schema for updating a lesson."""
    
    title: Optional[str] = Field(None, min_length=3, max_length=255, description="Lesson title")
    description: Optional[str] = Field(None, description="Lesson description")
    content: Optional[str] = Field(None, description="Lesson text content")
    type: Optional[LessonType] = Field(None, description="Lesson content type")
    video_url: Optional[str] = Field(None, max_length=500, description="Video URL")
    video_duration: Optional[int] = Field(None, ge=0, description="Video duration in seconds")
    transcript: Optional[str] = Field(None, description="Video transcript")
    resources: Optional[List[Dict[str, Any]]] = Field(None, description="Lesson resources")
    order_index: Optional[int] = Field(None, ge=0, description="Lesson order index")
    duration_minutes: Optional[int] = Field(None, ge=0, description="Estimated duration in minutes")
    is_preview: Optional[bool] = Field(None, description="Whether lesson is free preview")
    is_published: Optional[bool] = Field(None, description="Whether lesson is published")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Your First Python Program - Updated",
                "video_url": "https://example.com/lesson1_v2.mp4"
            }
        }
    )


class LessonResponse(TimestampSchema):
    """Schema for lesson response."""
    
    id: UUID = Field(..., description="Lesson ID")
    module_id: UUID = Field(..., description="Module ID")
    title: str = Field(..., description="Lesson title")
    description: Optional[str] = Field(None, description="Lesson description")
    content: Optional[str] = Field(None, description="Lesson text content")
    type: LessonType = Field(..., description="Lesson content type")
    video_url: Optional[str] = Field(None, description="Video URL")
    video_duration: Optional[int] = Field(None, description="Video duration in seconds")
    transcript: Optional[str] = Field(None, description="Video transcript")
    resources: Optional[List[Dict[str, Any]]] = Field(None, description="Lesson resources")
    order_index: int = Field(..., description="Lesson order index")
    duration_minutes: int = Field(..., description="Estimated duration in minutes")
    is_preview: bool = Field(..., description="Whether lesson is free preview")
    is_published: bool = Field(..., description="Whether lesson is published")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "module_id": "660e8400-e29b-41d4-a716-446655440001",
                "title": "Your First Python Program",
                "description": "Learn how to write your first Python program",
                "content": "# Hello World",
                "type": "video",
                "video_url": "https://example.com/lesson1.mp4",
                "video_duration": 600,
                "transcript": "In this lesson...",
                "resources": [{"name": "Slides", "url": "https://example.com/slides.pdf"}],
                "order_index": 0,
                "duration_minutes": 10,
                "is_preview": True,
                "is_published": True,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-12-10T00:00:00Z"
            }
        }
    )


class LessonListItem(BaseSchema):
    """Minimal lesson info for lists."""
    
    id: UUID = Field(..., description="Lesson ID")
    title: str = Field(..., description="Lesson title")
    type: LessonType = Field(..., description="Lesson content type")
    duration_minutes: int = Field(..., description="Estimated duration in minutes")
    is_preview: bool = Field(..., description="Whether lesson is free preview")
    is_published: bool = Field(..., description="Whether lesson is published")
    order_index: int = Field(..., description="Lesson order index")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Your First Python Program",
                "type": "video",
                "duration_minutes": 10,
                "is_preview": True,
                "is_published": True,
                "order_index": 0
            }
        }
    )


class ModuleWithLessons(ModuleResponse):
    """Module response with lessons."""
    
    lessons: List[LessonListItem] = Field(..., description="List of lessons in module")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "course_id": "660e8400-e29b-41d4-a716-446655440001",
                "title": "Introduction to Python",
                "order_index": 0,
                "duration_minutes": 180,
                "is_published": True,
                "lessons": [
                    {
                        "id": "770e8400-e29b-41d4-a716-446655440002",
                        "title": "Your First Python Program",
                        "type": "video",
                        "duration_minutes": 10,
                        "is_preview": True,
                        "is_published": True,
                        "order_index": 0
                    }
                ]
            }
        }
    )


class LessonComplete(BaseSchema):
    """Schema for marking lesson as complete."""
    
    time_spent_seconds: int = Field(..., ge=0, description="Time spent on lesson in seconds")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "time_spent_seconds": 650
            }
        }
    )


class LessonProgress(BaseSchema):
    """Schema for updating lesson progress."""
    
    video_progress_seconds: int = Field(..., ge=0, description="Video progress in seconds")
    time_spent_seconds: int = Field(..., ge=0, description="Time spent on lesson in seconds")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "video_progress_seconds": 300,
                "time_spent_seconds": 350
            }
        }
    )


class ModuleOrderItem(BaseSchema):
    """Schema for a single module order item."""

    module_id: UUID = Field(..., description="Module ID")
    order: int = Field(..., ge=0, description="New order index")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "module_id": "550e8400-e29b-41d4-a716-446655440000",
                "order": 0
            }
        }
    )


class ModuleReorder(BaseSchema):
    """Schema for reordering modules."""

    module_orders: List[ModuleOrderItem] = Field(..., description="List of module order items")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "module_orders": [
                    {"module_id": "550e8400-e29b-41d4-a716-446655440000", "order": 0},
                    {"module_id": "660e8400-e29b-41d4-a716-446655440001", "order": 1}
                ]
            }
        }
    )


class LessonOrderItem(BaseSchema):
    """Schema for a single lesson order item."""

    lesson_id: UUID = Field(..., description="Lesson ID")
    order: int = Field(..., ge=0, description="New order index")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "lesson_id": "550e8400-e29b-41d4-a716-446655440000",
                "order": 0
            }
        }
    )


class LessonReorder(BaseSchema):
    """Schema for reordering lessons."""

    lesson_orders: List[LessonOrderItem] = Field(..., description="List of lesson order items")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "lesson_orders": [
                    {"lesson_id": "550e8400-e29b-41d4-a716-446655440000", "order": 0},
                    {"lesson_id": "660e8400-e29b-41d4-a716-446655440001", "order": 1}
                ]
            }
        }
    )
