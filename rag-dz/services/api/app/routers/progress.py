"""
Progress tracking API routes compatible with Archon UI
"""
from fastapi import APIRouter
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["progress"])


@router.get("/progress/")
async def get_active_progress():
    """
    Get active progress operations
    Compatible with Archon UI
    """
    # TODO: Implement with real progress tracking
    # For now return empty list
    return []


@router.get("/progress/{operation_id}")
async def get_progress_by_id(operation_id: str):
    """Get progress for specific operation"""
    # TODO: Implement real progress tracking
    return {
        "id": operation_id,
        "status": "completed",
        "progress": 100,
        "message": "Operation completed"
    }
