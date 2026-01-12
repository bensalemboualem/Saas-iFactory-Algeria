#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AUDIT DES CHIFFRES - IAFactory Academy
Verifie la coherence de tous les calculs financiers
"""

import sys
import io
from pathlib import Path

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Ajouter le repertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    calculate_pricing,
    calculate_iafactory_investment,
    calculate_roi,
    PRICING_TIERS,
    IAFACTORY_COSTS,
    ROI_SCENARIOS,
)

def print_header(title, char="=", length=70):
    print(char * length)
    print(title)
    print(char * length)

def format_da(amount):
    """Formate un montant en DA avec separateurs"""
    if amount >= 1_000_000_000:
        return f"{amount/1_000_000_000:.1f} Mrd DA"
    elif amount >= 1_000_000:
        return f"{amount/1_000_000:.1f}M DA"
    elif amount >= 1_000:
        return f"{amount/1_000:.0f}K DA"
    else:
        return f"{amount:,.0f} DA"

def audit_pricing_tiers():
    """Audite les paliers de prix"""
    print_header("1. AUDIT DES PALIERS DE PRIX")

    print("\nPaliers configures:")
    print("-" * 50)
    for tier in PRICING_TIERS:
        max_val = "infini" if tier['max'] == float('inf') else f"{tier['max']:,}"
        print(f"  {tier['min']:,} - {max_val} eleves: {tier['price_per_student']:,} DA/mois")

    print("\nVerification prix/eleve/an (10 mois scolaires):")
    print("-" * 50)
    for tier in PRICING_TIERS:
        annual = tier['price_per_student'] * 10
        print(f"  {tier['price_per_student']:,} DA/mois x 10 = {annual:,} DA/an/eleve")

def audit_iafactory_costs():
    """Audite les couts IAFactory"""
    print_header("2. AUDIT DES COUTS IAFACTORY")

    print("\nCouts forfaitaires configures:")
    print("-" * 50)
    total = 0
    for key, value in IAFACTORY_COSTS.items():
        print(f"  {key}: {format_da(value)}")
        total += value
    print("-" * 50)
    print(f"  TOTAL: {format_da(total)}")

    print("\nAnalyse de coherence:")
    print("-" * 50)

    # Formation: devrait etre raisonnable pour 20 enseignants
    formation = IAFACTORY_COSTS.get('formation_forfait', 0)
    cost_per_teacher = formation / 20 if formation > 0 else 0
    print(f"  Formation/enseignant (20 profs): {format_da(cost_per_teacher)}")

    # Support: cout mensuel sur 6 mois
    support = IAFACTORY_COSTS.get('support_forfait', 0)
    monthly_support = support / 6 if support > 0 else 0
    print(f"  Support mensuel (6 mois): {format_da(monthly_support)}")

    # Contenu: cout par lecon (38 lecons)
    content = IAFACTORY_COSTS.get('content_creation', 0)
    cost_per_lesson = content / 38 if content > 0 else 0
    print(f"  Cout/lecon (38 lecons): {format_da(cost_per_lesson)}")

def audit_school_sizes():
    """Audite differentes tailles d'ecoles"""
    print_header("3. AUDIT PAR TAILLE D'ECOLE")

    test_sizes = [
        ("Petite ecole", 200),
        ("Nouvelle Horizon", 500),
        ("BBC School", 1600),
        ("Grande ecole", 3000),
        ("Reseau regional (10 ecoles)", 10000),
    ]

    for name, students in test_sizes:
        print(f"\n{'='*70}")
        print(f"{name.upper()} - {students:,} eleves")
        print(f"{'='*70}")

        pricing = calculate_pricing(students)
        investment = calculate_iafactory_investment(students)

        print(f"\nPRICING:")
        print(f"  Tier: {pricing['tier_label']}")
        print(f"  Prix/eleve/mois: {pricing['price_per_student_month']:,} DA")
        print(f"  Prix/eleve/an (10 mois): {pricing['price_per_student_month'] * 10:,} DA")
        print(f"  Revenus mensuels: {format_da(pricing['monthly_total'])}")
        print(f"  Revenus annuels: {format_da(pricing['annual_total'])}")

        print(f"\nINVESTISSEMENT IAFACTORY:")
        print(f"  Total: {format_da(investment['total'])}")
        per_student = investment['total'] / students
        print(f"  Par eleve: {format_da(per_student)}")

        # ROI simple (revenus / investissement)
        roi_annuel = pricing['annual_total'] / investment['total'] if investment['total'] > 0 else 0
        print(f"\nRATIOS:")
        print(f"  Revenus/Invest (1 an): {roi_annuel:.1f}x")
        print(f"  Revenus/Invest (3 ans): {roi_annuel * 3:.1f}x")
        print(f"  Breakeven: {1/roi_annuel:.1f} ans" if roi_annuel > 0 else "  Breakeven: N/A")

