"""
Service de transcription vocal pour professionnels libéraux
Médecins, avocats, experts-comptables (Suisse, France, Algérie)
"""

import os
import logging
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, BinaryIO
from .whisper_engine import get_whisper_engine

logger = logging.getLogger(__name__)


class TranscriptionService:
    """
    Service de transcription vocale professionnel

    Use Cases:
    - Médecins: Comptes-rendus de consultation
    - Avocats: Notes d'audience, dictées juridiques
    - Experts-comptables: Notes de rendez-vous client
    """

    def __init__(
        self,
        model_size: str = "base",  # Changé vers base (rapide)
        device: str = "auto",
        compute_type: str = "int8",  # CPU compatible
    ):
        """
        Initialise le service de transcription

        Args:
            model_size: Taille du modèle Whisper
            device: Device (auto, cpu, cuda)
            compute_type: Précision (float16, int8)
        """
        self.engine = get_whisper_engine(
            model_size=model_size,
            device=device,
            compute_type=compute_type,
        )
        self.temp_dir = Path(tempfile.gettempdir()) / "voice-agent"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def transcribe_file(
        self,
        audio_file: BinaryIO,
        filename: str,
        language: Optional[str] = None,
        professional_context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Transcrit un fichier audio uploadé

        Args:
            audio_file: Fichier audio (upload HTTP)
            filename: Nom du fichier
            language: Code langue (fr, en, ar) ou None
            professional_context: Contexte professionnel (medical, legal, accounting)

        Returns:
            Dict avec:
                - text: Texte brut transcrit
                - segments: Segments avec timestamps
                - language: Langue détectée
                - duration: Durée (secondes)
                - context: Contexte professionnel
        """
        # Sauvegarder temporairement le fichier
        temp_path = self.temp_dir / filename
        try:
            with open(temp_path, "wb") as f:
                f.write(audio_file.read())

            logger.info(f"Transcription fichier: {filename} (context={professional_context})")

            # Transcription
            result = self.engine.transcribe(
                str(temp_path),
                language=language,
                vad_filter=True,
                word_timestamps=False,  # Pas besoin pour usage professionnel
            )

            # Ajouter contexte
            result["filename"] = filename
            result["professional_context"] = professional_context

            # Nettoyage post-transcription selon contexte
            if professional_context:
                result["cleaned_text"] = self._clean_transcription(
                    result["text"], professional_context
                )

            return result

        except Exception as e:
            logger.error(f"Erreur transcription {filename}: {e}")
            raise

        finally:
            # Nettoyer fichier temporaire
            if temp_path.exists():
                temp_path.unlink()

    def transcribe_url(
        self,
        audio_url: str,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Transcrit un fichier audio depuis une URL

        Args:
            audio_url: URL du fichier audio
            language: Code langue

        Returns:
            Résultat de transcription
        """
        # Télécharger le fichier
        import requests

        temp_path = self.temp_dir / f"url_audio_{os.urandom(8).hex()}"
        try:
            response = requests.get(audio_url, stream=True)
            response.raise_for_status()

            with open(temp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Transcription
            result = self.engine.transcribe(
                str(temp_path),
                language=language,
                vad_filter=True,
            )

            result["source"] = "url"
            result["audio_url"] = audio_url

            return result

        finally:
            if temp_path.exists():
                temp_path.unlink()

    def detect_language(self, audio_file: BinaryIO, filename: str) -> Dict[str, float]:
        """
        Détecte la langue d'un fichier audio

        Args:
            audio_file: Fichier audio
            filename: Nom du fichier

        Returns:
            {"language": "fr", "probability": 0.98}
        """
        temp_path = self.temp_dir / filename
        try:
            with open(temp_path, "wb") as f:
                f.write(audio_file.read())

            return self.engine.detect_language(str(temp_path))

        finally:
            if temp_path.exists():
                temp_path.unlink()

    def _clean_transcription(self, text: str, context: str) -> str:
        """
        Nettoie la transcription selon le contexte professionnel

        Args:
            text: Texte brut
            context: medical, legal, accounting

        Returns:
            Texte nettoyé et structuré

        Note: Cette fonction sera enrichie avec des prompts LLM
        pour transformer les dictées brutes en documents structurés
        """
        # Nettoyages basiques
        text = text.strip()

        # Capitaliser première lettre
        if text:
            text = text[0].upper() + text[1:]

        # Ajouter ponctuation finale si manquante
        if text and text[-1] not in ".!?":
            text += "."

        # TODO: Intégrer avec LLM (Claude/Llama) pour nettoyage avancé
        # selon le contexte professionnel (médical, juridique, comptable)

        return text


def get_transcription_service(
    model_size: Optional[str] = None,
    device: str = "auto",
    compute_type: Optional[str] = None,
) -> TranscriptionService:
    """
    Crée une instance du service de transcription (SINGLETON SUPPRIMÉ)

    Hardware Aware: Auto-détecte GPU vs CPU

    Args:
        model_size: Taille du modèle (None = auto-detect)
        device: Device (auto, cpu, cuda)
        compute_type: Précision (None = auto-detect)

    Returns:
        Nouvelle instance TranscriptionService
    """
    # Créer NOUVELLE instance (pas de cache)
    return TranscriptionService(
        model_size=model_size or "base",
        device=device,
        compute_type=compute_type or "int8",
    )
