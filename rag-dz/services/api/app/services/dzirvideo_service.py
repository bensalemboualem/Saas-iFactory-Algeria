"""
Dzir IA Video - Generation Service
Handles video generation with AI engines
"""
import logging
import asyncio
import os
from typing import Dict, List, Optional
from pathlib import Path
import json

logger = logging.getLogger(__name__)

# Detect mode: api (external APIs), gpu (local GPU), demo (mock)
GENERATION_MODE = os.getenv("DZIRVIDEO_MODE", "api")

# Import engines based on mode
if GENERATION_MODE == "api":
    logger.info("🌐 Using API mode (external services)")
    from .engines.api_providers import (
        get_video_api_provider,
        get_tts_api_provider
    )
elif GENERATION_MODE == "gpu":
    logger.info("🎮 Using GPU mode (local inference)")
    from .engines import (
        get_video_engine,
        get_tts_engine,
        get_compositor
    )
else:
    logger.info("🎭 Using DEMO mode (mock generation)")
    GENERATION_MODE = "demo"

class DzirVideoService:
    """
    Service for generating videos with AI

    Features:
    - Text-to-video generation
    - Arabic/French/Darija TTS
    - Template-based generation
    - Multiple aspect ratios
    """

    def __init__(self):
        self.output_dir = Path("/tmp/dzirvideo")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize engines based on mode
        self.mode = GENERATION_MODE
        self.video_engine = None
        self.tts_engine = None
        self.compositor = None

        if self.mode == "api":
            try:
                self.video_engine = get_video_api_provider("replicate")
                self.tts_engine = get_tts_api_provider("google")
                logger.info("✅ API engines initialized (Replicate + Google TTS)")
            except Exception as e:
                logger.warning(f"Could not initialize API engines: {e}, falling back to DEMO mode")
                self.mode = "demo"

        elif self.mode == "gpu":
            try:
                self.video_engine = get_video_engine("zeroscope")
                self.tts_engine = get_tts_engine()
                self.compositor = get_compositor()
                logger.info("✅ GPU engines initialized (Zeroscope + Coqui TTS)")
            except Exception as e:
                logger.warning(f"Could not initialize GPU engines: {e}, falling back to DEMO mode")
                self.mode = "demo"

        logger.info(f"DzirVideoService initialized in {self.mode.upper()} mode")

    async def generate_video(
        self,
        script: str,
        template: Optional[str] = None,
        language: str = "ar",
        format: str = "16:9",
        duration: int = 30,
        music: Optional[str] = None
    ) -> Dict:
        """
        Generate a video from script

        Args:
            script: Video script/description
            template: Template ID (restaurant, real-estate, etc.)
            language: Voice language (ar, fr, dz)
            format: Aspect ratio (16:9, 9:16, 1:1)
            duration: Video duration in seconds
            music: Background music type

        Returns:
            Dict with video_path, thumbnail_path, duration, etc.
        """
        try:
            logger.info(f"Starting video generation: template={template}, lang={language}, duration={duration}s")

            # Step 1: Parse script and extract scenes
            scenes = await self._parse_script(script, template, duration)
            logger.info(f"Parsed {len(scenes)} scenes from script")

            # Step 2: Generate visuals for each scene
            scene_videos = []
            for i, scene in enumerate(scenes):
                logger.info(f"Generating scene {i+1}/{len(scenes)}: {scene['prompt'][:50]}...")
                scene_video = await self._generate_scene(scene, format)
                scene_videos.append(scene_video)

            # Step 3: Generate voice-over if needed
            audio_path = None
            if language in ["ar", "fr", "dz"]:
                logger.info(f"Generating voice-over in {language}...")
                audio_path = await self._generate_tts(script, language)

            # Step 4: Add background music if requested
            if music and music != "none":
                logger.info(f"Adding background music: {music}")
                music_path = await self._get_background_music(music)
            else:
                music_path = None

            # Step 5: Compose final video
            logger.info("Composing final video...")
            final_video = await self._compose_video(
                scene_videos=scene_videos,
                audio_path=audio_path,
                music_path=music_path,
                format=format,
                duration=duration
            )

            # Step 6: Generate thumbnail
            thumbnail_path = await self._generate_thumbnail(final_video)

            logger.info(f"Video generation completed: {final_video}")

            return {
                "video_path": str(final_video),
                "thumbnail_path": str(thumbnail_path),
                "duration": duration,
                "format": format,
                "language": language,
                "scenes_count": len(scenes)
            }

        except Exception as e:
            logger.error(f"Error generating video: {str(e)}")
            raise

    async def _parse_script(self, script: str, template: Optional[str], duration: int) -> List[Dict]:
        """
        Parse script and break it into scenes

        For MVP, we'll use simple heuristics:
        - Split by sentences
        - Allocate time evenly
        - Use template to guide scene types
        """
        # Simulate async processing
        await asyncio.sleep(0.1)

        # Simple sentence split
        sentences = [s.strip() for s in script.replace('\n', '. ').split('.') if s.strip()]

        # If template is provided, use it to structure scenes
        if template:
            template_scenes = self._get_template_scenes(template)
            num_scenes = min(len(template_scenes), max(3, duration // 10))
        else:
            num_scenes = max(3, min(len(sentences), duration // 10))

        # Allocate time per scene
        time_per_scene = duration / num_scenes

        scenes = []
        for i in range(num_scenes):
            if template and i < len(template_scenes):
                scene_type = template_scenes[i]
            else:
                scene_type = "generic"

            # Get relevant text for this scene
            if i < len(sentences):
                text = sentences[i]
            else:
                text = script[:100] if i == 0 else ""

            scenes.append({
                "scene_number": i + 1,
                "scene_type": scene_type,
                "text": text,
                "prompt": self._enhance_prompt_for_algeria(text, scene_type),
                "duration": time_per_scene
            })

        return scenes

    def _get_template_scenes(self, template: str) -> List[str]:
        """Get scene types for a template"""
        templates_map = {
            "restaurant": ["exterior", "interior", "dishes", "customers"],
            "real-estate": ["exterior", "living-room", "kitchen", "bedroom"],
            "ecommerce": ["product-showcase", "features", "benefits", "cta"],
            "education": ["intro", "content", "demo", "call-to-action"],
            "healthcare": ["facility", "staff", "services", "contact"],
            "tourism": ["destination", "activities", "accommodation", "booking"],
            "automotive": ["exterior-view", "interior-view", "features", "contact"],
            "beauty": ["salon", "services", "before-after", "booking"],
            "construction": ["project-overview", "progress", "team", "results"],
            "tech": ["problem", "solution", "features", "demo"]
        }
        return templates_map.get(template, ["intro", "content", "demo", "outro"])

    def _enhance_prompt_for_algeria(self, text: str, scene_type: str) -> str:
        """
        Enhance prompt with Algerian context
        """
        # Add Algerian cultural context
        algerian_elements = [
            "Algerian style architecture",
            "North African aesthetic",
            "Mediterranean atmosphere",
            "modern Algeria",
            "Algiers cityscape"
        ]

        # Combine text with scene type and Algerian context
        prompt = f"{text}. {scene_type} scene, {algerian_elements[0]}, professional cinematography, high quality"
        return prompt

    async def _generate_scene(self, scene: Dict, format: str) -> str:
        """
        Generate video for a single scene
        """
        scene_path = self.output_dir / f"scene_{scene['scene_number']}.mp4"

        if self.mode == "demo":
            # Demo mode: create placeholder
            await asyncio.sleep(0.5)
            logger.info(f"Scene {scene['scene_number']} generated (DEMO): {scene_path}")
            # Create empty file for demo
            scene_path.touch()
            return str(scene_path)

        elif self.mode == "api":
            # API mode: use Replicate
            try:
                logger.info(f"Generating scene via Replicate API: {scene['prompt'][:50]}...")
                video_path = self.video_engine.generate_video(
                    prompt=scene['prompt'],
                    duration=scene['duration'],
                    fps=8,
                    output_path=scene_path
                )
                logger.info(f"✅ Scene {scene['scene_number']} generated via API: {video_path}")
                return str(video_path)
            except Exception as e:
                logger.error(f"API generation failed: {e}, using placeholder")
                scene_path.touch()
                return str(scene_path)

        elif self.mode == "gpu":
            # GPU mode: use local Zeroscope
            try:
                logger.info(f"Generating scene via GPU: {scene['prompt'][:50]}...")
                video_path = self.video_engine.generate_video(
                    prompt=scene['prompt'],
                    num_frames=int(scene['duration'] * 8),
                    fps=8,
                    output_path=scene_path
                )
                logger.info(f"✅ Scene {scene['scene_number']} generated via GPU: {video_path}")
                return str(video_path)
            except Exception as e:
                logger.error(f"GPU generation failed: {e}")
                raise

    async def _generate_tts(self, text: str, language: str) -> str:
        """
        Generate text-to-speech audio
        """
        audio_path = self.output_dir / f"voiceover_{language}.wav"

        if self.mode == "demo":
            # Demo mode: create placeholder
            await asyncio.sleep(0.3)
            logger.info(f"TTS generated (DEMO): {audio_path}")
            audio_path.touch()
            return str(audio_path)

        elif self.mode == "api":
            # API mode: use Google Cloud TTS
            try:
                logger.info(f"Generating TTS via Google Cloud ({language}): {text[:50]}...")
                tts_path = self.tts_engine.synthesize(
                    text=text,
                    language=language,
                    output_path=audio_path
                )
                logger.info(f"✅ TTS generated via API: {tts_path}")
                return str(tts_path)
            except Exception as e:
                logger.error(f"API TTS failed: {e}, using placeholder")
                audio_path.touch()
                return str(audio_path)

        elif self.mode == "gpu":
            # GPU mode: use local Coqui TTS
            try:
                logger.info(f"Generating TTS via GPU ({language}): {text[:50]}...")
                tts_path = self.tts_engine.synthesize(
                    text=text,
                    language=language,
                    output_path=audio_path
                )
                logger.info(f"✅ TTS generated via GPU: {tts_path}")
                return str(tts_path)
            except Exception as e:
                logger.error(f"GPU TTS failed: {e}")
                raise

    async def _get_background_music(self, music_type: str) -> str:
        """
        Get background music file

        TODO: Implement music library
        For MVP, this returns a placeholder path
        """
        await asyncio.sleep(0.1)

        music_path = self.output_dir / f"music_{music_type}.mp3"
        logger.info(f"Background music (placeholder): {music_path}")

        return str(music_path)

    async def _compose_video(
        self,
        scene_videos: List[str],
        audio_path: Optional[str],
        music_path: Optional[str],
        format: str,
        duration: int
    ) -> Path:
        """
        Compose final video from scenes, audio, and music

        TODO: Implement MoviePy composition
        For MVP, this returns a placeholder path
        """
        await asyncio.sleep(1.0)  # Simulate processing

        # TODO: Use MoviePy to compose video
        # - Concatenate scene videos
        # - Add voice-over
        # - Mix with background music
        # - Adjust aspect ratio
        # - Export final video

        output_path = self.output_dir / f"final_video_{format.replace(':', 'x')}.mp4"
        logger.info(f"Video composed (placeholder): {output_path}")

        return output_path

    async def _generate_thumbnail(self, video_path: Path) -> Path:
        """
        Generate thumbnail from video

        TODO: Extract frame from video
        For MVP, this returns a placeholder path
        """
        await asyncio.sleep(0.2)

        thumbnail_path = video_path.parent / f"{video_path.stem}_thumb.jpg"
        logger.info(f"Thumbnail generated (placeholder): {thumbnail_path}")

        return thumbnail_path


# Singleton instance
_service_instance = None

def get_dzirvideo_service() -> DzirVideoService:
    """Get or create DzirVideoService singleton"""
    global _service_instance
    if _service_instance is None:
        _service_instance = DzirVideoService()
    return _service_instance
