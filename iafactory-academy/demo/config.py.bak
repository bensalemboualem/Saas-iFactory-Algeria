"""
IAFactory Academy - Configuration System
Switch ON/OFF pour versions BBC / Générique / Autres écoles
"""

from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime

# ============================================
# VERSIONS CONFIGURATION
# ============================================

VERSIONS: Dict[str, Dict[str, Any]] = {
    "generic": {
        "enabled": False,  # OFF - BBC activé pour test
        "name": "generic",
        "display_name": "IAFactory-School",
        "display_name_ar": "مدرسة IAFactory",
        "tagline": "Programme National IA pour l'Éducation",
        "tagline_ar": "البرنامج الوطني للذكاء الاصطناعي للتعليم",
        "logo_emoji": "🎓",
        "primary_color": "#3B82F6",  # Blue
        "students": 1600,
        "teachers": 20,
        "demo_mode": True,  # Permet modification dynamique
        "launch_date": "2026-02-03",
        "partner_type": "prospect",
        "contact_email": "contact@iafactory.ai",
    },
    "bbc": {
        "enabled": True,  # ✅ ACTIVÉ POUR TEST
        "name": "bbc",
        "display_name": "BBC School",
        "display_name_ar": "مدرسة بي بي سي",
        "tagline": "BBC School × IAFactory - Partenariat Stratégique",
        "tagline_ar": "مدرسة بي بي سي × IAFactory - شراكة استراتيجية",
        "logo_emoji": "🇩🇿",
        "primary_color": "#006233",  # Algeria Green
        "students": 1600,
        "teachers": 20,
        "demo_mode": False,  # Configuration fixe
        "launch_date": "2026-02-03",
        "partner_type": "strategic",
        "contact_email": "bbc@iafactory.ai",
        "special_note": "Partenaire stratégique - Investissement 100% IAFactory",
    },
    "nouvelle_horizon": {
        "enabled": False,  # OFF - Template pour nouvelle école
        "name": "nouvelle_horizon",
        "display_name": "Nouvelle Horizon Academy",
        "display_name_ar": "أكاديمية الأفق الجديد",
        "tagline": "Excellence Éducative avec l'IA",
        "tagline_ar": "التميز التعليمي مع الذكاء الاصطناعي",
        "logo_emoji": "🌟",
        "primary_color": "#8B5CF6",  # Purple
        "students": 500,
        "teachers": 12,
        "demo_mode": False,
        "launch_date": "2026-09-01",
        "partner_type": "client",
        "contact_email": "contact@iafactory.ai",
    },
}


# ============================================
# PRICING CONFIGURATION
# ============================================

PRICING_TIERS = [
    {"min": 0, "max": 499, "price_per_student": 700},      # < 500 élèves
    {"min": 500, "max": 999, "price_per_student": 650},    # 500-999
    {"min": 1000, "max": 1999, "price_per_student": 600},  # 1000-1999
    {"min": 2000, "max": float('inf'), "price_per_student": 550},  # 2000+
]

# Investissement IAFactory (forfait par école pilote)
IAFACTORY_COSTS = {
    "formation_forfait": 500000,     # DA forfait (20 enseignants)
    "support_forfait": 800000,       # DA support 6 mois
    "infrastructure": 0,             # DA (déjà en place chez l'école)
    "content_creation": 2000000,     # DA pour 38 leçons
    "platform_setup": 1500000,       # DA plateforme RAG
}

# ROI Projections
ROI_SCENARIOS = {
    "pessimistic": {"schools_phase2": 25, "schools_phase3": 250, "multiplier": 0.5},
    "realistic": {"schools_phase2": 50, "schools_phase3": 375, "multiplier": 0.75},
    "optimistic": {"schools_phase2": 75, "schools_phase3": 500, "multiplier": 1.0},
}


# ============================================
# CALCULATION FUNCTIONS
# ============================================

