"""
OCR_DZ - Utilitaires OCR
========================
Détection langue, nettoyage arabe/français, normalisation
"""

import re
import unicodedata
from typing import List, Optional, Tuple, Literal

# ============================================
# CONSTANTES ARABE
# ============================================

# Caractères arabes de base
ARABIC_RANGE = r'\u0600-\u06FF'
ARABIC_SUPPLEMENT = r'\u0750-\u077F'
ARABIC_EXTENDED_A = r'\u08A0-\u08FF'
ARABIC_PRESENTATION_A = r'\uFB50-\uFDFF'
ARABIC_PRESENTATION_B = r'\uFE70-\uFEFF'

# Pattern complet arabe
ARABIC_PATTERN = f'[{ARABIC_RANGE}{ARABIC_SUPPLEMENT}{ARABIC_EXTENDED_A}{ARABIC_PRESENTATION_A}{ARABIC_PRESENTATION_B}]'

# Diacritiques arabes (tashkeel)
TASHKEEL = r'[\u064B-\u0652\u0670]'

# Lettres arabes pour comptage
ARABIC_LETTERS = set('ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوىي')

# Normalisation caractères arabes
ARABIC_NORMALIZATION = {
    'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ٱ': 'ا',
    'ؤ': 'و',
    'ئ': 'ي',
    'ة': 'ه',
    'ى': 'ي',
    'ـ': '',  # Tatweel (kashida)
}

# Caractères français spéciaux
FRENCH_CHARS = set('àâäéèêëïîôùûüçœæÀÂÄÉÈÊËÏÎÔÙÛÜÇŒÆ')


# ============================================
# DÉTECTION LANGUE
# ============================================

LanguageCode = Literal["ar", "fr", "en", "mixed", "unknown"]


def detect_language(text: str) -> Tuple[LanguageCode, float]:
    """
    Détecter la langue du texte.
    
    Returns:
        Tuple[LanguageCode, float]: (langue, confiance)
    """
    if not text or not text.strip():
        return "unknown", 0.0
    
    text_clean = text.strip()
    total_chars = len(text_clean)
    
    if total_chars == 0:
        return "unknown", 0.0
    
    # Compter les caractères par type
    arabic_count = len(re.findall(ARABIC_PATTERN, text_clean))
    french_count = sum(1 for c in text_clean if c in FRENCH_CHARS)
    latin_count = sum(1 for c in text_clean if c.isalpha() and ord(c) < 256)
    
    # Calculer les ratios
    arabic_ratio = arabic_count / total_chars
    french_ratio = french_count / total_chars
    latin_ratio = latin_count / total_chars
    
    # Détecter la langue dominante
    if arabic_ratio > 0.3:
        # Principalement arabe
        if latin_ratio > 0.2:
            return "mixed", 0.7
        confidence = min(arabic_ratio * 1.2, 0.98)
        return "ar", confidence
    
    elif french_ratio > 0.05 or _has_french_words(text_clean):
        # Français (présence d'accents français ou mots français)
        confidence = 0.85 if french_ratio > 0.1 else 0.75
        return "fr", confidence
    
    elif latin_ratio > 0.5:
        # Latin mais pas d'accents français → anglais probable
        if _has_english_patterns(text_clean):
            return "en", 0.8
        # Par défaut français en Algérie
        return "fr", 0.6
    
    return "unknown", 0.3


def _has_french_words(text: str) -> bool:
    """Détecter des mots français courants."""
    french_markers = [
        r'\b(le|la|les|de|du|des|un|une|et|ou|en|sur|pour|dans|avec|est|sont)\b',
        r'\b(qui|que|quoi|dont|où|comment|pourquoi|quand)\b',
        r'\b(être|avoir|faire|aller|voir|savoir|pouvoir|vouloir)\b',
        r'\b(entreprise|société|fiscal|impôt|déclaration|travail)\b',
    ]
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in french_markers)


def _has_english_patterns(text: str) -> bool:
    """Détecter des patterns anglais."""
    english_markers = [
        r'\b(the|a|an|is|are|was|were|be|been|have|has|had)\b',
        r'\b(and|or|but|for|with|from|to|in|on|at)\b',
        r'\b(this|that|these|those|what|which|who|how|why)\b',
    ]
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in english_markers)


def get_language_name(code: LanguageCode) -> str:
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
# NETTOYAGE TEXTE
# ============================================

