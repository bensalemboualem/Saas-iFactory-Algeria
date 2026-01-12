"""
Request models for AI Tools API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum


class LanguageCode(str, Enum):
    """Supported language codes"""
    FRENCH = "fr"
    ARABIC = "ar"
    ENGLISH = "en"
    SPANISH = "es"
    GERMAN = "de"
    ITALIAN = "it"


class ImageSize(str, Enum):
    """Supported image sizes"""
    SMALL = "256x256"
    MEDIUM = "512x512"
    LARGE = "1024x1024"
    XLARGE = "1792x1024"
    PORTRAIT = "1024x1792"


class TextGenerationStyle(str, Enum):
    """Text generation styles"""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    CREATIVE = "creative"
    TECHNICAL = "technical"
    MARKETING = "marketing"


# ===================================
# Translation
# ===================================

class TranslateRequest(BaseModel):
    """Request for text translation"""
    text: str = Field(..., min_length=1, max_length=10000, description="Text to translate")
    source_language: LanguageCode = Field(..., description="Source language code")
    target_language: LanguageCode = Field(..., description="Target language code")
    preserve_formatting: bool = Field(default=True, description="Preserve text formatting")
    tenant_id: Optional[str] = Field(default=None, description="Tenant ID (rag-dz or helvetia)")
    
    @validator('target_language')
    def validate_different_languages(cls, v, values):
        if 'source_language' in values and v == values['source_language']:
            raise ValueError("Source and target languages must be different")
        return v


class BatchTranslateRequest(BaseModel):
    """Batch translation request"""
    texts: List[str] = Field(..., min_items=1, max_items=100, description="Texts to translate")
    source_language: LanguageCode
    target_language: LanguageCode
    preserve_formatting: bool = True
    tenant_id: Optional[str] = None


# ===================================
# Speech to Text
# ===================================

class SpeechToTextRequest(BaseModel):
    """Speech to text request"""
    language: Optional[LanguageCode] = Field(default=None, description="Audio language (auto-detect if not provided)")
    tenant_id: Optional[str] = None
    # File will be sent as multipart/form-data


# ===================================
# Text Generation
# ===================================

class TextGenerationRequest(BaseModel):
    """Text generation request"""
    prompt: str = Field(..., min_length=1, max_length=5000, description="Generation prompt")
    language: LanguageCode = Field(default=LanguageCode.FRENCH, description="Output language")
    style: TextGenerationStyle = Field(default=TextGenerationStyle.PROFESSIONAL, description="Writing style")
    max_tokens: int = Field(default=1000, ge=100, le=4000, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Creativity level (0-2)")
    model: Optional[str] = Field(default=None, description="Model to use (default: gpt-4o-mini)")
    tenant_id: Optional[str] = None


class TextImprovementRequest(BaseModel):
    """Text improvement/rewriting request"""
    text: str = Field(..., min_length=1, max_length=10000)
    language: LanguageCode = Field(default=LanguageCode.FRENCH)
    improvement_type: str = Field(
        default="grammar",
        description="Type: grammar, clarity, professional, creative, shorter, longer"
    )
    tenant_id: Optional[str] = None


# ===================================
# Image Generation
# ===================================

class ImageGenerationRequest(BaseModel):
    """Image generation request"""
    prompt: str = Field(..., min_length=1, max_length=1000, description="Image description")
    size: ImageSize = Field(default=ImageSize.LARGE, description="Image size")
    style: Optional[str] = Field(default="vivid", description="Style: vivid or natural")
    quality: Optional[str] = Field(default="standard", description="Quality: standard or hd")
    model: Optional[str] = Field(default=None, description="Model: dall-e-3, dall-e-2, stable-diffusion-xl")
    tenant_id: Optional[str] = None


class BatchImageGenerationRequest(BaseModel):
    """Batch image generation"""
    prompts: List[str] = Field(..., min_items=1, max_items=10)
    size: ImageSize = Field(default=ImageSize.LARGE)
    style: Optional[str] = "vivid"
    quality: Optional[str] = "standard"
    tenant_id: Optional[str] = None


# ===================================
# Background Removal
# ===================================

class BackgroundRemovalRequest(BaseModel):
    """Background removal request"""
    return_mask: bool = Field(default=False, description="Also return the mask")
    alpha_matting: bool = Field(default=True, description="Use alpha matting for better edges")
    tenant_id: Optional[str] = None
    # Image sent as multipart/form-data


# ===================================
# Image Upscaling
# ===================================

class ImageUpscaleRequest(BaseModel):
    """Image upscaling request"""
    scale_factor: int = Field(default=2, ge=2, le=4, description="Upscale factor (2x, 3x, 4x)")
    enhance_face: bool = Field(default=True, description="Enhance faces")
    tenant_id: Optional[str] = None
    # Image sent as multipart/form-data


# ===================================
# Image Transformation
# ===================================

class ImageToImageRequest(BaseModel):
    """Image-to-image transformation"""
    prompt: str = Field(..., min_length=1, max_length=1000, description="Transformation description")
    strength: float = Field(default=0.8, ge=0.0, le=1.0, description="Transformation strength (0-1)")
    preserve_structure: bool = Field(default=True, description="Preserve original structure")
    tenant_id: Optional[str] = None
    # Image sent as multipart/form-data


# ===================================
# Common
# ===================================

class HealthCheckRequest(BaseModel):
    """Health check request"""
    check_providers: bool = Field(default=False, description="Check AI provider connectivity")


class UsageStatsRequest(BaseModel):
    """Usage statistics request"""
    tenant_id: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
