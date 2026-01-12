"""
IAFactory - Configuration Tarification IA SaaS
================================================
Basé sur analyse Userpilot + IntuitionLabs 2025
Modèle: Crédits IA + Outcome-based pricing
"""

from dataclasses import dataclass
from typing import Dict, Optional, List
from enum import Enum
import json

# ==============================================
# COÛTS API ($/1M tokens) - Source: IntuitionLabs 2025
# ==============================================
API_COSTS = {
    "groq_llama": {"input": 0.20, "output": 0.50},      # Leader coût
    "grok_4_fast": {"input": 0.20, "output": 0.50},     # xAI
    "gemini_2_flash": {"input": 0.075, "output": 0.30}, # Google Flash
    "gemini_2_pro": {"input": 1.25, "output": 10.00},   # Google Pro
    "gpt_4o": {"input": 5.00, "output": 15.00},         # OpenAI
    "gpt_4o_mini": {"input": 0.15, "output": 0.60},     # OpenAI Mini
    "claude_sonnet": {"input": 3.00, "output": 15.00},  # Anthropic
    "claude_opus": {"input": 15.00, "output": 75.00},   # Anthropic Premium
}

# ==============================================
# SYSTÈME DE CRÉDITS IA
# ==============================================
class CreditType(Enum):
    TEXT = "text"
    VOICE = "voice"
    VIDEO = "video"
    IMAGE = "image"
    DOCUMENT = "document"
    WORKFLOW = "workflow"

# Coût en crédits par opération
CREDIT_COSTS = {
    # Chat & RAG (Low cost)
    "chat_message": 1,
    "rag_query": 2,
    "rag_complex": 5,

    # Voice (Medium cost)
    "voice_minute": 2,
    "voice_call": 10,
    "voice_agent": 20,

    # Video (High cost - Premium)
    "video_short": 50,
    "video_standard": 100,
    "video_long": 200,

    # Image (Medium cost)
    "image_generate": 10,
    "image_edit": 5,

    # Documents (Outcome-based)
    "doc_contract": 25,
    "doc_legal": 30,
    "doc_invoice": 5,
    "doc_report": 15,

    # Workflows (Value-based)
    "workflow_simple": 5,
    "workflow_complex": 20,
    "workflow_agent": 50,
}

# ==============================================
# PLANS TARIFAIRES
# ==============================================
@dataclass
class PricingPlan:
    name: str
    name_ar: str
    name_en: str
    price_chf: float
    price_dzd: float
    price_eur: float
    credits_monthly: int
    features: List[str]
    overage_rate_chf: float
    overage_rate_dzd: float
    max_users: int
    popular: bool = False

