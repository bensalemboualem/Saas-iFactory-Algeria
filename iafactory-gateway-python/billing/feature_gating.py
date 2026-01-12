"""
IAFactory - Feature Gating System
==================================
Contrôle d'accès aux fonctionnalités par plan
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime

# ==============================================
# FEATURE DEFINITIONS
# ==============================================

class Feature(Enum):
    # Basic (Gratuit)
    CHAT_BASIC = "chat_basic"
    RAG_BASIC = "rag_basic"
    QUERIES_LIMITED = "queries_limited"  # 5/jour

    # Pro
    CHAT_UNLIMITED = "chat_unlimited"
    RAG_ADVANCED = "rag_advanced"
    VOICE_TTS = "voice_tts"
    VOICE_STT = "voice_stt"
    EMAIL_INTEGRATION = "email_integration"
    CALENDAR_SYNC = "calendar_sync"

    # Business
    VIDEO_SHORT = "video_short"
    VIDEO_FULL = "video_full"
    DOCUMENT_GENERATION = "document_generation"
    WORKFLOW_AUTOMATION = "workflow_automation"
    AI_AGENTS = "ai_agents"
    API_ACCESS = "api_access"

    # Enterprise
    DEDICATED_SERVER = "dedicated_server"
    CUSTOM_MODELS = "custom_models"
    WHITE_LABEL = "white_label"
    SLA_99 = "sla_99"
    SLA_999 = "sla_999"

    # Digital Twin
    DIGITAL_TWIN = "digital_twin"
    VOICE_CLONE = "voice_clone"
    PERSONALITY_AI = "personality_ai"
    AVAILABILITY_24_7 = "availability_24_7"

# ==============================================
# PLAN DEFINITIONS
# ==============================================

@dataclass
class Plan:
    id: str
    name: str
    name_ar: str
    features: Set[Feature]
    credits_monthly: int
    price_chf: float
    price_dzd: float
    max_users: int
    daily_limit: Optional[int] = None  # None = unlimited

PLANS: Dict[str, Plan] = {
    # Algérie
    "dz_starter": Plan(
        id="dz_starter",
        name="Starter",
        name_ar="المبتدئ",
        features={Feature.CHAT_BASIC, Feature.RAG_BASIC, Feature.QUERIES_LIMITED},
        credits_monthly=100,
        price_chf=0,
        price_dzd=0,
        max_users=1,
        daily_limit=5
    ),
    "dz_pro": Plan(
        id="dz_pro",
        name="Pro",
        name_ar="المحترف",
        features={
            Feature.CHAT_UNLIMITED, Feature.RAG_ADVANCED,
            Feature.VOICE_TTS, Feature.VOICE_STT,
            Feature.EMAIL_INTEGRATION
        },
        credits_monthly=1000,
        price_chf=9.90,
        price_dzd=1990,
        max_users=3
    ),
    "dz_business": Plan(
        id="dz_business",
        name="Business",
        name_ar="الأعمال",
        features={
            Feature.CHAT_UNLIMITED, Feature.RAG_ADVANCED,
            Feature.VOICE_TTS, Feature.VOICE_STT,
            Feature.EMAIL_INTEGRATION, Feature.CALENDAR_SYNC,
            Feature.VIDEO_SHORT, Feature.DOCUMENT_GENERATION,
            Feature.WORKFLOW_AUTOMATION, Feature.API_ACCESS
        },
        credits_monthly=5000,
        price_chf=29.90,
        price_dzd=5990,
        max_users=10
    ),

    # Suisse
    "ch_pro": Plan(
        id="ch_pro",
        name="Pro CH",
        name_ar="المحترف سويسرا",
        features={
            Feature.CHAT_UNLIMITED, Feature.RAG_ADVANCED,
            Feature.VOICE_TTS, Feature.VOICE_STT,
            Feature.EMAIL_INTEGRATION, Feature.CALENDAR_SYNC
        },
        credits_monthly=2000,
        price_chf=29.90,
        price_dzd=5990,
        max_users=3
    ),
    "ch_business": Plan(
        id="ch_business",
        name="Business CH",
        name_ar="الأعمال سويسرا",
        features={
            Feature.CHAT_UNLIMITED, Feature.RAG_ADVANCED,
            Feature.VOICE_TTS, Feature.VOICE_STT,
            Feature.EMAIL_INTEGRATION, Feature.CALENDAR_SYNC,
            Feature.VIDEO_SHORT, Feature.VIDEO_FULL,
            Feature.DOCUMENT_GENERATION, Feature.WORKFLOW_AUTOMATION,
            Feature.AI_AGENTS, Feature.API_ACCESS, Feature.SLA_99
        },
        credits_monthly=10000,
        price_chf=99.90,
        price_dzd=19990,
        max_users=25
    ),
    "ch_enterprise": Plan(
        id="ch_enterprise",
        name="Enterprise",
        name_ar="المؤسسات",
        features={f for f in Feature},  # Toutes les features
        credits_monthly=50000,
        price_chf=299.90,
        price_dzd=59990,
        max_users=-1  # Illimité
    ),

    # Digital Twin
    "digital_twin": Plan(
        id="digital_twin",
        name="Double Numérique",
        name_ar="التوأم الرقمي",
        features={
            Feature.CHAT_UNLIMITED, Feature.RAG_ADVANCED,
            Feature.VOICE_TTS, Feature.VOICE_STT,
            Feature.EMAIL_INTEGRATION, Feature.CALENDAR_SYNC,
            Feature.VIDEO_SHORT, Feature.VIDEO_FULL,
            Feature.DOCUMENT_GENERATION, Feature.WORKFLOW_AUTOMATION,
            Feature.AI_AGENTS, Feature.API_ACCESS,
            Feature.DIGITAL_TWIN, Feature.VOICE_CLONE,
            Feature.PERSONALITY_AI, Feature.AVAILABILITY_24_7
        },
        credits_monthly=20000,
        price_chf=149.90,
        price_dzd=29990,
        max_users=1
    ),
}

# ==============================================
# FEATURE GATING SERVICE
# ==============================================

class FeatureGatingService:
    """Service de contrôle d'accès aux fonctionnalités"""

    def __init__(self):
        self.plans = PLANS

    def check_feature_access(
        self,
        user_plan_id: str,
        feature: Feature
    ) -> Dict:
        """
        Vérifie si un utilisateur a accès à une fonctionnalité

        Returns:
            {
                "allowed": bool,
                "reason": str,
                "upgrade_plan": str | None
            }
        """
        plan = self.plans.get(user_plan_id)

        if not plan:
            return {
                "allowed": False,
                "reason": "Plan invalide",
                "upgrade_plan": "dz_starter"
            }

        if feature in plan.features:
            return {
                "allowed": True,
                "reason": "Accès autorisé",
                "upgrade_plan": None
            }

        # Trouver le plan minimum qui inclut cette feature
        upgrade_plan = self._find_upgrade_plan(feature, user_plan_id)

        return {
            "allowed": False,
            "reason": f"Cette fonctionnalité nécessite le plan {upgrade_plan}",
            "upgrade_plan": upgrade_plan
        }

    def _find_upgrade_plan(self, feature: Feature, current_plan_id: str) -> str:
        """Trouve le plan minimum pour une feature"""
        current_plan = self.plans.get(current_plan_id)
        current_price = current_plan.price_chf if current_plan else 0

        # Trier les plans par prix
        sorted_plans = sorted(
            self.plans.values(),
            key=lambda p: p.price_chf
        )

        for plan in sorted_plans:
            if plan.price_chf > current_price and feature in plan.features:
                return plan.id

        return "ch_enterprise"  # Fallback

    def get_plan_features(self, plan_id: str) -> List[str]:
        """Retourne la liste des features d'un plan"""
        plan = self.plans.get(plan_id)
        if not plan:
            return []
        return [f.value for f in plan.features]

    def get_upgrade_suggestions(self, user_plan_id: str) -> Dict:
        """
        Suggère des upgrades basés sur l'usage
        """
        plan = self.plans.get(user_plan_id)
        if not plan:
            return {}

        suggestions = []
        sorted_plans = sorted(
            self.plans.values(),
            key=lambda p: p.price_chf
        )

        for p in sorted_plans:
            if p.price_chf > plan.price_chf:
                new_features = p.features - plan.features
                if new_features:
                    suggestions.append({
                        "plan_id": p.id,
                        "plan_name": p.name,
                        "price_chf": p.price_chf,
                        "price_dzd": p.price_dzd,
                        "new_features": [f.value for f in new_features],
                        "extra_credits": p.credits_monthly - plan.credits_monthly
                    })

        return {
            "current_plan": user_plan_id,
            "suggestions": suggestions[:3]  # Top 3
        }

    def generate_gate_response(
        self,
        feature: Feature,
        allowed: bool,
        upgrade_plan: Optional[str] = None
    ) -> Dict:
        """Génère une réponse pour le frontend"""
        if allowed:
            return {
                "status": "allowed",
                "message": None,
                "cta": None
            }

        upgrade = self.plans.get(upgrade_plan) if upgrade_plan else None

        return {
            "status": "blocked",
            "message": {
                "fr": f"Cette fonctionnalité nécessite le plan {upgrade.name if upgrade else 'supérieur'}",
                "ar": f"هذه الميزة تتطلب خطة {upgrade.name_ar if upgrade else 'أعلى'}",
                "en": f"This feature requires the {upgrade.name if upgrade else 'higher'} plan"
            },
            "cta": {
                "text": {
                    "fr": f"Passer à {upgrade.name if upgrade else 'Premium'}",
                    "ar": f"الترقية إلى {upgrade.name_ar if upgrade else 'بريميوم'}",
                    "en": f"Upgrade to {upgrade.name if upgrade else 'Premium'}"
                },
                "url": f"/pricing?upgrade={upgrade_plan}",
                "price": {
                    "chf": upgrade.price_chf if upgrade else 0,
                    "dzd": upgrade.price_dzd if upgrade else 0
                }
            }
        }


