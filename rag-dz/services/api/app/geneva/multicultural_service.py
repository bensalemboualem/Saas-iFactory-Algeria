"""
Geneva Multicultural Intelligence Service
==========================================

Gère la diversité culturelle extrême de Genève (110+ nationalités)

Fonctionnalités:
- Détection nuances culturelles par nationalité
- Interprétation expressions selon contexte culturel
- Détection multi-langues dans un même audio
- Geneva Mode: Haute précision pour accents non-natifs
"""

import logging
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CulturalNuance:
    """Nuance culturelle détectée"""
    expression: str
    nationality: str
    cultural_meaning: str
    literal_meaning: Optional[str]
    politeness_level: str  # 'very_formal', 'formal', 'neutral', 'informal'
    emotional_connotation: str  # 'positive', 'negative', 'neutral', 'ambiguous'
    confidence: float


@dataclass
class LanguageSegment:
    """Segment avec langue détectée"""
    segment_index: int
    start_time: float
    end_time: float
    detected_language: str
    language_confidence: float
    text_content: str
    accent_type: Optional[str] = None
    non_native_speaker: bool = False


# ============================================================
# CULTURAL PATTERNS Database (Common Misinterpretations)
# ============================================================

CULTURAL_PATTERNS = {
    'japanese': {
        # Indirection japonaise (politesse)
        'indirect_refusal': [
            (r'\b(yes.*but.*difficult|might be challenging|need to check)\b',
             'Refus poli indirect', 'negative', 'very_formal'),
            (r'\b(will consider|think about it|study the matter)\b',
             'Refus poli - Pas intéressé', 'negative', 'formal'),
            (r'\b(maybe.*later|another time perhaps)\b',
             'Refus doux', 'negative', 'formal'),
        ],
        'politeness_hedges': [
            (r'\b(perhaps|possibly|might)\b',
             'Atténuation culturelle japonaise', 'neutral', 'formal'),
        ]
    },

    'spanish': {
        # Emphase culturelle espagnole
        'time_flexibility': [
            (r'\b(ahora mismo|right now)\b',
             'Bientôt (pas forcément immédiat)', 'neutral', 'informal'),
            (r'\b(mañana|tomorrow)\b',
             'Futur proche (flexibilité temporelle)', 'neutral', 'informal'),
        ],
        'emotional_emphasis': [
            (r'\b(muy|mucho|muchísimo)\b',
             'Emphase émotionnelle forte', 'positive', 'informal'),
        ]
    },

    'algerian': {
        # Expressions culturelles algériennes
        'faith_expressions': [
            (r'\b(inchallah|inch\'allah)\b',
             'Si Dieu le veut - Espoir avec incertitude', 'positive', 'formal'),
            (r'\b(hamdoullah|el hamdoulillah)\b',
             'Louange à Dieu - Gratitude spirituelle', 'positive', 'formal'),
            (r'\b(baraka.*fik|allah.*barek)\b',
             'Que Dieu te bénisse - Remerciement profond', 'positive', 'very_formal'),
        ],
        'cultural_wisdom': [
            (r'\b(comme.*proverbe|قال.*مثل)\b',
             'Référence sagesse ancestrale', 'positive', 'formal'),
        ]
    },

    'swiss': {
        # Politesse suisse atténuée
        'polite_attenuation': [
            (r'\b(on pourrait peut-être|perhaps we could)\b',
             'Proposition ferme (politesse suisse)', 'neutral', 'formal'),
            (r'\b(il faudrait éventuellement)\b',
             'Suggestion forte atténuée', 'neutral', 'formal'),
        ],
        'precision': [
            (r'\b(exactement|précisément)\b',
             'Précision culturelle suisse', 'positive', 'formal'),
        ]
    },

    'french': {
        # Politesse française directe
        'direct_communication': [
            (r'\b(franchement|honnêtement)\b',
             'Franchise culturelle française', 'neutral', 'informal'),
        ]
    },

    'american': {
        # Communication américaine directe
        'direct_enthusiasm': [
            (r'\b(awesome|amazing|great)\b',
             'Enthousiasme culturel américain', 'positive', 'informal'),
        ]
    }
}


# ============================================================
# ACCENT DETECTION PATTERNS
# ============================================================

ACCENT_INDICATORS = {
    'spanish_speaking_english': [
        r'\b(espeak|estop|estreet)\b',  # 's' initial difficile
        r'\bes\s+',  # 'es' devant consonnes
    ],
    'japanese_speaking_english': [
        r'\b(r.*l|l.*r)\b',  # Confusion R/L
        r'\b(vely|velly)\b',  # "very" prononcé "vely"
    ],
    'french_speaking_english': [
        r'\b(ze|zis|zat)\b',  # 'th' → 'z'
        r'\b(ow you say)\b',  # "how you say"
    ],
    'arabic_speaking_french': [
        r'\b(bé|pé)\b',  # Confusion P/B
        r'[قكخ]',  # Caractères arabes mélangés
    ]
}