PLANS = {
    # ===========================================
    # 🚀 STRATÉGIE xAI - ALGÉRIE DOMINATION
    # ===========================================
    # Inspiré du contrat xAI gouvernement US: $0.42/agence/an
    # Objectif: Écraser la concurrence, lock-in institutionnel

    "dz_gov_agency": PricingPlan(
        name="Gouvernement Agence",
        name_ar="الوكالة الحكومية",
        name_en="Government Agency",
        price_chf=3.70,        # ~500 DZD
        price_dzd=500,         # 🔥 500 DZD/AN = $3.70/an comme xAI!
        price_eur=3.50,
        credits_monthly=500,   # 6000 crédits/an
        features=["chat", "rag", "voice", "email", "documents", "gov_priority"],
        overage_rate_chf=0.10,
        overage_rate_dzd=2,
        max_users=10
    ),
    "dz_gov_ministry": PricingPlan(
        name="Gouvernement Ministère",
        name_ar="الوزارة",
        name_en="Government Ministry",
        price_chf=37.00,       # ~5000 DZD
        price_dzd=5000,        # 🔥 5000 DZD/AN pour tout un ministère!
        price_eur=35.00,
        credits_monthly=10000, # 120,000 crédits/an
        features=["all", "gov_priority", "dedicated_support", "custom_training", "data_sovereignty"],
        overage_rate_chf=0.05,
        overage_rate_dzd=1,
        max_users=100
    ),
    "dz_gov_national": PricingPlan(
        name="Pack National",
        name_ar="الباقة الوطنية",
        name_en="National Pack",
        price_chf=370.00,      # ~50,000 DZD
        price_dzd=50000,       # 🔥 50,000 DZD/AN = accès national illimité
        price_eur=340.00,
        credits_monthly=100000,
        features=["all", "unlimited_agencies", "gov_priority", "on_premise_option", "24_7_support", "training_included"],
        overage_rate_chf=0.02,
        overage_rate_dzd=0.5,
        max_users=-1           # Illimité
    ),

    # ===========================================
    # 🎓 ÉDUCATION - GRATUIT (investissement futur)
    # ===========================================
    "dz_edu_university": PricingPlan(
        name="Université",
        name_ar="الجامعة",
        name_en="University",
        price_chf=0,
        price_dzd=0,           # 🎁 GRATUIT pour universités!
        price_eur=0,
        credits_monthly=2000,  # 24,000 crédits/an gratuits
        features=["chat", "rag", "voice", "documents", "edu_badge"],
        overage_rate_chf=0.10,
        overage_rate_dzd=2,
        max_users=50           # Étudiants + profs
    ),
    "dz_edu_student": PricingPlan(
        name="Étudiant",
        name_ar="الطالب",
        name_en="Student",
        price_chf=0,
        price_dzd=0,           # 🎁 GRATUIT pour étudiants!
        price_eur=0,
        credits_monthly=200,
        features=["chat", "rag_basic", "edu_badge"],
        overage_rate_chf=0.20,
        overage_rate_dzd=4,
        max_users=1
    ),

    # ===========================================
    # 🚀 STARTUPS - Prix de lancement agressif
    # ===========================================
    "dz_startup": PricingPlan(
        name="Startup",
        name_ar="الشركة الناشئة",
        name_en="Startup",
        price_chf=7.00,
        price_dzd=990,         # 🔥 990 DZD/AN = ~$7/an!
        price_eur=6.50,
        credits_monthly=1000,
        features=["chat", "rag", "voice", "email", "api_access", "startup_badge"],
        overage_rate_chf=0.15,
        overage_rate_dzd=3,
        max_users=5
    ),
    "dz_pme": PricingPlan(
        name="PME",
        name_ar="المؤسسة الصغيرة",
        name_en="SMB",
        price_chf=22.00,
        price_dzd=2990,        # 🔥 2990 DZD/AN = ~$22/an!
        price_eur=20.00,
        credits_monthly=3000,
        features=["chat", "rag", "voice", "email", "documents", "workflows", "api_access"],
        overage_rate_chf=0.12,
        overage_rate_dzd=2.5,
        max_users=15
    ),

    # ===========================================
    # ALGÉRIE - Plans standard (volume)
    # ===========================================
    "dz_starter": PricingPlan(
        name="Starter",
        name_ar="المبتدئ",
        name_en="Starter",
        price_chf=0,
        price_dzd=0,
        price_eur=0,
        credits_monthly=100,
        features=["chat", "rag_basic", "5_queries_day"],
        overage_rate_chf=0.50,
        overage_rate_dzd=10,
        max_users=1
    ),
    "dz_pro": PricingPlan(
        name="Pro",
        name_ar="المحترف",
        name_en="Pro",
        price_chf=9.90,
        price_dzd=1990,
        price_eur=9.00,
        credits_monthly=1000,
        features=["chat", "rag", "voice", "email", "unlimited_queries"],
        overage_rate_chf=0.25,
        overage_rate_dzd=5,
        max_users=3,
        popular=True
    ),
    "dz_business": PricingPlan(
        name="Business",
        name_ar="الأعمال",
        name_en="Business",
        price_chf=29.90,
        price_dzd=5990,
        price_eur=27.00,
        credits_monthly=5000,
        features=["chat", "rag", "voice", "video_short", "documents", "workflows", "api_access"],
        overage_rate_chf=0.15,
        overage_rate_dzd=3,
        max_users=10
    ),

    # ===========================================
    # SUISSE - Marché haute valeur
    # ===========================================
    "ch_pro": PricingPlan(
        name="Pro Suisse",
        name_ar="المحترف سويسرا",
        name_en="Pro Switzerland",
        price_chf=29.90,
        price_dzd=5990,
        price_eur=27.00,
        credits_monthly=2000,
        features=["chat", "rag", "voice", "email", "calendar", "priority_support"],
        overage_rate_chf=0.25,
        overage_rate_dzd=5,
        max_users=3
    ),
    "ch_business": PricingPlan(
        name="Business Suisse",
        name_ar="الأعمال سويسرا",
        name_en="Business Switzerland",
        price_chf=99.90,
        price_dzd=19990,
        price_eur=92.00,
        credits_monthly=10000,
        features=["chat", "rag", "voice", "video", "documents", "workflows", "agents", "api_access", "sla_99"],
        overage_rate_chf=0.15,
        overage_rate_dzd=3,
        max_users=25,
        popular=True
    ),
    "ch_enterprise": PricingPlan(
        name="Enterprise",
        name_ar="المؤسسات",
        name_en="Enterprise",
        price_chf=299.90,
        price_dzd=59990,
        price_eur=275.00,
        credits_monthly=50000,
        features=["all", "dedicated_server", "custom_models", "white_label", "sla_999"],
        overage_rate_chf=0.10,
        overage_rate_dzd=2,
        max_users=-1
    ),

    # ===========================================
    # DOUBLE NUMÉRIQUE - Premium
    # ===========================================
    "digital_twin": PricingPlan(
        name="Double Numérique",
        name_ar="التوأم الرقمي",
        name_en="Digital Twin",
        price_chf=149.90,
        price_dzd=29990,
        price_eur=137.00,
        credits_monthly=20000,
        features=["all", "digital_twin", "voice_clone", "personality_ai", "24_7_availability"],
        overage_rate_chf=0.08,
        overage_rate_dzd=2,
        max_users=1,
        popular=True
    ),
}

