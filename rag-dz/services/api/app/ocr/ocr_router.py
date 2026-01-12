"""
OCR_DZ - Router FastAPI
=======================
Endpoints OCR multilingue (arabe/français/anglais)
"""

import io
import time
import logging
from typing import Optional, List, Literal
from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from pydantic import BaseModel, Field

from .ocr_dz_pipeline import OCRPipeline, OCRResult, ocr_pipeline, OCREngine
from .ocr_utils import (
    detect_language,
    clean_arabic,
    normalize_arabic,
    LanguageCode,
    get_language_name,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ocr", tags=["OCR Multilingue DZ"])


# ============================================
# REQUEST/RESPONSE MODELS
# ============================================

class OCRExtractRequest(BaseModel):
    """Requête d'extraction OCR (pour URL)"""
    url: str = Field(..., description="URL du document à OCR")
    language_hint: Optional[LanguageCode] = Field(None, description="Langue attendue")
    enable_fallback: bool = Field(True, description="Activer fallback IA si qualité faible")


class DetectLanguageRequest(BaseModel):
    """Requête de détection de langue"""
    text: str = Field(..., min_length=10, description="Texte à analyser")


class DetectLanguageResponse(BaseModel):
    """Réponse détection de langue"""
    language: LanguageCode
    language_name: str
    confidence: float
    is_arabic: bool
    is_rtl: bool


class CleanTextRequest(BaseModel):
    """Requête de nettoyage de texte"""
    text: str = Field(..., description="Texte à nettoyer")
    language: LanguageCode = Field("ar", description="Langue du texte")
    normalize: bool = Field(True, description="Appliquer normalisation arabe")
    remove_tashkeel: bool = Field(False, description="Supprimer les diacritiques arabes")


class CleanTextResponse(BaseModel):
    """Réponse nettoyage de texte"""
    original: str
    cleaned: str
    language: LanguageCode
    characters_removed: int


class OCRBatchRequest(BaseModel):
    """Requête OCR batch (URLs)"""
    urls: List[str] = Field(..., min_items=1, max_items=10)
    language_hint: Optional[LanguageCode] = None


class OCRBatchResponse(BaseModel):
    """Réponse OCR batch"""
    results: List[OCRResult]
    total: int
    successful: int
    failed: int
    total_time_ms: int


# ============================================
# ENDPOINTS PRINCIPAUX
# ============================================

@router.post("/extract", response_model=OCRResult)
async def extract_text(
    file: UploadFile = File(..., description="Document à OCR (PDF ou image)"),
    language_hint: Optional[str] = Form(None, description="Langue attendue (ar, fr, en)"),
    enable_fallback: bool = Form(True, description="Activer fallback IA"),
):
    """
    📄 Extraire le texte d'un document (PDF ou image)
    
    **Formats supportés:**
    - PDF (multipages)
    - Images: PNG, JPG, JPEG, TIFF, BMP, GIF
    
    **Langues supportées:**
    - 🇩🇿 Arabe (RTL)
    - 🇫🇷 Français
    - 🇬🇧 Anglais
    - Mixte (arabe + français)
    
    **Processus:**
    1. Détection du type de fichier
    2. Prétraitement de l'image
    3. OCR Tesseract multilingue
    4. Détection automatique de la langue
    5. Nettoyage et normalisation
    6. Fallback IA si qualité faible (< 35%)
    
    **Retourne:**
    - Texte extrait
    - Langue détectée
    - Score de confiance
    - Dates et montants extraits
    """
    # Valider le type de fichier
    allowed_types = [
        "application/pdf",
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/tiff",
        "image/bmp",
        "image/gif",
    ]
    
    content_type = file.content_type or ""
    filename = file.filename or ""
    
    # Vérifier par extension si content_type manquant
    valid_extensions = [".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"]
    is_valid = (
        content_type in allowed_types or
        any(filename.lower().endswith(ext) for ext in valid_extensions)
    )
    
    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail=f"Type de fichier non supporté. Formats acceptés: PDF, PNG, JPG, TIFF, BMP, GIF",
        )
    
    try:
        # Lire le fichier
        file_bytes = await file.read()
        
        if len(file_bytes) == 0:
            raise HTTPException(status_code=400, detail="Fichier vide")
        
        if len(file_bytes) > 50 * 1024 * 1024:  # 50 MB
            raise HTTPException(status_code=400, detail="Fichier trop volumineux (max 50 MB)")
        
        # Configurer le pipeline
        pipeline = OCRPipeline(
            enable_fallback=enable_fallback,
            fallback_provider="claude",
        )
        
        # Parser language_hint
        lang_hint: Optional[LanguageCode] = None
        if language_hint:
            if language_hint.lower() in ["ar", "ara", "arabe", "arabic"]:
                lang_hint = "ar"
            elif language_hint.lower() in ["fr", "fra", "french", "français"]:
                lang_hint = "fr"
            elif language_hint.lower() in ["en", "eng", "english", "anglais"]:
                lang_hint = "en"
        
        # OCR
        result = await pipeline.auto_ocr(
            file_data=file_bytes,
            filename=filename,
            language_hint=lang_hint,
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur OCR: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'extraction: {str(e)}",
        )


