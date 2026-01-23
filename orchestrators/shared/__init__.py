"""
Shared modules for Nexus orchestrators.
Specific to IA Factory Algeria.
"""

from .chargily import ChargilyService, ChargilyPayment, ChargilyCheckout, CREDIT_PACKS
from .darija import DarijaService, DARIJA_TRANSLATIONS, DARIJA_PROMPTS, get_darija_service
from .credits import CreditSystem, CreditOperation, CreditBalance, CREDIT_RATES, get_credit_system
from .conformity import ConformityChecker, ConformityResult, ConformityLevel, get_conformity_checker
from .knowledge_dz import KnowledgeIndexer, DZ_KNOWLEDGE_SOURCES, WILAYAS
from .ui_rules import (
    UI_RULES,
    UIViolation,
    UIValidationResult,
    Severity,
    validate_ui,
    validate_ui_strict,
    get_tailwind_config,
    get_css_variables,
    get_i18n_config,
)

__all__ = [
    # Chargily
    "ChargilyService",
    "ChargilyPayment",
    "ChargilyCheckout",
    "CREDIT_PACKS",
    # Darija
    "DarijaService",
    "DARIJA_TRANSLATIONS",
    "DARIJA_PROMPTS",
    "get_darija_service",
    # Credits
    "CreditSystem",
    "CreditOperation",
    "CreditBalance",
    "CREDIT_RATES",
    "get_credit_system",
    # Conformity
    "ConformityChecker",
    "ConformityResult",
    "ConformityLevel",
    "get_conformity_checker",
    # Knowledge DZ
    "KnowledgeIndexer",
    "DZ_KNOWLEDGE_SOURCES",
    "WILAYAS",
    # UI Rules
    "UI_RULES",
    "UIViolation",
    "UIValidationResult",
    "Severity",
    "validate_ui",
    "validate_ui_strict",
    "get_tailwind_config",
    "get_css_variables",
    "get_i18n_config",
]

# Shared Utilities Package
