"""
Service de génération de mots-clés IA pour transcriptions vocales
Utilise le Multi-LLM Router pour générer des résumés intelligents
"""
import logging
import json
from typing import Optional

logger = logging.getLogger(__name__)


def generate_keywords_simple(text: str) -> str:
    """
    Génère 3 mots-clés en utilisant une approche simple basée sur la fréquence

    Args:
        text: Texte transcrit

    Returns:
        3 mots-clés séparés par virgule (ex: "consultation, diagnostic, traitement")

    Note: Version simple pour démarrer. Sera enrichie avec LLM plus tard.
    """
    if not text or len(text) < 10:
        return "court, audio, transcription"

    # Nettoyer et tokeniser
    words = text.lower().split()

    # Mots communs à filtrer (stop words français simplifié)
    stop_words = {
        "le", "la", "les", "un", "une", "de", "du", "des", "à", "au", "et",
        "est", "sont", "a", "ont", "pour", "dans", "sur", "par", "avec",
        "je", "tu", "il", "elle", "nous", "vous", "ils", "elles",
        "ce", "cette", "ces", "son", "sa", "ses", "mon", "ma", "mes",
        "que", "qui", "quoi", "où", "comment", "pourquoi", "quand",
        "mais", "ou", "donc", "car", "ni", "si", "bien", "alors",
    }

    # Compter fréquences (mots > 3 caractères, pas dans stop words)
    freq = {}
    for word in words:
        # Nettoyer ponctuation
        clean_word = "".join(c for c in word if c.isalnum())
        if len(clean_word) > 3 and clean_word not in stop_words:
            freq[clean_word] = freq.get(clean_word, 0) + 1

    # Top 3 mots
    if not freq:
        return "audio, vocal, transcription"

    top_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:3]
    keywords = ", ".join([w[0] for w in top_words])

    logger.info(f"Mots-clés générés (simple): {keywords}")
    return keywords


async def generate_keywords_llm(text: str, context: Optional[str] = None) -> str:
    """
    Génère 3 mots-clés en utilisant un LLM (Claude, Gemini, ou Llama)

    Args:
        text: Texte transcrit
        context: Contexte professionnel (medical, legal, accounting)

    Returns:
        3 mots-clés séparés par virgule

    TODO: Implémenter appel au Multi-LLM Router
    """
    # Pour l'instant, utiliser la version simple
    # Plus tard: appeler /api/multi-llm/chat avec un prompt optimisé
    return generate_keywords_simple(text)


def generate_keywords(text: str, use_llm: bool = False, context: Optional[str] = None) -> str:
    """
    Génère 3 mots-clés pour résumer une transcription

    Args:
        text: Texte transcrit
        use_llm: Si True, utilise un LLM (sinon méthode simple)
        context: Contexte professionnel

    Returns:
        3 mots-clés séparés par virgule

    Examples:
        >>> generate_keywords("Le patient présente des douleurs abdominales...")
        "patient, douleurs, abdominales"

        >>> generate_keywords("Rendez-vous avec expert-comptable pour bilan fiscal")
        "rendez-vous, expert-comptable, fiscal"
    """
    if use_llm:
        # Version future avec LLM
        import asyncio
        return asyncio.run(generate_keywords_llm(text, context))
    else:
        # Version simple et rapide
        return generate_keywords_simple(text)
