"""
Unit Tests for Dzir IA Video Multi-Generator System
Tests all 40 generators, registry, router, and API
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock

# Import generator components
import sys
sys.path.insert(0, 'src')

from generators.base import (
    BaseGenerator,
    GeneratorCapabilities,
    GenerationRequest,
    GenerationResult,
    GeneratorCategory,
    GenerationStatus,
    APIError,
    QuotaExceededError
)
from generators.registry import GeneratorRegistry, get_global_registry
from generators.router import SmartRouter, RoutingCriteria


# =====================================================================
# Base Generator Tests
# =====================================================================

class TestBaseGenerator:
    """Test BaseGenerator abstract class"""

    def test_capabilities_structure(self):
        """Test GeneratorCapabilities dataclass"""
        caps = GeneratorCapabilities(
            supports_text_to_video=True,
            max_duration_seconds=10.0,
            api_cost_per_second=0.05,
            quality_score=95
        )

        assert caps.supports_text_to_video is True
        assert caps.max_duration_seconds == 10.0
        assert caps.api_cost_per_second == 0.05
        assert caps.quality_score == 95

    def test_generation_request(self):
        """Test GenerationRequest model"""
        request = GenerationRequest(
            prompt="Test video",
            category=GeneratorCategory.TEXT_TO_VIDEO,
            duration_seconds=10.0
        )

        assert request.prompt == "Test video"
        assert request.category == GeneratorCategory.TEXT_TO_VIDEO
        assert request.duration_seconds == 10.0

    def test_generation_result(self):
        """Test GenerationResult model"""
        result = GenerationResult(
            status=GenerationStatus.COMPLETED,
            task_id="test-123",
            output_url="https://example.com/video.mp4"
        )

        assert result.status == GenerationStatus.COMPLETED
        assert result.task_id == "test-123"
        assert result.output_url == "https://example.com/video.mp4"


# =====================================================================
# WAN 2.1 Generator Tests (FREE - Alibaba)
# =====================================================================

class TestWAN21Generator:
    """Test WAN 2.1 generator (free Alibaba)"""

    @pytest.mark.asyncio
    async def test_capabilities(self):
        """Test WAN 2.1 capabilities"""
        from generators.text_to_video.wan_2_1 import WAN21Generator

        # Mock to avoid needing real API key
        with patch.dict('os.environ', {'ALIBABA_DASHSCOPE_API_KEY': 'test-key'}):
            gen = WAN21Generator()

        caps = gen.capabilities

        assert caps.supports_text_to_video is True
        assert caps.max_duration_seconds == 10.0
        assert caps.api_cost_per_second == 0.0  # Free
        assert caps.free_tier is True
        assert caps.quality_score == 85

    @pytest.mark.asyncio
    async def test_cost_estimation(self):
        """Test cost estimation"""
        from generators.text_to_video.wan_2_1 import WAN21Generator

        with patch.dict('os.environ', {'ALIBABA_DASHSCOPE_API_KEY': 'test-key'}):
            gen = WAN21Generator()

        cost = gen.estimate_cost(10.0)
        assert cost == 0.0  # Free generator


# =====================================================================
# FLUX.1 Generator Tests (FREE - Image)
# =====================================================================

class TestFLUX1Generator:
    """Test FLUX.1 free image generator"""

    @pytest.mark.asyncio
    async def test_capabilities(self):
        """Test FLUX.1 capabilities"""
        from generators.text_to_image.flux_1 import FLUX1Generator

        with patch.dict('os.environ', {'TOGETHER_API_KEY': 'test-key'}):
            gen = FLUX1Generator()

        caps = gen.capabilities

        assert caps.supports_text_to_image is True
        assert caps.api_cost_per_image == 0.0  # Free
        assert caps.free_tier is True
        assert caps.quality_score == 90


# =====================================================================
# Registry Tests
# =====================================================================

class TestGeneratorRegistry:
    """Test GeneratorRegistry functionality"""

    def test_registry_initialization(self):
        """Test registry creates properly"""
        registry = GeneratorRegistry()
        assert registry is not None
        assert isinstance(registry._generators, dict)

    def test_register_generator(self):
        """Test registering a generator"""
        from generators.text_to_video.wan_2_1 import WAN21Generator

        registry = GeneratorRegistry()
        registry.register("test_gen", WAN21Generator, provider="Test", tags=["test"])

        assert "test_gen" in registry._generators
        assert registry._metadata["test_gen"]["provider"] == "Test"

    def test_list_all_generators(self):
        """Test listing all generators"""
        registry = get_global_registry()

        generators = registry.list_all(enabled_only=False)

        # Should have 40 generators
        assert len(generators) >= 40

    def test_list_by_category(self):
        """Test listing by category"""
        registry = get_global_registry()

        text_to_video = registry.list_by_category(GeneratorCategory.TEXT_TO_VIDEO)

        # Should have 17 text-to-video generators
        assert len(text_to_video) >= 17

    def test_find_best_free_generator(self):
        """Test finding best free generator"""
        registry = get_global_registry()

        best = registry.find_best(
            category=GeneratorCategory.TEXT_TO_VIDEO,
            free_only=True,
            min_quality=80
        )

        assert best is not None
        # Should return WAN 2.1 or Kling AI (high quality free options)
        assert best in ["wan_2_1", "kling_ai", "luma_dream"]

    def test_get_summary(self):
        """Test registry summary"""
        registry = get_global_registry()

        summary = registry.get_summary()

        assert "total_generators" in summary
        assert "free_generators" in summary
        assert "by_category" in summary
        assert summary["total_generators"] >= 40


# =====================================================================
# Smart Router Tests
# =====================================================================

class TestSmartRouter:
    """Test SmartRouter auto-selection"""

    def test_router_initialization(self):
        """Test router creates properly"""
        router = SmartRouter()
        assert router is not None
        assert router.registry is not None

    def test_route_text_to_video_free_only(self):
        """Test routing with free-only constraint"""
        router = SmartRouter()

        generator_name = router.route_text_to_video(
            prompt="Test video",
            duration=10.0,
            budget=0.0,  # Free only
            quality_priority=True
        )

        # Should select a free generator
        assert generator_name in ["wan_2_1", "digen_sora", "cogvideo", "open_sora"]

    def test_route_text_to_video_premium(self):
        """Test routing with premium budget"""
        router = SmartRouter()

        generator_name = router.route_text_to_video(
            prompt="Test video",
            duration=10.0,
            budget=1.0,  # $1 budget
            quality_priority=True
        )

        # Should select high-quality generator (may be premium)
        assert generator_name is not None

    def test_route_text_to_image(self):
        """Test image routing"""
        router = SmartRouter()

        generator_name = router.route_text_to_image(
            prompt="Test image",
            budget=0.0,
            quality_priority=True
        )

        # Should select free image generator
        assert generator_name in ["qwen_vl", "flux_1"]

    def test_get_recommendation(self):
        """Test getting recommendations"""
        router = SmartRouter()

        rec = router.get_recommendation(
            category=GeneratorCategory.TEXT_TO_VIDEO,
            budget_level="free"
        )

        assert "primary_recommendation" in rec
        assert "alternatives" in rec
        assert rec["primary_recommendation"] is not None


# =====================================================================
# Scoring Algorithm Tests
# =====================================================================

class TestScoringAlgorithm:
    """Test router scoring logic"""

    def test_score_calculation_free_tier(self):
        """Test scoring for free tier generators"""
        router = SmartRouter()

        caps = GeneratorCapabilities(
            supports_text_to_video=True,
            max_duration_seconds=10.0,
            api_cost_per_second=0.0,
            free_tier=True,
            quality_score=85
        )

        criteria = RoutingCriteria(
            category=GeneratorCategory.TEXT_TO_VIDEO,
            free_only=True,
            quality_priority=True
        )

        score = router._calculate_score(caps, criteria)

        # Free tier should get bonus points
        assert score > 50

    def test_score_calculation_premium(self):
        """Test scoring for premium generators"""
        router = SmartRouter()

        caps = GeneratorCapabilities(
            supports_text_to_video=True,
            max_duration_seconds=60.0,
            api_cost_per_second=0.05,
            free_tier=False,
            quality_score=95
        )

        criteria = RoutingCriteria(
            category=GeneratorCategory.TEXT_TO_VIDEO,
            max_cost_usd=1.0,
            quality_priority=True
        )

        score = router._calculate_score(caps, criteria)

        # High quality should score well
        assert score > 70


# =====================================================================
# Integration Tests
# =====================================================================

class TestIntegration:
    """Integration tests for complete workflows"""

    def test_registry_router_integration(self):
        """Test registry and router work together"""
        registry = get_global_registry()
        router = SmartRouter(registry)

        request = GenerationRequest(
            prompt="Test video",
            category=GeneratorCategory.TEXT_TO_VIDEO,
            duration_seconds=10.0
        )

        criteria = RoutingCriteria(
            category=GeneratorCategory.TEXT_TO_VIDEO,
            free_only=True
        )

        generator_name = router.route(request, criteria)

        # Should successfully select a generator
        assert generator_name is not None

        # Generator should be in registry
        gen = registry.get(generator_name, api_key="test")
        assert gen is not None

    def test_all_generators_registered(self):
        """Test all 40 generators are registered"""
        registry = get_global_registry()

        expected_generators = [
            # Text-to-Video (17)
            "wan_2_1", "kling_ai", "pika_labs", "luma_dream", "hailuo_ai",
            "runway_gen4", "veo_2", "sora", "ltx_studio", "cogvideo",
            "open_sora", "starryai_video", "hunyuan_video", "mochi_1",
            "vidu_ai", "pollo_ai", "krea_video",

            # Text-to-Image (9)
            "qwen_vl", "flux_1", "dall_e_3", "midjourney", "ideogram",
            "leonardo_ai", "adobe_firefly", "playground_v2", "stable_diffusion_35",

            # Image-to-Video (1)
            "stable_video_diffusion",

            # Avatar (5)
            "vidnoz", "deepbrain_ai", "elai_io", "heygen", "synthesia",

            # Reels (7)
            "digen_sora", "pictory", "capcut", "lumen5", "descript",
            "invideo_ai", "canva_ai"
        ]

        all_generators = registry.list_all(enabled_only=False)

        for gen_name in expected_generators:
            assert gen_name in all_generators, f"Generator {gen_name} not registered"


# =====================================================================
# Error Handling Tests
# =====================================================================

class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_quota_exceeded_error(self):
        """Test QuotaExceededError is raised correctly"""
        error = QuotaExceededError("Daily quota exceeded")
        assert isinstance(error, Exception)
        assert "quota" in str(error).lower()

    def test_api_error(self):
        """Test APIError is raised correctly"""
        error = APIError("API returned 500")
        assert isinstance(error, Exception)
        assert "500" in str(error)

    def test_invalid_generator_name(self):
        """Test getting non-existent generator"""
        registry = GeneratorRegistry()

        with pytest.raises(KeyError):
            registry.get("nonexistent_generator")

    def test_disabled_generator(self):
        """Test accessing disabled generator"""
        registry = GeneratorRegistry()
        from generators.text_to_video.sora import SoraGenerator

        registry.register("test_disabled", SoraGenerator, enabled=False)

        with pytest.raises(ValueError, match="disabled"):
            registry.get("test_disabled")


# =====================================================================
# Performance Tests
# =====================================================================

class TestPerformance:
    """Performance and scalability tests"""

    def test_registry_load_time(self):
        """Test registry loads quickly"""
        import time

        start = time.time()
        registry = get_global_registry()
        end = time.time()

        # Should load in under 1 second
        assert (end - start) < 1.0

    def test_routing_performance(self):
        """Test routing is fast"""
        import time

        router = SmartRouter()

        start = time.time()
        for _ in range(100):
            router.route_text_to_video(
                prompt="Test",
                duration=10.0,
                budget=0.0
            )
        end = time.time()

        # 100 routes should complete in under 1 second
        assert (end - start) < 1.0


# =====================================================================
# Run Tests
# =====================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
