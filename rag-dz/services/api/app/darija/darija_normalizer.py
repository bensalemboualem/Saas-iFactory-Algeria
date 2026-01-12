"""
DARIJA_NLP - Normaliseur Principal
===================================
Pipeline complet de normalisation pour la darija algérienne
Clean → Detect → Convert → Normalize → Segment
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime

from pydantic import BaseModel, Field

from .darija_cleaner import (
    clean_text,
    clean_noise,
    tokenize_arabic,
    tokenize_sentences,
    has_arabic,
    has_latin,
    get_arabic_ratio,
    normalize_arabic_chars,
    remove_harakat,
    normalize_punctuation,
    normalize_numbers_arabic,
)
from .darija_arabizi import (
    arabizi_to_arabic,
    is_arabizi,
    get_arabizi_score,
    DARIJA_WORDS,
)


# ============================================
# TYPES ET ENUMS
# ============================================

class DialectType(str, Enum):
    """Type de dialecte/langue détecté."""
    DARIJA = "darija"           # Arabe algérien (en arabe)
    ARABIZI = "arabizi"         # Arabe algérien (en latin)
    MSA = "msa"                 # Arabe standard moderne
    FRENCH = "french"           # Français
    MIXED = "mixed"             # Mélange
    ENGLISH = "english"         # Anglais
    UNKNOWN = "unknown"         # Inconnu


class NormalizationLevel(str, Enum):
    """Niveau de normalisation appliqué."""
    NONE = "none"
    LIGHT = "light"       # Nettoyage basique
    MEDIUM = "medium"     # + Normalisation caractères
    FULL = "full"         # + Conversion arabizi
    AGGRESSIVE = "aggressive"  # + Suppression harakat


# ============================================
# MODÈLES DE DONNÉES
# ============================================

class NormalizationResult(BaseModel):
    """Résultat de la normalisation darija."""
    
    # Texte
    original: str = Field(..., description="Texte original")
    cleaned: str = Field(..., description="Texte nettoyé")
    normalized: str = Field(..., description="Texte normalisé")
    
    # Détection
    dialect: DialectType = Field(DialectType.UNKNOWN, description="Dialecte détecté")
    is_arabizi: bool = Field(False, description="Est en arabizi")
    language: str = Field("unknown", description="Langue principale")
    
    # Tokens
    tokens: List[str] = Field(default_factory=list, description="Mots tokenisés")
    sentences: List[str] = Field(default_factory=list, description="Phrases")
    
    # Métriques
    arabic_ratio: float = Field(0.0, description="Ratio de caractères arabes")
    word_count: int = Field(0, description="Nombre de mots")
    confidence: float = Field(0.0, description="Confiance de la détection")
    
    # Conversion
    arabizi_converted: bool = Field(False, description="Arabizi a été converti")
    darija_words_found: List[str] = Field(default_factory=list, description="Mots darija détectés")
    
    # Métadonnées
    level: NormalizationLevel = Field(NormalizationLevel.MEDIUM)
    processing_time_ms: int = Field(0)


class DetectionResult(BaseModel):
    """Résultat de la détection de dialecte."""
    dialect: DialectType
    language: str
    confidence: float
    is_arabizi: bool
    arabic_ratio: float
    signals: List[str] = Field(default_factory=list)


# ============================================
# DICTIONNAIRES DE DÉTECTION
# ============================================

# Mots-clés français courants
FRENCH_WORDS = {
    'le', 'la', 'les', 'de', 'du', 'des', 'un', 'une',
    'et', 'ou', 'mais', 'donc', 'car', 'ni', 'or',
    'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles',
    'est', 'sont', 'être', 'avoir', 'faire',
    'pour', 'dans', 'avec', 'sur', 'sous', 'entre',
    'ce', 'cette', 'ces', 'mon', 'ma', 'mes', 'ton', 'ta', 'tes',
    'bonjour', 'merci', 'oui', 'non', 'comment', 'pourquoi',
}

# Mots-clés anglais courants
ENGLISH_WORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were',
    'and', 'or', 'but', 'for', 'with', 'from', 'to',
    'i', 'you', 'he', 'she', 'it', 'we', 'they',
    'have', 'has', 'do', 'does', 'can', 'will', 'would',
    'this', 'that', 'these', 'those', 'what', 'which',
    'hello', 'thanks', 'yes', 'no', 'how', 'why',
}

# Mots arabe standard (MSA) vs darija
MSA_MARKERS = {
    'إن', 'أن', 'الذي', 'التي', 'الذين', 'اللاتي',
    'ليس', 'ليست', 'كان', 'كانت', 'يكون', 'تكون',
    'هذا', 'هذه', 'ذلك', 'تلك', 'هؤلاء', 'أولئك',
    'حيث', 'إذا', 'إذ', 'لأن', 'لكن', 'بل',
    'سوف', 'قد', 'لن', 'لم', 'لا',
}

# Mots darija spécifiques (en arabe)
DARIJA_MARKERS_AR = {
    'كيفاش', 'علاش', 'وقتاش', 'شحال', 'فين', 'وين',
    'واش', 'راه', 'راني', 'راك', 'راهي',
    'كاين', 'كاينة', 'ماكاش', 'ماكانش',
    'بزاف', 'شوية', 'دابا', 'دروك',
    'خويا', 'ختي', 'صحيتي', 'لاباس',
    'نحب', 'نبغي', 'ندير', 'نروح',
    'بالاك', 'قاع', 'برك', 'غير',
    'زعمة', 'والو', 'حتى', 'ملي',
}


# ============================================
# FONCTIONS DE DÉTECTION
# ============================================

def detect_dialect(text: str) -> DetectionResult:
    """
    Détecter le dialecte/langue du texte.
    
    Analyse:
    - Ratio arabe/latin
    - Mots-clés spécifiques
    - Patterns arabizi
    
    Returns:
        DetectionResult avec dialecte, langue et confiance
    """
    if not text or not text.strip():
        return DetectionResult(
            dialect=DialectType.UNKNOWN,
            language="unknown",
            confidence=0.0,
            is_arabizi=False,
            arabic_ratio=0.0,
        )
    
    text_clean = text.strip()
    signals = []
    
    # Calculer le ratio arabe
    arabic_ratio = get_arabic_ratio(text_clean)
    
    # Vérifier arabizi
    arabizi_detected = is_arabizi(text_clean)
    arabizi_score = get_arabizi_score(text_clean)
    
    # Tokeniser pour analyse
    words = text_clean.lower().split()
    words_set = set(words)
    
    # Compter les mots-clés
    french_count = len(words_set & FRENCH_WORDS)
    english_count = len(words_set & ENGLISH_WORDS)
    
    # Mots darija en arabizi
    darija_arabizi_count = len(words_set & set(DARIJA_WORDS.keys()))
    
    # Si texte arabe
    if arabic_ratio > 0.5:
        # Vérifier si MSA ou darija
        arabic_words = [w for w in words if has_arabic(w)]
        arabic_words_set = set(arabic_words)
        
        msa_count = len(arabic_words_set & MSA_MARKERS)
        darija_count = len(arabic_words_set & DARIJA_MARKERS_AR)
        
        if darija_count > msa_count:
            signals.append(f"Mots darija détectés: {darija_count}")
            return DetectionResult(
                dialect=DialectType.DARIJA,
                language="ar-dz",
                confidence=min(0.5 + darija_count * 0.1, 0.95),
                is_arabizi=False,
                arabic_ratio=arabic_ratio,
                signals=signals,
            )
        elif msa_count > 0:
            signals.append(f"Mots MSA détectés: {msa_count}")
            return DetectionResult(
                dialect=DialectType.MSA,
                language="ar",
                confidence=min(0.5 + msa_count * 0.1, 0.95),
                is_arabizi=False,
                arabic_ratio=arabic_ratio,
                signals=signals,
            )
        else:
            # Arabe générique, probablement darija
            signals.append("Texte arabe sans marqueurs MSA")
            return DetectionResult(
                dialect=DialectType.DARIJA,
                language="ar-dz",
                confidence=0.6,
                is_arabizi=False,
                arabic_ratio=arabic_ratio,
                signals=signals,
            )
    
    # Si arabizi détecté
    if arabizi_detected or arabizi_score > 0.3:
        signals.append(f"Score arabizi: {arabizi_score:.2f}")
        if darija_arabizi_count > 0:
            signals.append(f"Mots darija (arabizi): {darija_arabizi_count}")
        
        return DetectionResult(
            dialect=DialectType.ARABIZI,
            language="ar-dz-latn",
            confidence=max(arabizi_score, 0.6),
            is_arabizi=True,
            arabic_ratio=arabic_ratio,
            signals=signals,
        )
    
    # Si principalement français
    if french_count > english_count and french_count > 0:
        signals.append(f"Mots français: {french_count}")
        
        # Vérifier si mélange avec darija
        if darija_arabizi_count > 0:
            signals.append(f"Mélange avec darija: {darija_arabizi_count} mots")
            return DetectionResult(
                dialect=DialectType.MIXED,
                language="fr-dz",
                confidence=0.7,
                is_arabizi=darija_arabizi_count > 0,
                arabic_ratio=arabic_ratio,
                signals=signals,
            )
        
        return DetectionResult(
            dialect=DialectType.FRENCH,
            language="fr",
            confidence=min(0.5 + french_count * 0.05, 0.9),
            is_arabizi=False,
            arabic_ratio=arabic_ratio,
            signals=signals,
        )
    
    # Si principalement anglais
    if english_count > 0:
        signals.append(f"Mots anglais: {english_count}")
        return DetectionResult(
            dialect=DialectType.ENGLISH,
            language="en",
            confidence=min(0.5 + english_count * 0.05, 0.9),
            is_arabizi=False,
            arabic_ratio=arabic_ratio,
            signals=signals,
        )
    
    # Inconnu ou mélange
    if arabic_ratio > 0.2:
        signals.append("Texte mixte arabe/latin")
        return DetectionResult(
            dialect=DialectType.MIXED,
            language="mixed",
            confidence=0.4,
            is_arabizi=arabizi_detected,
            arabic_ratio=arabic_ratio,
            signals=signals,
        )
    
    return DetectionResult(
        dialect=DialectType.UNKNOWN,
        language="unknown",
        confidence=0.3,
        is_arabizi=False,
        arabic_ratio=arabic_ratio,
        signals=signals,
    )


# ============================================
# CLASSE PRINCIPALE
# ============================================

class DarijaNormalizer:
    """
    Normaliseur principal pour la darija algérienne.
    
    Pipeline:
    1. Nettoyage du texte
    2. Détection du dialecte
    3. Conversion arabizi → arabe (si nécessaire)
    4. Normalisation des caractères arabes
    5. Tokenisation
    """
    
    def __init__(
        self,
        level: NormalizationLevel = NormalizationLevel.MEDIUM,
        convert_arabizi: bool = True,
        remove_harakat_flag: bool = True,
        normalize_ta_marbuta: bool = False,
    ):
        """
        Initialiser le normaliseur.
        
        Args:
            level: Niveau de normalisation
            convert_arabizi: Convertir l'arabizi en arabe
            remove_harakat_flag: Supprimer les diacritiques
            normalize_ta_marbuta: Normaliser ة → ه
        """
        self.level = level
        self.convert_arabizi = convert_arabizi
        self.remove_harakat_flag = remove_harakat_flag
        self.normalize_ta_marbuta = normalize_ta_marbuta
    
    def normalize(self, text: str) -> NormalizationResult:
        """
        Normaliser un texte darija.
        
        Args:
            text: Texte à normaliser
        
        Returns:
            NormalizationResult avec texte normalisé et métadonnées
        """
        import time
        start_time = time.time()
        
        if not text or not text.strip():
            return NormalizationResult(
                original=text or "",
                cleaned="",
                normalized="",
                dialect=DialectType.UNKNOWN,
            )
        
        original = text
        
        # 1. Nettoyage basique
        cleaned = clean_text(
            text,
            remove_emojis_flag=True,
            remove_urls_flag=True,
            remove_emails_flag=True,
            remove_phones_flag=True,
            remove_harakat_flag=self.remove_harakat_flag,
            normalize_chars=True,
            reduce_repeats=True,
            remove_noise=True,
        )
        
        # 2. Détection du dialecte
        detection = detect_dialect(cleaned)
        
        # 3. Conversion arabizi si nécessaire
        arabizi_converted = False
        darija_words_found = []
        
        if self.convert_arabizi and detection.is_arabizi:
            # Trouver les mots darija avant conversion
            words = cleaned.lower().split()
            darija_words_found = [w for w in words if w in DARIJA_WORDS]
            
            # Convertir
            cleaned = arabizi_to_arabic(cleaned, use_dictionary=True)
            arabizi_converted = True
        
        # 4. Normalisation des caractères arabes
        normalized = normalize_arabic_chars(cleaned, self.normalize_ta_marbuta)
        
        # 5. Normalisation ponctuation et nombres
        normalized = normalize_punctuation(normalized)
        normalized = normalize_numbers_arabic(normalized)
        
        # 6. Nettoyage final
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        # 7. Tokenisation
        tokens = tokenize_arabic(normalized)
        sentences = tokenize_sentences(normalized)
        
        # Calculer le temps de traitement
        processing_time = int((time.time() - start_time) * 1000)
        
        return NormalizationResult(
            original=original,
            cleaned=cleaned,
            normalized=normalized,
            dialect=detection.dialect,
            is_arabizi=detection.is_arabizi,
            language=detection.language,
            tokens=tokens,
            sentences=sentences,
            arabic_ratio=detection.arabic_ratio,
            word_count=len(tokens),
            confidence=detection.confidence,
            arabizi_converted=arabizi_converted,
            darija_words_found=darija_words_found,
            level=self.level,
            processing_time_ms=processing_time,
        )
    
    def normalize_batch(self, texts: List[str]) -> List[NormalizationResult]:
        """Normaliser plusieurs textes."""
        return [self.normalize(text) for text in texts]
    
    def quick_normalize(self, text: str) -> str:
        """
        Normalisation rapide - retourne uniquement le texte normalisé.
        """
        result = self.normalize(text)
        return result.normalized


# ============================================
# FONCTIONS UTILITAIRES
# ============================================

# Instance globale par défaut
_default_normalizer = DarijaNormalizer()


def normalize_darija(text: str) -> NormalizationResult:
    """
    Normaliser un texte darija (fonction raccourcie).
    
    Utilise l'instance par défaut du normaliseur.
    """
    return _default_normalizer.normalize(text)


def quick_normalize(text: str) -> str:
    """Normalisation rapide - retourne uniquement le texte."""
    return _default_normalizer.quick_normalize(text)


def is_darija(text: str) -> bool:
    """Vérifier si le texte est en darija."""
    detection = detect_dialect(text)
    return detection.dialect in [DialectType.DARIJA, DialectType.ARABIZI]


def get_dialect_name(dialect: DialectType) -> str:
    """Obtenir le nom du dialecte."""
    names = {
        DialectType.DARIJA: "Darija (Arabe algérien)",
        DialectType.ARABIZI: "Arabizi (Darija en latin)",
        DialectType.MSA: "Arabe standard moderne",
        DialectType.FRENCH: "Français",
        DialectType.ENGLISH: "Anglais",
        DialectType.MIXED: "Mixte",
        DialectType.UNKNOWN: "Inconnu",
    }
    return names.get(dialect, "Inconnu")


def get_normalization_examples() -> List[Dict[str, Any]]:
    """Retourner des exemples de normalisation."""
    examples = [
        {
            "input": "salam khoya kifach rak",
            "output": "سلام خويا كيفاش راك",
            "dialect": "arabizi",
        },
        {
            "input": "wach dayer lyoum",
            "output": "واش داير ليوم",
            "dialect": "arabizi",
        },
        {
            "input": "n7eb ndir tasjil CNAS",
            "output": "نحب ندير تسجيل كناس",
            "dialect": "arabizi",
        },
        {
            "input": "كيفاش ندير التسجيل",
            "output": "كيفاش ندير التسجيل",
            "dialect": "darija",
        },
        {
            "input": "3andi mochkil m3a lkhedma",
            "output": "عندي مشكل مع الخدمة",
            "dialect": "arabizi",
        },
    ]
    return examples
