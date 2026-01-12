"""
OCR_DZ - Pipeline OCR Multilingue
=================================
Extraction arabe/français/anglais depuis PDF + images
Tesseract + Fallback IA (Claude Vision / GPT-4o)
"""

import os
import io
import base64
import tempfile
import logging
from pathlib import Path
from typing import Optional, List, Literal, Tuple, Union, BinaryIO
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from .ocr_utils import (
    detect_language,
    clean_arabic,
    clean_french,
    clean_english,
    clean_by_language,
    normalize_arabic,
    merge_pages_text,
    detect_pages_language,
    estimate_confidence,
    LanguageCode,
)

logger = logging.getLogger(__name__)


# ============================================
# CONFIGURATION
# ============================================

class OCREngine(str, Enum):
    """Moteur OCR utilisé"""
    TESSERACT = "tesseract"
    CLAUDE_VISION = "claude_vision"
    GPT4_VISION = "gpt4_vision"
    HYBRID = "hybrid"


class TesseractConfig:
    """Configuration Tesseract pour différentes langues."""
    
    # Configurations PSM (Page Segmentation Mode)
    # 3 = Fully automatic page segmentation
    # 6 = Assume a single uniform block of text
    # 11 = Sparse text (find as much text as possible)
    
    ARABIC = {
        "lang": "ara",
        "config": "--psm 6 --oem 1 -c preserve_interword_spaces=1",
    }
    
    ARABIC_RTL = {
        "lang": "ara",
        "config": "--psm 6 --oem 1 -c preserve_interword_spaces=1 -c textord_force_make_prop_words=F",
    }
    
    FRENCH = {
        "lang": "fra",
        "config": "--psm 6 --oem 1",
    }
    
    ENGLISH = {
        "lang": "eng",
        "config": "--psm 6 --oem 1",
    }
    
    MULTI = {
        "lang": "ara+fra+eng",
        "config": "--psm 6 --oem 1 -c preserve_interword_spaces=1",
    }
    
    # Pour les PDF scannés de mauvaise qualité
    LOW_QUALITY = {
        "lang": "ara+fra+eng",
        "config": "--psm 11 --oem 1 -c tessedit_do_invert=0",
    }


# ============================================
# MODÈLES DE DONNÉES
# ============================================

class PageOCRResult(BaseModel):
    """Résultat OCR pour une page."""
    page_number: int = Field(..., ge=1)
    text: str
    language: LanguageCode
    confidence: float = Field(..., ge=0.0, le=1.0)
    engine: OCREngine = OCREngine.TESSERACT


class OCRResult(BaseModel):
    """Résultat OCR complet."""
    # Texte extrait
    text: str = Field(..., description="Texte extrait complet")
    
    # Métadonnées
    language: LanguageCode = Field("unknown", description="Langue détectée")
    language_name: str = Field("Inconnu", description="Nom de la langue")
    confidence: float = Field(0.0, ge=0.0, le=1.0, description="Confiance OCR")
    
    # Informations fichier
    is_pdf: bool = Field(False, description="Est un PDF")
    pages: int = Field(1, ge=1, description="Nombre de pages")
    
    # Moteur utilisé
    engine: OCREngine = Field(OCREngine.TESSERACT, description="Moteur OCR utilisé")
    fallback_used: bool = Field(False, description="Fallback IA utilisé")
    
    # Détails par page (optionnel)
    pages_detail: Optional[List[PageOCRResult]] = Field(None, description="Détails par page")
    
    # Métadonnées extraites
    extracted_dates: List[str] = Field(default_factory=list, description="Dates extraites")
    extracted_amounts: List[str] = Field(default_factory=list, description="Montants extraits")
    
    # Timing
    processing_time_ms: int = Field(0, description="Temps de traitement en ms")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Erreurs
    error: Optional[str] = Field(None, description="Message d'erreur si échec")
    warnings: List[str] = Field(default_factory=list, description="Avertissements")


# ============================================
# CLASSE PRINCIPALE OCR PIPELINE
# ============================================