@router.post("/extract/quick")
async def extract_text_quick(
    file: UploadFile = File(...),
):
    """
    ⚡ Extraction rapide (paramètres par défaut)
    
    Version simplifiée pour intégration rapide.
    """
    result = await extract_text(file=file, language_hint=None, enable_fallback=True)
    
    return {
        "text": result.text,
        "language": result.language,
        "confidence": result.confidence,
        "pages": result.pages,
        "is_pdf": result.is_pdf,
    }


# ============================================
# ENDPOINTS DÉTECTION LANGUE
# ============================================

@router.post("/detect-language", response_model=DetectLanguageResponse)
async def detect_text_language(request: DetectLanguageRequest):
    """
    🔍 Détecter la langue d'un texte
    
    Analyse le texte et retourne:
    - Langue détectée (ar, fr, en, mixed)
    - Confiance (0-1)
    - Si texte RTL (arabe)
    """
    lang, confidence = detect_language(request.text)
    
    return DetectLanguageResponse(
        language=lang,
        language_name=get_language_name(lang),
        confidence=confidence,
        is_arabic=lang == "ar",
        is_rtl=lang == "ar",
    )


@router.get("/detect-language")
async def detect_language_get(
    text: str = Query(..., min_length=10, description="Texte à analyser"),
):
    """
    🔍 Détecter la langue (GET)
    """
    lang, confidence = detect_language(text)
    
    return {
        "language": lang,
        "language_name": get_language_name(lang),
        "confidence": confidence,
        "is_arabic": lang == "ar",
    }


# ============================================
# ENDPOINTS NETTOYAGE TEXTE
# ============================================

@router.post("/clean", response_model=CleanTextResponse)
async def clean_text(request: CleanTextRequest):
    """
    🧹 Nettoyer et normaliser un texte
    
    - Nettoyage des caractères invalides
    - Normalisation arabe (ة→ه, etc.)
    - Suppression optionnelle des diacritiques
    - Correction de la ponctuation
    """
    original = request.text
    
    if request.language == "ar":
        cleaned = clean_arabic(
            original,
            remove_tashkeel=request.remove_tashkeel,
            normalize=request.normalize,
        )
        if request.normalize:
            cleaned = normalize_arabic(cleaned)
    else:
        from .ocr_utils import clean_by_language
        cleaned = clean_by_language(original, request.language)
    
    return CleanTextResponse(
        original=original,
        cleaned=cleaned,
        language=request.language,
        characters_removed=len(original) - len(cleaned),
    )


@router.post("/normalize-arabic")
async def normalize_arabic_text(
    text: str = Form(..., description="Texte arabe à normaliser"),
):
    """
    🔤 Normaliser un texte arabe
    
    - أ/إ/آ → ا
    - ة → ه
    - ى → ي
    - Suppression tatweel
    - Correction erreurs OCR
    """
    normalized = normalize_arabic(text)
    
    return {
        "original": text,
        "normalized": normalized,
        "original_length": len(text),
        "normalized_length": len(normalized),
    }


# ============================================
# ENDPOINTS BATCH
# ============================================

@router.post("/extract/batch")
async def extract_text_batch(
    files: List[UploadFile] = File(..., description="Documents à OCR (max 10)"),
    language_hint: Optional[str] = Form(None),
):
    """
    📚 Extraction batch (plusieurs fichiers)
    
    Traite jusqu'à 10 fichiers en une requête.
    """
    if len(files) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 fichiers par batch",
        )
    
    start_time = time.time()
    results: List[OCRResult] = []
    successful = 0
    failed = 0
    
    pipeline = OCRPipeline(enable_fallback=True, fallback_provider="claude")
    
    for file in files:
        try:
            file_bytes = await file.read()
            
            result = await pipeline.auto_ocr(
                file_data=file_bytes,
                filename=file.filename,
                language_hint=language_hint,  # type: ignore
            )
            
            results.append(result)
            
            if result.error:
                failed += 1
            else:
                successful += 1
                
        except Exception as e:
            logger.error(f"Erreur batch OCR {file.filename}: {e}")
            results.append(OCRResult(
                text="",
                language="unknown",
                is_pdf=False,
                pages=0,
                error=str(e),
            ))
            failed += 1
    
    total_time = int((time.time() - start_time) * 1000)
    
    return OCRBatchResponse(
        results=results,
        total=len(files),
        successful=successful,
        failed=failed,
        total_time_ms=total_time,
    )