def clean_text_basic(text: str) -> str:
    """Nettoyage basique du texte."""
    if not text:
        return ""
    
    # Normaliser les espaces
    text = re.sub(r'\s+', ' ', text)
    
    # Supprimer les caractères de contrôle
    text = ''.join(c for c in text if unicodedata.category(c) != 'Cc' or c in '\n\t')
    
    # Normaliser les retours à la ligne
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def clean_arabic(text: str, remove_tashkeel: bool = False, normalize: bool = True) -> str:
    """
    Nettoyer et normaliser le texte arabe.
    
    Args:
        text: Texte à nettoyer
        remove_tashkeel: Supprimer les diacritiques (harakat)
        normalize: Appliquer la normalisation des caractères
    
    Returns:
        Texte nettoyé
    """
    if not text:
        return ""
    
    # Nettoyage basique
    text = clean_text_basic(text)
    
    # Supprimer les diacritiques si demandé
    if remove_tashkeel:
        text = re.sub(TASHKEEL, '', text)
    
    # Normaliser les caractères arabes
    if normalize:
        for old, new in ARABIC_NORMALIZATION.items():
            text = text.replace(old, new)
    
    # Supprimer les caractères arabes orphelins (erreurs OCR)
    # Garder les mots d'au moins 2 caractères arabes
    
    # Nettoyer les espaces autour de la ponctuation arabe
    text = re.sub(r'\s*([،؛؟!])\s*', r'\1 ', text)
    
    # Supprimer les espaces multiples
    text = re.sub(r' +', ' ', text)
    
    return text.strip()


def normalize_arabic(text: str) -> str:
    """
    Normalisation avancée du texte arabe.
    
    - Uniformise les variantes de lettres
    - Corrige les erreurs OCR courantes
    - Prépare pour la recherche
    """
    if not text:
        return ""
    
    # Appliquer le nettoyage de base
    text = clean_arabic(text, remove_tashkeel=True, normalize=True)
    
    # Corrections OCR courantes
    ocr_corrections = {
        'ﻻ': 'لا',
        'ﻷ': 'لأ',
        'ﻵ': 'لآ',
        'ﻹ': 'لإ',
        '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
        '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9',
    }
    
    for old, new in ocr_corrections.items():
        text = text.replace(old, new)
    
    # Supprimer les caractères non-imprimables arabes
    text = re.sub(r'[\u200B-\u200F\u202A-\u202E\u2066-\u2069]', '', text)
    
    return text.strip()


def clean_french(text: str) -> str:
    """
    Nettoyer le texte français.
    
    - Corriger la ponctuation
    - Normaliser les accents
    - Corriger les erreurs OCR courantes
    """
    if not text:
        return ""
    
    # Nettoyage basique
    text = clean_text_basic(text)
    
    # Corrections OCR courantes en français
    ocr_corrections = {
        'œ': 'oe',  # Ligature
        'æ': 'ae',  # Ligature
        '«': '"',
        '»': '"',
        ''': "'",
        ''': "'",
        '"': '"',
        '"': '"',
        '…': '...',
        '–': '-',
        '—': '-',
        '\u00A0': ' ',  # Espace insécable
    }
    
    for old, new in ocr_corrections.items():
        text = text.replace(old, new)
    
    # Corriger la ponctuation française
    # Espace avant : ; ? !
    text = re.sub(r'\s+([;:?!])', r' \1', text)
    # Pas d'espace après (
    text = re.sub(r'\(\s+', '(', text)
    # Pas d'espace avant )
    text = re.sub(r'\s+\)', ')', text)
    
    # Supprimer les espaces multiples
    text = re.sub(r' +', ' ', text)
    
    return text.strip()


def clean_english(text: str) -> str:
    """Nettoyer le texte anglais."""
    if not text:
        return ""
    
    text = clean_text_basic(text)
    
    # Corrections OCR
    text = text.replace(''', "'").replace(''', "'")
    text = text.replace('"', '"').replace('"', '"')
    
    return text.strip()


def clean_by_language(text: str, language: LanguageCode) -> str:
    """Nettoyer le texte selon la langue détectée."""
    cleaners = {
        "ar": clean_arabic,
        "fr": clean_french,
        "en": clean_english,
        "mixed": lambda t: clean_arabic(clean_french(t)),
        "unknown": clean_text_basic,
    }
    return cleaners.get(language, clean_text_basic)(text)


# ============================================
# FUSION DE PAGES
# ============================================

def merge_pages_text(
    pages: List[str],
    separator: str = "\n\n---\n\n",
    add_page_numbers: bool = False,
) -> str:
    """
    Fusionner le texte de plusieurs pages.
    
    Args:
        pages: Liste des textes de chaque page
        separator: Séparateur entre les pages
        add_page_numbers: Ajouter les numéros de page
    
    Returns:
        Texte fusionné
    """
    if not pages:
        return ""
    
    if len(pages) == 1:
        return pages[0].strip()
    
    merged_parts = []
    
    for i, page_text in enumerate(pages, 1):
        cleaned = page_text.strip()
        if cleaned:
            if add_page_numbers:
                merged_parts.append(f"[Page {i}]\n{cleaned}")
            else:
                merged_parts.append(cleaned)
    
    return separator.join(merged_parts)


