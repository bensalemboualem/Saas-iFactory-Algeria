"""
Génère tous les documents pour CH et DZ
"""

import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
sys.path.insert(0, str(BASE))

from templates.documents.proposition_commerciale import PropositionGenerator
from templates.presentations.teaching_assistant_deck import TeachingAssistantDeck
from templates.dashboards.kpi_dashboard import KPIDashboard

print("🏭 IA FACTORY - Génération Documents")
print("=" * 50)

# Propositions
gen = PropositionGenerator()
clients = [
    ({"company": "École Nouvelle Horizon"}, ["RAG System", "Training"], "CH"),
    ({"company": "Startup Tech Genève"}, ["RAG System"], "CH"),
    ({"company": "Algérie Télécom"}, ["RAG System", "Multi-Agent"], "DZ"),
    ({"company": "Université Alger"}, ["Training"], "DZ"),
]

print("\n📄 Propositions:")
for client, services, market in clients:
    f = gen.generate(client, services, market)
    print(f"  ✅ {f}")

# Decks
print("\n📊 Présentations:")
for market in ["CH", "DZ"]:
    f = TeachingAssistantDeck().generate(market)
    print(f"  ✅ {f}")

# Dashboard
print("\n📈 Dashboard:")
f = KPIDashboard().generate()
print(f"  ✅ {f}")

print("\n" + "=" * 50)
print("✅ TERMINÉ - Voir outputs/")
