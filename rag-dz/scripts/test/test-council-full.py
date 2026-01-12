#!/usr/bin/env python3
"""
Test complet du LLM Council avec tous les providers disponibles
"""
import requests
import json
import time

API_BASE = "http://localhost:8180"

def test_council_query():
    """Test une requête complète au Council"""
    print("=" * 60)
    print("TEST: Council Query avec 4 providers")
    print("=" * 60)

    query = "Quelle est la capitale de l'Algérie? Réponds en une phrase courte."

    print(f"\nQuestion: {query}")
    print(f"\nConsultation du Council en cours...")

    start = time.time()

    try:
        response = requests.post(
            f"{API_BASE}/api/council/query",
            json={
                "query": query,
                "enable_review": False  # Pas de revue pour aller plus vite
            },
            timeout=180
        )

        elapsed = time.time() - start

        if response.status_code == 200:
            data = response.json()

            print(f"\nReponse recue en {elapsed:.1f}s")
            print(f"\n{'='*60}")
            print("REPONSE FINALE DU COUNCIL")
            print('='*60)
            print(data['final_response'])

            print(f"\n{'='*60}")
            print("METADONNEES")
            print('='*60)
            print(f"Temps d'execution: {data['metadata']['execution_time']:.2f}s")
            print(f"Membres: {', '.join(data['metadata']['council_members'])}")
            print(f"President: {data['metadata']['chairman']}")

            print(f"\n{'='*60}")
            print("OPINIONS INDIVIDUELLES")
            print('='*60)
            for model, opinion in data['opinions'].items():
                print(f"\n{model.upper()}:")
                print(f"   {opinion[:100]}...")

            return True
        else:
            print(f"\nErreur HTTP {response.status_code}")
            print(response.text)
            return False

    except requests.exceptions.Timeout:
        print(f"\nTimeout apres {elapsed:.1f}s")
        print("   (Ollama peut etre lent, c'est normal)")
        return False
    except Exception as e:
        print(f"\nErreur: {str(e)}")
        return False

def test_providers():
    """Test la disponibilité des providers"""
    print("\n" + "=" * 60)
    print("TEST: Disponibilite des providers")
    print("=" * 60)

    try:
        response = requests.get(f"{API_BASE}/api/council/providers")
        providers = response.json()

        available = [p for p in providers if p['available']]
        unavailable = [p for p in providers if not p['available']]

        print(f"\nProviders disponibles ({len(available)}/{len(providers)}):")
        for p in available:
            print(f"   - {p['display_name']} ({p['name']}) - {p['model']}")

        if unavailable:
            print(f"\nProviders non configures ({len(unavailable)}):")
            for p in unavailable:
                print(f"   - {p['display_name']} ({p['name']}) - Cle API manquante")

        return len(available) > 0

    except Exception as e:
        print(f"\nErreur: {str(e)}")
        return False

if __name__ == "__main__":
    print("\nTEST COMPLET DU LLM COUNCIL")
    print("=" * 60)

    # Test 1: Providers
    if not test_providers():
        print("\nImpossible de tester le Council sans providers")
        exit(1)

    # Test 2: Query complète
    time.sleep(1)
    success = test_council_query()

    print("\n" + "=" * 60)
    if success:
        print("TOUS LES TESTS REUSSIS")
    else:
        print("CERTAINS TESTS ONT ECHOUE")
    print("=" * 60)