def detect_pages_language(pages: List[str]) -> Tuple[LanguageCode, float]:
    """
    Détecter la langue dominante sur plusieurs pages.
    
    Returns:
        Tuple[LanguageCode, float]: (langue dominante, confiance moyenne)
    """
    if not pages:
        return "unknown", 0.0
    
    detections = [detect_language(page) for page in pages if page.strip()]
    
    if not detections:
        return "unknown", 0.0
    
    # Compter les occurrences de chaque langue
    lang_counts: dict[str, int] = {}
    lang_confidences: dict[str, List[float]] = {}
    
    for lang, conf in detections:
        lang_counts[lang] = lang_counts.get(lang, 0) + 1
        if lang not in lang_confidences:
            lang_confidences[lang] = []
        lang_confidences[lang].append(conf)
    
    # Langue majoritaire
    dominant_lang = max(lang_counts, key=lambda k: lang_counts[k])
    avg_confidence = sum(lang_confidences[dominant_lang]) / len(lang_confidences[dominant_lang])
    
    return dominant_lang, avg_confidence  # type: ignore


# ============================================
# ESTIMATION CONFIANCE OCR
# ============================================

def estimate_confidence(text: str, language: LanguageCode = "unknown") -> float:
    """
    Estimer la confiance de l'OCR basée sur des heuristiques.
    
    Facteurs:
    - Longueur du texte
    - Ratio caractères valides
    - Présence de mots reconnaissables
    - Structure du texte
    
    Returns:
        float: Confiance entre 0 et 1
    """
    if not text or not text.strip():
        return 0.0
    
    text_clean = text.strip()
    total_chars = len(text_clean)
    
    if total_chars < 10:
        return 0.2
    
    # Score de base selon la longueur
    length_score = min(total_chars / 500, 1.0) * 0.3
    
    # Ratio de caractères valides (lettres, chiffres, ponctuation courante)
    valid_chars = sum(1 for c in text_clean if c.isalnum() or c in ' .,;:!?-()[]{}"\'\n\t،؛؟')
    valid_ratio = valid_chars / total_chars
    validity_score = valid_ratio * 0.3
    
    # Score de structure (présence de mots, phrases)
    words = text_clean.split()
    avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
    
    # Mots trop courts ou trop longs = mauvais OCR
    if avg_word_length < 2 or avg_word_length > 20:
        structure_score = 0.1
    elif 3 <= avg_word_length <= 10:
        structure_score = 0.25
    else:
        structure_score = 0.15
    
    # Score spécifique à la langue
    lang_score = 0.0
    if language == "ar":
        # Vérifier la cohérence du texte arabe
        arabic_chars = len(re.findall(ARABIC_PATTERN, text_clean))
        if arabic_chars > 0:
            arabic_ratio = arabic_chars / sum(1 for c in text_clean if not c.isspace())
            lang_score = arabic_ratio * 0.15
    elif language == "fr":
        # Vérifier les mots français
        if _has_french_words(text_clean):
            lang_score = 0.15
    elif language == "en":
        if _has_english_patterns(text_clean):
            lang_score = 0.15
    
    total_score = length_score + validity_score + structure_score + lang_score
    
    # Normaliser entre 0 et 1
    return min(max(total_score, 0.0), 1.0)


# ============================================
# UTILITAIRES RTL (RIGHT-TO-LEFT)
# ============================================

def prepare_rtl_text(text: str) -> str:
    """
    Préparer le texte arabe pour l'affichage RTL.
    
    Utilise arabic_reshaper et bidi si disponibles.
    """
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except ImportError:
        # Sans les librairies, retourner tel quel
        return text


def is_rtl_text(text: str) -> bool:
    """Vérifier si le texte est principalement RTL (arabe)."""
    if not text:
        return False
    
    arabic_chars = len(re.findall(ARABIC_PATTERN, text))
    total_letters = sum(1 for c in text if c.isalpha())
    
    if total_letters == 0:
        return False
    
    return arabic_chars / total_letters > 0.5


# ============================================
# EXTRACTION DE MÉTADONNÉES
# ============================================

def extract_numbers(text: str) -> List[str]:
    """Extraire tous les nombres du texte."""
    # Nombres arabes et occidentaux
    pattern = r'[\d٠-٩]+(?:[.,][\d٠-٩]+)?'
    return re.findall(pattern, text)


def extract_dates_dz(text: str) -> List[str]:
    """Extraire les dates au format algérien (DD/MM/YYYY)."""
    patterns = [
        r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
        r'\d{1,2}\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}',
        r'\d{1,2}\s+(?:جانفي|فيفري|مارس|أفريل|ماي|جوان|جويلية|أوت|سبتمبر|أكتوبر|نوفمبر|ديسمبر)\s+\d{4}',
    ]
    
    dates = []
    for pattern in patterns:
        dates.extend(re.findall(pattern, text, re.IGNORECASE))
    
    return dates


def extract_amounts_dzd(text: str) -> List[Tuple[str, str]]:
    """
    Extraire les montants en DZD.
    
    Returns:
        List[Tuple[amount, currency]]
    """
    patterns = [
        (r'([\d\s.,]+)\s*(?:DA|DZD|دج|دينار)', 'DZD'),
        (r'([\d\s.,]+)\s*(?:dinars?)', 'DZD'),
    ]
    
    amounts = []
    for pattern, currency in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            # Nettoyer le montant
            amount = re.sub(r'\s+', '', match)
            amounts.append((amount, currency))
    
    return amounts
