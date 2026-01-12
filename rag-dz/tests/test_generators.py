import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def test_proposition():
    from templates.documents.proposition_commerciale import PropositionGenerator
    gen = PropositionGenerator()
    
    f1 = gen.generate({"company": "Test CH"}, ["RAG System"], "CH")
    assert Path(f1).exists()
    print(f"✅ Proposition CH: {f1}")
    
    f2 = gen.generate({"company": "Test DZ"}, ["RAG System"], "DZ")
    assert Path(f2).exists()
    print(f"✅ Proposition DZ: {f2}")

def test_deck():
    from templates.presentations.teaching_assistant_deck import TeachingAssistantDeck
    
    f1 = TeachingAssistantDeck().generate("CH")
    assert Path(f1).exists()
    print(f"✅ Deck CH: {f1}")
    
    f2 = TeachingAssistantDeck().generate("DZ")
    assert Path(f2).exists()
    print(f"✅ Deck DZ: {f2}")

def test_dashboard():
    from templates.dashboards.kpi_dashboard import KPIDashboard
    
    f = KPIDashboard().generate()
    assert Path(f).exists()
    print(f"✅ Dashboard: {f}")

if __name__ == "__main__":
    print("\n🧪 Tests Générateurs\n")
    test_proposition()
    test_deck()
    test_dashboard()
    print("\n✅ TOUS LES TESTS PASSÉS!\n")
