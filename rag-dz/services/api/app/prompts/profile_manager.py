"""
Profile Manager for Specialized User Profiles
==============================================

Manages user profiles and applies appropriate system prompts based on:
- User type (Education, Psychologist, General)
- Domain/Country context (Algeria, Switzerland, Geneva)
- Professional requirements

Created: 2025-12-16
"""

from typing import Dict, Any, Optional
from enum import Enum

from .education_prompts import (
    EDUCATION_SYSTEM_PROMPT,
    EDUCATION_SUMMARY_PROMPT,
    EDUCATION_ARABIC_KEYWORDS,
    EDUCATION_FRENCH_KEYWORDS,
)
from .psychologist_prompts import (
    PSY_SYSTEM_PROMPT,
    PSY_SUMMARY_PROMPT,
    PSY_EMOTION_PROMPT,
    PSY_STRESS_INDICATORS,
    PSY_ANXIETY_INDICATORS,
    PSY_DEPRESSION_INDICATORS,
    PSY_CRISIS_KEYWORDS,
)


class UserProfile(str, Enum):
    """User profile types"""
    EDUCATION = "education"  # Algeria schools/universities
    PSYCHOLOGIST = "psychologist"  # Geneva clinical practitioners
    GENERAL = "general"  # Default multi-purpose


class DomainContext(str, Enum):
    """Domain/country context"""
    ALGERIA = "algeria"  # iafactoryalgeria.com
    SWITZERLAND = "switzerland"  # iafactory.ch
    GENEVA = "geneva"  # Default multicultural


def get_user_profile_from_domain(domain: str) -> tuple[UserProfile, DomainContext]:
    """
    Detect user profile and domain context from domain name

    Args:
        domain: Domain name (e.g., "iafactory.ch", "iafactoryalgeria.com")

    Returns:
        Tuple of (UserProfile, DomainContext)

    Examples:
        "iafactory.ch" → (PSYCHOLOGIST, SWITZERLAND)
        "iafactoryalgeria.com" → (EDUCATION, ALGERIA)
        "suisse.iafactory.pro" → (PSYCHOLOGIST, SWITZERLAND)
        "algerie.iafactory.pro" → (EDUCATION, ALGERIA)
    """
    domain_lower = domain.lower()

    # Switzerland / Psychologist profile
    if any(x in domain_lower for x in ["iafactory.ch", "suisse", "switzerland", "ch"]):
        return UserProfile.PSYCHOLOGIST, DomainContext.SWITZERLAND

    # Algeria / Education profile
    if any(x in domain_lower for x in ["algeria", "algerie", "dz"]):
        return UserProfile.EDUCATION, DomainContext.ALGERIA

    # Default: Geneva multicultural
    return UserProfile.GENERAL, DomainContext.GENEVA


def get_system_prompt(profile: UserProfile, task: str = "general") -> str:
    """
    Get specialized system prompt for user profile

    Args:
        profile: User profile type
        task: Task type ("general", "summary", "emotion")

    Returns:
        System prompt string
    """
    if profile == UserProfile.EDUCATION:
        if task == "summary":
            return EDUCATION_SUMMARY_PROMPT
        return EDUCATION_SYSTEM_PROMPT

    elif profile == UserProfile.PSYCHOLOGIST:
        if task == "summary":
            return PSY_SUMMARY_PROMPT
        elif task == "emotion":
            return PSY_EMOTION_PROMPT
        return PSY_SYSTEM_PROMPT

    else:  # GENERAL
        return _get_general_system_prompt()


def _get_general_system_prompt() -> str:
    """Default system prompt for general users"""
    return """You are an AI assistant for IA Factory - Geneva Digital Butler.

**Context**: Multicultural Geneva (110+ nationalities)
**Focus**: Voice transcription, Emotional intelligence, Cultural sensitivity

**Your Role**:
1. Provide accurate transcription summaries
2. Detect emotional states and cultural nuances
3. Extract key concepts and professional terminology
4. Support multilingual contexts (French, English, Arabic, etc.)

**Tone**: Professional, neutral, helpful

Maintain high accuracy and respect cultural diversity in all interactions.
"""


