from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class VideoGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=2000)
    mode: Literal["text-to-video", "image-to-video"]
    image_url: Optional[str] = None
    duration: Literal[5, 10] = 5
    aspect_ratio: Literal["16:9", "9:16", "1:1"] = "16:9"
    model: str = "kling-1.6"


class VideoGenerateResponse(BaseModel):
    task_id: str
    estimated_time: int  # seconds
    credits: int


class VideoStatusResponse(BaseModel):
    task_id: str
    status: Literal["pending", "processing", "completed", "failed"]
    progress: int = 0
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class ProjectResponse(BaseModel):
    id: str
    name: str
    prompt: str
    mode: Literal["text-to-video", "image-to-video"]
    status: Literal["pending", "processing", "completed", "failed"]
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration: int
    aspect_ratio: str
    credits_used: int
    created_at: datetime


# Audio schemas
class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    voice_id: str
    language: Literal["darija", "arabic", "french"] = "darija"


class TTSResponse(BaseModel):
    audio_url: str
    duration: float
    credits: int


class VoiceResponse(BaseModel):
    id: str
    name: str
    language: str
    preview_url: Optional[str] = None
    is_custom: bool = False


# Template schemas
class TemplateResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    thumbnail_url: str
    preview_url: Optional[str] = None
    duration: int
    credits: int
    parameters: dict = {}


# Credits schemas
class CreditBalanceResponse(BaseModel):
    balance: int
    last_updated: datetime


class CreditHistoryItem(BaseModel):
    id: str
    type: Literal["purchase", "generation", "voice", "refund"]
    amount: int
    description: str
    created_at: datetime


class PurchaseRequest(BaseModel):
    pack_id: str
    payment_method: str = "ccp"  # CCP, Baridimob, etc.


# Auth schemas
class UserCreate(BaseModel):
    email: str
    password: str
    name: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    credits: int
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
