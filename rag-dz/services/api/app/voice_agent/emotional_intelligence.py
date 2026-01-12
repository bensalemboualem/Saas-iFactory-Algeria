"""
Emotional Intelligence & Cultural Awareness Engine
===================================================
Analyse l'intent, l'émotion et le contexte culturel des transcriptions

Use Cases:
- Suisse: Détection stress/cognitive load → Résumé "Calm & Direct"
- Algérie: Détection patrimoine culturel → Tag "Heritage Value"
"""

import re
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class EmotionAnalysisResult:
    """Résultat complet de l'analyse émotionnelle"""
    detected_emotion: str  # 'calm', 'stressed', 'neutral', 'confident', 'uncertain'
    stress_level: int  # 0-10 (0 = calm, 10 = très stressé)
    cognitive_load: int  # 0-10 (charge cognitive)

    # Contenu patrimonial (Algérie)
    heritage_detected: bool
    heritage_type: Optional[str]  # 'proverb', 'historical_reference', 'cultural_wisdom'
    heritage_content: Optional[str]

    # Recommandation
    recommended_summary_style: str  # 'calm_direct', 'empathetic', 'technical', 'heritage_enriched'
    ai_confidence: float  # 0.0-1.0

    # Métadonnées
    keywords_extracted: List[str]
    professional_terms: List[str]


# ==============================================================================
# Patterns de détection culturelle et émotionnelle
# ==============================================================================

# Indicateurs de stress (surtout pour professionnels suisses)
STRESS_INDICATORS = [
    r'\b(urgent|immédiat|rapidement|tout de suite|au plus vite)\b',
    r'\b(problème|souci|difficulté|complication|blocage)\b',
    r'\b(stressé|pressé|débordé|surchargé|épuisé)\b',
    r'\b(il faut|on doit|obligé de|impératif)\b',
    r'\b(délai|échéance|deadline|retard)\b',
]

# Indicateurs de calme
CALM_INDICATORS = [
    r'\b(tranquille|serein|posé|calme|détendu)\b',
    r'\b(planifié|prévu|organisé|structuré)\b',
    r'\b(on va|nous allons|je vais)\b',
    r'\b(progressivement|étape par étape|doucement)\b',
]

# Patrimoine algérien: proverbes et sagesse locale
ALGERIAN_HERITAGE_PATTERNS = {
    'proverb': [
        r'comme dit le proverbe',
        r'comme disaient nos grands-parents',
        r'selon la sagesse',
        r'الحكمة تقول',  # La sagesse dit
        r'يقول المثل',  # Le proverbe dit
    ],
    'historical_reference': [
        r'\b(indépendance|révolution|moudjahid|chouhada)\b',
        r'\b(novembre 1954|1962|bataille d\'alger)\b',
        r'\b(émir abdelkader|messali hadj|ben badis)\b',
    ],
    'cultural_wisdom': [
        r'\b(baraka|inchallah|mabrouk|hamdoullah)\b',
        r'\b(solidarité|entraide|twiza|العونة)\b',
        r'\b(famille|communauté|الجيران)\b',  # Famille, voisins
    ],
    'local_tradition': [
        r'\b(ramadan|aid|mouled|yennayer)\b',
        r'\b(couscous|chorba|chakhchoukha)\b',
        r'\b(raï|chaabi|andalous|قصبة)\b',
    ]
}

# Termes professionnels par domaine
PROFESSIONAL_TERMS_PATTERNS = {
    'medical': [
        r'\b(diagnostic|symptôme|traitement|ordonnance|consultation)\b',
        r'\b(patient|pathologie|thérapie|analyse|radio)\b',
        r'\b(tension|glycémie|température|pouls)\b',
    ],
    'legal': [
        r'\b(contrat|clause|procédure|tribunal|jurisprudence)\b',
        r'\b(plainte|avocat|juge|audience|jugement)\b',
        r'\b(article|loi|code|décret|arrêt)\b',
    ],
    'accounting': [
        r'\b(comptabilité|bilan|actif|passif|crédit|débit)\b',
        r'\b(facture|déclaration|tva|fiscalité|audit)\b',
        r'\b(exercice|clôture|provision|amortissement)\b',
    ],
}


def analyze_intent_and_emotion(
    text: str,
    user_country: str = "algeria",  # "algeria" ou "switzerland"
    professional_context: Optional[str] = None
) -> EmotionAnalysisResult:
    """
    Analyse l'intent, l'émotion et le contexte culturel d'un texte

    Args:
        text: Texte transcrit à analyser
        user_country: Pays de l'utilisateur ("algeria" ou "switzerland")
        professional_context: Contexte professionnel ("medical", "legal", "accounting")

    Returns:
        EmotionAnalysisResult avec tous les indicateurs
    """
    text_lower = text.lower()

    # 1. Détection stress (critique pour Suisse)
    stress_level = _calculate_stress_level(text_lower)

    # 2. Détection patrimoine culturel (critique pour Algérie)
    heritage_detected, heritage_type, heritage_content = _detect_heritage_content(text)

    # 3. Charge cognitive (nombre de concepts complexes)
    cognitive_load = _calculate_cognitive_load(text_lower, professional_context)

    # 4. Émotion dominante
    detected_emotion = _detect_dominant_emotion(text_lower, stress_level)

    # 5. Extraction keywords professionnels
    professional_terms = _extract_professional_terms(text_lower, professional_context)
    keywords_extracted = _extract_general_keywords(text_lower)

    # 6. Recommandation de style de résumé
    recommended_style = _recommend_summary_style(
        stress_level=stress_level,
        heritage_detected=heritage_detected,
        user_country=user_country,
        cognitive_load=cognitive_load
    )

    # 7. Confiance de l'analyse
    ai_confidence = _calculate_confidence(text)

    logger.info(
        f"Emotion analysis: emotion={detected_emotion}, stress={stress_level}/10, "
        f"cognitive_load={cognitive_load}/10, heritage={heritage_detected}, "
        f"style={recommended_style}"
    )

    return EmotionAnalysisResult(
        detected_emotion=detected_emotion,
        stress_level=stress_level,
        cognitive_load=cognitive_load,
        heritage_detected=heritage_detected,
        heritage_type=heritage_type,
        heritage_content=heritage_content,
        recommended_summary_style=recommended_style,
        ai_confidence=ai_confidence,
        keywords_extracted=keywords_extracted,
        professional_terms=professional_terms
    )


