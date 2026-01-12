"""
IA FACTORY - Génère tous les documents d'un coup
"""

import sys
from pathlib import Path

BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

print("🏭 IA FACTORY - GÉNÉRATION DOCUMENTS")
print("📧 CH: contact@iafactory.ch")
print("📧 DZ: contact@iafactoryalgeria.com")
print("=" * 50)

# Create folders
for d in ["outputs/propositions", "outputs/presentations", "outputs/dashboards"]:
    (BASE / d).mkdir(parents=True, exist_ok=True)

# Generate proposals
print("\n📄 Propositions commerciales...")
from templates.documents.proposition_commerciale import PropositionGenerator
gen = PropositionGenerator()
print(f"  ✅ {gen.generate({'company': 'Swiss Demo Corp'}, ['RAG System', 'Training'], 'CH')}")
print(f"  ✅ {gen.generate({'company': 'Algérie Télécom'}, ['RAG System', 'Multi-Agent'], 'DZ')}")

# Generate presentations
print("\n📊 Présentations...")
from templates.presentations.teaching_assistant_deck import TeachingAssistantDeck
print(f"  ✅ {TeachingAssistantDeck().generate('CH')}")
print(f"  ✅ {TeachingAssistantDeck().generate('DZ')}")

# Generate dashboard
print("\n📈 Dashboard KPIs...")
from templates.dashboards.kpi_dashboard import KPIDashboard
print(f"  ✅ {KPIDashboard().generate()}")

print("\n" + "=" * 50)
print("✅ TOUS LES DOCUMENTS GÉNÉRÉS!")
print("📁 Voir dossier: outputs/")
