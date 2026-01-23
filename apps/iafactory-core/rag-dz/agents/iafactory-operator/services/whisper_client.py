"""
IA Factory Operator - Whisper Client
Audio transcription using OpenAI Whisper
"""

import os
import tempfile
import subprocess
from typing import Dict, Any, Optional, List
from pathlib import Path

import structlog

from core.config import settings

logger = structlog.get_logger(__name__)


class WhisperClient:
    """
    Audio transcription client using Whisper.
    Supports:
    - OpenAI Whisper API (cloud)
    - Local Whisper model (faster-whisper)
    """
    
    def __init__(
        self,
        openai_key: Optional[str] = None,
        use_local: bool = False,
        local_model: str = "base",
    ):
        self.openai_key = openai_key or settings.openai_api_key
        self.use_local = use_local or False
        self.local_model = local_model
        
        self._local_model = None
    
    async def transcribe(
        self,
        video_path: str,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Transcribe audio from video file.
        Returns dict with 'text' and 'segments'.
        """
        # Extract audio first
        audio_path = await self._extract_audio(video_path)
        
        try:
            if self.use_local:
                result = await self._transcribe_local(audio_path, language)
            else:
                result = await self._transcribe_openai(audio_path, language)
            
            return result
            
        finally:
            # Cleanup temp audio
            if os.path.exists(audio_path):
                os.remove(audio_path)
    
    async def _extract_audio(self, video_path: str) -> str:
        """Extract audio from video to temp file"""
        audio_path = tempfile.mktemp(suffix=".wav")
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vn",  # No video
            "-acodec", "pcm_s16le",
            "-ar", "16000",  # 16kHz for Whisper
            "-ac", "1",  # Mono
            audio_path,
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            logger.error(f"Audio extraction failed: {result.stderr}")
            raise RuntimeError(f"Failed to extract audio: {result.stderr}")
        
        return audio_path
    
    async def _transcribe_openai(
        self,
        audio_path: str,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Transcribe using OpenAI Whisper API"""
        import openai
        
        client = openai.OpenAI(api_key=self.openai_key)
        
        with open(audio_path, "rb") as audio_file:
            # Get basic transcription
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language,
                response_format="verbose_json",
            )
        
        # Parse response
        segments = []
        if hasattr(transcript, 'segments') and transcript.segments:
            for seg in transcript.segments:
                segments.append({
                    "start": seg.get("start", 0),
                    "end": seg.get("end", 0),
                    "text": seg.get("text", "").strip(),
                })
        
        return {
            "text": transcript.text if hasattr(transcript, 'text') else str(transcript),
            "segments": segments,
            "language": language or "auto",
        }
    
    async def _transcribe_local(
        self,
        audio_path: str,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Transcribe using local Whisper model"""
        try:
            from faster_whisper import WhisperModel
            
            if self._local_model is None:
                model_path = self.local_model
                logger.info(f"Loading Whisper model: {model_path}")
                self._local_model = WhisperModel(
                    model_path,
                    device="cpu",
                    compute_type="int8",
                )
            
            segments_gen, info = self._local_model.transcribe(
                audio_path,
                language=language,
                beam_size=5,
                word_timestamps=True,
            )
            
            segments = []
            full_text = []
            
            for segment in segments_gen:
                segments.append({
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip(),
                })
                full_text.append(segment.text.strip())
            
            return {
                "text": " ".join(full_text),
                "segments": segments,
                "language": info.language if info else language,
            }
            
        except ImportError:
            logger.warning("faster-whisper not installed, falling back to OpenAI API")
            return await self._transcribe_openai(audio_path, language)
    
    async def detect_language(self, video_path: str) -> str:
        """Detect language of audio in video"""
        audio_path = await self._extract_audio(video_path)
        
        try:
            if self.use_local:
                from faster_whisper import WhisperModel
                
                if self._local_model is None:
                    self._local_model = WhisperModel(
                        self.local_model,
                        device="cpu",
                        compute_type="int8",
                    )
                
                _, info = self._local_model.transcribe(
                    audio_path,
                    beam_size=1,
                )
                return info.language
            else:
                # Use first 30 seconds for language detection
                result = await self._transcribe_openai(audio_path)
                return result.get("language", "fr")
                
        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)


# =============================================================================
# SINGLETON
# =============================================================================

_whisper_client: Optional[WhisperClient] = None


def get_whisper_client() -> WhisperClient:
    """Get or create Whisper client singleton"""
    global _whisper_client
    if _whisper_client is None:
        _whisper_client = WhisperClient()
    return _whisper_client