def _calculate_stress_level(text: str) -> int:
    """
    Calcule le niveau de stress (0-10)
    Crucial pour professionnels suisses débordés
    """
    stress_count = 0
    calm_count = 0

    for pattern in STRESS_INDICATORS:
        stress_count += len(re.findall(pattern, text, re.IGNORECASE))

    for pattern in CALM_INDICATORS:
        calm_count += len(re.findall(pattern, text, re.IGNORECASE))

    # Normaliser sur 10
    if stress_count + calm_count == 0:
        return 5  # Neutre par défaut

    stress_ratio = stress_count / (stress_count + calm_count)
    stress_level = int(stress_ratio * 10)

    return min(10, max(0, stress_level))


def _detect_heritage_content(text: str) -> tuple[bool, Optional[str], Optional[str]]:
    """
    Détecte le contenu patrimonial algérien
    (proverbes, histoire, sagesse locale)
    """
    for heritage_type, patterns in ALGERIAN_HERITAGE_PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Extraire le contexte (50 caractères avant/après)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()

                logger.info(f"Heritage detected: type={heritage_type}, content={context[:100]}...")
                return True, heritage_type, context

    return False, None, None


def _calculate_cognitive_load(text: str, professional_context: Optional[str]) -> int:
    """
    Calcule la charge cognitive (nombre de concepts complexes)
    Haut = besoin de résumé empathique
    """
    # Compter les termes techniques
    tech_terms_count = 0

    if professional_context and professional_context in PROFESSIONAL_TERMS_PATTERNS:
        patterns = PROFESSIONAL_TERMS_PATTERNS[professional_context]
        for pattern in patterns:
            tech_terms_count += len(re.findall(pattern, text, re.IGNORECASE))

    # Compter les phrases complexes (> 20 mots)
    sentences = re.split(r'[.!?]', text)
    complex_sentences = sum(1 for s in sentences if len(s.split()) > 20)

    # Normaliser sur 10
    cognitive_load = min(10, (tech_terms_count // 3) + (complex_sentences // 2))

    return cognitive_load


def _detect_dominant_emotion(text: str, stress_level: int) -> str:
    """
    Détecte l'émotion dominante
    """
    if stress_level >= 7:
        return 'stressed'
    elif stress_level <= 3:
        return 'calm'
    elif 'incertain' in text or 'peut-être' in text or 'pas sûr' in text:
        return 'uncertain'
    elif 'confiant' in text or 'sûr' in text or 'certain' in text:
        return 'confident'
    else:
        return 'neutral'


def _extract_professional_terms(text: str, professional_context: Optional[str]) -> List[str]:
    """
    Extrait les termes professionnels du texte
    Pour enrichir le lexique personnel
    """
    if not professional_context or professional_context not in PROFESSIONAL_TERMS_PATTERNS:
        return []

    terms = []
    patterns = PROFESSIONAL_TERMS_PATTERNS[professional_context]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        terms.extend(matches)

    # Dédupliquer et normaliser
    return list(set([t.lower() for t in terms]))


def _extract_general_keywords(text: str, min_length: int = 4, max_keywords: int = 10) -> List[str]:
    """
    Extrait les mots-clés généraux (noms, verbes importants)
    """
    # Supprimer les mots de liaison
    stop_words = {'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'ou', 'dans', 'sur', 'pour', 'par', 'avec', 'sans'}

    words = re.findall(r'\b\w+\b', text.lower())
    keywords = [w for w in words if len(w) >= min_length and w not in stop_words]

    # Compter les fréquences
    freq = {}
    for word in keywords:
        freq[word] = freq.get(word, 0) + 1

    # Top N mots
    sorted_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [kw for kw, _ in sorted_keywords[:max_keywords]]


def _recommend_summary_style(
    stress_level: int,
    heritage_detected: bool,
    user_country: str,
    cognitive_load: int
) -> str:
    """
    Recommande le style de résumé optimal

    - Suisse + stress élevé → 'calm_direct' (apaisant et structuré)
    - Algérie + patrimoine → 'heritage_enriched' (valorise la culture)
    - Charge cognitive élevée → 'empathetic' (empathique et simple)
    - Neutre → 'technical' (factuel)
    """
    if user_country == "switzerland" and stress_level >= 7:
        return 'calm_direct'

    if user_country == "algeria" and heritage_detected:
        return 'heritage_enriched'

    if cognitive_load >= 7:
        return 'empathetic'

    return 'technical'


def _calculate_confidence(text: str) -> float:
    """
    Calcule la confiance de l'analyse (basé sur la longueur du texte)
    """
    word_count = len(text.split())

    if word_count < 10:
        return 0.3
    elif word_count < 50:
        return 0.6
    elif word_count < 100:
        return 0.8
    else:
        return 0.95
