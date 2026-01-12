"""
IA Factory - Distribution Models
Phase 3: Multi-Platform Publishing & Scheduling
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class Platform(str, Enum):
    """Supported social media platforms"""
    INSTAGRAM_REELS = "instagram_reels"
    TIKTOK = "tiktok"
    YOUTUBE_SHORTS = "youtube_shorts"
    LINKEDIN = "linkedin"
    FACEBOOK_REELS = "facebook_reels"
    TWITTER = "twitter"


class PublishStatus(str, Enum):
    """Publishing status"""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PlatformSpec(BaseModel):
    """Platform technical specifications"""
    
    platform: Platform
    aspect_ratio: str = Field(default="9:16")
    width: int = Field(default=1080)
    height: int = Field(default=1920)
    max_duration: int = Field(default=90, description="Max duration in seconds")
    recommended_fps: int = Field(default=30)
    caption_style: str = Field(default="default")
    max_file_size_mb: int = Field(default=100)
    max_caption_length: int = Field(default=2200)
    max_hashtags: int = Field(default=30)


# Platform specifications
PLATFORM_SPECS = {
    Platform.INSTAGRAM_REELS: PlatformSpec(
        platform=Platform.INSTAGRAM_REELS,
        aspect_ratio="9:16",
        width=1080,
        height=1920,
        max_duration=90,
        recommended_fps=30,
        caption_style="white_bold",
        max_file_size_mb=100,
        max_caption_length=2200,
        max_hashtags=30
    ),
    Platform.TIKTOK: PlatformSpec(
        platform=Platform.TIKTOK,
        aspect_ratio="9:16",
        width=1080,
        height=1920,
        max_duration=180,
        recommended_fps=30,
        caption_style="trending",
        max_file_size_mb=287,
        max_caption_length=2200,
        max_hashtags=5
    ),
    Platform.YOUTUBE_SHORTS: PlatformSpec(
        platform=Platform.YOUTUBE_SHORTS,
        aspect_ratio="9:16",
        width=1080,
        height=1920,
        max_duration=60,
        recommended_fps=60,
        caption_style="bright",
        max_file_size_mb=256,
        max_caption_length=5000,
        max_hashtags=15
    ),
    Platform.LINKEDIN: PlatformSpec(
        platform=Platform.LINKEDIN,
        aspect_ratio="9:16",
        width=1080,
        height=1350,
        max_duration=600,
        recommended_fps=30,
        caption_style="professional",
        max_file_size_mb=75,
        max_caption_length=3000,
        max_hashtags=5
    ),
    Platform.FACEBOOK_REELS: PlatformSpec(
        platform=Platform.FACEBOOK_REELS,
        aspect_ratio="9:16",
        width=1080,
        height=1920,
        max_duration=90,
        recommended_fps=30,
        caption_style="default",
        max_file_size_mb=100,
        max_caption_length=2200,
        max_hashtags=30
    ),
    Platform.TWITTER: PlatformSpec(
        platform=Platform.TWITTER,
        aspect_ratio="16:9",
        width=1920,
        height=1080,
        max_duration=140,
        recommended_fps=30,
        caption_style="minimal",
        max_file_size_mb=512,
        max_caption_length=280,
        max_hashtags=3
    )
}


class PlatformCredentials(BaseModel):
    """Platform API credentials (encrypted in production)"""
    
    platform: Platform
    access_token: str = Field(...)
    refresh_token: Optional[str] = Field(None)
    account_id: Optional[str] = Field(None)
    page_id: Optional[str] = Field(None)  # For Facebook pages
    expires_at: Optional[datetime] = Field(None)
    is_valid: bool = Field(default=True)


class PlatformConfig(BaseModel):
    """Platform configuration for a brand"""
    
    id: Optional[str] = Field(None)
    brand_id: str = Field(...)
    platform: Platform
    
    # Connection
    is_connected: bool = Field(default=False)
    credentials: Optional[PlatformCredentials] = Field(None)
    
    # Settings
    auto_publish: bool = Field(default=False)
    default_hashtags: List[str] = Field(default=[])
    caption_template: str = Field(default="")
    
    # Schedule
    enabled_days: List[int] = Field(default=[0, 1, 2, 3, 4, 5, 6])  # 0=Monday
    optimal_times: List[str] = Field(default=["19:00", "20:00", "21:00"])
    
    # Metadata
    connected_at: Optional[datetime] = Field(None)
    last_published_at: Optional[datetime] = Field(None)


class AdaptedContent(BaseModel):
    """Platform-adapted content"""
    
    platform: Platform
    caption: str = Field(...)
    hashtags: List[str] = Field(default=[])
    video_url: str = Field(...)
    thumbnail_url: Optional[str] = Field(None)
    
    # Platform-specific metadata
    mentions: List[str] = Field(default=[])
    location_tag: Optional[str] = Field(None)
    music_id: Optional[str] = Field(None)  # For TikTok/Instagram
    
    # Technical
    file_size_mb: float = Field(default=0)
    duration: float = Field(default=0)
    format_valid: bool = Field(default=True)


class ScheduledPost(BaseModel):
    """Scheduled content post"""
    
    id: Optional[str] = Field(None)
    brand_id: str = Field(...)
    content_id: str = Field(...)
    video_id: str = Field(...)
    
    # Platform info
    platform: Platform
    adapted_content: AdaptedContent
    
    # Scheduling
    scheduled_time: datetime = Field(...)
    timezone: str = Field(default="Africa/Algiers")
    
    # Status
    status: PublishStatus = Field(default=PublishStatus.SCHEDULED)
    retry_count: int = Field(default=0)
    max_retries: int = Field(default=3)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    published_at: Optional[datetime] = Field(None)
    error_message: Optional[str] = Field(None)


class PublishResult(BaseModel):
    """Result of publishing to a platform"""
    
    id: Optional[str] = Field(None)
    scheduled_post_id: str = Field(...)
    brand_id: str = Field(...)
    
    # Platform info
    platform: Platform
    platform_post_id: Optional[str] = Field(None)  # ID on the platform
    platform_url: Optional[str] = Field(None)  # URL to view the post
    
    # Status
    success: bool = Field(...)
    status: PublishStatus = Field(...)
    error_message: Optional[str] = Field(None)
    
    # Timing
    published_at: Optional[datetime] = Field(None)
    duration_seconds: float = Field(default=0)
    
    # Response data
    platform_response: Dict[str, Any] = Field(default={})


class ContentCalendarEntry(BaseModel):
    """Calendar entry for content planning"""
    
    id: Optional[str] = Field(None)
    brand_id: str = Field(...)
    
    # Content reference
    content_id: Optional[str] = Field(None)
    video_id: Optional[str] = Field(None)
    
    # Display info
    title: str = Field(...)
    pillar_name: str = Field(...)
    thumbnail_url: Optional[str] = Field(None)
    
    # Scheduling
    scheduled_time: datetime = Field(...)
    platforms: List[Platform] = Field(default=[Platform.INSTAGRAM_REELS])
    
    # Status
    status: PublishStatus = Field(default=PublishStatus.PENDING)
    
    # Colors for UI
    color: str = Field(default="#3B82F6")


class MonthlyCalendar(BaseModel):
    """Monthly content calendar"""
    
    brand_id: str = Field(...)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(...)
    
    entries: List[ContentCalendarEntry] = Field(default=[])
    
    # Statistics
    total_posts: int = Field(default=0)
    posts_by_pillar: Dict[str, int] = Field(default={})
    posts_by_platform: Dict[str, int] = Field(default={})
    
    # Status
    published_count: int = Field(default=0)
    scheduled_count: int = Field(default=0)
    pending_count: int = Field(default=0)
