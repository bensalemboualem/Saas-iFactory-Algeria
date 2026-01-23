"""
DzirVideo - Subtitle Generation Module
Creates word-by-word or full-line subtitles with timing
"""

import srt
from pathlib import Path
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class SubtitleGenerator:
    """Generate subtitles with word-by-word or line-by-line timing"""

    def __init__(self, style: str = "word_by_word"):
        """
        Initialize subtitle generator

        Args:
            style: "word_by_word" or "full_lines"
        """
        self.style = style

    def generate_subtitles(
        self,
        text: str,
        duration: float,
        output_path: str | Path,
        words_per_subtitle: int = 1
    ) -> str:
        """
        Generate subtitle file from text

        Args:
            text: Full text to subtitle
            duration: Total audio duration in seconds
            output_path: Path to save .srt file
            words_per_subtitle: Number of words per subtitle (1 for word-by-word)

        Returns:
            str: Path to generated subtitle file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Split text into words
        words = text.split()
        total_words = len(words)

        # Calculate time per word (evenly distributed)
        time_per_word = duration / total_words if total_words > 0 else 0

        # Generate subtitle entries
        subtitles = []

        if self.style == "word_by_word":
            # One word per subtitle
            for i, word in enumerate(words):
                start_time = timedelta(seconds=i * time_per_word)
                end_time = timedelta(seconds=(i + 1) * time_per_word)

                subtitle = srt.Subtitle(
                    index=i + 1,
                    start=start_time,
                    end=end_time,
                    content=word
                )
                subtitles.append(subtitle)

        else:  # full_lines
            # Group words into lines (e.g., 5-8 words per line)
            lines = []
            current_line = []

            for word in words:
                current_line.append(word)
                if len(current_line) >= words_per_subtitle:
                    lines.append(" ".join(current_line))
                    current_line = []

            # Add remaining words
            if current_line:
                lines.append(" ".join(current_line))

            # Generate subtitles for lines
            time_per_line = duration / len(lines) if lines else 0

            for i, line in enumerate(lines):
                start_time = timedelta(seconds=i * time_per_line)
                end_time = timedelta(seconds=(i + 1) * time_per_line)

                subtitle = srt.Subtitle(
                    index=i + 1,
                    start=start_time,
                    end=end_time,
                    content=line
                )
                subtitles.append(subtitle)

        # Write SRT file
        srt_content = srt.compose(subtitles)
        output_path.write_text(srt_content, encoding='utf-8')

        logger.info(f"Subtitles generated: {output_path} ({len(subtitles)} entries)")
        return str(output_path)

    def generate_ass_style(
        self,
        font_size: int = 60,
        font_color: str = "white",
        outline_color: str = "black",
        outline_width: int = 2,
        position: str = "center"
    ) -> str:
        """
        Generate ASS (Advanced SubStation Alpha) style string for FFmpeg

        Args:
            font_size: Font size in pixels
            font_color: Primary font color
            outline_color: Outline color
            outline_width: Outline width in pixels
            position: "center" or "bottom"

        Returns:
            str: ASS style string for FFmpeg
        """
        # Convert color names to ASS format (&HAABBGGRR)
        color_map = {
            "white": "&H00FFFFFF",
            "black": "&H00000000",
            "yellow": "&H0000FFFF",
            "red": "&H000000FF",
            "blue": "&H00FF0000"
        }

        primary_color = color_map.get(font_color.lower(), "&H00FFFFFF")
        outline_color_ass = color_map.get(outline_color.lower(), "&H00000000")

        # Position: Alignment 2 = bottom center, 5 = middle center
        alignment = "5" if position == "center" else "2"

        style = (
            f"FontSize={font_size},"
            f"PrimaryColour={primary_color},"
            f"OutlineColour={outline_color_ass},"
            f"BorderStyle=1,"
            f"Outline={outline_width},"
            f"Shadow=0,"
            f"Alignment={alignment},"
            f"MarginV=80"  # Vertical margin from edge
        )

        return style


if __name__ == "__main__":
    # Test subtitle generation
    logging.basicConfig(level=logging.INFO)

    text = "Bonjour à tous, ceci est un test de génération de sous-titres automatiques."
    duration = 5.0

    gen = SubtitleGenerator(style="word_by_word")
    srt_path = gen.generate_subtitles(
        text=text,
        duration=duration,
        output_path="./output/subtitles/test.srt"
    )

    print(f"Subtitles generated: {srt_path}")
    print(Path(srt_path).read_text(encoding='utf-8'))
