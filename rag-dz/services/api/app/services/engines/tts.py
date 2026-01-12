"""
Text-to-Speech Engine for Arabic, French, and Algerian Darija
Professional voice synthesis with Coqui TTS
"""
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Literal
import torch
from TTS.api import TTS
from pydub import AudioSegment
import numpy as np

logger = logging.getLogger(__name__)

LanguageCode = Literal["ar", "fr", "dz", "en"]

class TTSEngine:
    """
    Professional Text-to-Speech for multiple languages

    Supports:
    - Arabic (Modern Standard Arabic)
    - French (France & Maghreb accent)
    - Darija (Algerian dialect - via fine-tuned model)
    - English (fallback)
    """

    def __init__(
        self,
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        self.device = device
        self.models = {}  # Cache for loaded models

        # Model configurations for each language
        self.model_configs = {
            "ar": {
                "model_name": "tts_models/ar/css10/vits",
                "speaker": None,
                "description": "Arabic (Modern Standard)"
            },
            "fr": {
                "model_name": "tts_models/fr/css10/vits",
                "speaker": None,
                "description": "French (Standard)"
            },
            "dz": {
                # For Darija, we use French model with Arabic text
                # Or a fine-tuned model if available
                "model_name": "tts_models/multilingual/multi-dataset/your_tts",
                "speaker": "french_female",
                "description": "Darija Algérienne (Experimental)"
            },
            "en": {
                "model_name": "tts_models/en/ljspeech/tacotron2-DDC",
                "speaker": None,
                "description": "English (Fallback)"
            }
        }

        logger.info(f"TTSEngine initialized on {device}")

    def load_model(self, language: LanguageCode) -> TTS:
        """Load TTS model for specified language"""
        if language in self.models:
            return self.models[language]

        try:
            config = self.model_configs.get(language)
            if not config:
                raise ValueError(f"Unsupported language: {language}")

            logger.info(f"Loading TTS model for {language}: {config['description']}")

            # Initialize TTS model
            tts = TTS(
                model_name=config["model_name"],
                progress_bar=False,
                gpu=(self.device == "cuda")
            )

            self.models[language] = tts
            logger.info(f"Model loaded successfully for {language}")

            return tts

        except Exception as e:
            logger.error(f"Failed to load TTS model for {language}: {str(e)}")
            # Fallback to English
            if language != "en":
                logger.warning(f"Falling back to English TTS")
                return self.load_model("en")
            raise

    def synthesize(
        self,
        text: str,
        language: LanguageCode = "ar",
        output_path: Optional[Path] = None,
        speed: float = 1.0,
        pitch: float = 1.0
    ) -> Path:
        """
        Synthesize speech from text

        Args:
            text: Text to synthesize
            language: Language code (ar, fr, dz, en)
            output_path: Where to save audio
            speed: Speech speed multiplier (0.5-2.0)
            pitch: Pitch adjustment (-12 to +12 semitones)

        Returns:
            Path to generated audio file
        """
        try:
            # Load appropriate model
            tts = self.load_model(language)

            # Generate output path
            if output_path is None:
                output_path = Path("/tmp") / f"tts_{os.urandom(8).hex()}.wav"

            logger.info(f"Synthesizing {len(text)} characters in {language}...")

            # Get speaker if specified in config
            config = self.model_configs[language]
            speaker = config.get("speaker")

            # Synthesize speech
            if speaker:
                tts.tts_to_file(
                    text=text,
                    file_path=str(output_path),
                    speaker=speaker
                )
            else:
                tts.tts_to_file(
                    text=text,
                    file_path=str(output_path)
                )

            # Apply speed and pitch adjustments
            if speed != 1.0 or pitch != 0.0:
                audio = AudioSegment.from_wav(str(output_path))

                # Adjust speed
                if speed != 1.0:
                    audio = audio.speedup(playback_speed=speed)

                # Adjust pitch (requires pydub with ffmpeg)
                if pitch != 0.0:
                    # Convert semitones to frequency ratio
                    freq_ratio = 2 ** (pitch / 12.0)
                    new_sample_rate = int(audio.frame_rate * freq_ratio)
                    audio = audio._spawn(
                        audio.raw_data,
                        overrides={'frame_rate': new_sample_rate}
                    )
                    audio = audio.set_frame_rate(44100)

                # Save modified audio
                audio.export(str(output_path), format="wav")

            logger.info(f"Speech synthesized: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"TTS synthesis failed: {str(e)}")
            raise

    def synthesize_script(
        self,
        script: str,
        language: LanguageCode = "ar",
        scene_timestamps: Optional[list] = None,
        output_path: Optional[Path] = None
    ) -> Dict:
        """
        Synthesize full script with scene markers

        Args:
            script: Full script text
            language: Language code
            scene_timestamps: List of (scene_num, start_time, text) tuples
            output_path: Output audio file path

        Returns:
            Dict with audio_path, duration, scene_timings
        """
        try:
            # If no scene timestamps, treat as single scene
            if not scene_timestamps:
                audio_path = self.synthesize(script, language, output_path)
                audio = AudioSegment.from_wav(str(audio_path))
                return {
                    "audio_path": audio_path,
                    "duration": len(audio) / 1000.0,  # Convert to seconds
                    "scene_timings": [(0, 0.0, len(audio) / 1000.0)]
                }

            # Process each scene
            scene_audios = []
            scene_timings = []
            current_time = 0.0

            for scene_num, scene_text in scene_timestamps:
                # Synthesize scene audio
                scene_path = Path("/tmp") / f"scene_{scene_num}_{os.urandom(4).hex()}.wav"
                audio_path = self.synthesize(scene_text, language, scene_path)

                # Load audio
                audio = AudioSegment.from_wav(str(audio_path))
                scene_audios.append(audio)

                # Track timing
                duration = len(audio) / 1000.0
                scene_timings.append((scene_num, current_time, current_time + duration))
                current_time += duration

            # Concatenate all scene audios
            combined_audio = scene_audios[0]
            for audio in scene_audios[1:]:
                # Add small pause between scenes (200ms)
                combined_audio += AudioSegment.silent(duration=200)
                combined_audio += audio

            # Save combined audio
            if output_path is None:
                output_path = Path("/tmp") / f"voiceover_{os.urandom(8).hex()}.wav"

            combined_audio.export(str(output_path), format="wav")

            logger.info(f"Full script synthesized: {len(scene_audios)} scenes, {len(combined_audio)/1000:.1f}s")

            return {
                "audio_path": output_path,
                "duration": len(combined_audio) / 1000.0,
                "scene_timings": scene_timings
            }

        except Exception as e:
            logger.error(f"Script synthesis failed: {str(e)}")
            raise

    def synthesize_darija(
        self,
        text: str,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Special handling for Algerian Darija

        Since Darija is a mix of Arabic, French, and Berber,
        we use intelligent language detection and switching
        """
        try:
            logger.info("Synthesizing Algerian Darija (experimental)...")

            # Detect language mix in text
            # Simple heuristic: Arabic script vs Latin script
            has_arabic = any('\u0600' <= c <= '\u06FF' for c in text)
            has_latin = any('a' <= c.lower() <= 'z' for c in text)

            if has_arabic and not has_latin:
                # Pure Arabic script - use Arabic TTS
                return self.synthesize(text, "ar", output_path)
            elif has_latin and not has_arabic:
                # Pure Latin script - use French TTS
                return self.synthesize(text, "fr", output_path)
            else:
                # Mixed script - use multilingual model
                # For now, use French model (better for Maghreb accent)
                return self.synthesize(text, "fr", output_path, speed=0.95)

        except Exception as e:
            logger.error(f"Darija synthesis failed: {str(e)}")
            raise


class VoiceCloner:
    """
    Advanced: Voice cloning for custom Algerian voices
    """

    def __init__(self, device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        self.device = device
        self.tts = None

    def load_model(self):
        """Load YourTTS model for voice cloning"""
        if self.tts is not None:
            return

        try:
            logger.info("Loading YourTTS for voice cloning...")

            self.tts = TTS(
                model_name="tts_models/multilingual/multi-dataset/your_tts",
                progress_bar=False,
                gpu=(self.device == "cuda")
            )

            logger.info("Voice cloning model loaded")

        except Exception as e:
            logger.error(f"Failed to load voice cloning model: {str(e)}")
            raise

    def clone_voice(
        self,
        text: str,
        speaker_wav: Path,
        language: str = "fr",
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Clone a voice from reference audio

        Args:
            text: Text to synthesize
            speaker_wav: Reference audio file with target voice
            language: Target language
            output_path: Output audio path
        """
        try:
            self.load_model()

            if output_path is None:
                output_path = Path("/tmp") / f"cloned_{os.urandom(8).hex()}.wav"

            logger.info(f"Cloning voice from {speaker_wav.name}...")

            self.tts.tts_to_file(
                text=text,
                file_path=str(output_path),
                speaker_wav=str(speaker_wav),
                language=language
            )

            logger.info(f"Voice cloned: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Voice cloning failed: {str(e)}")
            raise


# Factory function
def get_tts_engine(**kwargs):
    """Get TTS engine instance"""
    return TTSEngine(**kwargs)


def get_voice_cloner(**kwargs):
    """Get voice cloning engine"""
    return VoiceCloner(**kwargs)