def calculate_pricing(students: int) -> Dict[str, Any]:
    """
    Calcule le prix dégressif basé sur le nombre d'élèves
    Retourne prix/mois/élève et total annuel
    """
    price_per_student = 700  # Default

    for tier in PRICING_TIERS:
        if tier["min"] <= students <= tier["max"]:
            price_per_student = tier["price_per_student"]
            break

    monthly_total = students * price_per_student
    annual_total = monthly_total * 10  # 10 mois scolaires

    return {
        "students": students,
        "price_per_student_month": price_per_student,
        "monthly_total": monthly_total,
        "annual_total": annual_total,
        "annual_total_millions": round(annual_total / 1_000_000, 2),
        "tier_label": get_tier_label(students),
    }


def get_tier_label(students: int) -> str:
    """Retourne le label du tier de prix"""
    if students < 500:
        return "Standard"
    elif students < 1000:
        return "Premium"
    elif students < 2000:
        return "Enterprise"
    else:
        return "National"


def calculate_iafactory_investment(students: int) -> Dict[str, Any]:
    """
    Calcule l'investissement total IAFactory pour une école
    Utilise des forfaits fixes (pas de calcul par élève)
    """
    formation = IAFACTORY_COSTS["formation_forfait"]
    support = IAFACTORY_COSTS["support_forfait"]
    content = IAFACTORY_COSTS["content_creation"]
    platform = IAFACTORY_COSTS["platform_setup"]
    infrastructure = IAFACTORY_COSTS["infrastructure"]

    total = formation + support + content + platform + infrastructure

    return {
        "formation": formation,
        "support": support,
        "content": content,
        "platform": platform,
        "infrastructure": infrastructure,
        "total": total,
        "total_millions": round(total / 1_000_000, 2),
        "breakdown": {
            "Formation enseignants": formation,
            "Support technique": support,
            "Création contenu": content,
            "Plateforme RAG": platform,
            "Infrastructure": infrastructure,
        }
    }


def calculate_roi(students: int, years: int = 3) -> Dict[str, Any]:
    """
    Calcule le ROI sur plusieurs années avec 3 scénarios
    Phase 1: École pilote (investissement)
    Phase 2: Expansion écoles privées
    Phase 3: Contrat national
    """
    pricing = calculate_pricing(students)
    investment = calculate_iafactory_investment(students)

    results = {}

    for scenario_name, scenario in ROI_SCENARIOS.items():
        # Phase 1: Investissement (année 1)
        phase1_revenue = 0  # Gratuit pour école pilote
        phase1_cost = investment["total"]

        # Phase 2: Écoles privées (année 2)
        phase2_schools = scenario["schools_phase2"]
        phase2_students = phase2_schools * 100  # ~100 élèves/école moyenne
        phase2_pricing = calculate_pricing(phase2_students)
        phase2_revenue = phase2_schools * 1_100_000  # 1.1M DA par école
        phase2_cost = 500_000  # Maintenance

        # Phase 3: National (année 3)
        phase3_schools = scenario["schools_phase3"]
        phase3_revenue = phase3_schools * 1_000_000  # 1M DA par école (volume)
        phase3_cost = 0  # Économies d'échelle

        # Totaux
        total_investment = phase1_cost + phase2_cost + phase3_cost
        total_revenue = phase1_revenue + phase2_revenue + phase3_revenue
        net_profit = total_revenue - total_investment
        roi_multiplier = round(total_revenue / total_investment, 0) if total_investment > 0 else 0

        results[scenario_name] = {
            "phase1": {"revenue": phase1_revenue, "cost": phase1_cost},
            "phase2": {"revenue": phase2_revenue, "cost": phase2_cost, "schools": phase2_schools},
            "phase3": {"revenue": phase3_revenue, "cost": phase3_cost, "schools": phase3_schools},
            "total_investment": total_investment,
            "total_investment_millions": round(total_investment / 1_000_000, 2),
            "total_revenue": total_revenue,
            "total_revenue_millions": round(total_revenue / 1_000_000, 0),
            "net_profit": net_profit,
            "net_profit_millions": round(net_profit / 1_000_000, 0),
            "roi_multiplier": int(roi_multiplier),
        }

    return results


