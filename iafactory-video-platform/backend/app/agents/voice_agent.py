"""
Voice Agent - TTS, STT et génération audio
"""
from typing import List, Dict, Any, Optional
from app.agents.base import BaseAgent, AgentTask, AgentResult
from app.core.config import settings


class VoiceAgent(BaseAgent):
    """
    Agent de gestion audio/voix.

    TTS Providers:
    - ElevenLabs
    - OpenAI TTS
    - Google TTS
    - Azure TTS
    - Bark (open source)
    - XTTS (Coqui)

    STT Providers:
    - Whisper (OpenAI)
    - Deepgram
    - AssemblyAI
    - Google STT

    Music Providers:
    - Suno AI
    - Udio
    - MusicGen (Meta)

    Responsabilités:
    - Génère des voix off (TTS)
    - Transcrit l'audio (STT)
    - Clone des voix
    - Génère de la musique
    - Gère les effets sonores
    """

    @property
    def agent_type(self) -> str:
        return "voice"

    @property
    def capabilities(self) -> List[str]:
        return [
            "text_to_speech",
            "speech_to_text",
            "clone_voice",
            "list_voices",
            "generate_music",
            "generate_sfx",
            "enhance_audio"
        ]

    # Coûts TTS par 1000 caractères
    TTS_COSTS = {
        "elevenlabs": 30,    # ~$0.30 pour 1000 chars
        "openai": 15,        # ~$0.15 pour 1000 chars
        "google": 4,         # ~$0.04 pour 1000 chars
        "azure": 5,          # ~$0.05 pour 1000 chars
        "bark": 0,           # Open source
        "xtts": 0,           # Open source
    }

    # Coûts STT par minute
    STT_COSTS = {
        "whisper": 1,        # ~$0.01 par minute
        "deepgram": 2,       # ~$0.02 par minute
        "assemblyai": 3,     # ~$0.03 par minute
        "google": 2,         # ~$0.02 par minute
    }

    # Voix prédéfinies par provider
    VOICES = {
        "elevenlabs": [
            {"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel", "gender": "female", "accent": "american"},
            {"id": "AZnzlk1XvdvUeBnXmlld", "name": "Domi", "gender": "female", "accent": "american"},
            {"id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella", "gender": "female", "accent": "american"},
            {"id": "ErXwobaYiN019PkySvjV", "name": "Antoni", "gender": "male", "accent": "american"},
            {"id": "MF3mGyEYCl7XYWbV9V6O", "name": "Elli", "gender": "female", "accent": "american"},
            {"id": "TxGEqnHWrfWFTfGW9XjX", "name": "Josh", "gender": "male", "accent": "american"},
            {"id": "pNInz6obpgDQGcFmaJgB", "name": "Adam", "gender": "male", "accent": "american"},
            {"id": "yoZ06aMxZJJ28mfd3POQ", "name": "Sam", "gender": "male", "accent": "american"},
        ],
        "openai": [
            {"id": "alloy", "name": "Alloy", "gender": "neutral", "accent": "american"},
            {"id": "echo", "name": "Echo", "gender": "male", "accent": "american"},
            {"id": "fable", "name": "Fable", "gender": "male", "accent": "british"},
            {"id": "onyx", "name": "Onyx", "gender": "male", "accent": "american"},
            {"id": "nova", "name": "Nova", "gender": "female", "accent": "american"},
            {"id": "shimmer", "name": "Shimmer", "gender": "female", "accent": "american"},
        ]
    }

    def __init__(
        self,
        default_tts_provider: str = None,
        default_stt_provider: str = None
    ):
        super().__init__()
        self.default_tts_provider = default_tts_provider or settings.DEFAULT_TTS_PROVIDER
        self.default_stt_provider = default_stt_provider or settings.DEFAULT_STT_PROVIDER

    async def _execute_task(self, task: AgentTask) -> AgentResult:
        """Exécute une tâche audio"""

        handlers = {
            "text_to_speech": self._text_to_speech,
            "speech_to_text": self._speech_to_text,
            "clone_voice": self._clone_voice,
            "list_voices": self._list_voices,
            "generate_music": self._generate_music,
            "generate_sfx": self._generate_sfx,
            "enhance_audio": self._enhance_audio,
        }

        handler = handlers.get(task.task_type)
        return await handler(task)

    async def _text_to_speech(self, task: AgentTask) -> AgentResult:
        """
        Convertit du texte en audio (voix off).
        """
        text = task.input_data.get("text", "")
        voice_id = task.input_data.get("voice_id")
        provider = task.input_data.get("provider", self.default_tts_provider)
        language = task.input_data.get("language", "fr")
        speed = task.input_data.get("speed", 1.0)
        emotion = task.input_data.get("emotion", "neutral")

        if not text:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="Text is required"
            )

        # Estimation de la durée (environ 150 mots par minute)
        word_count = len(text.split())
        estimated_duration = (word_count / 150) * 60 / speed  # en secondes

        # TODO: Appel réel à l'API du provider
        audio_result = {
            "audio_id": f"tts_{task.task_id[:8]}",
            "text": text[:100] + "..." if len(text) > 100 else text,
            "provider": provider,
            "voice_id": voice_id,
            "language": language,
            "speed": speed,
            "emotion": emotion,
            "duration": estimated_duration,
            "format": "mp3",
            "sample_rate": 44100,
            "url": f"https://placeholder.com/tts_{task.task_id[:8]}.mp3",
            "local_path": None
        }

        # Calcul du coût basé sur le nombre de caractères
        char_count = len(text)
        cost_per_1k = self.TTS_COSTS.get(provider, 15)
        cost = int((char_count / 1000) * cost_per_1k)

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"audio": audio_result},
            cost_cents=cost,
            metadata={"estimated_duration": estimated_duration, "char_count": char_count}
        )

    async def _speech_to_text(self, task: AgentTask) -> AgentResult:
        """
        Transcrit de l'audio en texte.
        """
        audio_path = task.input_data.get("audio_path")
        audio_url = task.input_data.get("audio_url")
        provider = task.input_data.get("provider", self.default_stt_provider)
        language = task.input_data.get("language", "fr")
        include_timestamps = task.input_data.get("timestamps", True)

        if not audio_path and not audio_url:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="audio_path or audio_url is required"
            )

        # TODO: Appel réel à l'API du provider
        transcription = {
            "transcription_id": f"stt_{task.task_id[:8]}",
            "provider": provider,
            "language": language,
            "text": "Transcription placeholder...",
            "confidence": 0.95,
            "duration": 60,  # secondes
            "words": []  # Liste de mots avec timestamps si demandé
        }

        if include_timestamps:
            transcription["segments"] = [
                {"start": 0, "end": 2, "text": "Transcription"},
                {"start": 2, "end": 4, "text": "placeholder..."}
            ]

        # Coût basé sur la durée
        duration_minutes = transcription["duration"] / 60
        cost = int(duration_minutes * self.STT_COSTS.get(provider, 2))

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"transcription": transcription},
            cost_cents=cost
        )

    async def _clone_voice(self, task: AgentTask) -> AgentResult:
        """
        Clone une voix à partir d'échantillons audio.
        """
        voice_samples = task.input_data.get("voice_samples", [])
        voice_name = task.input_data.get("name", "Custom Voice")
        provider = task.input_data.get("provider", "elevenlabs")
        description = task.input_data.get("description", "")

        if len(voice_samples) < 1:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="At least 1 voice sample is required"
            )

        # TODO: Appel API pour clonage de voix
        cloned_voice = {
            "voice_id": f"voice_{task.task_id[:8]}",
            "name": voice_name,
            "provider": provider,
            "description": description,
            "samples_count": len(voice_samples),
            "status": "created"
        }

        # Clonage de voix coûte un forfait
        cost = 500 if provider == "elevenlabs" else 200

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"voice": cloned_voice},
            cost_cents=cost
        )

    async def _list_voices(self, task: AgentTask) -> AgentResult:
        """Liste les voix disponibles pour un provider"""
        provider = task.input_data.get("provider", self.default_tts_provider)
        language = task.input_data.get("language")

        voices = self.VOICES.get(provider, [])

        # Filtrer par langue si spécifié
        if language:
            # TODO: Filtrage réel par langue supportée
            pass

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={
                "provider": provider,
                "voices": voices,
                "total": len(voices)
            }
        )

    async def _generate_music(self, task: AgentTask) -> AgentResult:
        """
        Génère de la musique avec IA.
        Providers: Suno, Udio, MusicGen
        """
        prompt = task.input_data.get("prompt", "")
        duration = task.input_data.get("duration", 30)  # secondes
        provider = task.input_data.get("provider", "suno")
        genre = task.input_data.get("genre", "background")
        mood = task.input_data.get("mood", "neutral")
        instrumental = task.input_data.get("instrumental", True)

        if not prompt:
            # Générer un prompt basé sur le mood et genre
            prompt = f"{mood} {genre} music, {duration} seconds"

        # TODO: Appel réel à l'API
        music_result = {
            "music_id": f"music_{task.task_id[:8]}",
            "prompt": prompt,
            "provider": provider,
            "duration": duration,
            "genre": genre,
            "mood": mood,
            "instrumental": instrumental,
            "format": "mp3",
            "url": f"https://placeholder.com/music_{task.task_id[:8]}.mp3",
            "local_path": None
        }

        # Coûts musique
        music_costs = {"suno": 10, "udio": 10, "musicgen": 0}
        cost = music_costs.get(provider, 10)

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"music": music_result},
            cost_cents=cost
        )

    async def _generate_sfx(self, task: AgentTask) -> AgentResult:
        """
        Génère des effets sonores.
        """
        description = task.input_data.get("description", "")
        duration = task.input_data.get("duration", 5)
        provider = task.input_data.get("provider", "elevenlabs")  # ElevenLabs SFX

        if not description:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="Description is required"
            )

        # TODO: Appel API
        sfx_result = {
            "sfx_id": f"sfx_{task.task_id[:8]}",
            "description": description,
            "provider": provider,
            "duration": duration,
            "format": "mp3",
            "url": f"https://placeholder.com/sfx_{task.task_id[:8]}.mp3",
            "local_path": None
        }

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"sfx": sfx_result},
            cost_cents=5
        )

    async def _enhance_audio(self, task: AgentTask) -> AgentResult:
        """
        Améliore la qualité audio (débruitage, normalisation).
        """
        audio_path = task.input_data.get("audio_path")
        enhancements = task.input_data.get("enhancements", ["denoise", "normalize"])

        if not audio_path:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="audio_path is required"
            )

        available_enhancements = [
            "denoise",       # Suppression du bruit
            "normalize",     # Normalisation du volume
            "compress",      # Compression dynamique
            "eq",            # Égalisation
            "remove_silence" # Suppression des silences
        ]

        applied = [e for e in enhancements if e in available_enhancements]

        result = {
            "enhanced_id": f"enhanced_{task.task_id[:8]}",
            "original_audio": audio_path,
            "enhancements_applied": applied,
            "local_path": None
        }

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"enhanced_audio": result},
            cost_cents=0  # Peut être fait localement
        )

    def get_best_voice_for_content(
        self,
        content_type: str,
        language: str = "fr",
        gender: str = None
    ) -> Dict[str, Any]:
        """
        Recommande la meilleure voix selon le type de contenu.
        """
        recommendations = {
            "corporate": {"provider": "elevenlabs", "voice_id": "21m00Tcm4TlvDq8ikWAM"},
            "educational": {"provider": "openai", "voice_id": "nova"},
            "narrative": {"provider": "elevenlabs", "voice_id": "EXAVITQu4vr4xnSDxMaL"},
            "casual": {"provider": "openai", "voice_id": "alloy"},
            "dramatic": {"provider": "elevenlabs", "voice_id": "ErXwobaYiN019PkySvjV"},
        }

        return recommendations.get(content_type, recommendations["educational"])