# ==============================================
# MIDDLEWARE DECORATOR
# ==============================================

def require_feature(feature: Feature):
    """
    Decorator pour protéger les endpoints par feature

    Usage:
        @require_feature(Feature.VIDEO_FULL)
        async def generate_video(request):
            ...
    """
    def decorator(func):
        async def wrapper(request, *args, **kwargs):
            # Get user plan from request (JWT token, session, etc.)
            user_plan = getattr(request.state, 'user_plan', 'dz_starter')

            gating = FeatureGatingService()
            access = gating.check_feature_access(user_plan, feature)

            if not access["allowed"]:
                from fastapi import HTTPException
                raise HTTPException(
                    status_code=403,
                    detail=gating.generate_gate_response(
                        feature,
                        allowed=False,
                        upgrade_plan=access["upgrade_plan"]
                    )
                )

            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


# ==============================================
# TEST
# ==============================================

if __name__ == "__main__":
    service = FeatureGatingService()

    print("=" * 60)
    print("FEATURE GATING TEST")
    print("=" * 60)

    # Test différents scénarios
    tests = [
        ("dz_starter", Feature.CHAT_BASIC, "Chat basique"),
        ("dz_starter", Feature.VIDEO_FULL, "Vidéo complète"),
        ("dz_pro", Feature.VOICE_TTS, "Text-to-Speech"),
        ("dz_pro", Feature.AI_AGENTS, "Agents IA"),
        ("ch_business", Feature.AI_AGENTS, "Agents IA"),
        ("digital_twin", Feature.VOICE_CLONE, "Clone vocal"),
    ]

    for plan_id, feature, desc in tests:
        result = service.check_feature_access(plan_id, feature)
        status = "✅" if result["allowed"] else "❌"
        print(f"\n{status} [{plan_id}] {desc}")
        if not result["allowed"]:
            print(f"   → Upgrade: {result['upgrade_plan']}")

    # Test suggestions upgrade
    print("\n" + "=" * 60)
    print("UPGRADE SUGGESTIONS (dz_pro)")
    print("=" * 60)
    suggestions = service.get_upgrade_suggestions("dz_pro")
    for s in suggestions["suggestions"]:
        print(f"\n→ {s['plan_name']} ({s['price_chf']} CHF)")
        print(f"  +{s['extra_credits']} crédits")
        print(f"  Nouvelles features: {', '.join(s['new_features'][:3])}...")
