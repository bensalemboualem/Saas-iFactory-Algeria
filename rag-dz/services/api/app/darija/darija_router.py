"""
DARIJA_NLP - Router FastAPI
===========================
Endpoints NLP pour la darija algérienne
Normalisation, Arabizi→Arabe, Détection dialecte
"""

import logging
from typing import Optional, List
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from .darija_cleaner import (
    clean_text,
    clean_noise,
    tokenize_arabic,
    tokenize_sentences,
    has_arabic,
    get_arabic_ratio,
)
from .darija_arabizi import (
    arabizi_to_arabic,
    is_arabizi,
    get_arabizi_score,
    get_arabizi_examples,
    DARIJA_WORDS,
)
from .darija_normalizer import (
    normalize_darija,
    detect_dialect,
    DarijaNormalizer,
    NormalizationResult,
    DetectionResult,
    DialectType,
    NormalizationLevel,
    get_dialect_name,
    get_normalization_examples,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/darija", tags=["Darija NLP"])


# ============================================
# REQUEST/RESPONSE MODELS
# ============================================

class NormalizeRequest(BaseModel):
    """Requête de normalisation."""
    text: str = Field(..., min_length=1, max_length=10000, description="Texte à normaliser")
    convert_arabizi: bool = Field(True, description="Convertir l'arabizi en arabe")
    remove_harakat: bool = Field(True, description="Supprimer les diacritiques")
    level: Optional[str] = Field("medium", description="Niveau: light, medium, full, aggressive")


class ArabiziRequest(BaseModel):
    """Requête de conversion arabizi."""
    text: str = Field(..., min_length=1, max_length=10000, description="Texte arabizi")
    use_dictionary: bool = Field(True, description="Utiliser le dictionnaire darija")


class CleanRequest(BaseModel):
    """Requête de nettoyage."""
    text: str = Field(..., min_length=1, max_length=10000)
    remove_emojis: bool = Field(True)
    remove_urls: bool = Field(True)
    remove_noise: bool = Field(True)
    reduce_repeats: bool = Field(True)


class DetectRequest(BaseModel):
    """Requête de détection."""
    text: str = Field(..., min_length=1, max_length=10000)


class TokenizeRequest(BaseModel):
    """Requête de tokenisation."""
    text: str = Field(..., min_length=1, max_length=10000)
    keep_punctuation: bool = Field(False)


class BatchNormalizeRequest(BaseModel):
    """Requête de normalisation batch."""
    texts: List[str] = Field(..., min_items=1, max_items=100)
    convert_arabizi: bool = Field(True)


# Responses
class ArabiziResponse(BaseModel):
    """Réponse conversion arabizi."""
    original: str
    arabic: str
    is_arabizi: bool
    arabizi_score: float
    words_converted: int


class CleanResponse(BaseModel):
    """Réponse nettoyage."""
    original: str
    cleaned: str
    characters_removed: int
    words_count: int


class TokenizeResponse(BaseModel):
    """Réponse tokenisation."""
    text: str
    tokens: List[str]
    sentences: List[str]
    word_count: int
    sentence_count: int


class BatchNormalizeResponse(BaseModel):
    """Réponse normalisation batch."""
    results: List[NormalizationResult]
    total: int
    total_time_ms: int


# ============================================
# ENDPOINTS PRINCIPAUX
# ============================================

@router.post("/normalize", response_model=NormalizationResult)
async def normalize_text(request: NormalizeRequest):
    """
    📝 Normaliser un texte darija
    
    Pipeline complet:
    1. Nettoyage (bruit, répétitions, URLs, emojis)
    2. Détection du dialecte (darija/arabizi/MSA/français)
    3. Conversion arabizi → arabe (si activé)
    4. Normalisation caractères arabes
    5. Tokenisation
    
    **Exemples d'entrées:**
    - "salam khoya kifach rak" → "سلام خويا كيفاش راك"
    - "wach dayer lyoum" → "واش داير ليوم"
    - "n7eb ndir tasjil CNAS" → "نحب ندير تسجيل كناس"
    
    **Langues supportées:**
    - 🇩🇿 Darija (arabe algérien)
    - 🔤 Arabizi (darija en caractères latins)
    - 📖 Arabe standard (MSA)
    - 🇫🇷 Français
    - Mélange de langues
    """
    try:
        # Créer le normaliseur avec les options
        level = NormalizationLevel.MEDIUM
        if request.level:
            try:
                level = NormalizationLevel(request.level.lower())
            except ValueError:
                pass
        
        normalizer = DarijaNormalizer(
            level=level,
            convert_arabizi=request.convert_arabizi,
            remove_harakat_flag=request.remove_harakat,
        )
        
        result = normalizer.normalize(request.text)
        return result
        
    except Exception as e:
        logger.error(f"Erreur normalisation: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la normalisation: {str(e)}",
        )


@router.post("/normalize/quick")
async def normalize_quick(request: NormalizeRequest):
    """
    ⚡ Normalisation rapide (résultat simplifié)
    """
    result = normalize_darija(request.text)
    
    return {
        "original": result.original,
        "normalized": result.normalized,
        "dialect": result.dialect.value,
        "is_arabizi": result.is_arabizi,
        "word_count": result.word_count,
    }


@router.post("/normalize/batch", response_model=BatchNormalizeResponse)
async def normalize_batch(request: BatchNormalizeRequest):
    """
    📚 Normaliser plusieurs textes en batch
    """
    import time
    start_time = time.time()
    
    normalizer = DarijaNormalizer(convert_arabizi=request.convert_arabizi)
    results = normalizer.normalize_batch(request.texts)
    
    total_time = int((time.time() - start_time) * 1000)
    
    return BatchNormalizeResponse(
        results=results,
        total=len(results),
        total_time_ms=total_time,
    )


# ============================================
# ENDPOINTS DÉTECTION
# ============================================

@router.post("/detect", response_model=DetectionResult)
async def detect_text_dialect(request: DetectRequest):
    """
    🔍 Détecter le dialecte d'un texte
    
    Analyse le texte et retourne:
    - Dialecte détecté (darija, arabizi, msa, french, english, mixed)
    - Langue (ar-dz, ar, fr, en, mixed)
    - Confiance (0-1)
    - Signaux de détection
    
    **Exemples:**
    - "salam khoya" → arabizi (ar-dz-latn)
    - "كيفاش ندير" → darija (ar-dz)
    - "Comment ça va" → french (fr)
    """
    return detect_dialect(request.text)


@router.get("/detect")
async def detect_dialect_get(
    text: str = Query(..., min_length=1, description="Texte à analyser"),
):
    """
    🔍 Détecter le dialecte (GET)
    """
    result = detect_dialect(text)
    
    return {
        "dialect": result.dialect.value,
        "dialect_name": get_dialect_name(result.dialect),
        "language": result.language,
        "confidence": result.confidence,
        "is_arabizi": result.is_arabizi,
        "arabic_ratio": result.arabic_ratio,
        "signals": result.signals,
    }


# ============================================
# ENDPOINTS ARABIZI
# ============================================

@router.post("/arabizi", response_model=ArabiziResponse)
async def convert_arabizi(request: ArabiziRequest):
    """
    🔤→🔠 Convertir de l'arabizi en arabe
    
    Conversion des caractères latins en arabe:
    - kh → خ
    - gh → غ
    - ch → ش
    - 3 → ع
    - 7 → ح
    - 9 → ق
    
    **Exemples:**
    - "salam khoya" → "سلام خويا"
    - "3andi mochkil" → "عندي مشكل"
    - "kifach ndir" → "كيفاش ندير"
    """
    original = request.text
    arabic = arabizi_to_arabic(original, use_dictionary=request.use_dictionary)
    
    # Compter les mots convertis
    original_words = original.lower().split()
    darija_words = [w for w in original_words if w in DARIJA_WORDS]
    
    return ArabiziResponse(
        original=original,
        arabic=arabic,
        is_arabizi=is_arabizi(original),
        arabizi_score=get_arabizi_score(original),
        words_converted=len(darija_words),
    )


@router.get("/arabizi")
async def convert_arabizi_get(
    text: str = Query(..., min_length=1, description="Texte arabizi"),
):
    """
    🔤→🔠 Convertir arabizi (GET)
    """
    arabic = arabizi_to_arabic(text)
    
    return {
        "original": text,
        "arabic": arabic,
        "is_arabizi": is_arabizi(text),
    }


# ============================================
# ENDPOINTS NETTOYAGE
# ============================================

@router.post("/clean", response_model=CleanResponse)
async def clean_text_endpoint(request: CleanRequest):
    """
    🧹 Nettoyer un texte
    
    - Supprimer les emojis
    - Supprimer les URLs
    - Supprimer le bruit (hhh, lol, mdr)
    - Réduire les répétitions (salammmm → salam)
    - Normaliser les espaces
    """
    original = request.text
    cleaned = clean_text(
        original,
        remove_emojis_flag=request.remove_emojis,
        remove_urls_flag=request.remove_urls,
        remove_noise=request.remove_noise,
        reduce_repeats=request.reduce_repeats,
    )
    
    return CleanResponse(
        original=original,
        cleaned=cleaned,
        characters_removed=len(original) - len(cleaned),
        words_count=len(cleaned.split()),
    )


# ============================================
# ENDPOINTS TOKENISATION
# ============================================

@router.post("/tokenize", response_model=TokenizeResponse)
async def tokenize_text(request: TokenizeRequest):
    """
    ✂️ Tokeniser un texte arabe/darija
    
    Segmentation en:
    - Mots (tokens)
    - Phrases (sentences)
    """
    tokens = tokenize_arabic(request.text, keep_punctuation=request.keep_punctuation)
    sentences = tokenize_sentences(request.text)
    
    return TokenizeResponse(
        text=request.text,
        tokens=tokens,
        sentences=sentences,
        word_count=len(tokens),
        sentence_count=len(sentences),
    )


# ============================================
# ENDPOINTS STATUT ET DÉMO
# ============================================

@router.get("/health")
async def health_check():
    """
    🏥 Vérifier l'état du service Darija NLP
    """
    return {
        "status": "healthy",
        "service": "DARIJA_NLP",
        "version": "1.0.0",
        "features": {
            "normalization": True,
            "arabizi_conversion": True,
            "dialect_detection": True,
            "tokenization": True,
            "cleaning": True,
        },
    }


@router.get("/status")
async def get_status():
    """
    📊 Statut détaillé du service
    """
    return {
        "service": "DARIJA_NLP",
        "version": "1.0.0",
        "description": "Premier moteur NLP pour la darija algérienne",
        "endpoints": {
            "/api/darija/normalize": "POST - Normalisation complète",
            "/api/darija/normalize/quick": "POST - Normalisation rapide",
            "/api/darija/normalize/batch": "POST - Normalisation batch",
            "/api/darija/detect": "POST/GET - Détection dialecte",
            "/api/darija/arabizi": "POST/GET - Conversion arabizi",
            "/api/darija/clean": "POST - Nettoyage texte",
            "/api/darija/tokenize": "POST - Tokenisation",
        },
        "supported_dialects": [
            {"code": "darija", "name": "Darija (Arabe algérien)", "script": "arabe"},
            {"code": "arabizi", "name": "Arabizi", "script": "latin"},
            {"code": "msa", "name": "Arabe standard moderne", "script": "arabe"},
            {"code": "french", "name": "Français", "script": "latin"},
            {"code": "mixed", "name": "Mixte", "script": "mixed"},
        ],
        "dictionary_size": len(DARIJA_WORDS),
        "arabizi_patterns": 35,
    }


@router.get("/dictionary")
async def get_dictionary(
    limit: int = Query(50, ge=1, le=500, description="Nombre max de mots"),
    search: Optional[str] = Query(None, description="Rechercher un mot"),
):
    """
    📖 Consulter le dictionnaire darija
    """
    words = list(DARIJA_WORDS.items())
    
    if search:
        search_lower = search.lower()
        words = [
            (k, v) for k, v in words 
            if search_lower in k.lower() or search_lower in v
        ]
    
    words = words[:limit]
    
    return {
        "words": [{"arabizi": k, "arabic": v} for k, v in words],
        "total": len(words),
        "dictionary_total": len(DARIJA_WORDS),
    }


@router.get("/demo/normalize")
async def demo_normalize():
    """
    🎯 Démo normalisation
    
    Exemples de normalisation darija.
    """
    examples = get_normalization_examples()
    results = []
    
    for ex in examples:
        result = normalize_darija(ex["input"])
        results.append({
            "input": ex["input"],
            "expected": ex["output"],
            "actual": result.normalized,
            "match": result.normalized == ex["output"],
            "dialect": result.dialect.value,
            "confidence": result.confidence,
        })
    
    return {
        "demo": "normalize",
        "examples": results,
        "success_rate": sum(1 for r in results if r["match"]) / len(results) if results else 0,
    }


@router.get("/demo/arabizi")
async def demo_arabizi():
    """
    🎯 Démo conversion arabizi
    """
    examples = get_arabizi_examples()
    results = []
    
    for arabizi, expected in examples:
        actual = arabizi_to_arabic(arabizi)
        results.append({
            "arabizi": arabizi,
            "expected": expected,
            "actual": actual,
            "match": actual == expected,
        })
    
    return {
        "demo": "arabizi",
        "examples": results,
        "success_rate": sum(1 for r in results if r["match"]) / len(results) if results else 0,
    }


@router.get("/demo/detect")
async def demo_detect():
    """
    🎯 Démo détection dialecte
    """
    examples = [
        {"text": "salam khoya kifach rak", "expected": "arabizi"},
        {"text": "كيفاش راك اليوم", "expected": "darija"},
        {"text": "Comment allez-vous aujourd'hui", "expected": "french"},
        {"text": "How are you today", "expected": "english"},
        {"text": "إن شاء الله سوف نلتقي غداً", "expected": "msa"},
        {"text": "wach rak bien khouya", "expected": "arabizi"},
    ]
    
    results = []
    for ex in examples:
        detection = detect_dialect(ex["text"])
        results.append({
            "text": ex["text"],
            "expected": ex["expected"],
            "detected": detection.dialect.value,
            "match": detection.dialect.value == ex["expected"],
            "confidence": detection.confidence,
            "signals": detection.signals,
        })
    
    return {
        "demo": "detect",
        "examples": results,
        "success_rate": sum(1 for r in results if r["match"]) / len(results) if results else 0,
    }


@router.get("/examples")
async def get_examples():
    """
    📚 Exemples d'utilisation
    """
    return {
        "normalize": {
            "endpoint": "POST /api/darija/normalize",
            "request": {
                "text": "salam khoya kifach ndir tasjil casnos",
                "convert_arabizi": True,
            },
            "response": {
                "normalized": "سلام خويا كيفاش ندير تسجيل كاسنوس",
                "dialect": "arabizi",
                "is_arabizi": True,
            },
        },
        "detect": {
            "endpoint": "POST /api/darija/detect",
            "request": {"text": "wach rak lyoum"},
            "response": {
                "dialect": "arabizi",
                "language": "ar-dz-latn",
                "confidence": 0.8,
            },
        },
        "arabizi": {
            "endpoint": "POST /api/darija/arabizi",
            "request": {"text": "3andi mochkil m3a lkhedma"},
            "response": {
                "arabic": "عندي مشكل مع الخدمة",
                "is_arabizi": True,
            },
        },
    }
