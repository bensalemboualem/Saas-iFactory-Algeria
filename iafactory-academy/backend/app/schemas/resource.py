"""
Resource and Bookmark schemas.
"""
from typing import Optional
from pydantic import Field, ConfigDict
from uuid import UUID

from app.schemas.base import BaseSchema, TimestampSchema, FilterParams
from app.models.resource import ResourceType


class ResourceCreate(BaseSchema):
    """Schema for creating a new resource."""
    
    title: str = Field(..., min_length=3, max_length=255, description="Resource title")
    description: Optional[str] = Field(None, description="Resource description")
    type: ResourceType = Field(ResourceType.DOCUMENT, description="Resource type")
    file_url: Optional[str] = Field(None, max_length=500, description="File URL")
    file_size: Optional[int] = Field(None, ge=0, description="File size in bytes")
    external_url: Optional[str] = Field(None, max_length=500, description="External URL")
    thumbnail_url: Optional[str] = Field(None, max_length=500, description="Thumbnail URL")
    is_public: bool = Field(False, description="Whether resource is public")
    tags: Optional[str] = Field(None, max_length=500, description="Comma-separated tags")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Python Cheat Sheet",
                "description": "Quick reference for Python syntax",
                "type": "document",
                "file_url": "https://example.com/python-cheat-sheet.pdf",
                "file_size": 524288,
                "thumbnail_url": "https://example.com/thumbnails/cheatsheet.jpg",
                "is_public": True,
                "tags": "python,reference,beginner"
            }
        }
    )


class ResourceUpdate(BaseSchema):
    """Schema for updating a resource."""
    
    title: Optional[str] = Field(None, min_length=3, max_length=255, description="Resource title")
    description: Optional[str] = Field(None, description="Resource description")
    type: Optional[ResourceType] = Field(None, description="Resource type")
    file_url: Optional[str] = Field(None, max_length=500, description="File URL")
    file_size: Optional[int] = Field(None, ge=0, description="File size in bytes")
    external_url: Optional[str] = Field(None, max_length=500, description="External URL")
    thumbnail_url: Optional[str] = Field(None, max_length=500, description="Thumbnail URL")
    is_public: Optional[bool] = Field(None, description="Whether resource is public")
    tags: Optional[str] = Field(None, max_length=500, description="Comma-separated tags")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Python Cheat Sheet 2024",
                "is_public": True
            }
        }
    )


class ResourceResponse(TimestampSchema):
    """Schema for resource response."""
    
    id: UUID = Field(..., description="Resource ID")
    title: str = Field(..., description="Resource title")
    description: Optional[str] = Field(None, description="Resource description")
    type: ResourceType = Field(..., description="Resource type")
    file_url: Optional[str] = Field(None, description="File URL")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    external_url: Optional[str] = Field(None, description="External URL")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail URL")
    downloads_count: int = Field(..., description="Number of downloads")
    is_public: bool = Field(..., description="Whether resource is public")
    tags: Optional[str] = Field(None, description="Comma-separated tags")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Python Cheat Sheet",
                "description": "Quick reference for Python syntax",
                "type": "document",
                "file_url": "https://example.com/python-cheat-sheet.pdf",
                "file_size": 524288,
                "external_url": None,
                "thumbnail_url": "https://example.com/thumbnails/cheatsheet.jpg",
                "downloads_count": 1250,
                "is_public": True,
                "tags": "python,reference,beginner",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-12-10T00:00:00Z"
            }
        }
    )


class ResourceListItem(BaseSchema):
    """Minimal resource info for lists."""
    
    id: UUID = Field(..., description="Resource ID")
    title: str = Field(..., description="Resource title")
    type: ResourceType = Field(..., description="Resource type")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail URL")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    downloads_count: int = Field(..., description="Number of downloads")
    is_public: bool = Field(..., description="Whether resource is public")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Python Cheat Sheet",
                "type": "document",
                "thumbnail_url": "https://example.com/thumbnails/cheatsheet.jpg",
                "file_size": 524288,
                "downloads_count": 1250,
                "is_public": True
            }
        }
    )