# ==============================================
# FEATURE GATING (avec stratégie xAI)
# ==============================================
# Plans gouvernement/éducation/startup ont accès généreux pour lock-in
ALL_DZ_PLANS = ["dz_gov_agency", "dz_gov_ministry", "dz_gov_national", "dz_edu_university", "dz_edu_student", "dz_startup", "dz_pme", "dz_starter", "dz_pro", "dz_business"]
ALL_CH_PLANS = ["ch_pro", "ch_business", "ch_enterprise"]
GOV_PLANS = ["dz_gov_agency", "dz_gov_ministry", "dz_gov_national"]
EDU_PLANS = ["dz_edu_university", "dz_edu_student"]
PREMIUM_DZ = ["dz_gov_ministry", "dz_gov_national", "dz_pme", "dz_business"]
PREMIUM_CH = ["ch_business", "ch_enterprise"]

FEATURE_GATES = {
    # Basique - tout le monde
    "chat": ALL_DZ_PLANS + ALL_CH_PLANS + ["digital_twin"],
    "rag_basic": ALL_DZ_PLANS + ALL_CH_PLANS + ["digital_twin"],

    # RAG avancé - plans payants + gouvernement (stratégie xAI: donner aux institutions)
    "rag": GOV_PLANS + EDU_PLANS + ["dz_startup", "dz_pme", "dz_pro", "dz_business"] + ALL_CH_PLANS + ["digital_twin"],

    # Voice - généreux pour gouvernement/éducation
    "voice": GOV_PLANS + ["dz_edu_university", "dz_startup", "dz_pme", "dz_pro", "dz_business"] + ALL_CH_PLANS + ["digital_twin"],

    # Email - plans payants + institutions
    "email": GOV_PLANS + ["dz_startup", "dz_pme", "dz_pro", "dz_business"] + ALL_CH_PLANS + ["digital_twin"],

    # Documents - gouvernement + business
    "documents": GOV_PLANS + ["dz_edu_university", "dz_pme", "dz_business"] + ALL_CH_PLANS + ["digital_twin"],

    # Video court - business seulement
    "video_short": ["dz_gov_national", "dz_business"] + PREMIUM_CH + ["digital_twin"],

    # Video complet - premium uniquement (profit center)
    "video": PREMIUM_CH + ["digital_twin"],

    # Workflows - business + gouvernement avancé
    "workflows": ["dz_gov_ministry", "dz_gov_national", "dz_pme", "dz_business"] + ALL_CH_PLANS + ["digital_twin"],

    # Agents IA - premium CH (profit center)
    "agents": PREMIUM_CH + ["dz_gov_national", "digital_twin"],

    # API access - startups + business (pour intégrations)
    "api_access": GOV_PLANS + ["dz_startup", "dz_pme", "dz_business"] + ALL_CH_PLANS + ["digital_twin"],

    # Digital Twin - exclusif
    "digital_twin": ["digital_twin"],

    # Features spéciales gouvernement
    "gov_priority": GOV_PLANS,
    "data_sovereignty": ["dz_gov_ministry", "dz_gov_national", "ch_enterprise"],
    "on_premise_option": ["dz_gov_national", "ch_enterprise"],

    # Badges (pour marketing/communauté)
    "edu_badge": EDU_PLANS,
    "startup_badge": ["dz_startup"],
}

