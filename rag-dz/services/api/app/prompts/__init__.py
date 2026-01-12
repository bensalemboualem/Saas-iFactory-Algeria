"""
Prompt Library for Specialized Profiles
========================================

PHASE 4: Expert Layer

Two specialized profiles:
1. Algeria Education: Schools (French/Arabic, academic terminology)
2. Geneva Psychologist: Clinical (privacy, emotional nuance, stress/anxiety)

Created: 2025-12-16
"""

from .education_prompts import EDUCATION_SYSTEM_PROMPT, EDUCATION_SUMMARY_PROMPT
from .psychologist_prompts import PSY_SYSTEM_PROMPT, PSY_SUMMARY_PROMPT, PSY_EMOTION_PROMPT
from .profile_manager import (
    UserProfile,
    DomainContext,
    get_user_profile_from_domain,
    get_system_prompt,
    get_profile_metadata,
    get_profile_config,
    apply_profile_filters,
)

__all__ = [
    # Direct prompts
    "EDUCATION_SYSTEM_PROMPT",
    "EDUCATION_SUMMARY_PROMPT",
    "PSY_SYSTEM_PROMPT",
    "PSY_SUMMARY_PROMPT",
    "PSY_EMOTION_PROMPT",
    # Profile management
    "UserProfile",
    "DomainContext",
    "get_user_profile_from_domain",
    "get_system_prompt",
    "get_profile_metadata",
    "get_profile_config",
    "apply_profile_filters",
]