# ============================================
# ENDPOINTS STATUT ET DÉMO
# ============================================

@router.get("/health")
async def health_check():
    """
    🏥 Vérifier l'état du service OCR
    """
    status = ocr_pipeline.get_status()
    return {
        "status": "healthy" if status["tesseract_available"] else "degraded",
        **status,
    }


@router.get("/status")
async def get_status():
    """
    📊 Statut détaillé du service OCR
    """
    status = ocr_pipeline.get_status()
    
    return {
        **status,
        "endpoints": {
            "/api/ocr/extract": "POST - Extraction OCR (PDF/image)",
            "/api/ocr/extract/quick": "POST - Extraction rapide",
            "/api/ocr/extract/batch": "POST - Extraction batch",
            "/api/ocr/detect-language": "POST - Détection langue",
            "/api/ocr/clean": "POST - Nettoyage texte",
            "/api/ocr/normalize-arabic": "POST - Normalisation arabe",
        },
        "features": {
            "multi_language": True,
            "arabic_rtl": True,
            "pdf_multipage": True,
            "ai_fallback": status["fallback_enabled"],
            "auto_detection": True,
        },
        "limits": {
            "max_file_size_mb": 50,
            "max_batch_files": 10,
            "max_pdf_pages": 100,
        },
    }


@router.get("/demo/arabic")
async def demo_arabic():
    """
    🇩🇿 Démo texte arabe
    
    Exemple de détection et nettoyage de texte arabe.
    """
    sample_text = """
    بسم الله الرحمن الرحيم
    الجمهورية الجزائرية الديمقراطية الشعبية
    وزارة المالية - المديرية العامة للضرائب
    
    إشعار بالدفع رقم: 2024/12345
    المبلغ الإجمالي: 150.000,00 دج
    تاريخ الاستحقاق: 15/01/2025
    """
    
    lang, confidence = detect_language(sample_text)
    cleaned = clean_arabic(sample_text)
    normalized = normalize_arabic(sample_text)
    
    return {
        "demo": "arabic",
        "original": sample_text.strip(),
        "language": lang,
        "confidence": confidence,
        "cleaned": cleaned,
        "normalized": normalized,
        "is_rtl": True,
    }


@router.get("/demo/mixed")
async def demo_mixed():
    """
    🇩🇿🇫🇷 Démo texte mixte (arabe + français)
    
    Exemple de document bilingue algérien.
    """
    sample_text = """
    RÉPUBLIQUE ALGÉRIENNE DÉMOCRATIQUE ET POPULAIRE
    الجمهورية الجزائرية الديمقراطية الشعبية
    
    MINISTÈRE DES FINANCES
    وزارة المالية
    
    Numéro de contribuable (NIF): 123456789012345
    رقم التعريف الجبائي
    
    Montant IRG: 45.000,00 DA
    مبلغ الضريبة على الدخل الإجمالي
    """
    
    lang, confidence = detect_language(sample_text)
    
    return {
        "demo": "mixed",
        "original": sample_text.strip(),
        "language": lang,
        "confidence": confidence,
        "note": "Ce type de document mixte est courant en Algérie",
    }


@router.get("/supported-formats")
async def get_supported_formats():
    """
    📋 Liste des formats supportés
    """
    return {
        "documents": {
            "pdf": {
                "extension": ".pdf",
                "mime_type": "application/pdf",
                "multipage": True,
                "max_pages": 100,
            },
        },
        "images": {
            "png": {"extension": ".png", "mime_type": "image/png"},
            "jpg": {"extension": ".jpg", "mime_type": "image/jpeg"},
            "jpeg": {"extension": ".jpeg", "mime_type": "image/jpeg"},
            "tiff": {"extension": ".tiff", "mime_type": "image/tiff"},
            "bmp": {"extension": ".bmp", "mime_type": "image/bmp"},
            "gif": {"extension": ".gif", "mime_type": "image/gif"},
        },
        "languages": {
            "ar": {"name": "Arabe", "rtl": True, "tesseract_code": "ara"},
            "fr": {"name": "Français", "rtl": False, "tesseract_code": "fra"},
            "en": {"name": "Anglais", "rtl": False, "tesseract_code": "eng"},
        },
    }