def get_profile_metadata(profile: UserProfile, context: DomainContext) -> Dict[str, Any]:
    """
    Get metadata for user profile (branding, features, etc.)

    Args:
        profile: User profile type
        context: Domain context

    Returns:
        Dict with profile metadata
    """
    if profile == UserProfile.EDUCATION:
        return {
            "profile": "education",
            "tagline": "IA Factory - Shaping the Future",
            "primary_color": "#22c55e",  # Green
            "gradient": "linear-gradient(135deg, #22c55e 0%, #15803d 100%)",
            "flag": "🇩🇿",
            "country": "Algeria",
            "focus": "Innovation & Future",
            "features": [
                "knowledge_extraction",
                "academic_terminology",
                "bilingual_french_arabic",
                "exam_preparation",
                "student_progress_tracking",
            ],
            "keywords": EDUCATION_FRENCH_KEYWORDS + EDUCATION_ARABIC_KEYWORDS,
        }

    elif profile == UserProfile.PSYCHOLOGIST:
        return {
            "profile": "psychologist",
            "tagline": "IA Factory - Privacy & Precision",
            "primary_color": "#ef4444",  # Red
            "gradient": "linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)",
            "flag": "🇨🇭",
            "country": "Switzerland",
            "focus": "Privacy & Compliance",
            "features": [
                "extreme_privacy",
                "clinical_neutrality",
                "emotion_nuance_detection",
                "stress_anxiety_tracking",
                "crisis_indicators",
                "nlpd_compliance",
            ],
            "crisis_keywords": PSY_CRISIS_KEYWORDS,
            "stress_indicators": PSY_STRESS_INDICATORS,
            "anxiety_indicators": PSY_ANXIETY_INDICATORS,
            "depression_indicators": PSY_DEPRESSION_INDICATORS,
        }

    else:  # GENERAL (Geneva Multicultural)
        return {
            "profile": "general",
            "tagline": "IA Factory - Geneva Digital Butler",
            "primary_color": "#667eea",  # Purple
            "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "flag": "🌍",
            "country": "Geneva",
            "focus": "Multicultural Intelligence",
            "features": [
                "110_nationalities_support",
                "cultural_nuances",
                "multilingual",
                "heritage_detection",
                "roi_tracking",
            ],
        }


def apply_profile_filters(
    text: str,
    profile: UserProfile,
    keywords: Optional[list] = None
) -> Dict[str, Any]:
    """
    Apply profile-specific filters and analysis

    Args:
        text: Text to analyze
        profile: User profile
        keywords: Optional keywords already extracted

    Returns:
        Dict with profile-specific analysis
    """
    result = {
        "profile": profile.value,
        "filters_applied": [],
    }

    if profile == UserProfile.PSYCHOLOGIST:
        # Check for crisis indicators
        text_lower = text.lower()
        crisis_detected = []

        for keyword in PSY_CRISIS_KEYWORDS:
            if keyword in text_lower:
                crisis_detected.append(keyword)

        if crisis_detected:
            result["crisis_alert"] = {
                "detected": True,
                "keywords": crisis_detected,
                "severity": "CRITICAL",
                "action_required": "Immediate therapist review required",
            }
            result["filters_applied"].append("crisis_detection")

        # Detect stress level
        stress_count = sum(1 for indicator in PSY_STRESS_INDICATORS if indicator in text_lower)
        anxiety_count = sum(1 for indicator in PSY_ANXIETY_INDICATORS if indicator in text_lower)
        depression_count = sum(1 for indicator in PSY_DEPRESSION_INDICATORS if indicator in text_lower)

        result["clinical_assessment"] = {
            "stress_indicators_count": stress_count,
            "anxiety_indicators_count": anxiety_count,
            "depression_indicators_count": depression_count,
            "estimated_stress_level": min(10, stress_count * 2),
            "estimated_anxiety_level": min(10, anxiety_count * 2),
        }
        result["filters_applied"].append("clinical_assessment")

    elif profile == UserProfile.EDUCATION:
        # Detect academic keywords
        text_lower = text.lower()
        french_count = sum(1 for kw in EDUCATION_FRENCH_KEYWORDS if kw in text_lower)
        arabic_keywords_found = [kw for kw in EDUCATION_ARABIC_KEYWORDS if kw in text]

        result["academic_analysis"] = {
            "french_academic_keywords": french_count,
            "arabic_keywords_found": arabic_keywords_found,
            "bilingual_content": len(arabic_keywords_found) > 0 and french_count > 0,
            "primary_language": "arabic" if len(arabic_keywords_found) > french_count else "french",
        }
        result["filters_applied"].append("academic_analysis")

    return result


# Export convenience function
def get_profile_config(domain: str) -> Dict[str, Any]:
    """
    Get complete profile configuration from domain

    Args:
        domain: Domain name

    Returns:
        Complete profile config with prompts, metadata, and filters

    Example:
        config = get_profile_config("iafactory.ch")
        # Returns Psychologist profile with Swiss branding
    """
    profile, context = get_user_profile_from_domain(domain)
    metadata = get_profile_metadata(profile, context)

    return {
        "profile": profile.value,
        "context": context.value,
        "metadata": metadata,
        "system_prompt": get_system_prompt(profile),
        "summary_prompt": get_system_prompt(profile, task="summary"),
    }
