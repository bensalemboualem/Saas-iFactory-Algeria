"""
Digital Twin (Agent Double) Module
===================================

PHASE 2: Intelligence personnalisée et ROI

Fonctionnalités:
- Lexique personnel par professionnel (médecins, avocats, experts-comptables)
- Analyse émotionnelle et culturelle (stress, heritage)
- Tracking ROI: Tokens économisés (Faster-Whisper vs Cloud APIs)

Tables DB:
- user_preferences_lexicon: Vocabulaire privé de chaque utilisateur
- emotion_analysis_logs: Analyses émotionnelles par transcription
- tokens_saved_tracking: ROI tracking

Row-Level Security (RLS):
- Toutes les tables utilisent tenant_id pour isolation stricte
- Algérie ≠ Suisse (données jamais partagées)
"""

from . import repository
from . import router

__all__ = ["repository", "router"]
