"""
Pipeline v2 - Multi-Generator Integration for YouTube Shorts
Integrates 40 AI generators into complete video production pipeline
"""

import os
import asyncio
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path

from generators.registry import get_global_registry
from generators.router import SmartRouter, RoutingCriteria
from generators.base import GenerationRequest, GeneratorCategory

logger = logging.getLogger(__name__)


@dataclass
class SceneConfig:
    """Configuration for a single scene"""
    prompt: str
    duration_seconds: float
    visual_style: Optional[str] = None
    transition: str = "fade"  # fade, cut, dissolve


@dataclass
class PipelineConfig:
    """Complete pipeline configuration"""
    script_text: str
    title: str
    description: str = ""
    tags: List[str] = None

    # Generator selection
    use_ai_video: bool = True
    generator_name: Optional[str] = None  # None = auto-select
    max_budget_usd: float = 0.0  # 0 = free only

    # Video settings
    aspect_ratio: str = "9:16"  # Vertical for Shorts
    resolution: str = "1080p"
    fps: int = 30

    # Audio settings
    voice: str = "default"
    tts_engine: str = "coqui"  # coqui, elevenlabs, etc.

    # Publishing
    publish: bool = False
    privacy_status: str = "public"


class PipelineV2:
    """
    Enhanced pipeline with multi-generator AI video support

    Workflow:
    1. Script analysis & scene splitting
    2. TTS generation (audio)
    3. Subtitle generation
    4. AI video generation (clips per scene) OR static background
    5. Clip assembly (FFmpeg)
    6. Final rendering
    7. YouTube upload
    """

    def __init__(self):
        self.registry = get_global_registry()
        self.router = SmartRouter(self.registry)
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

    async def run_full_pipeline(self, config: PipelineConfig) -> Dict:
        """
        Run complete video generation pipeline

        Args:
            config: Pipeline configuration

        Returns:
            Dictionary with video_path, upload_url, etc.
        """
        logger.info(f"Starting Pipeline v2 for: {config.title}")

        try:
            # Step 1: Generate audio (TTS)
            logger.info("Step 1/7: Generating audio...")
            audio_path, total_duration = await self._generate_audio(
                config.script_text,
                config.voice,
                config.tts_engine
            )

            # Step 2: Generate subtitles
            logger.info("Step 2/7: Generating subtitles...")
            subtitle_path = await self._generate_subtitles(
                config.script_text,
                total_duration
            )

            # Step 3: Analyze script & split into scenes
            logger.info("Step 3/7: Analyzing script...")
            scenes = await self._split_into_scenes(
                config.script_text,
                total_duration
            )

            # Step 4: Generate video clips
            logger.info(f"Step 4/7: Generating video clips...")
            if config.use_ai_video:
                # NEW: Use AI generators
                video_clips = await self._generate_ai_clips(
                    scenes,
                    config
                )
            else:
                # OLD: Static background
                video_clips = [await self._create_static_background(total_duration, config)]

            # Step 5: Assemble clips with audio and subtitles
            logger.info("Step 5/7: Assembling final video...")
            final_video = await self._assemble_final_video(
                video_clips,
                audio_path,
                subtitle_path,
                config
            )

            # Step 6: Post-processing (optional effects)
            logger.info("Step 6/7: Post-processing...")
            final_video = await self._post_process(final_video, config)

            # Step 7: Upload to YouTube
            upload_result = None
            if config.publish:
                logger.info("Step 7/7: Uploading to YouTube...")
                upload_result = await self._upload_to_youtube(
                    final_video,
                    config.title,
                    config.description,
                    config.tags,
                    config.privacy_status
                )

            logger.info("✅ Pipeline completed successfully!")

            return {
                "success": True,
                "video_path": str(final_video),
                "audio_path": str(audio_path),
                "subtitle_path": str(subtitle_path),
                "duration_seconds": total_duration,
                "scenes_count": len(scenes),
                "upload_result": upload_result,
                "clips_generated": len(video_clips)
            }

        except Exception as e:
            logger.error(f"Pipeline error: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _generate_audio(
        self,
        text: str,
        voice: str,
        engine: str
    ) -> tuple[Path, float]:
        """
        Generate audio from text using TTS

        Returns:
            Tuple of (audio_path, duration)
        """
        # Import TTS generator (existing)
        from tts.generator import TTSGenerator

        tts = TTSGenerator(engine=engine)
        audio_path = self.output_dir / "audio.wav"

        duration = await tts.generate(text, str(audio_path), voice=voice)

        return audio_path, duration

    async def _generate_subtitles(
        self,
        text: str,
        duration: float
    ) -> Path:
        """Generate subtitle file (SRT format)"""
        from subtitles.generator import SubtitleGenerator

        sub_gen = SubtitleGenerator()
        subtitle_path = self.output_dir / "subtitles.srt"

        await sub_gen.generate(text, duration, str(subtitle_path))

        return subtitle_path

    async def _split_into_scenes(
        self,
        script: str,
        total_duration: float
    ) -> List[SceneConfig]:
        """
        Split script into scenes for AI generation

        Uses AI (Qwen Optimizer) to analyze script and create scenes
        """
        from ai_assistant.qwen_optimizer import QwenOptimizer

        optimizer = QwenOptimizer(api_key=os.getenv("ALIBABA_DASHSCOPE_API_KEY"))

        # Ask Qwen to split into scenes
        scene_analysis = await optimizer.analyze_scenes(script, total_duration)

        # Convert to SceneConfig objects
        scenes = []
        for i, scene_data in enumerate(scene_analysis):
            scenes.append(SceneConfig(
                prompt=scene_data["visual_prompt"],
                duration_seconds=scene_data["duration"],
                visual_style=scene_data.get("style"),
                transition=scene_data.get("transition", "fade")
            ))

        logger.info(f"Script split into {len(scenes)} scenes")

        return scenes

    async def _generate_ai_clips(
        self,
        scenes: List[SceneConfig],
        config: PipelineConfig
    ) -> List[Path]:
        """
        Generate AI video clips for each scene

        Uses SmartRouter to select optimal generator
        """
        # Select generator (once for all scenes)
        if config.generator_name:
            generator_name = config.generator_name
            logger.info(f"Using specified generator: {generator_name}")
        else:
            # Auto-select using SmartRouter
            criteria = RoutingCriteria(
                category=GeneratorCategory.TEXT_TO_VIDEO,
                max_cost_usd=config.max_budget_usd,
                free_only=(config.max_budget_usd == 0),
                quality_priority=True,
                required_aspect_ratio=config.aspect_ratio
            )

            # Use first scene for routing decision
            sample_request = GenerationRequest(
                prompt=scenes[0].prompt,
                category=GeneratorCategory.TEXT_TO_VIDEO,
                duration_seconds=scenes[0].duration_seconds,
                aspect_ratio=config.aspect_ratio
            )

            generator_name = self.router.route(sample_request, criteria)
            logger.info(f"Auto-selected generator: {generator_name}")

        # Get generator instance
        generator = self.registry.get(generator_name)

        # Generate clips in parallel
        logger.info(f"Generating {len(scenes)} clips with {generator_name}...")

        tasks = []
        for i, scene in enumerate(scenes):
            request = GenerationRequest(
                prompt=scene.prompt,
                category=GeneratorCategory.TEXT_TO_VIDEO,
                duration_seconds=scene.duration_seconds,
                aspect_ratio=config.aspect_ratio,
                style=scene.visual_style
            )
            tasks.append(self._generate_single_clip(generator, request, i))

        clips = await asyncio.gather(*tasks)

        logger.info(f"All {len(clips)} clips generated successfully")

        return clips

    async def _generate_single_clip(
        self,
        generator,
        request: GenerationRequest,
        clip_index: int
    ) -> Path:
        """Generate a single clip and download it"""
        # Generate
        result = await generator.generate(request)

        # Poll for completion
        max_attempts = 60  # 5 minutes
        for attempt in range(max_attempts):
            status = await generator.check_status(result.task_id)

            if status.status.value == "completed":
                # Download clip
                clip_path = self.output_dir / f"clip_{clip_index:03d}.mp4"
                await self._download_clip(status.output_url, clip_path)
                return clip_path

            elif status.status.value == "failed":
                raise Exception(f"Clip {clip_index} generation failed: {status.error_message}")

            await asyncio.sleep(5)  # Wait 5s between polls

        raise Exception(f"Clip {clip_index} generation timeout")

    async def _download_clip(self, url: str, output_path: Path):
        """Download generated clip from URL"""
        import aiohttp

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.read()
                output_path.write_bytes(content)

    async def _create_static_background(
        self,
        duration: float,
        config: PipelineConfig
    ) -> Path:
        """Create static background video (fallback)"""
        import subprocess

        bg_path = self.output_dir / "background.mp4"

        # Create solid color background with FFmpeg
        cmd = [
            "ffmpeg",
            "-f", "lavfi",
            "-i", f"color=c=black:s=1080x1920:d={duration}",
            "-r", str(config.fps),
            "-pix_fmt", "yuv420p",
            "-y",
            str(bg_path)
        ]

        subprocess.run(cmd, check=True)

        return bg_path

    async def _assemble_final_video(
        self,
        video_clips: List[Path],
        audio_path: Path,
        subtitle_path: Path,
        config: PipelineConfig
    ) -> Path:
        """
        Assemble clips, audio, and subtitles into final video

        Uses FFmpeg for clip concatenation and overlay
        """
        import subprocess

        final_path = self.output_dir / "final_video.mp4"

        if len(video_clips) == 1:
            # Single clip - just overlay subtitles and audio
            cmd = [
                "ffmpeg",
                "-i", str(video_clips[0]),
                "-i", str(audio_path),
                "-vf", f"subtitles={subtitle_path}",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "192k",
                "-y",
                str(final_path)
            ]
        else:
            # Multiple clips - concatenate first
            concat_list = self.output_dir / "concat_list.txt"
            concat_list.write_text("\n".join([f"file '{clip}'" for clip in video_clips]))

            concat_path = self.output_dir / "concatenated.mp4"

            # Step 1: Concatenate clips
            subprocess.run([
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_list),
                "-c", "copy",
                "-y",
                str(concat_path)
            ], check=True)

            # Step 2: Add audio and subtitles
            cmd = [
                "ffmpeg",
                "-i", str(concat_path),
                "-i", str(audio_path),
                "-vf", f"subtitles={subtitle_path}",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "192k",
                "-y",
                str(final_path)
            ]

        subprocess.run(cmd, check=True)

        logger.info(f"Final video assembled: {final_path}")

        return final_path

    async def _post_process(self, video_path: Path, config: PipelineConfig) -> Path:
        """Optional post-processing (effects, filters, etc.)"""
        # For now, just return as-is
        # Could add: color grading, stabilization, noise reduction, etc.
        return video_path

    async def _upload_to_youtube(
        self,
        video_path: Path,
        title: str,
        description: str,
        tags: List[str],
        privacy_status: str
    ) -> Dict:
        """Upload video to YouTube"""
        from youtube.uploader import YouTubeUploader

        uploader = YouTubeUploader()

        result = await uploader.upload(
            video_path=str(video_path),
            title=title,
            description=description,
            tags=tags or [],
            privacy_status=privacy_status,
            category_id="22"  # People & Blogs
        )

        logger.info(f"Uploaded to YouTube: {result.get('url')}")

        return result


