"""
DARIJA_NLP - Module NLP Darija Algérienne
==========================================
Premier moteur NLP pour la darija (arabe algérien)
Normalisation, Arabizi→Arabe, Nettoyage, Segmentation
"""

from .darija_cleaner import (
    clean_text,
    clean_noise,
    tokenize_arabic,
    remove_emojis,
    remove_harakat,
    normalize_arabic_chars,
)
from .darija_arabizi import (
    arabizi_to_arabic,
    is_arabizi,
    ARABIZI_MAP,
    DARIJA_WORDS,
)
from .darija_normalizer import (
    normalize_darija,
    detect_dialect,
    DarijaNormalizer,
    NormalizationResult,
    DialectType,
)
from .darija_router import router as darija_router

__all__ = [
    # Cleaner
    "clean_text",
    "clean_noise",
    "tokenize_arabic",
    "remove_emojis",
    "remove_harakat",
    "normalize_arabic_chars",
    # Arabizi
    "arabizi_to_arabic",
    "is_arabizi",
    "ARABIZI_MAP",
    "DARIJA_WORDS",
    # Normalizer
    "normalize_darija",
    "detect_dialect",
    "DarijaNormalizer",
    "NormalizationResult",
    "DialectType",
    # Router
    "darija_router",
]
