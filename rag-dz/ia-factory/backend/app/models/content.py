"""
IA Factory - Content Models
Phase 2: Script & Video Content
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ContentStatus(str, Enum):
    """Content lifecycle status"""
    DRAFT = "draft"
    GENERATING = "generating"
    GENERATED = "generated"
    EDITING = "editing"
    EDITED = "edited"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"
    ARCHIVED = "archived"


class VideoFormat(str, Enum):
    """Video format types"""
    REELS = "9:16"
    LANDSCAPE = "16:9"
    SQUARE = "1:1"


class Platform(str, Enum):
    """Supported platforms"""
    INSTAGRAM_REELS = "instagram_reels"
    TIKTOK = "tiktok"
    YOUTUBE_SHORTS = "youtube_shorts"
    LINKEDIN = "linkedin"
    FACEBOOK_REELS = "facebook_reels"
    TWITTER = "twitter"


class ScriptTiming(BaseModel):
    """Script timing breakdown"""
    hook: str = Field(default="0-2s", description="Hook timing")
    body: str = Field(default="2-12s", description="Body timing")
    cta: str = Field(default="12-15s", description="CTA timing")


class TextOverlay(BaseModel):
    """Text overlay configuration"""
    text: str = Field(..., description="Overlay text")
    time_start: float = Field(..., ge=0, description="Start time in seconds")
    time_end: float = Field(..., ge=0, description="End time in seconds")
    position: str = Field(default="bottom", description="Position: top, center, bottom")
    style: str = Field(default="default", description="Style preset")
    font_size: int = Field(default=60)
    color: str = Field(default="#FFFFFF")


class Script(BaseModel):
    """Generated script for video content"""
    
    id: Optional[str] = Field(None)
    brand_id: str = Field(...)
    pillar_id: Optional[str] = Field(None)
    
    # Content
    topic: str = Field(..., description="Topic/angle for this script")
    hook: str = Field(..., description="Opening hook (first 2 seconds)")
    body: str = Field(..., description="Main message content")
    cta: str = Field(..., description="Call to action")
    full_script: Optional[str] = Field(None, description="Full narration text")
    
    # Timing & Structure
    timing: ScriptTiming = Field(default_factory=ScriptTiming)
    duration: int = Field(default=15, ge=5, le=120, description="Target duration in seconds")
    
    # Suggestions
    suggested_music_mood: str = Field(default="upbeat")
    suggested_visuals: List[str] = Field(default=[])
    text_overlays: List[TextOverlay] = Field(default=[])
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    status: ContentStatus = Field(default=ContentStatus.DRAFT)
    language: str = Field(default="en")
    
    class Config:
        json_schema_extra = {
            "example": {
                "topic": "5 AI Tools Every Entrepreneur Needs",
                "hook": "Stop wasting 10 hours a week on tasks AI can do in minutes!",
                "body": "Here are 5 AI tools that will transform your business...",
                "cta": "Follow for more AI tips that actually work!",
                "timing": {"hook": "0-2s", "body": "2-12s", "cta": "12-15s"},
                "suggested_music_mood": "energetic",
                "suggested_visuals": ["screen recordings", "product shots", "talking head"]
            }
        }


class VideoGeneration(BaseModel):
    """Video generation job configuration"""
    
    id: Optional[str] = Field(None)
    script_id: str = Field(...)
    brand_id: str = Field(...)
    
    # Generation settings
    prompt: str = Field(..., description="Video generation prompt")
    format: VideoFormat = Field(default=VideoFormat.REELS)
    quality: str = Field(default="high")
    style: str = Field(default="modern")
    
    # Status
    status: ContentStatus = Field(default=ContentStatus.GENERATING)
    progress: int = Field(default=0, ge=0, le=100)
    error_message: Optional[str] = Field(None)
    
    # Output
    raw_video_url: Optional[str] = Field(None)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = Field(None)
    generation_time_seconds: Optional[float] = Field(None)


class EditingPlan(BaseModel):
    """AI-generated editing plan"""
    
    cuts: List[Dict[str, Any]] = Field(default=[], description="Cut points")
    transitions: List[Dict[str, Any]] = Field(default=[], description="Transition effects")
    text_overlays: List[Dict[str, Any]] = Field(default=[], description="Text overlay timing")
    color_grade: str = Field(default="vibrant", description="Color grading style")
    audio_mix: Dict[str, Any] = Field(default={}, description="Audio mixing settings")


class Video(BaseModel):
    """Edited video content"""
    
    id: Optional[str] = Field(None)
    script_id: str = Field(...)
    generation_id: Optional[str] = Field(None)
    brand_id: str = Field(...)
    
    # Content info
    title: str = Field(...)
    description: str = Field(default="")
    hashtags: List[str] = Field(default=[])
    
    # Video files
    raw_video_url: Optional[str] = Field(None)
    edited_video_url: Optional[str] = Field(None)
    thumbnail_url: Optional[str] = Field(None)
    
    # Platform versions
    platform_versions: Dict[str, str] = Field(default={}, description="Platform-specific URLs")
    
    # Technical specs
    duration: float = Field(default=0)
    format: VideoFormat = Field(default=VideoFormat.REELS)
    width: int = Field(default=1080)
    height: int = Field(default=1920)
    fps: int = Field(default=30)
    file_size_mb: float = Field(default=0)
    
    # Editing
    editing_plan: Optional[EditingPlan] = Field(None)
    
    # Status
    status: ContentStatus = Field(default=ContentStatus.DRAFT)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    pillar_id: Optional[str] = Field(None)


class ContentPiece(BaseModel):
    """Complete content piece combining script and video"""
    
    id: Optional[str] = Field(None)
    brand_id: str = Field(...)
    
    # References
    script: Script
    video: Optional[Video] = Field(None)
    
    # Content metadata
    pillar_name: str = Field(...)
    topic: str = Field(...)
    
    # Scheduling
    scheduled_time: Optional[datetime] = Field(None)
    target_platforms: List[Platform] = Field(default=[Platform.INSTAGRAM_REELS])
    
    # Status
    status: ContentStatus = Field(default=ContentStatus.DRAFT)
    
    # Performance (filled after publishing)
    performance: Optional[Dict[str, Any]] = Field(None)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    published_at: Optional[datetime] = Field(None)


class ContentBatch(BaseModel):
    """Batch of content pieces (e.g., 30 videos from 1 topic)"""
    
    id: Optional[str] = Field(None)
    brand_id: str = Field(...)
    
    # Configuration
    source_topic: str = Field(..., description="Original topic expanded into batch")
    num_pieces: int = Field(default=30)
    
    # Content
    content_pieces: List[ContentPiece] = Field(default=[])
    
    # Status
    status: ContentStatus = Field(default=ContentStatus.DRAFT)
    scripts_generated: int = Field(default=0)
    videos_generated: int = Field(default=0)
    videos_edited: int = Field(default=0)
    videos_scheduled: int = Field(default=0)
    videos_published: int = Field(default=0)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = Field(None)
