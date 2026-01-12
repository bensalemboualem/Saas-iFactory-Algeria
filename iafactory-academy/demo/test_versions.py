#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test des versions - IAFactory Academy
Verifie que toutes les configurations fonctionnent correctement
"""

import sys
import io
from pathlib import Path

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Ajouter le repertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    VERSIONS,
    get_active_config,
    get_config_by_name,
    calculate_pricing,
    calculate_iafactory_investment,
    calculate_roi,
    list_versions,
)

def print_separator(char="=", length=70):
    print(char * length)

def test_all_versions():
    """Test toutes les versions configurées"""
    print_separator()
    print("🧪 TEST DES VERSIONS - IAFactory Academy")
    print_separator()

    # Afficher le statut de toutes les versions
    print("\n📋 STATUT DES VERSIONS:")
    print("-" * 40)
    for name, enabled in list_versions().items():
        status = "✅ ON" if enabled else "❌ OFF"
        print(f"  {name}: {status}")

    # Tester chaque version
    for version_name, config in VERSIONS.items():
        print(f"\n{'='*70}")
        print(f"📦 VERSION: {version_name.upper()}")
        print(f"{'='*70}")

        # Info de base
        print(f"\n📌 INFORMATIONS:")
        print(f"  Enabled: {'✅ OUI' if config['enabled'] else '❌ NON'}")
        print(f"  Nom affiché: {config['display_name']}")
        print(f"  Nom arabe: {config['display_name_ar']}")
        print(f"  Élèves: {config['students']:,}")
        print(f"  Enseignants: {config['teachers']}")
        print(f"  Type partenaire: {config['partner_type']}")
        print(f"  Mode démo: {'✅' if config.get('demo_mode') else '❌'}")
        print(f"  Couleur: {config['primary_color']}")
        print(f"  Emoji: {config['logo_emoji']}")

        # Calculs
        students = config['students']
        pricing = calculate_pricing(students)
        investment = calculate_iafactory_investment(students)
        roi = calculate_roi(students)

        print(f"\n💰 PRICING ({students:,} élèves):")
        print(f"  Tier: {pricing['tier_label']}")
        print(f"  Prix/élève/mois: {pricing['price_per_student_month']:,} DA")
        print(f"  Total mensuel: {pricing['monthly_total']:,} DA")
        print(f"  Total annuel: {pricing['annual_total']:,} DA ({pricing['annual_total_millions']}M DA)")

        print(f"\n🏗️ INVESTISSEMENT IAFACTORY:")
        print(f"  Formation: {investment['formation']:,} DA")
        print(f"  Contenu: {investment['content']:,} DA")
        print(f"  Plateforme: {investment['platform']:,} DA")
        print(f"  Support: {investment['support']:,} DA")
        print(f"  TOTAL: {investment['total']:,} DA ({investment['total_millions']}M DA)")

        print(f"\n📈 ROI (3 SCÉNARIOS):")
        for scenario_name, data in roi.items():
            emoji = "🔴" if scenario_name == "pessimistic" else "🟡" if scenario_name == "realistic" else "🟢"
            print(f"  {emoji} {scenario_name.upper()}:")
            print(f"     Phase 2: {data['phase2']['schools']} écoles → {data['phase2']['revenue']/1_000_000:.0f}M DA")
            print(f"     Phase 3: {data['phase3']['schools']} écoles → {data['phase3']['revenue']/1_000_000:.0f}M DA")
            print(f"     Total revenus: {data['total_revenue_millions']}M DA")
            print(f"     Profit net: {data['net_profit_millions']}M DA")
            print(f"     ROI: ×{data['roi_multiplier']}")

    # Test de la version active
    print(f"\n{'='*70}")
    print("🎯 VERSION ACTIVE (get_active_config)")
    print(f"{'='*70}")

    active = get_active_config()
    print(f"\n  Nom: {active['display_name']}")
    print(f"  Élèves: {active['students']:,}")
    print(f"  Type: {active['partner_type']}")
    print(f"  Coût école: {active['metrics']['cost_for_school']}")
    print(f"  Investissement IAF: {active['metrics']['investment_total']}")
    print(f"  ROI: {active['metrics']['roi_range']}")
    print(f"  Revenus potentiels: {active['metrics']['revenue_range']}")

    # Test get_config_by_name
    print(f"\n{'='*70}")
    print("🔍 TEST get_config_by_name('bbc')")
    print(f"{'='*70}")

    bbc = get_config_by_name("bbc")
    print(f"\n  Nom: {bbc['display_name']}")
    print(f"  Coût pour BBC: {bbc['metrics']['cost_for_school']}")
    print(f"  Note spéciale: {bbc.get('special_note', 'N/A')}")

    # Résumé
    print(f"\n{'='*70}")
    print("✅ RÉSUMÉ DU TEST")
    print(f"{'='*70}")
    print(f"\n  Versions testées: {len(VERSIONS)}")
    print(f"  Version active: {active['display_name']}")
    print(f"  BBC enabled: {'✅' if VERSIONS['bbc']['enabled'] else '❌'}")
    print(f"  Generic enabled: {'✅' if VERSIONS['generic']['enabled'] else '❌'}")

    print(f"\n{'='*70}")
    print("🎉 TEST TERMINÉ AVEC SUCCÈS!")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    test_all_versions()