def audit_roi_scenarios():
    """Audite les scenarios ROI"""
    print_header("4. AUDIT DES SCENARIOS ROI")

    print("\nScenarios configures:")
    print("-" * 50)
    for name, scenario in ROI_SCENARIOS.items():
        print(f"  {name.upper()}:")
        print(f"    Phase 2: {scenario['schools_phase2']} ecoles")
        print(f"    Phase 3: {scenario['schools_phase3']} ecoles")

    print("\nProjections detaillees (BBC: 1600 eleves):")
    print("-" * 50)

    roi = calculate_roi(1600)
    investment = calculate_iafactory_investment(1600)

    for scenario_name, data in roi.items():
        emoji = "pessimiste" if scenario_name == "pessimistic" else "realiste" if scenario_name == "realistic" else "optimiste"
        print(f"\n  {scenario_name.upper()} ({emoji}):")
        print(f"    Phase 1 (pilote): Invest {format_da(data['phase1']['cost'])}, Rev {format_da(data['phase1']['revenue'])}")
        print(f"    Phase 2 ({data['phase2']['schools']} ecoles): Rev {format_da(data['phase2']['revenue'])}")
        print(f"    Phase 3 ({data['phase3']['schools']} ecoles): Rev {format_da(data['phase3']['revenue'])}")
        print(f"    ---")
        print(f"    Investissement total: {format_da(data['total_investment'])}")
        print(f"    Revenus totaux: {format_da(data['total_revenue'])}")
        print(f"    Profit net: {format_da(data['net_profit'])}")
        print(f"    ROI: x{data['roi_multiplier']}")