class ResourceFilterParams(FilterParams):
    """Filter parameters for resources."""
    
    type: Optional[ResourceType] = Field(None, description="Filter by resource type")
    is_public: Optional[bool] = Field(None, description="Filter by public status")
    tags: Optional[str] = Field(None, description="Filter by tags (comma-separated)")
    search: Optional[str] = Field(None, min_length=1, max_length=200, description="Search query")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "document",
                "is_public": True,
                "tags": "python,beginner",
                "search": "cheat sheet"
            }
        }
    )


class BookmarkCreate(BaseSchema):
    """Schema for creating a bookmark."""
    
    resource_id: UUID = Field(..., description="Resource ID to bookmark")
    notes: Optional[str] = Field(None, max_length=1000, description="Personal notes")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "resource_id": "550e8400-e29b-41d4-a716-446655440000",
                "notes": "Great reference for Python syntax"
            }
        }
    )


class BookmarkUpdate(BaseSchema):
    """Schema for updating a bookmark."""
    
    notes: Optional[str] = Field(None, max_length=1000, description="Personal notes")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "notes": "Updated notes about this resource"
            }
        }
    )


class BookmarkResponse(TimestampSchema):
    """Schema for bookmark response."""
    
    id: UUID = Field(..., description="Bookmark ID")
    user_id: UUID = Field(..., description="User ID")
    resource_id: UUID = Field(..., description="Resource ID")
    notes: Optional[str] = Field(None, description="Personal notes")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "660e8400-e29b-41d4-a716-446655440001",
                "resource_id": "770e8400-e29b-41d4-a716-446655440002",
                "notes": "Great reference for Python syntax",
                "created_at": "2024-06-15T00:00:00Z",
                "updated_at": "2024-06-15T00:00:00Z"
            }
        }
    )


class BookmarkWithResource(BookmarkResponse):
    """Bookmark response with resource details."""
    
    resource: ResourceListItem = Field(..., description="Resource details")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "660e8400-e29b-41d4-a716-446655440001",
                "resource_id": "770e8400-e29b-41d4-a716-446655440002",
                "notes": "Great reference for Python syntax",
                "resource": {
                    "id": "770e8400-e29b-41d4-a716-446655440002",
                    "title": "Python Cheat Sheet",
                    "type": "document",
                    "thumbnail_url": "https://example.com/thumbnails/cheatsheet.jpg",
                    "file_size": 524288,
                    "downloads_count": 1250,
                    "is_public": True
                },
                "created_at": "2024-06-15T00:00:00Z"
            }
        }
    )


class BookmarkFilterParams(FilterParams):
    """Filter parameters for bookmarks."""
    
    resource_type: Optional[ResourceType] = Field(None, description="Filter by resource type")
    resource_id: Optional[UUID] = Field(None, description="Filter by specific resource")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "resource_type": "document"
            }
        }
    )


class ResourceStats(BaseSchema):
    """Resource statistics."""
    
    total_resources: int = Field(..., description="Total number of resources")
    public_resources: int = Field(..., description="Number of public resources")
    private_resources: int = Field(..., description="Number of private resources")
    total_downloads: int = Field(..., description="Total downloads across all resources")
    most_downloaded: Optional[ResourceListItem] = Field(None, description="Most downloaded resource")
    resources_by_type: dict = Field(..., description="Count of resources by type")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_resources": 350,
                "public_resources": 280,
                "private_resources": 70,
                "total_downloads": 45000,
                "most_downloaded": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "title": "Python Cheat Sheet",
                    "type": "document",
                    "downloads_count": 5200
                },
                "resources_by_type": {
                    "document": 180,
                    "video": 80,
                    "ebook": 45,
                    "code": 30,
                    "tool": 15
                }
            }
        }
    )
