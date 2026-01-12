"""
Geneva Multi-Cultural Intelligence Module
=========================================

Support 110+ nationalités de Genève

Fonctionnalités:
- Cultural nuances detection (expressions culturelles)
- Multi-language detection dans un même audio
- Geneva Mode: Haute précision pour accents non-natifs
- User linguistic profiles

Created: 2025-01-16
"""

from . import multicultural_service
from . import repository

__all__ = ["multicultural_service", "repository"]