def get_active_config() -> Dict[str, Any]:
    """
    Retourne la configuration active (première version enabled)
    avec tous les calculs pré-remplis
    """
    # Trouver la version active
    active_version = None
    for name, config in VERSIONS.items():
        if config["enabled"]:
            active_version = config.copy()
            break

    if active_version is None:
        # Fallback sur generic
        active_version = VERSIONS["generic"].copy()

    # Ajouter les calculs
    students = active_version["students"]

    active_version["pricing"] = calculate_pricing(students)
    active_version["investment"] = calculate_iafactory_investment(students)
    active_version["roi"] = calculate_roi(students)

    # Calculer les métriques clés
    roi_pessimistic = active_version["roi"]["pessimistic"]["roi_multiplier"]
    roi_optimistic = active_version["roi"]["optimistic"]["roi_multiplier"]
    revenue_pessimistic = active_version["roi"]["pessimistic"]["total_revenue_millions"]
    revenue_optimistic = active_version["roi"]["optimistic"]["total_revenue_millions"]

    active_version["metrics"] = {
        "roi_range": f"×{roi_pessimistic}-×{roi_optimistic}",
        "revenue_range": f"{revenue_pessimistic}-{revenue_optimistic}M DA",
        "investment_total": f"{active_version['investment']['total_millions']}M DA",
        "cost_for_school": "0 DA" if active_version.get("partner_type") == "strategic" else f"{active_version['pricing']['annual_total_millions']}M DA/an",
    }

    return active_version


def get_config_by_name(name: str) -> Dict[str, Any]:
    """
    Retourne une configuration spécifique par nom
    """
    if name not in VERSIONS:
        raise ValueError(f"Configuration '{name}' not found. Available: {list(VERSIONS.keys())}")

    config = VERSIONS[name].copy()
    students = config["students"]

    config["pricing"] = calculate_pricing(students)
    config["investment"] = calculate_iafactory_investment(students)
    config["roi"] = calculate_roi(students)

    roi_pessimistic = config["roi"]["pessimistic"]["roi_multiplier"]
    roi_optimistic = config["roi"]["optimistic"]["roi_multiplier"]
    revenue_pessimistic = config["roi"]["pessimistic"]["total_revenue_millions"]
    revenue_optimistic = config["roi"]["optimistic"]["total_revenue_millions"]

    config["metrics"] = {
        "roi_range": f"×{roi_pessimistic}-×{roi_optimistic}",
        "revenue_range": f"{revenue_pessimistic}-{revenue_optimistic}M DA",
        "investment_total": f"{config['investment']['total_millions']}M DA",
        "cost_for_school": "0 DA" if config.get("partner_type") == "strategic" else f"{config['pricing']['annual_total_millions']}M DA/an",
    }

    return config


def enable_version(name: str) -> None:
    """
    Active une version et désactive les autres
    """
    if name not in VERSIONS:
        raise ValueError(f"Version '{name}' not found")

    for version_name in VERSIONS:
        VERSIONS[version_name]["enabled"] = (version_name == name)


def list_versions() -> Dict[str, bool]:
    """
    Liste toutes les versions avec leur statut
    """
    return {name: config["enabled"] for name, config in VERSIONS.items()}


# ============================================
# CLI HELPERS
# ============================================

if __name__ == "__main__":
    import json

    print("=" * 60)
    print("IAFactory Academy - Configuration System")
    print("=" * 60)

    print("\n📋 Versions disponibles:")
    for name, enabled in list_versions().items():
        status = "✅ ON" if enabled else "❌ OFF"
        print(f"  - {name}: {status}")

    print("\n📊 Configuration active:")
    config = get_active_config()
    print(f"  Nom: {config['display_name']}")
    print(f"  Élèves: {config['students']}")
    print(f"  Investissement: {config['metrics']['investment_total']}")
    print(f"  ROI: {config['metrics']['roi_range']}")
    print(f"  Revenus potentiels: {config['metrics']['revenue_range']}")

    print("\n💰 Détail ROI (3 scénarios):")
    for scenario, data in config["roi"].items():
        print(f"  {scenario}: {data['total_revenue_millions']}M DA (×{data['roi_multiplier']})")
