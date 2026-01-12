"""
Base Generator Interface for Dzir IA Video
Common interface for all AI image and video generators
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class GeneratorCategory(str, Enum):
    """Categories of generators"""
    TEXT_TO_VIDEO = "text_to_video"
    IMAGE_TO_VIDEO = "image_to_video"
    TEXT_TO_IMAGE = "text_to_image"
    IMAGE_TO_IMAGE = "image_to_image"
    AVATAR_VIDEO = "avatar_video"
    REELS_SHORTFORM = "reels_shortform"


class GenerationStatus(str, Enum):
    """Status of a generation task"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class GeneratorCapabilities:
    """Capabilities and limits of a generator"""

    # What it supports
    supports_text_to_video: bool = False
    supports_image_to_video: bool = False
    supports_text_to_image: bool = False
    supports_image_to_image: bool = False
    supports_avatar_video: bool = False
    supports_reels_shortform: bool = False

    # Technical specs
    max_duration_seconds: float = 10.0
    min_duration_seconds: float = 1.0
    max_resolution: str = "1080p"  # 1080p, 4K, etc.
    supported_aspect_ratios: List[str] = field(default_factory=lambda: ["16:9", "9:16", "1:1"])
    max_fps: int = 30

    # Pricing
    api_cost_per_second: float = 0.0  # USD per second of video
    api_cost_per_image: float = 0.0   # USD per image
    free_tier: bool = False
    free_credits_per_day: int = 0

    # Quality metrics (0-100)
    quality_score: int = 70  # Overall quality score
    realism_score: int = 70  # How realistic is the output
    coherence_score: int = 70  # Temporal coherence (for video)
    prompt_adherence_score: int = 70  # How well it follows prompts

    # Speed
    avg_generation_time_seconds: float = 30.0
    supports_async: bool = True  # If API is async (polling-based)

    # Features
    supports_negative_prompts: bool = False
    supports_style_presets: bool = False
    supports_custom_dimensions: bool = False
    supports_batch_generation: bool = False


@dataclass
class GenerationRequest:
    """Request for content generation"""

    # Core parameters
    prompt: str
    category: GeneratorCategory

    # Optional parameters
    negative_prompt: Optional[str] = None
    duration_seconds: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    aspect_ratio: Optional[str] = None
    fps: Optional[int] = None
    style_preset: Optional[str] = None

    # Input files (for image-to-video, etc.)
    input_image_url: Optional[str] = None
    input_video_url: Optional[str] = None

    # Metadata
    task_id: Optional[str] = None
    user_id: Optional[str] = None


@dataclass
class GenerationResult:
    """Result of a generation task"""

    # Status
    status: GenerationStatus
    task_id: str

    # Output
    output_url: Optional[str] = None
    output_local_path: Optional[str] = None
    thumbnail_url: Optional[str] = None

    # Metadata
    duration_seconds: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    file_size_mb: Optional[float] = None

    # Timing
    generation_time_seconds: Optional[float] = None
    estimated_completion_time: Optional[float] = None  # For pending tasks

    # Error handling
    error_message: Optional[str] = None
    error_code: Optional[str] = None

    # Cost tracking
    estimated_cost_usd: float = 0.0


class BaseGenerator(ABC):
    """
    Abstract base class for all AI generators

    All generator implementations must inherit from this class
    and implement the required methods.
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize generator

        Args:
            api_key: API key for the service (if required)
            **kwargs: Additional configuration parameters
        """
        self.api_key = api_key
        self.config = kwargs
        self.capabilities = self._define_capabilities()
        self._validate_config()

    @abstractmethod
    def _define_capabilities(self) -> GeneratorCapabilities:
        """
        Define what this generator can do

        Returns:
            GeneratorCapabilities object
        """
        pass

    @abstractmethod
    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate content (video, image, etc.)

        Args:
            request: Generation request parameters

        Returns:
            GenerationResult with status and output

        Raises:
            ValueError: If request parameters are invalid
            APIError: If API call fails
        """
        pass

    @abstractmethod
    async def check_status(self, task_id: str) -> GenerationResult:
        """
        Check status of a generation task

        Args:
            task_id: Task identifier

        Returns:
            GenerationResult with current status
        """
        pass

    @abstractmethod
    async def cancel(self, task_id: str) -> bool:
        """
        Cancel a running generation task

        Args:
            task_id: Task identifier

        Returns:
            True if cancelled successfully
        """
        pass

    def estimate_cost(self, request: GenerationRequest) -> float:
        """
        Estimate cost for a generation request

        Args:
            request: Generation request

        Returns:
            Estimated cost in USD
        """
        if request.category in [GeneratorCategory.TEXT_TO_VIDEO, GeneratorCategory.IMAGE_TO_VIDEO]:
            duration = request.duration_seconds or 5.0
            return duration * self.capabilities.api_cost_per_second
        else:
            return self.capabilities.api_cost_per_image

    def validate_request(self, request: GenerationRequest) -> bool:
        """
        Validate if this generator can handle the request

        Args:
            request: Generation request

        Returns:
            True if request is valid for this generator

        Raises:
            ValueError: If request is invalid
        """
        # Check category support
        category_support_map = {
            GeneratorCategory.TEXT_TO_VIDEO: self.capabilities.supports_text_to_video,
            GeneratorCategory.IMAGE_TO_VIDEO: self.capabilities.supports_image_to_video,
            GeneratorCategory.TEXT_TO_IMAGE: self.capabilities.supports_text_to_image,
            GeneratorCategory.IMAGE_TO_IMAGE: self.capabilities.supports_image_to_image,
            GeneratorCategory.AVATAR_VIDEO: self.capabilities.supports_avatar_video,
            GeneratorCategory.REELS_SHORTFORM: self.capabilities.supports_reels_shortform,
        }

        if not category_support_map.get(request.category, False):
            raise ValueError(f"Generator does not support {request.category}")

        # Check duration limits (for video)
        if request.duration_seconds:
            if request.duration_seconds > self.capabilities.max_duration_seconds:
                raise ValueError(
                    f"Requested duration {request.duration_seconds}s exceeds max "
                    f"{self.capabilities.max_duration_seconds}s"
                )
            if request.duration_seconds < self.capabilities.min_duration_seconds:
                raise ValueError(
                    f"Requested duration {request.duration_seconds}s below min "
                    f"{self.capabilities.min_duration_seconds}s"
                )

        # Check aspect ratio
        if request.aspect_ratio:
            if request.aspect_ratio not in self.capabilities.supported_aspect_ratios:
                raise ValueError(
                    f"Aspect ratio {request.aspect_ratio} not supported. "
                    f"Supported: {self.capabilities.supported_aspect_ratios}"
                )

        return True

    def _validate_config(self):
        """Validate generator configuration"""
        # Override in subclasses if needed
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(quality={self.capabilities.quality_score})"

    def __repr__(self) -> str:
        return self.__str__()


class GeneratorError(Exception):
    """Base exception for generator errors"""
    pass


class APIError(GeneratorError):
    """API call failed"""
    pass


class QuotaExceededError(GeneratorError):
    """API quota exceeded"""
    pass


class InvalidRequestError(GeneratorError):
    """Invalid request parameters"""
    pass
