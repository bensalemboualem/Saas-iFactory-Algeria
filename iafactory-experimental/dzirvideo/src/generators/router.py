"""
Smart Router for Dzir IA Video
Intelligent routing to select optimal AI generator based on requirements
"""

from typing import Optional, List, Dict
import logging
from dataclasses import dataclass

from .base import GeneratorCategory, GenerationRequest
from .registry import GeneratorRegistry

logger = logging.getLogger(__name__)


@dataclass
class RoutingCriteria:
    """Criteria for generator selection"""

    # Required
    category: GeneratorCategory

    # Constraints
    max_cost_usd: Optional[float] = None  # Maximum budget
    max_generation_time_seconds: Optional[float] = None  # Speed requirement
    min_quality_score: int = 70  # Minimum quality threshold
    free_only: bool = False  # Only use free generators

    # Preferences
    quality_priority: bool = True  # Prioritize quality over cost/speed
    speed_priority: bool = False  # Prioritize speed
    cost_priority: bool = False  # Prioritize low cost

    # Requirements
    required_aspect_ratio: Optional[str] = None  # e.g., "9:16"
    required_resolution: Optional[str] = None  # e.g., "1080p", "4K"
    required_features: List[str] = None  # e.g., ["negative_prompts", "style_presets"]


class SmartRouter:
    """
    Intelligent router for automatic generator selection

    Analyzes request requirements and selects the optimal generator
    based on quality, cost, speed, and other criteria.
    """

    def __init__(self, registry: Optional[GeneratorRegistry] = None):
        """
        Initialize router

        Args:
            registry: Generator registry (uses global if not provided)
        """
        if registry is None:
            from .registry import get_global_registry
            registry = get_global_registry()
        self.registry = registry

    def route(
        self,
        request: GenerationRequest,
        criteria: Optional[RoutingCriteria] = None,
        fallback_order: Optional[List[str]] = None
    ) -> str:
        """
        Route request to optimal generator

        Args:
            request: Generation request
            criteria: Routing criteria (auto-detected if not provided)
            fallback_order: Ordered list of fallback generators

        Returns:
            Generator name

        Raises:
            ValueError: If no suitable generator found
        """
        if criteria is None:
            criteria = self._auto_detect_criteria(request)

        # Get candidates
        candidates = self._get_candidates(criteria)

        if not candidates:
            # Try fallback
            if fallback_order:
                for generator_name in fallback_order:
                    try:
                        generator = self.registry.get(generator_name)
                        if generator.validate_request(request):
                            logger.info(f"Using fallback generator: {generator_name}")
                            return generator_name
                    except:
                        continue

            raise ValueError(f"No suitable generator found for {criteria.category}")

        # Score and rank candidates
        ranked = self._rank_candidates(candidates, criteria, request)

        if not ranked:
            raise ValueError("No generators passed ranking criteria")

        best_generator = ranked[0][0]
        logger.info(f"Selected generator: {best_generator} (score: {ranked[0][1]:.2f})")

        return best_generator

    def route_text_to_video(
        self,
        prompt: str,
        duration: float = 10.0,
        budget: Optional[float] = None,
        quality_priority: bool = True,
        aspect_ratio: str = "9:16"
    ) -> str:
        """
        Route text-to-video request

        Args:
            prompt: Text prompt
            duration: Video duration in seconds
            budget: Maximum budget in USD (None = unlimited)
            quality_priority: Prioritize quality over cost
            aspect_ratio: Video aspect ratio

        Returns:
            Generator name
        """
        request = GenerationRequest(
            prompt=prompt,
            category=GeneratorCategory.TEXT_TO_VIDEO,
            duration_seconds=duration,
            aspect_ratio=aspect_ratio
        )

        criteria = RoutingCriteria(
            category=GeneratorCategory.TEXT_TO_VIDEO,
            max_cost_usd=budget,
            quality_priority=quality_priority,
            free_only=(budget == 0),
            required_aspect_ratio=aspect_ratio
        )

        # Default fallback order (free generators first)
        fallback = ["wan_2_1", "kling_ai", "digen_sora", "pika_labs", "luma_dream"]

        return self.route(request, criteria, fallback_order=fallback)

    def route_text_to_image(
        self,
        prompt: str,
        budget: Optional[float] = None,
        quality_priority: bool = True,
        resolution: str = "1080p"
    ) -> str:
        """
        Route text-to-image request

        Args:
            prompt: Text prompt
            budget: Maximum budget in USD
            quality_priority: Prioritize quality
            resolution: Image resolution

        Returns:
            Generator name
        """
        request = GenerationRequest(
            prompt=prompt,
            category=GeneratorCategory.TEXT_TO_IMAGE
        )

        criteria = RoutingCriteria(
            category=GeneratorCategory.TEXT_TO_IMAGE,
            max_cost_usd=budget,
            quality_priority=quality_priority,
            free_only=(budget == 0),
            required_resolution=resolution
        )

        fallback = ["qwen_vl", "flux_1", "ideogram", "leonardo_ai"]

        return self.route(request, criteria, fallback_order=fallback)

    def get_recommendation(
        self,
        category: GeneratorCategory,
        budget_level: str = "free"  # free, budget, premium
    ) -> Dict:
        """
        Get generator recommendation with explanation

        Args:
            category: Generator category
            budget_level: Budget tier (free/budget/premium)

        Returns:
            Dictionary with recommendation and reasoning
        """
        budget_map = {
            "free": 0.0,
            "budget": 0.10,  # $0.10 per generation
            "premium": 1.0   # Up to $1 per generation
        }

        criteria = RoutingCriteria(
            category=category,
            max_cost_usd=budget_map.get(budget_level, 0.0),
            free_only=(budget_level == "free"),
            quality_priority=(budget_level == "premium")
        )

        candidates = self._get_candidates(criteria)

        if not candidates:
            return {
                "generator": None,
                "reason": f"No generators available for {category} at {budget_level} tier"
            }

        # Get top 3
        ranked = self._rank_candidates(candidates, criteria, None)[:3]

        recommendations = []
        for gen_name, score in ranked:
            caps = self.registry.get_capabilities(gen_name)
            meta = self.registry.get_metadata(gen_name)

            recommendations.append({
                "name": gen_name,
                "score": score,
                "provider": meta.get("provider", "Unknown"),
                "quality": caps.quality_score,
                "cost_per_sec": caps.api_cost_per_second,
                "cost_per_image": caps.api_cost_per_image,
                "free_tier": caps.free_tier,
                "avg_time": caps.avg_generation_time_seconds
            })

        return {
            "primary_recommendation": recommendations[0],
            "alternatives": recommendations[1:],
            "budget_level": budget_level,
            "category": category.value
        }

    def _auto_detect_criteria(self, request: GenerationRequest) -> RoutingCriteria:
        """Auto-detect routing criteria from request"""
        return RoutingCriteria(
            category=request.category,
            quality_priority=True,
            required_aspect_ratio=request.aspect_ratio,
            required_resolution=f"{request.width}x{request.height}" if request.width else None
        )

    def _get_candidates(self, criteria: RoutingCriteria) -> List[str]:
        """Get candidate generators matching criteria"""
        return self.registry.list_by_category(
            criteria.category,
            enabled_only=True
        )

    def _rank_candidates(
        self,
        candidates: List[str],
        criteria: RoutingCriteria,
        request: Optional[GenerationRequest]
    ) -> List[tuple]:
        """
        Rank candidates by suitability score

        Returns:
            List of (generator_name, score) tuples, sorted by score descending
        """
        scored = []

        for name in candidates:
            try:
                generator = self.registry.get(name)
                caps = generator.capabilities

                # Validate request if provided
                if request:
                    try:
                        generator.validate_request(request)
                    except ValueError as e:
                        logger.debug(f"Generator {name} rejected: {e}")
                        continue

                # Calculate score
                score = self._calculate_score(caps, criteria)

                scored.append((name, score))

            except Exception as e:
                logger.error(f"Error scoring generator {name}: {e}")

        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)

        return scored

    def _calculate_score(self, caps, criteria: RoutingCriteria) -> float:
        """
        Calculate suitability score for a generator

        Returns:
            Score (0-100)
        """
        score = 0.0

        # Base score from quality
        score += caps.quality_score * 0.4  # 40% weight

        # Cost scoring
        if criteria.free_only:
            if caps.free_tier:
                score += 30  # Bonus for free tier
            else:
                return 0  # Reject non-free if free_only
        elif criteria.max_cost_usd is not None:
            if criteria.category in [GeneratorCategory.TEXT_TO_VIDEO, GeneratorCategory.IMAGE_TO_VIDEO]:
                cost = caps.api_cost_per_second * 10  # Assume 10s video
            else:
                cost = caps.api_cost_per_image

            if cost > criteria.max_cost_usd:
                return 0  # Reject if over budget

            # Score inversely proportional to cost
            cost_score = max(0, 30 * (1 - cost / criteria.max_cost_usd))
            score += cost_score

        # Speed scoring
        if criteria.max_generation_time_seconds:
            if caps.avg_generation_time_seconds <= criteria.max_generation_time_seconds:
                speed_score = 20
            else:
                speed_score = max(0, 20 * (criteria.max_generation_time_seconds / caps.avg_generation_time_seconds))
            score += speed_score

        # Priority adjustments
        if criteria.quality_priority:
            score += caps.quality_score * 0.2  # Extra 20% for quality
        if criteria.speed_priority:
            speed_score = max(0, 30 * (60.0 / caps.avg_generation_time_seconds))  # Assuming 60s baseline
            score += speed_score * 0.3
        if criteria.cost_priority:
            if caps.free_tier:
                score += 40

        # Feature bonuses
        if criteria.required_features:
            if caps.supports_negative_prompts and "negative_prompts" in criteria.required_features:
                score += 5
            if caps.supports_style_presets and "style_presets" in criteria.required_features:
                score += 5

        return min(100, score)  # Cap at 100


# Convenience function
def auto_route(
    prompt: str,
    category: GeneratorCategory,
    budget: Optional[float] = None,
    **kwargs
) -> str:
    """
    Automatically route a generation request

    Args:
        prompt: Text prompt
        category: Generation category
        budget: Maximum budget (None = unlimited, 0 = free only)
        **kwargs: Additional request parameters

    Returns:
        Generator name
    """
    router = SmartRouter()

    request = GenerationRequest(
        prompt=prompt,
        category=category,
        **kwargs
    )

    criteria = RoutingCriteria(
        category=category,
        max_cost_usd=budget,
        free_only=(budget == 0)
    )

    return router.route(request, criteria)
