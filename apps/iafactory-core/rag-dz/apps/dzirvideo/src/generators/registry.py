"""
Generator Registry for Dzir IA Video
Central registry to manage and discover all available AI generators
"""

from typing import Dict, List, Type, Optional
import logging
from .base import BaseGenerator, GeneratorCategory, GeneratorCapabilities

logger = logging.getLogger(__name__)


class GeneratorRegistry:
    """
    Central registry for all AI generators

    Manages registration, discovery, and retrieval of generators.
    Allows querying generators by category, quality, cost, etc.
    """

    def __init__(self):
        """Initialize empty registry"""
        self._generators: Dict[str, Type[BaseGenerator]] = {}
        self._instances: Dict[str, BaseGenerator] = {}  # Cached instances
        self._metadata: Dict[str, Dict] = {}  # Additional metadata

    def register(
        self,
        name: str,
        generator_class: Type[BaseGenerator],
        enabled: bool = True,
        **metadata
    ):
        """
        Register a generator

        Args:
            name: Unique identifier (e.g., "wan_2_1", "kling_ai")
            generator_class: Generator class (subclass of BaseGenerator)
            enabled: Whether generator is enabled
            **metadata: Additional metadata (provider, tags, etc.)
        """
        if not issubclass(generator_class, BaseGenerator):
            raise ValueError(f"{generator_class} must inherit from BaseGenerator")

        if name in self._generators:
            logger.warning(f"Generator '{name}' already registered, overwriting")

        self._generators[name] = generator_class
        self._metadata[name] = {
            "enabled": enabled,
            "provider": metadata.get("provider", "Unknown"),
            "tags": metadata.get("tags", []),
            **metadata
        }

        logger.info(f"Registered generator: {name} ({generator_class.__name__})")

    def unregister(self, name: str):
        """
        Unregister a generator

        Args:
            name: Generator name
        """
        if name in self._generators:
            del self._generators[name]
            if name in self._instances:
                del self._instances[name]
            if name in self._metadata:
                del self._metadata[name]
            logger.info(f"Unregistered generator: {name}")

    def get(
        self,
        name: str,
        api_key: Optional[str] = None,
        **config
    ) -> BaseGenerator:
        """
        Get generator instance by name

        Args:
            name: Generator name
            api_key: API key for the service
            **config: Additional configuration

        Returns:
            Generator instance

        Raises:
            KeyError: If generator not found
        """
        if name not in self._generators:
            raise KeyError(f"Generator '{name}' not registered")

        if not self._metadata[name]["enabled"]:
            raise ValueError(f"Generator '{name}' is disabled")

        # Return cached instance if exists and no new config
        if name in self._instances and not config and not api_key:
            return self._instances[name]

        # Create new instance
        generator_class = self._generators[name]
        instance = generator_class(api_key=api_key, **config)
        self._instances[name] = instance

        return instance

    def list_all(self, enabled_only: bool = True) -> List[str]:
        """
        List all registered generators

        Args:
            enabled_only: Only return enabled generators

        Returns:
            List of generator names
        """
        if enabled_only:
            return [
                name for name, meta in self._metadata.items()
                if meta.get("enabled", True)
            ]
        return list(self._generators.keys())

    def list_by_category(
        self,
        category: GeneratorCategory,
        enabled_only: bool = True
    ) -> List[str]:
        """
        List generators supporting a specific category

        Args:
            category: Generator category
            enabled_only: Only return enabled generators

        Returns:
            List of generator names
        """
        result = []
        for name in self.list_all(enabled_only=enabled_only):
            try:
                generator = self.get(name)
                caps = generator.capabilities

                # Check if supports category
                category_support_map = {
                    GeneratorCategory.TEXT_TO_VIDEO: caps.supports_text_to_video,
                    GeneratorCategory.IMAGE_TO_VIDEO: caps.supports_image_to_video,
                    GeneratorCategory.TEXT_TO_IMAGE: caps.supports_text_to_image,
                    GeneratorCategory.IMAGE_TO_IMAGE: caps.supports_image_to_image,
                    GeneratorCategory.AVATAR_VIDEO: caps.supports_avatar_video,
                    GeneratorCategory.REELS_SHORTFORM: caps.supports_reels_shortform,
                }

                if category_support_map.get(category, False):
                    result.append(name)

            except Exception as e:
                logger.error(f"Error checking generator {name}: {e}")

        return result

    def find_best(
        self,
        category: GeneratorCategory,
        max_cost: Optional[float] = None,
        min_quality: int = 70,
        free_only: bool = False,
        enabled_only: bool = True,
        sort_by: str = "quality"  # quality, cost, speed
    ) -> Optional[str]:
        """
        Find best generator matching criteria

        Args:
            category: Required category
            max_cost: Maximum cost per second/image (None = unlimited)
            min_quality: Minimum quality score (0-100)
            free_only: Only free generators
            enabled_only: Only enabled generators
            sort_by: Sorting criterion (quality, cost, speed)

        Returns:
            Generator name, or None if no match
        """
        candidates = self.list_by_category(category, enabled_only=enabled_only)

        if not candidates:
            return None

        # Filter by criteria
        valid_candidates = []
        for name in candidates:
            try:
                generator = self.get(name)
                caps = generator.capabilities

                # Check free_only
                if free_only and not caps.free_tier:
                    continue

                # Check quality
                if caps.quality_score < min_quality:
                    continue

                # Check cost
                if max_cost is not None:
                    if category in [GeneratorCategory.TEXT_TO_VIDEO, GeneratorCategory.IMAGE_TO_VIDEO]:
                        if caps.api_cost_per_second > max_cost:
                            continue
                    else:
                        if caps.api_cost_per_image > max_cost:
                            continue

                valid_candidates.append((name, caps))

            except Exception as e:
                logger.error(f"Error evaluating generator {name}: {e}")

        if not valid_candidates:
            return None

        # Sort by criterion
        if sort_by == "quality":
            valid_candidates.sort(key=lambda x: x[1].quality_score, reverse=True)
        elif sort_by == "cost":
            if category in [GeneratorCategory.TEXT_TO_VIDEO, GeneratorCategory.IMAGE_TO_VIDEO]:
                valid_candidates.sort(key=lambda x: x[1].api_cost_per_second)
            else:
                valid_candidates.sort(key=lambda x: x[1].api_cost_per_image)
        elif sort_by == "speed":
            valid_candidates.sort(key=lambda x: x[1].avg_generation_time_seconds)

        return valid_candidates[0][0]

    def get_metadata(self, name: str) -> Dict:
        """
        Get metadata for a generator

        Args:
            name: Generator name

        Returns:
            Metadata dictionary
        """
        if name not in self._metadata:
            raise KeyError(f"Generator '{name}' not registered")
        return self._metadata[name].copy()

    def get_capabilities(self, name: str) -> GeneratorCapabilities:
        """
        Get capabilities for a generator

        Args:
            name: Generator name

        Returns:
            GeneratorCapabilities object
        """
        generator = self.get(name)
        return generator.capabilities

    def get_summary(self) -> Dict:
        """
        Get summary statistics of registry

        Returns:
            Dictionary with counts by category
        """
        summary = {
            "total_generators": len(self._generators),
            "enabled_generators": len(self.list_all(enabled_only=True)),
            "by_category": {},
            "free_generators": 0,
            "premium_generators": 0,
        }

        for category in GeneratorCategory:
            summary["by_category"][category.value] = len(
                self.list_by_category(category, enabled_only=True)
            )

        for name in self.list_all(enabled_only=True):
            try:
                generator = self.get(name)
                if generator.capabilities.free_tier:
                    summary["free_generators"] += 1
                else:
                    summary["premium_generators"] += 1
            except:
                pass

        return summary


