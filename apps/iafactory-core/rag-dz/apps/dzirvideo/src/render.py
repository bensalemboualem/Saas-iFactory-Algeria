"""
DzirVideo - Video Rendering Module
Uses FFmpeg to create vertical videos (9:16) with audio and subtitles
"""

import ffmpeg
import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)


class VideoRenderer:
    """Render videos using FFmpeg"""

    def __init__(
        self,
        width: int = 1080,
        height: int = 1920,
        fps: int = 30,
        background_color: str = "#0f172a"
    ):
        """
        Initialize video renderer

        Args:
            width: Video width in pixels (default: 1080 for 9:16)
            height: Video height in pixels (default: 1920 for 9:16)
            fps: Frames per second (default: 30)
            background_color: Background color hex (default: dark blue)
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.background_color = background_color

    def create_background(self, duration: float, output_path: str | Path) -> str:
        """
        Create a solid color or gradient background video

        Args:
            duration: Video duration in seconds
            output_path: Path to save background video

        Returns:
            str: Path to generated background video
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Create gradient background image
        bg_image_path = output_path.parent / "bg_temp.png"
        self._create_gradient_image(bg_image_path)

        # Generate video from image
        logger.info(f"Creating background video ({duration}s)")

        stream = (
            ffmpeg
            .input(str(bg_image_path), loop=1, t=duration, framerate=self.fps)
            .output(
                str(output_path),
                vcodec='libx264',
                pix_fmt='yuv420p',
                **{'b:v': '2M'}
            )
            .overwrite_output()
        )

        stream.run(quiet=True)

        # Clean up temp image
        if bg_image_path.exists():
            bg_image_path.unlink()

        logger.info(f"Background created: {output_path}")
        return str(output_path)

    def _create_gradient_image(self, output_path: Path):
        """Create a gradient background image"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)

        # Parse hex color
        color_hex = self.background_color.lstrip('#')
        r = int(color_hex[0:2], 16)
        g = int(color_hex[2:4], 16)
        b = int(color_hex[4:6], 16)

        # Create vertical gradient (darker at top, lighter at bottom)
        for y in range(self.height):
            # Gradient from base color to slightly lighter
            factor = y / self.height
            new_r = min(255, int(r + (50 * factor)))
            new_g = min(255, int(g + (50 * factor)))
            new_b = min(255, int(b + (80 * factor)))

            draw.line([(0, y), (self.width, y)], fill=(new_r, new_g, new_b))

        img.save(output_path)

    def render_video(
        self,
        audio_path: str | Path,
        subtitle_path: str | Path,
        output_path: str | Path,
        subtitle_style: str,
        title: str | None = None
    ) -> str:
        """
        Render final video with audio and subtitles

        Args:
            audio_path: Path to audio file (MP3)
            subtitle_path: Path to subtitle file (SRT)
            output_path: Path to save final video
            subtitle_style: ASS style string for subtitles
            title: Optional title text to overlay

        Returns:
            str: Path to rendered video
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        audio_path = Path(audio_path)
        subtitle_path = Path(subtitle_path)

        # Get audio duration
        probe = ffmpeg.probe(str(audio_path))
        duration = float(probe['format']['duration'])

        # Create background video
        bg_path = output_path.parent / "bg_temp.mp4"
        self.create_background(duration, bg_path)

        logger.info("Rendering final video with audio and subtitles...")

        # Build FFmpeg command
        video = ffmpeg.input(str(bg_path))
        audio = ffmpeg.input(str(audio_path))

        # Burn subtitles into video
        video = video.filter(
            'subtitles',
            str(subtitle_path),
            force_style=subtitle_style
        )

        # Combine video and audio
        stream = ffmpeg.output(
            video,
            audio,
            str(output_path),
            vcodec='libx264',
            acodec='aac',
            **{
                'b:v': '4M',
                'b:a': '192k',
                'preset': 'medium',
                'pix_fmt': 'yuv420p'
            }
        ).overwrite_output()

        # Run FFmpeg
        stream.run(quiet=False, capture_stdout=True, capture_stderr=True)

        # Clean up temp background
        if bg_path.exists():
            bg_path.unlink()

        logger.info(f"Video rendered: {output_path} ({duration:.2f}s)")
        return str(output_path)


if __name__ == "__main__":
    # Test video rendering (requires audio and subtitle files)
    logging.basicConfig(level=logging.INFO)

    renderer = VideoRenderer()

    # Example: create background only
    bg_path = renderer.create_background(
        duration=5.0,
        output_path="./output/videos/test_bg.mp4"
    )
    print(f"Background created: {bg_path}")