def detect_cultural_nuances(
    text: str,
    user_nationality: Optional[str] = None,
    detected_language: str = "fr"
) -> List[CulturalNuance]:
    """
    Détecte les nuances culturelles dans le texte

    Args:
        text: Texte transcrit
        user_nationality: Nationalité de l'utilisateur
        detected_language: Langue détectée

    Returns:
        Liste de nuances culturelles détectées
    """
    nuances = []
    text_lower = text.lower()

    # Si nationalité connue, chercher patterns spécifiques
    if user_nationality and user_nationality in CULTURAL_PATTERNS:
        patterns = CULTURAL_PATTERNS[user_nationality]

        for category, pattern_list in patterns.items():
            for pattern, cultural_meaning, emotion, politeness in pattern_list:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)

                for match in matches:
                    expression = match.group(0)

                    nuances.append(CulturalNuance(
                        expression=expression,
                        nationality=user_nationality,
                        cultural_meaning=cultural_meaning,
                        literal_meaning=None,  # Could be enhanced
                        politeness_level=politeness,
                        emotional_connotation=emotion,
                        confidence=0.75
                    ))

    # Sinon, chercher dans toutes les cultures
    else:
        for nationality, patterns in CULTURAL_PATTERNS.items():
            for category, pattern_list in patterns.items():
                for pattern, cultural_meaning, emotion, politeness in pattern_list:
                    matches = re.finditer(pattern, text_lower, re.IGNORECASE)

                    for match in matches:
                        expression = match.group(0)

                        nuances.append(CulturalNuance(
                            expression=expression,
                            nationality=nationality,
                            cultural_meaning=cultural_meaning,
                            literal_meaning=None,
                            politeness_level=politeness,
                            emotional_connotation=emotion,
                            confidence=0.65  # Lower confidence if nationality unknown
                        ))

    logger.info(f"🌍 Detected {len(nuances)} cultural nuances for nationality={user_nationality}")
    return nuances


def detect_accent_type(
    text: str,
    detected_language: str,
    user_nationality: Optional[str] = None
) -> Tuple[Optional[str], bool]:
    """
    Détecte le type d'accent (non-natif) dans le texte

    Args:
        text: Texte transcrit
        detected_language: Langue détectée
        user_nationality: Nationalité de l'utilisateur

    Returns:
        (accent_type, non_native_speaker)
    """
    text_lower = text.lower()
    accent_type = None
    non_native_speaker = False

    # Détecter signes d'accent non-natif
    for accent_key, patterns in ACCENT_INDICATORS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                accent_type = accent_key
                non_native_speaker = True
                logger.info(f"🎤 Accent non-natif détecté: {accent_type}")
                break

        if non_native_speaker:
            break

    # Si nationalité connue + langue différente = non-natif probable
    if user_nationality and detected_language:
        native_language_map = {
            'spanish': 'es',
            'french': 'fr',
            'japanese': 'ja',
            'algerian': 'ar',
            'swiss': 'fr',  # Simplification (peut être de/it/fr)
            'american': 'en',
        }

        expected_native = native_language_map.get(user_nationality.lower())

        if expected_native and expected_native != detected_language:
            non_native_speaker = True
            if not accent_type:
                accent_type = f"{detected_language}_{user_nationality}_accent"

    return accent_type, non_native_speaker


def detect_multi_languages_in_segments(
    segments: List[Dict[str, Any]],
    threshold_confidence: float = 0.7
) -> List[LanguageSegment]:
    """
    Détecte plusieurs langues dans les segments d'une transcription

    Note: Faster-Whisper détecte déjà la langue par segment.
    Cette fonction enrichit avec détection accent et formatage.

    Args:
        segments: Liste de segments Whisper
        threshold_confidence: Seuil de confiance minimum

    Returns:
        Liste de LanguageSegment avec métadonnées
    """
    language_segments = []

    for idx, segment in enumerate(segments):
        # Extraire données Whisper
        start_time = segment.get('start', 0.0)
        end_time = segment.get('end', 0.0)
        text = segment.get('text', '')

        # Whisper peut donner une langue par segment
        detected_lang = segment.get('language', 'unknown')
        lang_confidence = segment.get('language_probability', 0.0)

        # Détecter type d'accent
        accent_type, non_native = detect_accent_type(
            text=text,
            detected_language=detected_lang
        )

        lang_segment = LanguageSegment(
            segment_index=idx,
            start_time=start_time,
            end_time=end_time,
            detected_language=detected_lang,
            language_confidence=lang_confidence,
            text_content=text,
            accent_type=accent_type,
            non_native_speaker=non_native
        )

        language_segments.append(lang_segment)

    # Log statistiques
    languages_found = set(s.detected_language for s in language_segments)
    non_native_count = sum(1 for s in language_segments if s.non_native_speaker)

    logger.info(
        f"🌐 Multi-language detection: {len(languages_found)} langues trouvées, "
        f"{non_native_count} segments avec accent non-natif"
    )

    return language_segments


def apply_geneva_mode_processing(
    text: str,
    user_linguistic_profile: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Applique le traitement Geneva Mode pour haute précision accents

    Geneva Mode: Optimisations spéciales pour transcriptions multi-culturelles

    Args:
        text: Texte transcrit brut
        user_linguistic_profile: Profil linguistique de l'utilisateur

    Returns:
        Métadonnées de traitement Geneva Mode
    """
    geneva_metadata = {
        "geneva_mode_applied": False,
        "accent_sensitivity_level": 3,
        "detected_nationalities": [],
        "cultural_nuances_count": 0,
        "multi_language_detected": False,
    }

    if not user_linguistic_profile:
        return geneva_metadata

    # Geneva Mode activé ?
    if not user_linguistic_profile.get('geneva_mode_enabled', False):
        return geneva_metadata

    geneva_metadata["geneva_mode_applied"] = True
    geneva_metadata["accent_sensitivity_level"] = user_linguistic_profile.get(
        'accent_sensitivity_level', 3
    )

    # Détecter nuances culturelles
    nationality = user_linguistic_profile.get('nationality')
    if nationality:
        nuances = detect_cultural_nuances(
            text=text,
            user_nationality=nationality
        )
        geneva_metadata["cultural_nuances_count"] = len(nuances)
        geneva_metadata["detected_nationalities"] = [nationality]

    logger.info(
        f"🇨🇭 Geneva Mode applied: sensitivity={geneva_metadata['accent_sensitivity_level']}/5, "
        f"nuances={geneva_metadata['cultural_nuances_count']}"
    )

    return geneva_metadata
