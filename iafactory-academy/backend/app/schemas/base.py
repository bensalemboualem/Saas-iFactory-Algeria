"""
Base Pydantic schemas for common patterns.
"""
from typing import Generic, TypeVar, Optional, List, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {}
        }
    )


class TimestampSchema(BaseSchema):
    """Schema with timestamp fields."""
    
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class PaginationParams(BaseModel):
    """Pagination query parameters."""
    
    page: int = Field(1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    @property
    def skip(self) -> int:
        """Calculate number of items to skip."""
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """Get page size as limit."""
        return self.page_size
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "page": 1,
                "page_size": 20
            }
        }
    )


class PaginationMeta(BaseModel):
    """Pagination metadata for responses."""
    
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total_items: int = Field(..., description="Total number of items")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "page": 1,
                "page_size": 20,
                "total_items": 150,
                "total_pages": 8,
                "has_next": True,
                "has_prev": False
            }
        }
    )


T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""
    
    items: List[T] = Field(..., description="List of items")
    meta: PaginationMeta = Field(..., description="Pagination metadata")
    
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseSchema):
    """Simple message response."""
    
    message: str = Field(..., description="Response message")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Operation completed successfully"
            }
        }
    )


class ErrorResponse(BaseSchema):
    """Error response schema."""
    
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Resource not found",
                "error_code": "NOT_FOUND"
            }
        }
    )


class SuccessResponse(BaseSchema):
    """Success response with optional data."""
    
    success: bool = Field(True, description="Success status")
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Optional data")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Operation completed",
                "data": {"id": "123"}
            }
        }
    )


class IDResponse(BaseSchema):
    """Response with just an ID."""
    
    id: UUID = Field(..., description="Resource ID")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    )


class SearchParams(BaseModel):
    """Search query parameters."""
    
    q: Optional[str] = Field(None, min_length=1, max_length=200, description="Search query")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "q": "python programming"
            }
        }
    )


class SortParams(BaseModel):
    """Sort query parameters."""
    
    sort_by: Optional[str] = Field(None, description="Field to sort by")
    sort_order: Optional[str] = Field("asc", pattern="^(asc|desc)$", description="Sort order")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "sort_by": "created_at",
                "sort_order": "desc"
            }
        }
    )


class FilterParams(BaseModel):
    """Base filter parameters."""
    
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    created_after: Optional[datetime] = Field(None, description="Filter by creation date after")
    created_before: Optional[datetime] = Field(None, description="Filter by creation date before")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "is_active": True,
                "created_after": "2024-01-01T00:00:00Z"
            }
        }
    )


class BulkOperationResponse(BaseSchema):
    """Response for bulk operations."""
    
    success_count: int = Field(..., description="Number of successful operations")
    error_count: int = Field(..., description="Number of failed operations")
    errors: Optional[List[Dict[str, Any]]] = Field(None, description="List of errors")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success_count": 8,
                "error_count": 2,
                "errors": [
                    {"id": "123", "error": "Invalid data"}
                ]
            }
        }
    )
