"""
DzirVideo - Text-to-Speech Module
Uses Coqui TTS for French audio generation
"""

import os
from pathlib import Path
from TTS.api import TTS
from pydub import AudioSegment
import logging

logger = logging.getLogger(__name__)


class TTSGenerator:
    """Generate audio from text using Coqui TTS"""

    def __init__(self, model_name: str = "tts_models/fr/css10/vits", speed: float = 1.0):
        """
        Initialize TTS generator

        Args:
            model_name: TTS model to use (default: French VITS)
            speed: Speech speed multiplier (default: 1.0)
        """
        self.model_name = model_name
        self.speed = speed
        logger.info(f"Loading TTS model: {model_name}")
        self.tts = TTS(model_name)
        logger.info("TTS model loaded successfully")

    def generate_audio(
        self,
        text: str,
        output_path: str | Path,
        speaker: str | None = None
    ) -> tuple[str, float]:
        """
        Generate audio from text

        Args:
            text: Text to convert to speech
            output_path: Path to save audio file
            speaker: Optional speaker name (for multi-speaker models)

        Returns:
            tuple: (audio_path, duration_seconds)
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate audio
        logger.info(f"Generating audio for: {text[:50]}...")

        # TTS generates WAV by default
        temp_path = output_path.with_suffix('.wav')

        if speaker and hasattr(self.tts, 'speakers'):
            self.tts.tts_to_file(text=text, file_path=str(temp_path), speaker=speaker)
        else:
            self.tts.tts_to_file(text=text, file_path=str(temp_path))

        # Load audio and adjust speed if needed
        audio = AudioSegment.from_wav(temp_path)

        if self.speed != 1.0:
            logger.info(f"Adjusting speed to {self.speed}x")
            audio = audio.speedup(playback_speed=self.speed)

        # Export as MP3
        final_path = output_path.with_suffix('.mp3')
        audio.export(str(final_path), format='mp3', bitrate='192k')

        # Clean up temp WAV
        if temp_path.exists() and temp_path != final_path:
            temp_path.unlink()

        duration = len(audio) / 1000.0  # Convert ms to seconds
        logger.info(f"Audio generated: {final_path} ({duration:.2f}s)")

        return str(final_path), duration

    def estimate_duration(self, text: str) -> float:
        """
        Estimate audio duration without generating (rough estimate)

        Args:
            text: Text to estimate

        Returns:
            float: Estimated duration in seconds
        """
        # Average: ~150 words/minute in French = ~2.5 words/second
        words = len(text.split())
        return (words / 2.5) / self.speed


if __name__ == "__main__":
    # Test TTS
    logging.basicConfig(level=logging.INFO)

    tts = TTSGenerator()
    audio_path, duration = tts.generate_audio(
        "Bonjour, ceci est un test de génération audio en français.",
        output_path="./output/audio/test.mp3"
    )

    print(f"Audio généré: {audio_path}")
    print(f"Durée: {duration:.2f}s")
