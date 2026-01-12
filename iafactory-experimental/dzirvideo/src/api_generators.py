"""
API Endpoints for Dzir IA Video Multi-Generator System
Exposes all 31 AI generators via REST API
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
import logging

from generators.base import GeneratorCategory, GenerationRequest, GenerationStatus
from generators.registry import get_global_registry
from generators.router import SmartRouter, RoutingCriteria

logger = logging.getLogger(__name__)

# =====================================================================
# Router
# =====================================================================

router = APIRouter(prefix="/api/v1/generators", tags=["generators"])


# =====================================================================
# Request/Response Models
# =====================================================================

class GenerateRequest(BaseModel):
    """Request to generate content"""
    prompt: str = Field(..., description="Text prompt for generation")
    category: str = Field(..., description="Category: text-to-video, text-to-image, etc.")
    generator_name: Optional[str] = Field(None, description="Specific generator (auto-select if null)")

    # Optional parameters
    duration_seconds: Optional[float] = Field(10.0, description="Video duration (for video generators)")
    aspect_ratio: Optional[str] = Field("9:16", description="Aspect ratio (16:9, 9:16, 1:1, etc.)")
    resolution: Optional[str] = Field("1080p", description="Resolution (720p, 1080p, 4K)")
    style: Optional[str] = Field(None, description="Style preset")
    negative_prompt: Optional[str] = Field(None, description="Negative prompt")

    # Routing preferences
    max_budget_usd: Optional[float] = Field(None, description="Maximum budget (0 = free only)")
    quality_priority: bool = Field(True, description="Prioritize quality over cost")
    speed_priority: bool = Field(False, description="Prioritize speed")


class GenerateResponse(BaseModel):
    """Response from generate endpoint"""
    success: bool
    task_id: str
    generator_name: str
    status: str
    estimated_completion_time: Optional[float] = None
    estimated_cost_usd: Optional[float] = None
    message: Optional[str] = None


class StatusResponse(BaseModel):
    """Response from status check"""
    success: bool
    task_id: str
    generator_name: str
    status: str
    output_url: Optional[str] = None
    error_message: Optional[str] = None
    progress_percentage: Optional[float] = None


class GeneratorInfo(BaseModel):
    """Information about a generator"""
    name: str
    provider: str
    category: str
    quality_score: int
    api_cost_per_second: float
    api_cost_per_image: float
    free_tier: bool
    free_credits_per_day: int
    max_duration_seconds: float
    max_resolution: str
    avg_generation_time_seconds: float
    enabled: bool
    tags: List[str]


class MultiGenerateRequest(BaseModel):
    """Request to generate with multiple generators for comparison"""
    prompt: str
    category: str
    generators: List[str] = Field(..., description="List of generator names to compare")
    duration_seconds: Optional[float] = 10.0
    aspect_ratio: Optional[str] = "9:16"


class RecommendationRequest(BaseModel):
    """Request for generator recommendation"""
    category: str
    budget_level: str = Field("free", description="Budget level: free, budget, premium")


# =====================================================================
# Endpoints
# =====================================================================

@router.get("/list", response_model=List[str])
async def list_generators(
    category: Optional[str] = None,
    enabled_only: bool = True
):
    """
    List all available generators

    Args:
        category: Filter by category (text-to-video, text-to-image, etc.)
        enabled_only: Only return enabled generators

    Returns:
        List of generator names
    """
    registry = get_global_registry()

    if category:
        try:
            cat_enum = GeneratorCategory(category.replace("-", "_").upper())
            generators = registry.list_by_category(cat_enum, enabled_only=enabled_only)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    else:
        generators = registry.list_all(enabled_only=enabled_only)

    return generators


@router.get("/info/{generator_name}", response_model=GeneratorInfo)
async def get_generator_info(generator_name: str):
    """
    Get detailed information about a specific generator

    Args:
        generator_name: Generator identifier

    Returns:
        GeneratorInfo object
    """
    registry = get_global_registry()

    try:
        generator = registry.get(generator_name)
        metadata = registry.get_metadata(generator_name)
        caps = generator.capabilities

        # Determine primary category
        if caps.supports_text_to_video:
            category = "text-to-video"
        elif caps.supports_image_to_video:
            category = "image-to-video"
        elif caps.supports_text_to_image:
            category = "text-to-image"
        elif caps.supports_avatar_video:
            category = "avatar-video"
        elif caps.supports_reels_shortform:
            category = "reels-shortform"
        else:
            category = "unknown"

        return GeneratorInfo(
            name=generator_name,
            provider=metadata.get("provider", "Unknown"),
            category=category,
            quality_score=caps.quality_score,
            api_cost_per_second=caps.api_cost_per_second,
            api_cost_per_image=caps.api_cost_per_image,
            free_tier=caps.free_tier,
            free_credits_per_day=caps.free_credits_per_day,
            max_duration_seconds=caps.max_duration_seconds,
            max_resolution=caps.max_resolution,
            avg_generation_time_seconds=caps.avg_generation_time_seconds,
            enabled=metadata.get("enabled", True),
            tags=metadata.get("tags", [])
        )

    except KeyError:
        raise HTTPException(status_code=404, detail=f"Generator '{generator_name}' not found")
    except Exception as e:
        logger.error(f"Error getting generator info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary")
async def get_summary():
    """
    Get summary statistics of all generators

    Returns:
        Summary dictionary with counts by category
    """
    registry = get_global_registry()
    return registry.get_summary()


@router.post("/generate", response_model=GenerateResponse)
async def generate_content(request: GenerateRequest, background_tasks: BackgroundTasks):
    """
    Generate content using AI

    Args:
        request: Generation request

    Returns:
        GenerateResponse with task ID and status
    """
    registry = get_global_registry()
    router_instance = SmartRouter(registry)

    try:
        # Parse category
        category_enum = GeneratorCategory(request.category.replace("-", "_").upper())

        # Select generator (auto-route if not specified)
        if request.generator_name:
            generator_name = request.generator_name
            logger.info(f"Using specified generator: {generator_name}")
        else:
            # Auto-route using SmartRouter
            criteria = RoutingCriteria(
                category=category_enum,
                max_cost_usd=request.max_budget_usd,
                quality_priority=request.quality_priority,
                speed_priority=request.speed_priority,
                free_only=(request.max_budget_usd == 0),
                required_aspect_ratio=request.aspect_ratio
            )

            gen_request = GenerationRequest(
                prompt=request.prompt,
                category=category_enum,
                duration_seconds=request.duration_seconds,
                aspect_ratio=request.aspect_ratio,
                style=request.style,
                negative_prompt=request.negative_prompt
            )

            generator_name = router_instance.route(gen_request, criteria)
            logger.info(f"Auto-routed to generator: {generator_name}")

        # Get generator instance
        generator = registry.get(generator_name)

        # Build generation request
        gen_request = GenerationRequest(
            prompt=request.prompt,
            category=category_enum,
            duration_seconds=request.duration_seconds,
            aspect_ratio=request.aspect_ratio,
            style=request.style,
            negative_prompt=request.negative_prompt
        )

        # Estimate cost
        estimated_cost = generator.estimate_cost(request.duration_seconds)

        # Generate
        result = await generator.generate(gen_request)

        return GenerateResponse(
            success=True,
            task_id=result.task_id,
            generator_name=generator_name,
            status=result.status.value,
            estimated_completion_time=result.estimated_completion_time,
            estimated_cost_usd=estimated_cost,
            message=f"Generation started with {generator_name}"
        )

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{generator_name}/{task_id}", response_model=StatusResponse)
async def check_status(generator_name: str, task_id: str):
    """
    Check generation status

    Args:
        generator_name: Generator identifier
        task_id: Task ID from generate endpoint

    Returns:
        StatusResponse with current status and output URL if ready
    """
    registry = get_global_registry()

    try:
        generator = registry.get(generator_name)
        result = await generator.check_status(task_id)

        return StatusResponse(
            success=True,
            task_id=task_id,
            generator_name=generator_name,
            status=result.status.value,
            output_url=result.output_url,
            error_message=result.error_message,
            progress_percentage=result.progress_percentage
        )

    except KeyError:
        raise HTTPException(status_code=404, detail=f"Generator '{generator_name}' not found")
    except Exception as e:
        logger.error(f"Status check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cancel/{generator_name}/{task_id}")
async def cancel_generation(generator_name: str, task_id: str):
    """
    Cancel ongoing generation

    Args:
        generator_name: Generator identifier
        task_id: Task ID to cancel

    Returns:
        Success status
    """
    registry = get_global_registry()

    try:
        generator = registry.get(generator_name)
        success = await generator.cancel(task_id)

        if success:
            return {"success": True, "message": f"Task {task_id} cancelled"}
        else:
            return {"success": False, "message": "Cancellation not supported or failed"}

    except KeyError:
        raise HTTPException(status_code=404, detail=f"Generator '{generator_name}' not found")
    except Exception as e:
        logger.error(f"Cancel error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare", response_model=Dict)
async def compare_generators(request: MultiGenerateRequest):
    """
    Generate with multiple generators for comparison

    Args:
        request: Multi-generate request

    Returns:
        Dictionary with task IDs for each generator
    """
    registry = get_global_registry()
    category_enum = GeneratorCategory(request.category.replace("-", "_").upper())

    results = {}

    for generator_name in request.generators:
        try:
            generator = registry.get(generator_name)

            gen_request = GenerationRequest(
                prompt=request.prompt,
                category=category_enum,
                duration_seconds=request.duration_seconds,
                aspect_ratio=request.aspect_ratio
            )

            result = await generator.generate(gen_request)

            results[generator_name] = {
                "success": True,
                "task_id": result.task_id,
                "status": result.status.value,
                "estimated_time": result.estimated_completion_time
            }

        except Exception as e:
            logger.error(f"Error with generator {generator_name}: {e}")
            results[generator_name] = {
                "success": False,
                "error": str(e)
            }

    return {
        "success": True,
        "prompt": request.prompt,
        "generators": results,
        "message": f"Comparison started with {len(request.generators)} generators"
    }


@router.post("/recommend", response_model=Dict)
async def get_recommendation(request: RecommendationRequest):
    """
    Get generator recommendation based on criteria

    Args:
        request: Recommendation request

    Returns:
        Recommendation with top generators and reasoning
    """
    router_instance = SmartRouter()

    try:
        category_enum = GeneratorCategory(request.category.replace("-", "_").upper())
        recommendation = router_instance.get_recommendation(
            category=category_enum,
            budget_level=request.budget_level
        )

        return recommendation

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estimate-cost/{generator_name}")
async def estimate_cost(
    generator_name: str,
    duration_seconds: float = 10.0,
    num_images: int = 1
):
    """
    Estimate cost for a generation

    Args:
        generator_name: Generator identifier
        duration_seconds: Duration for video generators
        num_images: Number of images for image generators

    Returns:
        Cost estimate in USD
    """
    registry = get_global_registry()

    try:
        generator = registry.get(generator_name)
        caps = generator.capabilities

        if caps.supports_text_to_video or caps.supports_image_to_video:
            cost = caps.api_cost_per_second * duration_seconds
        else:
            cost = caps.api_cost_per_image * num_images

        return {
            "generator_name": generator_name,
            "estimated_cost_usd": cost,
            "duration_seconds": duration_seconds,
            "num_images": num_images,
            "free_tier": caps.free_tier,
            "free_credits_per_day": caps.free_credits_per_day
        }

    except KeyError:
        raise HTTPException(status_code=404, detail=f"Generator '{generator_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