class OCRPipeline:
    """
    Pipeline OCR multilingue pour l'Algérie.
    
    Supporte:
    - Images (PNG, JPG, TIFF, BMP)
    - PDF (multipages)
    - Arabe, Français, Anglais
    - Fallback IA si OCR classique échoue
    """
    
    # Seuil de confiance pour activer le fallback IA
    CONFIDENCE_THRESHOLD = 0.35
    
    def __init__(
        self,
        tesseract_path: Optional[str] = None,
        poppler_path: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
        default_language: LanguageCode = "fr",
        enable_fallback: bool = True,
        fallback_provider: Literal["claude", "openai"] = "claude",
    ):
        """
        Initialiser le pipeline OCR.
        
        Args:
            tesseract_path: Chemin vers Tesseract (auto-détecté si None)
            poppler_path: Chemin vers Poppler pour PDF (auto-détecté si None)
            openai_api_key: Clé API OpenAI pour GPT-4 Vision
            anthropic_api_key: Clé API Anthropic pour Claude Vision
            default_language: Langue par défaut
            enable_fallback: Activer le fallback IA
            fallback_provider: Provider pour le fallback (claude ou openai)
        """
        self.tesseract_path = tesseract_path
        self.poppler_path = poppler_path
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.default_language = default_language
        self.enable_fallback = enable_fallback
        self.fallback_provider = fallback_provider
        
        # Configurer Tesseract si chemin fourni
        if tesseract_path:
            os.environ["TESSERACT_CMD"] = tesseract_path
        
        # Vérifier la disponibilité des outils
        self._check_dependencies()
    
    def _check_dependencies(self) -> None:
        """Vérifier les dépendances disponibles."""
        self.tesseract_available = False
        self.pdf_available = False
        
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            self.tesseract_available = True
            logger.info("Tesseract OCR disponible")
        except Exception as e:
            logger.warning(f"Tesseract non disponible: {e}")
        
        try:
            from pdf2image import convert_from_bytes
            self.pdf_available = True
            logger.info("pdf2image disponible")
        except ImportError:
            logger.warning("pdf2image non disponible")
    
    # ============================================
    # EXTRACTION IMAGE
    # ============================================
    
    def extract_text_from_image(
        self,
        image: "Image.Image",
        language_hint: Optional[LanguageCode] = None,
        config: Optional[dict] = None,
    ) -> PageOCRResult:
        """
        Extraire le texte d'une image avec Tesseract.
        
        Args:
            image: Image PIL
            language_hint: Indice sur la langue (ara, fra, eng)
            config: Configuration Tesseract personnalisée
        
        Returns:
            PageOCRResult avec texte et métadonnées
        """
        from PIL import Image
        import pytesseract
        
        # Prétraitement de l'image
        processed_image = self._preprocess_image(image)
        
        # Sélectionner la config Tesseract
        if config:
            tess_config = config
        elif language_hint == "ar":
            tess_config = TesseractConfig.ARABIC_RTL
        elif language_hint == "fr":
            tess_config = TesseractConfig.FRENCH
        elif language_hint == "en":
            tess_config = TesseractConfig.ENGLISH
        else:
            # Multi-langue par défaut
            tess_config = TesseractConfig.MULTI
        
        try:
            # OCR avec Tesseract
            text = pytesseract.image_to_string(
                processed_image,
                lang=tess_config["lang"],
                config=tess_config["config"],
            )
            
            # Détecter la langue du résultat
            detected_lang, lang_conf = detect_language(text)
            
            # Si arabe détecté, re-OCR avec config arabe optimisée
            if detected_lang == "ar" and language_hint != "ar":
                text_ar = pytesseract.image_to_string(
                    processed_image,
                    lang=TesseractConfig.ARABIC_RTL["lang"],
                    config=TesseractConfig.ARABIC_RTL["config"],
                )
                if len(text_ar) > len(text) * 0.8:
                    text = text_ar
            
            # Nettoyer le texte
            text = clean_by_language(text, detected_lang)
            
            # Estimer la confiance
            confidence = estimate_confidence(text, detected_lang)
            
            return PageOCRResult(
                page_number=1,
                text=text,
                language=detected_lang,
                confidence=confidence,
                engine=OCREngine.TESSERACT,
            )
            
        except Exception as e:
            logger.error(f"Erreur OCR Tesseract: {e}")
            return PageOCRResult(
                page_number=1,
                text="",
                language="unknown",
                confidence=0.0,
                engine=OCREngine.TESSERACT,
            )
    
    def _preprocess_image(self, image: "Image.Image") -> "Image.Image":
        """
        Prétraitement de l'image pour améliorer l'OCR.
        
        - Conversion en niveaux de gris
        - Redimensionnement si trop petit
        - Amélioration du contraste
        - Binarisation adaptative
        """
        from PIL import Image, ImageEnhance, ImageFilter
        
        # Convertir en RGB si nécessaire
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convertir en niveaux de gris
        gray = image.convert('L')
        
        # Redimensionner si l'image est trop petite
        width, height = gray.size
        if width < 1000 or height < 1000:
            scale = max(1000 / width, 1000 / height)
            new_size = (int(width * scale), int(height * scale))
            gray = gray.resize(new_size, Image.Resampling.LANCZOS)
        
        # Améliorer le contraste
        enhancer = ImageEnhance.Contrast(gray)
        gray = enhancer.enhance(1.5)
        
        # Améliorer la netteté
        gray = gray.filter(ImageFilter.SHARPEN)
        
        return gray
    
    # ============================================
    # EXTRACTION PDF
    # ============================================
    
    def extract_text_from_pdf(
        self,
        pdf_data: Union[bytes, BinaryIO, str, Path],
        language_hint: Optional[LanguageCode] = None,
        max_pages: Optional[int] = None,
        dpi: int = 300,
    ) -> OCRResult:
        """
        Extraire le texte d'un PDF (scanné ou non).
        
        Args:
            pdf_data: Données PDF (bytes, file-like, ou chemin)
            language_hint: Indice sur la langue
            max_pages: Nombre max de pages à traiter
            dpi: Résolution pour conversion en image
        
        Returns:
            OCRResult complet
        """
        import time
        start_time = time.time()
        
        from pdf2image import convert_from_bytes, convert_from_path
        from PIL import Image
        
        # Charger le PDF
        try:
            if isinstance(pdf_data, (str, Path)):
                images = convert_from_path(
                    str(pdf_data),
                    dpi=dpi,
                    poppler_path=self.poppler_path,
                )
            elif isinstance(pdf_data, bytes):
                images = convert_from_bytes(
                    pdf_data,
                    dpi=dpi,
                    poppler_path=self.poppler_path,
                )
            else:
                # File-like object
                pdf_bytes = pdf_data.read()
                images = convert_from_bytes(
                    pdf_bytes,
                    dpi=dpi,
                    poppler_path=self.poppler_path,
                )
        except Exception as e:
            logger.error(f"Erreur conversion PDF: {e}")
            return OCRResult(
                text="",
                language="unknown",
                is_pdf=True,
                pages=0,
                error=f"Erreur conversion PDF: {str(e)}",
            )
        
        # Limiter le nombre de pages
        if max_pages:
            images = images[:max_pages]
        
        total_pages = len(images)
        pages_results: List[PageOCRResult] = []
        warnings: List[str] = []
        
        # OCR page par page
        for i, img in enumerate(images, 1):
            logger.info(f"OCR page {i}/{total_pages}")
            
            page_result = self.extract_text_from_image(img, language_hint)
            page_result.page_number = i
            pages_results.append(page_result)
            
            # Vérifier si fallback nécessaire
            if page_result.confidence < self.CONFIDENCE_THRESHOLD and self.enable_fallback:
                warnings.append(f"Page {i}: confiance faible ({page_result.confidence:.2f})")
        
        # Fusionner les résultats
        texts = [p.text for p in pages_results]
        merged_text = merge_pages_text(texts)
        
        # Détecter la langue dominante
        dominant_lang, avg_confidence = detect_pages_language(texts)
        
        # Vérifier si fallback nécessaire globalement
        fallback_used = False
        if avg_confidence < self.CONFIDENCE_THRESHOLD and self.enable_fallback:
            # Tenter le fallback IA sur les pages à faible confiance
            for i, page_result in enumerate(pages_results):
                if page_result.confidence < self.CONFIDENCE_THRESHOLD:
                    try:
                        img_bytes = self._image_to_bytes(images[i])
                        fallback_result = self.fallback_llm_ocr(img_bytes)
                        if fallback_result and len(fallback_result) > len(page_result.text) * 0.5:
                            pages_results[i].text = fallback_result
                            pages_results[i].engine = (
                                OCREngine.CLAUDE_VISION 
                                if self.fallback_provider == "claude" 
                                else OCREngine.GPT4_VISION
                            )
                            fallback_used = True
                    except Exception as e:
                        logger.warning(f"Fallback échoué page {i+1}: {e}")
            
            # Refusionner si fallback utilisé
            if fallback_used:
                texts = [p.text for p in pages_results]
                merged_text = merge_pages_text(texts)
                dominant_lang, avg_confidence = detect_pages_language(texts)
        
        # Extraire les métadonnées
        from .ocr_utils import extract_dates_dz, extract_amounts_dzd
        dates = extract_dates_dz(merged_text)
        amounts = [a[0] for a in extract_amounts_dzd(merged_text)]
        
        # Calculer le temps de traitement
        processing_time = int((time.time() - start_time) * 1000)
        
        return OCRResult(
            text=merged_text,
            language=dominant_lang,
            language_name=self._get_language_name(dominant_lang),
            confidence=avg_confidence,
            is_pdf=True,
            pages=total_pages,
            engine=OCREngine.HYBRID if fallback_used else OCREngine.TESSERACT,
            fallback_used=fallback_used,
            pages_detail=pages_results,
            extracted_dates=dates[:10],
            extracted_amounts=amounts[:10],
            processing_time_ms=processing_time,
            warnings=warnings,
        )
    
    def _image_to_bytes(self, image: "Image.Image") -> bytes:
        """Convertir une image PIL en bytes."""
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()
    
    # ============================================
    # FALLBACK LLM OCR (Vision IA)
    # ============================================
    
    async def fallback_llm_ocr_async(
        self,
        image_bytes: bytes,
        language_hint: Optional[LanguageCode] = None,
    ) -> Optional[str]:
        """
        OCR via LLM Vision (Claude ou GPT-4) - Version async.
        
        Args:
            image_bytes: Image en bytes
            language_hint: Indice sur la langue attendue
        
        Returns:
            Texte extrait ou None si échec
        """
        if self.fallback_provider == "claude":
            return await self._claude_vision_ocr(image_bytes, language_hint)
        else:
            return await self._gpt4_vision_ocr(image_bytes, language_hint)
    
    def fallback_llm_ocr(
        self,
        image_bytes: bytes,
        language_hint: Optional[LanguageCode] = None,
    ) -> Optional[str]:
        """
        OCR via LLM Vision - Version synchrone.
        """
        import asyncio
        
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Dans un contexte async existant
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        asyncio.run,
                        self.fallback_llm_ocr_async(image_bytes, language_hint)
                    )
                    return future.result(timeout=60)
            else:
                return loop.run_until_complete(
                    self.fallback_llm_ocr_async(image_bytes, language_hint)
                )
        except Exception as e:
            logger.error(f"Erreur fallback LLM OCR: {e}")
            return None
    
    async def _claude_vision_ocr(
        self,
        image_bytes: bytes,
        language_hint: Optional[LanguageCode] = None,
    ) -> Optional[str]:
        """OCR via Claude Vision."""
        if not self.anthropic_api_key:
            logger.warning("Clé Anthropic non configurée pour fallback")
            return None
        
        try:
            import anthropic
            
            client = anthropic.AsyncAnthropic(api_key=self.anthropic_api_key)
            
            # Encoder l'image en base64
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Construire le prompt selon la langue
            lang_instruction = ""
            if language_hint == "ar":
                lang_instruction = "Le document est probablement en arabe. "
            elif language_hint == "fr":
                lang_instruction = "Le document est probablement en français. "
            
            prompt = f"""Tu es un expert en OCR (reconnaissance optique de caractères).
{lang_instruction}
Extrais TOUT le texte visible dans cette image, en préservant:
- La structure des paragraphes
- L'ordre de lecture (droite à gauche pour l'arabe)
- Les nombres et dates
- La ponctuation

Retourne UNIQUEMENT le texte extrait, sans commentaires ni explications.
Si le texte est en arabe, retourne-le en arabe.
Si le texte est mixte (arabe/français), préserve les deux langues."""

            response = await client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_b64,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt,
                            },
                        ],
                    }
                ],
            )
            
            text = response.content[0].text
            return clean_by_language(text, language_hint or "unknown")
            
        except Exception as e:
            logger.error(f"Erreur Claude Vision: {e}")
            return None
    
    async def _gpt4_vision_ocr(
        self,
        image_bytes: bytes,
        language_hint: Optional[LanguageCode] = None,
    ) -> Optional[str]:
        """OCR via GPT-4 Vision."""
        if not self.openai_api_key:
            logger.warning("Clé OpenAI non configurée pour fallback")
            return None
        
        try:
            from openai import AsyncOpenAI
            
            client = AsyncOpenAI(api_key=self.openai_api_key)
            
            # Encoder l'image en base64
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Construire le prompt
            lang_instruction = ""
            if language_hint == "ar":
                lang_instruction = "Le document est probablement en arabe. "
            elif language_hint == "fr":
                lang_instruction = "Le document est probablement en français. "
            
            prompt = f"""Tu es un expert en OCR.
{lang_instruction}
Extrais TOUT le texte visible dans cette image.
Préserve la structure et l'ordre de lecture.
Retourne UNIQUEMENT le texte, sans commentaires."""

            response = await client.chat.completions.create(
                model="gpt-4o",
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_b64}",
                                },
                            },
                        ],
                    }
                ],
            )
            
            text = response.choices[0].message.content or ""
            return clean_by_language(text, language_hint or "unknown")
            
        except Exception as e:
            logger.error(f"Erreur GPT-4 Vision: {e}")
            return None
    
    # ============================================
    # AUTO OCR (DÉTECTION AUTOMATIQUE)
    # ============================================
    
    async def auto_ocr(
        self,
        file_data: Union[bytes, BinaryIO],
        filename: Optional[str] = None,
        language_hint: Optional[LanguageCode] = None,
    ) -> OCRResult:
        """
        OCR automatique avec détection du type de fichier.
        
        - Détecte si image ou PDF
        - Applique l'OCR approprié
        - Fallback IA si confiance faible
        
        Args:
            file_data: Données du fichier
            filename: Nom du fichier (pour détecter le type)
            language_hint: Indice sur la langue
        
        Returns:
            OCRResult complet
        """
        import time
        from PIL import Image
        
        start_time = time.time()
        
        # Lire les bytes
        if hasattr(file_data, 'read'):
            file_bytes = file_data.read()
        else:
            file_bytes = file_data
        
        # Détecter le type de fichier
        is_pdf = self._is_pdf(file_bytes, filename)
        
        if is_pdf:
            # Traiter comme PDF
            result = self.extract_text_from_pdf(file_bytes, language_hint)
        else:
            # Traiter comme image
            try:
                image = Image.open(io.BytesIO(file_bytes))
                page_result = self.extract_text_from_image(image, language_hint)
                
                # Vérifier si fallback nécessaire
                fallback_used = False
                if page_result.confidence < self.CONFIDENCE_THRESHOLD and self.enable_fallback:
                    fallback_text = await self.fallback_llm_ocr_async(file_bytes, language_hint)
                    if fallback_text and len(fallback_text) > len(page_result.text) * 0.5:
                        page_result.text = fallback_text
                        page_result.engine = (
                            OCREngine.CLAUDE_VISION
                            if self.fallback_provider == "claude"
                            else OCREngine.GPT4_VISION
                        )
                        fallback_used = True
                        # Recalculer confiance
                        lang, _ = detect_language(fallback_text)
                        page_result.language = lang
                        page_result.confidence = estimate_confidence(fallback_text, lang)
                
                # Extraire les métadonnées
                from .ocr_utils import extract_dates_dz, extract_amounts_dzd
                dates = extract_dates_dz(page_result.text)
                amounts = [a[0] for a in extract_amounts_dzd(page_result.text)]
                
                result = OCRResult(
                    text=page_result.text,
                    language=page_result.language,
                    language_name=self._get_language_name(page_result.language),
                    confidence=page_result.confidence,
                    is_pdf=False,
                    pages=1,
                    engine=page_result.engine,
                    fallback_used=fallback_used,
                    pages_detail=[page_result],
                    extracted_dates=dates[:10],
                    extracted_amounts=amounts[:10],
                    processing_time_ms=int((time.time() - start_time) * 1000),
                )
                
            except Exception as e:
                logger.error(f"Erreur OCR image: {e}")
                result = OCRResult(
                    text="",
                    language="unknown",
                    is_pdf=False,
                    pages=0,
                    error=f"Erreur OCR: {str(e)}",
                    processing_time_ms=int((time.time() - start_time) * 1000),
                )
        
        return result
    
    def _is_pdf(self, data: bytes, filename: Optional[str] = None) -> bool:
        """Détecter si le fichier est un PDF."""
        # Vérifier le magic number
        if data[:4] == b'%PDF':
            return True
        
        # Vérifier l'extension
        if filename:
            return filename.lower().endswith('.pdf')
        
        return False
    
    def _get_language_name(self, code: LanguageCode) -> str:
        """Obtenir le nom de la langue."""
        names = {
            "ar": "Arabe",
            "fr": "Français",
            "en": "Anglais",
            "mixed": "Mixte (Arabe/Français)",
            "unknown": "Inconnu",
        }
        return names.get(code, "Inconnu")
    
    # ============================================
    # UTILITAIRES
    # ============================================
    
    def get_status(self) -> dict:
        """Obtenir le statut du pipeline OCR."""
        return {
            "service": "OCR_DZ",
            "version": "1.0.0",
            "tesseract_available": self.tesseract_available,
            "pdf_available": self.pdf_available,
            "fallback_enabled": self.enable_fallback,
            "fallback_provider": self.fallback_provider,
            "openai_configured": bool(self.openai_api_key),
            "anthropic_configured": bool(self.anthropic_api_key),
            "supported_formats": ["pdf", "png", "jpg", "jpeg", "tiff", "bmp", "gif"],
            "supported_languages": ["ar", "fr", "en"],
        }


# ============================================
# INSTANCE GLOBALE
# ============================================

ocr_pipeline = OCRPipeline()