# Global registry instance
_global_registry: Optional[GeneratorRegistry] = None


def get_global_registry() -> GeneratorRegistry:
    """
    Get or create global registry instance

    Returns:
        GeneratorRegistry singleton
    """
    global _global_registry
    if _global_registry is None:
        _global_registry = GeneratorRegistry()
        _load_default_generators()
    return _global_registry


def _load_default_generators():
    """
    Load default generators into global registry

    Called automatically when global registry is first created.
    Registers all 31 implemented AI generators.
    """
    registry = get_global_registry()

    # =================================================================
    # TEXT-TO-VIDEO GENERATORS (12)
    # =================================================================

    # Free/Freemium Text-to-Video
    from .text_to_video import (
        WAN21Generator,
        KlingAIGenerator,
        PikaLabsGenerator,
        LumaDreamGenerator,
        HailuoAIGenerator,
    )

    registry.register("wan_2_1", WAN21Generator,
                     provider="Alibaba Cloud", tags=["free", "text-to-video"])
    registry.register("kling_ai", KlingAIGenerator,
                     provider="Kuaishou", tags=["freemium", "text-to-video", "high-quality"])
    registry.register("pika_labs", PikaLabsGenerator,
                     provider="Pika", tags=["freemium", "text-to-video", "creative"])
    registry.register("luma_dream", LumaDreamGenerator,
                     provider="Luma AI", tags=["freemium", "text-to-video", "cinematic"])
    registry.register("hailuo_ai", HailuoAIGenerator,
                     provider="Minimax", tags=["freemium", "text-to-video", "cheap"])

    # Premium Text-to-Video
    from .text_to_video import (
        RunwayGen4Generator,
        Veo2Generator,
        SoraGenerator,
        LTXStudioGenerator,
    )

    registry.register("runway_gen4", RunwayGen4Generator,
                     provider="Runway ML", tags=["premium", "text-to-video", "sota"])
    registry.register("veo_2", Veo2Generator,
                     provider="Google DeepMind", tags=["premium", "text-to-video"])
    registry.register("sora", SoraGenerator,
                     provider="OpenAI", tags=["premium", "text-to-video"], enabled=False)
    registry.register("ltx_studio", LTXStudioGenerator,
                     provider="LTX", tags=["premium", "text-to-video", "film"])

    # Open Source Text-to-Video
    from .text_to_video import (
        CogVideoGenerator,
        OpenSoraGenerator,
        StarryAIVideoGenerator,
    )

    registry.register("cogvideo", CogVideoGenerator,
                     provider="Zhipu AI", tags=["open-source", "text-to-video"])
    registry.register("open_sora", OpenSoraGenerator,
                     provider="Community", tags=["open-source", "text-to-video"])
    registry.register("starryai_video", StarryAIVideoGenerator,
                     provider="StarryAI", tags=["freemium", "text-to-video"])

    # =================================================================
    # TEXT-TO-IMAGE GENERATORS (6)
    # =================================================================

    from .text_to_image import (
        QwenVLGenerator,
        FLUX1Generator,
        DALLE3Generator,
        MidjourneyGenerator,
        IdeogramGenerator,
        LeonardoAIGenerator,
    )

    # Free/Freemium
    registry.register("qwen_vl", QwenVLGenerator,
                     provider="Alibaba Cloud", tags=["free", "text-to-image"])
    registry.register("flux_1", FLUX1Generator,
                     provider="Black Forest Labs", tags=["free", "text-to-image", "fast"])
    registry.register("ideogram", IdeogramGenerator,
                     provider="Ideogram", tags=["freemium", "text-to-image", "text-rendering"])
    registry.register("leonardo_ai", LeonardoAIGenerator,
                     provider="Leonardo", tags=["freemium", "text-to-image", "artistic"])

    # Premium
    registry.register("dall_e_3", DALLE3Generator,
                     provider="OpenAI", tags=["premium", "text-to-image"])
    registry.register("midjourney", MidjourneyGenerator,
                     provider="Midjourney", tags=["premium", "text-to-image", "artistic"])

    # =================================================================
    # IMAGE-TO-VIDEO GENERATORS (1)
    # =================================================================

    from .image_to_video import StableVideoDiffusionGenerator

    registry.register("stable_video_diffusion", StableVideoDiffusionGenerator,
                     provider="Stability AI", tags=["free", "image-to-video", "open-source"])

    # =================================================================
    # AVATAR/TALKING HEAD GENERATORS (5)
    # =================================================================

    from .avatar_video import (
        VidnozGenerator,
        DeepBrainAIGenerator,
        ElaiIOGenerator,
        HeyGenGenerator,
        SynthesiaGenerator,
    )

    registry.register("vidnoz", VidnozGenerator,
                     provider="Vidnoz", tags=["freemium", "avatar", "talking-head"])
    registry.register("deepbrain_ai", DeepBrainAIGenerator,
                     provider="DeepBrain", tags=["premium", "avatar", "high-quality"])
    registry.register("elai_io", ElaiIOGenerator,
                     provider="Elai", tags=["freemium", "avatar"])
    registry.register("heygen", HeyGenGenerator,
                     provider="HeyGen", tags=["premium", "avatar", "enterprise"])
    registry.register("synthesia", SynthesiaGenerator,
                     provider="Synthesia", tags=["premium", "avatar", "corporate"])

    # =================================================================
    # REELS/SHORT-FORM GENERATORS (6)
    # =================================================================

    from .reels_shortform import (
        DIGENSoraGenerator,
        PictoryGenerator,
        CapCutGenerator,
        Lumen5Generator,
        DescriptGenerator,
        InVideoAIGenerator,
    )

    registry.register("digen_sora", DIGENSoraGenerator,
                     provider="DIGEN", tags=["free", "reels", "shorts", "unlimited"])
    registry.register("pictory", PictoryGenerator,
                     provider="Pictory.ai", tags=["freemium", "reels", "article-to-video"])
    registry.register("capcut", CapCutGenerator,
                     provider="ByteDance", tags=["free", "reels", "tiktok", "editing"])
    registry.register("lumen5", Lumen5Generator,
                     provider="Lumen5", tags=["freemium", "reels", "blog-to-video"])
    registry.register("descript", DescriptGenerator,
                     provider="Descript", tags=["freemium", "reels", "editing"])
    registry.register("invideo_ai", InVideoAIGenerator,
                     provider="InVideo", tags=["freemium", "reels", "marketing"])
    registry.register("canva_ai", CanvaAIGenerator,
                     provider="Canva", tags=["freemium", "reels", "design", "templates"])

    # =================================================================
    # NEW GENERATORS (9) - Phase 5.1
    # =================================================================

    # Additional Text-to-Video (5)
    from .text_to_video import (
        HunyuanVideoGenerator,
        Mochi1Generator,
        ViduAIGenerator,
        PolloAIGenerator,
        KreaVideoGenerator,
    )

    registry.register("hunyuan_video", HunyuanVideoGenerator,
                     provider="Tencent", tags=["open-source", "text-to-video"])
    registry.register("mochi_1", Mochi1Generator,
                     provider="Genmo AI", tags=["open-source", "text-to-video"])
    registry.register("vidu_ai", ViduAIGenerator,
                     provider="Tencent", tags=["freemium", "text-to-video"])
    registry.register("pollo_ai", PolloAIGenerator,
                     provider="Pollo Labs", tags=["freemium", "text-to-video", "fast"])
    registry.register("krea_video", KreaVideoGenerator,
                     provider="Krea", tags=["freemium", "text-to-video", "creative"])

    # NEW: 3 additional text-to-video generators
    from .text_to_video import (
        Hailuo23Generator,
        NanoGenerator,
        BananProGenerator,
    )

    registry.register("hailuo_2_3", Hailuo23Generator,
                     provider="MiniMax", tags=["freemium", "text-to-video", "upgraded"])
    registry.register("nano", NanoGenerator,
                     provider="Nano AI", tags=["freemium", "text-to-video", "fastest"])
    registry.register("banan_pro", BananProGenerator,
                     provider="Banan Pro", tags=["premium", "text-to-video", "professional", "4k"])

    # Additional Text-to-Image (3)
    from .text_to_image import (
        AdobeFireflyGenerator,
        PlaygroundV2Generator,
        StableDiffusion35Generator,
    )

    registry.register("adobe_firefly", AdobeFireflyGenerator,
                     provider="Adobe", tags=["premium", "text-to-image", "professional"])
    registry.register("playground_v2", PlaygroundV2Generator,
                     provider="PlaygroundAI", tags=["freemium", "text-to-image", "control"])
    registry.register("stable_diffusion_35", StableDiffusion35Generator,
                     provider="Stability AI", tags=["premium", "text-to-image", "latest"])

    # Additional Reels (1)
    from .reels_shortform import CanvaAIGenerator

    registry.register("canva_ai", CanvaAIGenerator,
                     provider="Canva", tags=["freemium", "reels", "templates"])

    logger.info(f"Loaded 43 default generators into registry (40 original + 3 new)")