def audit_coherence_check():
    """Verification finale de coherence"""
    print_header("5. VERIFICATION DE COHERENCE")

    checks = []

    # Check 1: Prix par eleve raisonnable
    pricing = calculate_pricing(1600)
    monthly_fee = pricing['price_per_student_month']
    if 500 <= monthly_fee <= 1000:
        checks.append(("Prix/eleve/mois (500-1000 DA)", True, f"{monthly_fee} DA"))
    else:
        checks.append(("Prix/eleve/mois (500-1000 DA)", False, f"{monthly_fee} DA"))

    # Check 2: Investissement total raisonnable (< 10M DA)
    investment = calculate_iafactory_investment(1600)
    if investment['total'] <= 10_000_000:
        checks.append(("Investissement < 10M DA", True, format_da(investment['total'])))
    else:
        checks.append(("Investissement < 10M DA", False, format_da(investment['total'])))

    # Check 3: ROI positif meme scenario pessimiste
    roi = calculate_roi(1600)
    if roi['pessimistic']['roi_multiplier'] > 1:
        checks.append(("ROI pessimiste > 1x", True, f"x{roi['pessimistic']['roi_multiplier']}"))
    else:
        checks.append(("ROI pessimiste > 1x", False, f"x{roi['pessimistic']['roi_multiplier']}"))

    # Check 4: Breakeven < 1 an
    annual_revenue = pricing['annual_total']
    breakeven_years = investment['total'] / annual_revenue if annual_revenue > 0 else 999
    if breakeven_years < 1:
        checks.append(("Breakeven < 1 an", True, f"{breakeven_years:.2f} ans"))
    else:
        checks.append(("Breakeven < 1 an", False, f"{breakeven_years:.2f} ans"))

    # Check 5: Revenus Phase 3 > Phase 2
    if roi['realistic']['phase3']['revenue'] > roi['realistic']['phase2']['revenue']:
        checks.append(("Phase 3 > Phase 2 revenus", True, "OK"))
    else:
        checks.append(("Phase 3 > Phase 2 revenus", False, "NOK"))

    print("\nResultats des verifications:")
    print("-" * 60)
    all_passed = True
    for check_name, passed, value in checks:
        status = "[OK]" if passed else "[ERREUR]"
        print(f"  {status} {check_name}: {value}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("RESULTAT: TOUS LES CHECKS PASSES")
    else:
        print("RESULTAT: CERTAINS CHECKS ONT ECHOUE")
    print("=" * 60)

def audit_comparaison_bbc():
    """Compare les chiffres actuels avec la presentation originale"""
    print_header("6. COMPARAISON AVEC CHIFFRES ORIGINAUX")

    print("\nChiffres attendus (presentation ministre):")
    print("-" * 50)
    original = {
        "students": 1600,
        "investment_total": 4_800_000,  # 4.8M DA
        "annual_revenue": 9_600_000,    # 9.6M DA
        "roi_pessimistic": 52,          # x52
        "roi_optimistic": 110,          # x110
        "revenue_pessimistic": 278_000_000,  # 278M DA
        "revenue_optimistic": 582_000_000,   # 582M DA
    }

    print(f"  Eleves: {original['students']:,}")
    print(f"  Investissement: {format_da(original['investment_total'])}")
    print(f"  Revenus annuels ecole pilote: {format_da(original['annual_revenue'])}")
    print(f"  ROI pessimiste: x{original['roi_pessimistic']}")
    print(f"  ROI optimiste: x{original['roi_optimistic']}")

    print("\nChiffres calcules actuels:")
    print("-" * 50)
    pricing = calculate_pricing(1600)
    investment = calculate_iafactory_investment(1600)
    roi = calculate_roi(1600)

    current = {
        "students": 1600,
        "investment_total": investment['total'],
        "annual_revenue": pricing['annual_total'],
        "roi_pessimistic": roi['pessimistic']['roi_multiplier'],
        "roi_optimistic": roi['optimistic']['roi_multiplier'],
        "revenue_pessimistic": roi['pessimistic']['total_revenue'],
        "revenue_optimistic": roi['optimistic']['total_revenue'],
    }

    print(f"  Eleves: {current['students']:,}")
    print(f"  Investissement: {format_da(current['investment_total'])}")
    print(f"  Revenus annuels ecole pilote: {format_da(current['annual_revenue'])}")
    print(f"  ROI pessimiste: x{current['roi_pessimistic']}")
    print(f"  ROI optimiste: x{current['roi_optimistic']}")

    print("\nEcarts:")
    print("-" * 50)
    for key in ['investment_total', 'annual_revenue', 'roi_pessimistic', 'roi_optimistic']:
        diff = current[key] - original[key]
        pct = (diff / original[key] * 100) if original[key] != 0 else 0
        status = "OK" if abs(pct) < 5 else "ECART"
        print(f"  {key}: {diff:+,.0f} ({pct:+.1f}%) [{status}]")


if __name__ == "__main__":
    print("\n")
    audit_pricing_tiers()
    print("\n")
    audit_iafactory_costs()
    print("\n")
    audit_school_sizes()
    print("\n")
    audit_roi_scenarios()
    print("\n")
    audit_coherence_check()
    print("\n")
    audit_comparaison_bbc()
    print("\n")
