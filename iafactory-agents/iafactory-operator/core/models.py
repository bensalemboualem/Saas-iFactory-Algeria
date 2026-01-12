"""
IA Factory Operator - Pydantic Models
API request/response models and internal data structures
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


# =============================================================================
# ENUMS
# =============================================================================

class PlatformEnum(str, Enum):
    """Supported output platforms"""
    instagram_reels = "instagram_reels"
    tiktok = "tiktok"
    youtube_shorts = "youtube_shorts"
    square = "square"  # 1:1 for feed posts


class InputTypeEnum(str, Enum):
    """Types of input video"""
    raw_video = "raw_video"
    veo_output = "veo_output"
    uploaded = "uploaded"


class JobStatusEnum(str, Enum):
    """Job status states"""
    pending = "pending"
    downloading = "downloading"
    analyzing = "analyzing"
    planning = "planning"
    rendering = "rendering"
    uploading = "uploading"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class TemplateEnum(str, Enum):
    """Pre-defined editing templates"""
    product_demo = "product_demo"
    talking_head = "talking_head"
    food_promo = "food_promo"
    real_estate = "real_estate"
    fashion = "fashion"
    algerian_minimal = "algerian_minimal"
    energetic = "energetic"
    cinematic = "cinematic"
    custom = "custom"


class StyleEnum(str, Enum):
    """Visual styles"""
    default = "default"
    algerian_minimal = "algerian_minimal"
    professional = "professional"
    vibrant = "vibrant"
    dark = "dark"
    retro = "retro"


class LanguageEnum(str, Enum):
    """Supported languages"""
    fr = "fr"
    ar = "ar"
    en = "en"
    darija = "darija"  # Algerian Arabic


# =============================================================================
# REQUEST MODELS
# =============================================================================

class VideoEditRequest(BaseModel):
    """Request to create a video editing job"""
    
    input_type: InputTypeEnum = Field(
        default=InputTypeEnum.raw_video,
        description="Type of input video"
    )
    source_video_url: HttpUrl = Field(
        ...,
        description="URL of the source video to process"
    )
    template: TemplateEnum = Field(
        default=TemplateEnum.algerian_minimal,
        description="Editing template to use"
    )
    target_duration: int = Field(
        default=15,
        ge=5,
        le=180,
        description="Target duration in seconds"
    )
    platforms: List[PlatformEnum] = Field(
        default=[PlatformEnum.instagram_reels],
        description="Target platforms for export"
    )
    style: StyleEnum = Field(
        default=StyleEnum.default,
        description="Visual style to apply"
    )
    language: LanguageEnum = Field(
        default=LanguageEnum.fr,
        description="Primary language for captions/voiceover"
    )
    add_captions: bool = Field(
        default=True,
        description="Whether to add auto-generated captions"
    )
    add_music: bool = Field(
        default=False,
        description="Whether to add background music"
    )
    music_style: Optional[str] = Field(
        default=None,
        description="Style of background music if add_music=True"
    )
    voiceover_text: Optional[str] = Field(
        default=None,
        description="Custom voiceover text (if provided, will generate TTS)"
    )
    webhook_url: Optional[HttpUrl] = Field(
        default=None,
        description="URL to notify when job completes"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata to store with the job"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "input_type": "raw_video",
                "source_video_url": "https://cdn.iafactory.com/uploads/video_123.mp4",
                "template": "product_demo",
                "target_duration": 15,
                "platforms": ["instagram_reels", "tiktok"],
                "style": "algerian_minimal",
                "language": "fr",
                "add_captions": True,
                "webhook_url": "https://iafactory.com/webhooks/video-complete"
            }
        }


class VideoJobCreate(BaseModel):
    """Internal model for job creation"""
    request: VideoEditRequest
    user_id: Optional[str] = None
    priority: int = Field(default=0, ge=0, le=10)


# =============================================================================
# RESPONSE MODELS
# =============================================================================

class VideoOutput(BaseModel):
    """Output video for a specific platform"""
    
    platform: PlatformEnum
    duration: float
    aspect_ratio: str
    width: int
    height: int
    video_url: str
    thumbnail_url: Optional[str] = None
    file_size: Optional[int] = None
    codec: str = "h264"


class JobProgress(BaseModel):
    """Detailed progress information"""
    
    stage: str
    percent: int
    message: str
    started_at: Optional[datetime] = None
    estimated_remaining: Optional[int] = None  # seconds


class VideoJobResponse(BaseModel):
    """Response model for video job status"""
    
    job_id: str
    status: JobStatusEnum
    progress: int = Field(default=0, ge=0, le=100)
    progress_detail: Optional[JobProgress] = None
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    input: VideoEditRequest
    outputs: List[VideoOutput] = []
    
    transcript: Optional[str] = None
    scenes_detected: int = 0
    
    logs: List[str] = []
    error: Optional[str] = None
    
    # Billing info
    processing_time_seconds: Optional[float] = None
    credits_used: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "opv_20251206_abc123",
                "status": "completed",
                "progress": 100,
                "created_at": "2025-12-06T10:00:00Z",
                "updated_at": "2025-12-06T10:02:30Z",
                "outputs": [
                    {
                        "platform": "instagram_reels",
                        "duration": 15,
                        "aspect_ratio": "9:16",
                        "width": 1080,
                        "height": 1920,
                        "video_url": "https://cdn.iafactory.com/outputs/opv_abc123_instagram.mp4"
                    }
                ]
            }
        }


# =============================================================================
# LIST RESPONSE
# =============================================================================

class JobListResponse(BaseModel):
    """Paginated list of jobs"""
    
    jobs: List[VideoJobResponse]
    total: int
    page: int
    per_page: int
    has_more: bool


# =============================================================================
# WEBHOOK PAYLOAD
# =============================================================================

class WebhookPayload(BaseModel):
    """Payload sent to webhook URL on job completion"""
    
    event: str = "video.job.completed"
    job_id: str
    status: JobStatusEnum
    outputs: List[VideoOutput]
    error: Optional[str] = None
    timestamp: datetime
    signature: Optional[str] = None


# =============================================================================
# TEMPLATE INFO
# =============================================================================

class TemplateInfo(BaseModel):
    """Information about an editing template"""
    
    id: TemplateEnum
    name: str
    name_ar: str
    name_en: str
    description: str
    icon: str
    recommended_duration: int
    supports_captions: bool = True
    supports_music: bool = True


class PlatformInfo(BaseModel):
    """Information about a platform"""
    
    id: PlatformEnum
    name: str
    aspect_ratio: str
    width: int
    height: int
    max_duration: int
    recommended_duration: int