# ==============================================
# CALCUL ROI
# ==============================================
ROI_VALUES_CHF = {
    "chat_message": 0.50,
    "rag_query": 2.00,
    "voice_minute": 5.00,
    "voice_call": 25.00,
    "doc_contract": 150.00,
    "doc_legal": 200.00,
    "workflow_run": 10.00,
    "agent_task": 50.00,
}

TIME_SAVED_MINUTES = {
    "chat_message": 2,
    "rag_query": 10,
    "voice_minute": 5,
    "doc_contract": 120,
    "doc_legal": 180,
    "workflow_run": 30,
}

def calculate_user_roi(usage: Dict[str, int]) -> Dict:
    """Calcule le ROI pour affichage dashboard"""
    total_value = 0
    total_time = 0

    for action, count in usage.items():
        if action in ROI_VALUES_CHF:
            total_value += ROI_VALUES_CHF[action] * count
        if action in TIME_SAVED_MINUTES:
            total_time += TIME_SAVED_MINUTES[action] * count

    return {
        "money_saved_chf": round(total_value, 2),
        "money_saved_dzd": round(total_value * 200, 2),  # Taux approximatif
        "time_saved_hours": round(total_time / 60, 1),
        "equivalent_salary_chf": round(total_time / 60 * 50, 2),
        "tasks_completed": sum(usage.values()),
    }

def export_plans_json():
    """Exporte les plans en JSON pour le frontend"""
    plans_json = {}
    for key, plan in PLANS.items():
        plans_json[key] = {
            "name": plan.name,
            "name_ar": plan.name_ar,
            "name_en": plan.name_en,
            "price": {
                "chf": plan.price_chf,
                "dzd": plan.price_dzd,
                "eur": plan.price_eur,
            },
            "credits": plan.credits_monthly,
            "features": plan.features,
            "overage": {
                "chf": plan.overage_rate_chf,
                "dzd": plan.overage_rate_dzd,
            },
            "max_users": plan.max_users,
            "popular": plan.popular,
        }
    return plans_json

if __name__ == "__main__":
    print("IAFactory Pricing Configuration")
    print("=" * 50)
    print(f"Plans disponibles: {len(PLANS)}")
    for key, plan in PLANS.items():
        print(f"  - {plan.name}: {plan.price_chf} CHF / {plan.price_dzd} DZD")
    print(f"\nFeatures gérées: {len(FEATURE_GATES)}")
    print(f"Types de crédits: {len(CREDIT_COSTS)}")

    # Export JSON
    with open("plans.json", "w") as f:
        json.dump(export_plans_json(), f, indent=2, ensure_ascii=False)
    print("\nPlans exportés vers plans.json")
