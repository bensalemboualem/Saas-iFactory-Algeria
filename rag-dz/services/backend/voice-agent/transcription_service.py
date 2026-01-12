"""
Service de transcription vocal pour professionnels libéraux
Médecins, avocats, experts-comptables (Suisse, France, Algérie)
"""

import os
import logging
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, BinaryIO
try:
    from .whisper_engine import get_whisper_engine
except ImportError:
    from whisper_engine import get_whisper_engine

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
        model_size: str = "large-v3",
        device: str = "auto",
        compute_type: str = "auto",
    ):
        """
        Initialise le service de transcription

        Args:
            model_size: Taille du modèle Whisper
            device: Device (auto, cpu, cuda)
            compute_type: Précision (auto, float16, int8)
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
        Nettoie la transcription selon le contexte professionnel avec IA

        Args:
            text: Texte brut
            context: medical, legal, accounting

        Returns:
            Texte nettoyé et structuré par l'IA

        Utilise Claude/GPT pour transformer les dictées brutes en documents
        professionnels structurés selon le contexte
        """
        # Nettoyages basiques d'abord
        text = text.strip()
        if not text:
            return text

        # Capitaliser première lettre
        text = text[0].upper() + text[1:]

        # Ajouter ponctuation finale si manquante
        if text[-1] not in ".!?":
            text += "."

        # Nettoyage avancé avec LLM selon contexte
        try:
            cleaned_text = self._clean_with_llm(text, context)
            return cleaned_text if cleaned_text else text
        except Exception as e:
            logger.warning(f"LLM cleaning failed: {e}, using basic cleanup")
            return text

    def _clean_with_llm(self, text: str, context: str) -> str:
        """
        Nettoie le texte avec Claude/GPT selon le contexte professionnel

        Args:
            text: Texte brut de la transcription
            context: Contexte professionnel

        Returns:
            Texte structuré et nettoyé
        """
        import os

        # Prompts selon contexte
        context_prompts = {
            "medical": """Tu es un assistant médical expert. Transforme cette dictée vocale brute en compte-rendu médical structuré et professionnel.

Règles:
- Corrige les fautes de transcription
- Structure en paragraphes clairs
- Utilise la terminologie médicale appropriée
- Garde les informations médicales exactes (symptômes, diagnostics, traitements)
- Format: Introduction, Examen clinique, Diagnostic, Traitement/Recommandations

Dictée brute:
{text}

Compte-rendu structuré:""",

            "legal": """Tu es un assistant juridique expert. Transforme cette dictée vocale brute en note juridique structurée et professionnelle.

Règles:
- Corrige les fautes de transcription
- Structure en sections claires
- Utilise la terminologie juridique appropriée
- Garde tous les détails juridiques importants
- Format: Contexte, Faits, Analyse juridique, Conclusions

Dictée brute:
{text}

Note juridique structurée:""",

            "accounting": """Tu es un assistant comptable expert. Transforme cette dictée vocale brute en note comptable structurée et professionnelle.

Règles:
- Corrige les fautes de transcription
- Structure en sections claires
- Utilise la terminologie comptable appropriée
- Garde tous les chiffres et montants exacts
- Format: Client, Période, Opérations, Observations

Dictée brute:
{text}

Note comptable structurée:"""
        }

        prompt = context_prompts.get(context, "")
        if not prompt:
            return text

        prompt = prompt.format(text=text)

        # Essayer avec Anthropic Claude d'abord (meilleur pour le texte structuré)
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            try:
                import anthropic

                client = anthropic.Anthropic(api_key=anthropic_key)
                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=2048,
                    temperature=0.3,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )

                cleaned = message.content[0].text.strip()
                logger.info(f"Text cleaned with Claude (context={context})")
                return cleaned

            except Exception as e:
                logger.warning(f"Claude cleaning failed: {e}")

        # Fallback: OpenAI GPT
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                import openai

                client = openai.OpenAI(api_key=openai_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }],
                    temperature=0.3,
                    max_tokens=2048
                )

                cleaned = response.choices[0].message.content.strip()
                logger.info(f"Text cleaned with GPT (context={context})")
                return cleaned

            except Exception as e:
                logger.warning(f"GPT cleaning failed: {e}")

        # Pas de clé API disponible
        logger.warning("No LLM API key available for cleaning")
        return text


# Instance globale
_transcription_service: Optional[TranscriptionService] = None


def get_transcription_service(
    model_size: str = "large-v3",
    device: str = "auto",
) -> TranscriptionService:
    """
    Récupère l'instance singleton du service de transcription

    Args:
        model_size: Taille du modèle
        device: Device

    Returns:
        Instance TranscriptionService
    """
    global _transcription_service

    if _transcription_service is None:
        _transcription_service = TranscriptionService(
            model_size=model_size,
            device=device,
        )

    return _transcription_service
