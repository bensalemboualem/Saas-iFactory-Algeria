"""
Faster-Whisper Engine Integration
Moteur de reconnaissance vocale souverain (4x plus rapide)
"""

import os
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)


class WhisperEngine:
    """
    Faster-Whisper Engine pour reconnaissance vocale souveraine

    Supporte:
    - Français (France, Suisse, Belgique, Québec)
    - Anglais (US, UK, médical)
    - Arabe (littéraire, dialectes)
    - Darija algérienne

    Avantages:
    - 4x plus rapide que Whisper OpenAI
    - 70% moins de VRAM
    - Mode offline total (souverain)
    - Précision identique
    """

    # Modèles disponibles (du plus petit au plus grand)
    MODELS = {
        "tiny": "guillaumekln/faster-whisper-tiny",
        "base": "guillaumekln/faster-whisper-base",
        "small": "guillaumekln/faster-whisper-small",
        "medium": "guillaumekln/faster-whisper-medium",
        "large-v2": "guillaumekln/faster-whisper-large-v2",
        "large-v3": "guillaumekln/faster-whisper-large-v3",  # Le plus puissant
        "distil-large-v3": "distil-whisper/distil-large-v3",  # Distilled (léger)
    }

    def __init__(
        self,
        model_size: str = "base",  # Changé de large-v3 vers base (10x plus rapide)
        device: str = "auto",
        compute_type: str = "int8",  # Changé vers int8 (CPU compatible)
        download_root: Optional[str] = None,
    ):
        """
        Initialise le moteur Faster-Whisper

        Args:
            model_size: Taille du modèle (tiny, base, small, medium, large-v2, large-v3, distil-large-v3)
            device: Device à utiliser (auto, cpu, cuda)
            compute_type: Précision (int8, float16, int8, int8_float16)
            download_root: Dossier de téléchargement des modèles
        """
        self.model_size = model_size
        self.device = self._detect_device() if device == "auto" else device
        self.compute_type = compute_type

        # Dossier de téléchargement des modèles
        if download_root is None:
            download_root = os.path.join(
                os.path.dirname(__file__), "models"
            )
        self.download_root = Path(download_root)
        self.download_root.mkdir(parents=True, exist_ok=True)

        logger.info(
            f"Initializing Faster-Whisper: model={model_size}, "
            f"device={self.device}, compute={compute_type}"
        )

        # Charger le modèle
        self.model = self._load_model()

    def _detect_device(self) -> str:
        """Détecte automatiquement le meilleur device (CPU/GPU)"""
        try:
            import torch
            if torch.cuda.is_available():
                logger.info("GPU CUDA détecté")
                return "cuda"
        except ImportError:
            pass

        logger.info("Utilisation du CPU")
        return "cpu"

    def _load_model(self) -> WhisperModel:
        """Charge le modèle Faster-Whisper"""
        try:
            model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
                download_root=str(self.download_root),
            )
            logger.info(f"Modèle {self.model_size} chargé avec succès")
            return model
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle: {e}")
            raise

    def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
        task: str = "transcribe",
        beam_size: int = 5,
        vad_filter: bool = True,
        word_timestamps: bool = False,
    ) -> Dict[str, Any]:
        """
        Transcrit un fichier audio

        Args:
            audio_path: Chemin du fichier audio
            language: Code langue (fr, en, ar) ou None pour détection auto
            task: "transcribe" ou "translate" (traduit en anglais)
            beam_size: Taille du beam search (5 par défaut, bon compromis)
            vad_filter: Utiliser Voice Activity Detection (recommandé)
            word_timestamps: Retourner timestamps par mot

        Returns:
            Dict avec:
                - text: Texte transcrit complet
                - segments: Liste des segments avec timestamps
                - language: Langue détectée
                - duration: Durée audio (secondes)
        """
        try:
            logger.info(f"Transcription: {audio_path} (lang={language})")

            # Transcription
            segments, info = self.model.transcribe(
                audio_path,
                language=language,
                task=task,
                beam_size=beam_size,
                vad_filter=vad_filter,
                word_timestamps=word_timestamps,
            )

            # Collecter les segments
            segments_list = []
            full_text = []

            for segment in segments:
                segment_dict = {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip(),
                }

                if word_timestamps and hasattr(segment, "words"):
                    segment_dict["words"] = [
                        {
                            "start": word.start,
                            "end": word.end,
                            "word": word.word,
                            "probability": word.probability,
                        }
                        for word in segment.words
                    ]

                segments_list.append(segment_dict)
                full_text.append(segment.text.strip())

            result = {
                "text": " ".join(full_text),
                "segments": segments_list,
                "language": info.language,
                "language_probability": info.language_probability,
                "duration": info.duration,
                "duration_after_vad": info.duration_after_vad if vad_filter else None,
            }

            logger.info(
                f"Transcription réussie: {len(segments_list)} segments, "
                f"lang={info.language} ({info.language_probability:.2%})"
            )

            return result

        except Exception as e:
            logger.error(f"Erreur transcription: {e}")
            raise

    def transcribe_batch(
        self,
        audio_paths: List[str],
        batch_size: int = 8,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Transcrit plusieurs fichiers audio en batch (plus rapide)

        Args:
            audio_paths: Liste des chemins audio
            batch_size: Taille du batch (8 recommandé)
            **kwargs: Paramètres de transcribe()

        Returns:
            Liste des résultats de transcription
        """
        results = []

        for audio_path in audio_paths:
            try:
                result = self.transcribe(audio_path, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Erreur batch {audio_path}: {e}")
                results.append({"error": str(e), "audio_path": audio_path})

        return results

    def detect_language(self, audio_path: str) -> Dict[str, float]:
        """
        Détecte la langue d'un fichier audio

        Returns:
            Dict {langue: probabilité} (ex: {"fr": 0.98, "en": 0.02})
        """
        try:
            _, info = self.model.transcribe(audio_path, beam_size=1, max_length=30)
            return {
                "language": info.language,
                "probability": info.language_probability,
            }
        except Exception as e:
            logger.error(f"Erreur détection langue: {e}")
            raise


def _detect_optimal_config() -> tuple[str, str]:
    """
    Détecte la configuration optimale selon le hardware disponible

    Returns:
        (model_size, compute_type) optimaux
    """
    import torch

    # Check GPU NVIDIA disponible
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # GB

        logger.info(f"GPU détecté: {gpu_name} ({vram:.1f}GB VRAM)")

        # Config Suisse/Europe: GPU puissant
        if vram >= 8:
            return ("large-v3", "float16")  # Meilleure qualité
        elif vram >= 4:
            return ("base", "float16")  # Bon compromis
        else:
            return ("base", "int8")  # GPU faible
    else:
        # Config Algérie/CPU only
        logger.info("CPU uniquement détecté - Config Algérie")
        return ("base", "int8")  # CPU compatible


def get_whisper_engine(
    model_size: Optional[str] = None,
    device: str = "auto",
    compute_type: Optional[str] = None,
) -> WhisperEngine:
    """
    Crée une instance du moteur Whisper avec détection hardware intelligente

    SINGLETON SUPPRIMÉ: Permet changement dynamique de config

    Args:
        model_size: Taille du modèle (None = auto-detect)
        device: Device (auto, cpu, cuda)
        compute_type: Précision (None = auto-detect)

    Returns:
        Nouvelle instance WhisperEngine

    Hardware Aware:
        - GPU NVIDIA présent (Suisse) → float16 + large-v3
        - CPU uniquement (Algérie) → int8 + base
    """
    # Auto-détection si non spécifié
    if model_size is None or compute_type is None:
        detected_model, detected_compute = _detect_optimal_config()
        model_size = model_size or detected_model
        compute_type = compute_type or detected_compute
        logger.info(f"Config auto-détectée: {model_size} + {compute_type}")

    # Créer NOUVELLE instance (pas de singleton)
    return WhisperEngine(
        model_size=model_size,
        device=device,
        compute_type=compute_type,
    )