# =====================================================================
# Convenience Functions
# =====================================================================

async def create_youtube_short(
    script: str,
    title: str,
    generator: Optional[str] = None,
    budget: float = 0.0,
    publish: bool = False
) -> Dict:
    """
    Convenience function to create YouTube Short

    Args:
        script: Video script text
        title: Video title
        generator: Generator name (None = auto-select)
        budget: Maximum budget USD (0 = free only)
        publish: Whether to publish to YouTube

    Returns:
        Result dictionary
    """
    pipeline = PipelineV2()

    config = PipelineConfig(
        script_text=script,
        title=title,
        use_ai_video=True,
        generator_name=generator,
        max_budget_usd=budget,
        publish=publish
    )

    return await pipeline.run_full_pipeline(config)


async def create_comparison_video(
    script: str,
    generators: List[str],
    title: str
) -> Dict:
    """
    Create comparison video using multiple generators

    Generates same script with multiple generators and creates
    side-by-side comparison video
    """
    pipeline = PipelineV2()

    results = []
    for gen_name in generators:
        config = PipelineConfig(
            script_text=script,
            title=f"{title} - {gen_name}",
            use_ai_video=True,
            generator_name=gen_name,
            publish=False
        )

        result = await pipeline.run_full_pipeline(config)
        results.append(result)

    # TODO: Create side-by-side comparison with FFmpeg

    return {
        "success": True,
        "generators": generators,
        "results": results
    }
