"""
Response models for AI Tools API
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class BaseResponse(BaseModel):
    """Base response model"""
    success: bool = Field(default=True)
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseResponse):
    """Error response"""
    success: bool = False
    error_code: str
    error_details: Optional[Dict[str, Any]] = None


# ===================================
# Translation
# ===================================

class TranslateResponse(BaseResponse):
    """Translation response"""
    translated_text: str
    source_language: str
    target_language: str
    character_count: int
    provider: str = Field(default="openai")
    cached: bool = Field(default=False, description="Result from cache")


class BatchTranslateResponse(BaseResponse):
    """Batch translation response"""
    translations: List[TranslateResponse]
    total_characters: int
    provider: str = "openai"


# ===================================
# Speech to Text
# ===================================

class SpeechToTextResponse(BaseResponse):
    """Speech to text response"""
    text: str
    language: str
    duration_seconds: float
    provider: str = "openai"
    confidence: Optional[float] = None


class SpeechToTextSegment(BaseModel):
    """Timestamped transcript segment"""
    start: float
    end: float
    text: str
    confidence: Optional[float] = None


class DetailedSpeechToTextResponse(SpeechToTextResponse):
    """Detailed speech to text with timestamps"""
    segments: List[SpeechToTextSegment]


# ===================================
# Text Generation
# ===================================

class TextGenerationResponse(BaseResponse):
    """Text generation response"""
    generated_text: str
    prompt: str
    language: str
    model: str
    tokens_used: int
    finish_reason: str = Field(default="stop")


class TextImprovementResponse(BaseResponse):
    """Text improvement response"""
    improved_text: str
    original_text: str
    improvement_type: str
    changes_summary: Optional[str] = None
    tokens_used: int


# ===================================
# Image Generation
# ===================================

class ImageGenerationResponse(BaseResponse):
    """Image generation response"""
    image_url: str
    prompt: str
    revised_prompt: Optional[str] = None  # DALL-E 3 revised prompt
    size: str
    model: str
    storage_path: Optional[str] = None


class BatchImageGenerationResponse(BaseResponse):
    """Batch image generation response"""
    images: List[ImageGenerationResponse]
    total_images: int


# ===================================
# Background Removal
# ===================================

class BackgroundRemovalResponse(BaseResponse):
    """Background removal response"""
    image_url: str
    mask_url: Optional[str] = None
    original_size: Dict[str, int]  # {"width": 1024, "height": 768}
    provider: str = "rembg"
    storage_path: Optional[str] = None


# ===================================
# Image Upscaling
# ===================================

class ImageUpscaleResponse(BaseResponse):
    """Image upscaling response"""
    image_url: str
    original_size: Dict[str, int]
    upscaled_size: Dict[str, int]
    scale_factor: int
    provider: str
    storage_path: Optional[str] = None


# ===================================
# Image Transformation
# ===================================

class ImageToImageResponse(BaseResponse):
    """Image-to-image response"""
    image_url: str
    prompt: str
    strength: float
    model: str
    storage_path: Optional[str] = None


# ===================================
# Health & Stats
# ===================================

class ProviderStatus(BaseModel):
    """AI Provider status"""
    name: str
    available: bool
    latency_ms: Optional[float] = None
    error: Optional[str] = None


class HealthCheckResponse(BaseResponse):
    """Health check response"""
    status: str = "healthy"
    version: str
    environment: str
    providers: Optional[List[ProviderStatus]] = None


class UsageStats(BaseModel):
    """Usage statistics"""
    total_requests: int
    requests_by_tool: Dict[str, int]
    tokens_used: int
    images_generated: int
    audio_minutes_transcribed: float
    cost_estimate_usd: float


class UsageStatsResponse(BaseResponse):
    """Usage statistics response"""
    stats: UsageStats
    period_start: datetime
    period_end: datetime
    tenant_id: Optional[str] = None


# ===================================
# Common
# ===================================

class FileUploadResponse(BaseResponse):
    """File upload response"""
    file_id: str
    filename: str
    size_bytes: int
    mime_type: str
    storage_path: str


class ProcessingStatus(BaseModel):
    """Async processing status"""
    task_id: str
    status: str  # pending, processing, completed, failed
    progress: int = Field(ge=0, le=100)
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ProcessingStatusResponse(BaseResponse):
    """Processing status response"""
    task: ProcessingStatus
