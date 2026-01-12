"""
OCR_DZ - Module OCR Multilingue Algérie
=======================================
Extraction arabe/français/anglais depuis PDF + images
Support RTL, normalisation arabe, fallback IA
"""

from .ocr_utils import (
    detect_language,
    clean_arabic,
    clean_french,
    normalize_arabic,
    merge_pages_text,
    estimate_confidence,
)
from .ocr_dz_pipeline import OCRPipeline, ocr_pipeline, OCRResult
from .ocr_router import router as ocr_router

__all__ = [
    "detect_language",
    "clean_arabic",
    "clean_french",
    "normalize_arabic",
    "merge_pages_text",
    "estimate_confidence",
    "OCRPipeline",
    "ocr_pipeline",
    "OCRResult",
    "ocr_router",
]
