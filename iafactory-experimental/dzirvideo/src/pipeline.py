"""
DzirVideo - Main Pipeline Orchestrator
Coordinates TTS → Subtitles → Rendering → Upload
"""

import logging
from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv

from .tts import TTSGenerator
from .subtitles import SubtitleGenerator
from .render import VideoRenderer
from .upload import YouTubeUploader

logger = logging.getLogger(__name__)
load_dotenv()


class VideoPipeline:
    """Main pipeline orchestrator"""

    def __init__(self, config: dict | None = None):
        """
        Initialize pipeline with configuration

        Args:
            config: Optional configuration dict (uses .env if None)
        """
        self.config = config or self._load_config()

        # Initialize components
        self.tts = TTSGenerator(
            model_name=self.config.get('tts_model', 'tts_models/fr/css10/vits'),
            speed=float(self.config.get('tts_speed', 1.0))
        )

        self.subtitle_gen = SubtitleGenerator(
            style=self.config.get('subtitle_style', 'word_by_word')
        )

        self.renderer = VideoRenderer(
            width=int(self.config.get('video_width', 1080)),
            height=int(self.config.get('video_height', 1920)),
            fps=int(self.config.get('video_fps', 30)),
            background_color=self.config.get('video_background_color', '#0f172a')
        )

        # YouTube uploader (lazy initialization)
        self._uploader = None

    def _load_config(self) -> dict:
        """Load configuration from environment variables"""
        return {
            'tts_model': os.getenv('TTS_MODEL', 'tts_models/fr/css10/vits'),
            'tts_speed': os.getenv('TTS_SPEED', '1.0'),
            'subtitle_style': os.getenv('SUBTITLE_STYLE', 'word_by_word'),
            'subtitle_position': os.getenv('SUBTITLE_POSITION', 'center'),
            'subtitle_font_size': os.getenv('SUBTITLE_FONT_SIZE', '60'),
            'subtitle_font_color': os.getenv('SUBTITLE_FONT_COLOR', 'white'),
            'subtitle_outline_color': os.getenv('SUBTITLE_OUTLINE_COLOR', 'black'),
            'subtitle_outline_width': os.getenv('SUBTITLE_OUTLINE_WIDTH', '2'),
            'video_width': os.getenv('VIDEO_WIDTH', '1080'),
            'video_height': os.getenv('VIDEO_HEIGHT', '1920'),
            'video_fps': os.getenv('VIDEO_FPS', '30'),
            'video_background_color': os.getenv('VIDEO_BACKGROUND_COLOR', '#0f172a'),
            'output_dir': os.getenv('OUTPUT_DIR', './output'),
            'youtube_client_id': os.getenv('YOUTUBE_CLIENT_ID'),
            'youtube_client_secret': os.getenv('YOUTUBE_CLIENT_SECRET'),
            'youtube_refresh_token': os.getenv('YOUTUBE_REFRESH_TOKEN'),
        }

    @property
    def uploader(self) -> YouTubeUploader:
        """Lazy load YouTube uploader"""
        if not self._uploader:
            self._uploader = YouTubeUploader(
                client_id=self.config['youtube_client_id'],
                client_secret=self.config['youtube_client_secret'],
                refresh_token=self.config['youtube_refresh_token']
            )
        return self._uploader

    def generate_video(
        self,
        script_text: str,
        title: str,
        output_name: str | None = None
    ) -> dict:
        """
        Generate video from script text

        Args:
            script_text: Text to convert to video
            title: Video title
            output_name: Optional output filename (auto-generated if None)

        Returns:
            dict: Paths to generated files
        """
        if not output_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"video_{timestamp}"

        output_dir = Path(self.config['output_dir'])
        output_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Starting video generation: {title}")
        logger.info(f"Script: {script_text[:100]}...")

        # Step 1: Generate audio (TTS)
        logger.info("[1/4] Generating audio with TTS...")
        audio_path, duration = self.tts.generate_audio(
            text=script_text,
            output_path=output_dir / "audio" / f"{output_name}.mp3"
        )

        # Step 2: Generate subtitles
        logger.info("[2/4] Generating subtitles...")
        subtitle_path = self.subtitle_gen.generate_subtitles(
            text=script_text,
            duration=duration,
            output_path=output_dir / "subtitles" / f"{output_name}.srt"
        )

        # Get subtitle style
        subtitle_style = self.subtitle_gen.generate_ass_style(
            font_size=int(self.config['subtitle_font_size']),
            font_color=self.config['subtitle_font_color'],
            outline_color=self.config['subtitle_outline_color'],
            outline_width=int(self.config['subtitle_outline_width']),
            position=self.config['subtitle_position']
        )

        # Step 3: Render video
        logger.info("[3/4] Rendering video...")
        video_path = self.renderer.render_video(
            audio_path=audio_path,
            subtitle_path=subtitle_path,
            output_path=output_dir / "videos" / f"{output_name}.mp4",
            subtitle_style=subtitle_style,
            title=title
        )

        logger.info("[4/4] Video generation complete!")

        return {
            'success': True,
            'video_path': video_path,
            'audio_path': audio_path,
            'subtitle_path': subtitle_path,
            'duration': duration,
            'title': title
        }

    def publish_video(
        self,
        video_path: str,
        title: str,
        description: str = "",
        tags: list[str] | None = None,
        privacy_status: str = "public"
    ) -> dict:
        """
        Upload video to YouTube

        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            privacy_status: "public", "private", or "unlisted"

        Returns:
            dict: Upload result with video URL
        """
        logger.info(f"Publishing video to YouTube: {title}")

        result = self.uploader.upload_video(
            video_path=video_path,
            title=title,
            description=description,
            tags=tags,
            privacy_status=privacy_status
        )

        return result

    def run_full_pipeline(
        self,
        script_text: str,
        title: str,
        description: str = "",
        tags: list[str] | None = None,
        publish: bool = True,
        privacy_status: str = "public"
    ) -> dict:
        """
        Run full pipeline: Generate + Publish

        Args:
            script_text: Text script
            title: Video title
            description: Video description
            tags: List of tags
            publish: Whether to publish to YouTube
            privacy_status: YouTube privacy status

        Returns:
            dict: Complete pipeline result
        """
        logger.info("=" * 60)
        logger.info(f"FULL PIPELINE: {title}")
        logger.info("=" * 60)

        # Generate video
        gen_result = self.generate_video(
            script_text=script_text,
            title=title
        )

        if not gen_result['success']:
            return gen_result

        result = {
            **gen_result,
            'published': False,
            'youtube_url': None
        }

        # Publish if requested
        if publish:
            upload_result = self.publish_video(
                video_path=gen_result['video_path'],
                title=title,
                description=description,
                tags=tags,
                privacy_status=privacy_status
            )

            result['published'] = upload_result.get('success', False)
            result['youtube_url'] = upload_result.get('url')
            result['youtube_video_id'] = upload_result.get('video_id')

        logger.info("=" * 60)
        logger.info("PIPELINE COMPLETE")
        logger.info(f"Video: {result['video_path']}")
        if result['published']:
            logger.info(f"YouTube: {result['youtube_url']}")
        logger.info("=" * 60)

        return result


if __name__ == "__main__":
    # Test pipeline
    logging.basicConfig(level=logging.INFO)

    pipeline = VideoPipeline()

    result = pipeline.run_full_pipeline(
        script_text="Bonjour à tous! Aujourd'hui, je vous présente un outil incroyable pour automatiser la création de vidéos YouTube Shorts. C'est simple, rapide, et 100% open-source!",
        title="Test DzirVideo - Automatisation YouTube Shorts",
        description="Vidéo de test générée automatiquement avec DzirVideo",
        tags=["shorts", "automation", "tts", "ai"],
        publish=False  # Set to True to actually upload
    )

    print("\nRésultat:", result)
