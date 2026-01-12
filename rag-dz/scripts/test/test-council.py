#!/usr/bin/env python3
"""
Script de test pour LLM Council
Teste la connectivité et le bon fonctionnement du système
"""
import asyncio
import json
import time
from datetime import datetime
import httpx


API_BASE = "http://localhost:8180"
COLORS = {
    "green": "\033[92m",
    "red": "\033[91m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "reset": "\033[0m"
}


def print_colored(text: str, color: str):
    """Print avec couleur"""
    print(f"{COLORS.get(color, '')}{text}{COLORS['reset']}")


async def test_council_health():
    """Test 1: Health check du service Council"""
    print_colored("\n🏥 Test 1: Health Check Council", "blue")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE}/api/council/health")

            if response.status_code == 200:
                data = response.json()
                print_colored(f"✅ Status: {data['status']}", "green")
                print_colored(f"   Providers disponibles: {data['available_providers']}/{len(data['providers'])}", "green")
                print_colored(f"   Providers: {', '.join(data['providers'])}", "green")
                print_colored(f"   Chairman: {data['chairman_available']}", "green")
                return True
            else:
                print_colored(f"❌ Erreur: {response.status_code}", "red")
                return False

    except Exception as e:
        print_colored(f"❌ Erreur connexion: {e}", "red")
        return False


async def test_providers_list():
    """Test 2: Liste des providers"""
    print_colored("\n📋 Test 2: Liste des Providers", "blue")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE}/api/council/providers")

            if response.status_code == 200:
                providers = response.json()

                for provider in providers:
                    status = "✅" if provider["available"] else "❌"
                    color = "green" if provider["available"] else "red"
                    print_colored(
                        f"{status} {provider['display_name']} ({provider['model']}) - "
                        f"Role: {provider['role']} - Cost: ${provider['cost_per_1k']}/1K",
                        color
                    )

                return True
            else:
                print_colored(f"❌ Erreur: {response.status_code}", "red")
                return False

    except Exception as e:
        print_colored(f"❌ Erreur: {e}", "red")
        return False


async def test_providers_connectivity():
    """Test 3: Test de connectivité de chaque provider"""
    print_colored("\n🔌 Test 3: Connectivité des Providers", "blue")

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{API_BASE}/api/council/test")

            if response.status_code == 200:
                data = response.json()

                for provider, result in data["results"].items():
                    if result["status"] == "ok":
                        print_colored(f"✅ {provider}: OK", "green")
                        print_colored(f"   Réponse: {result.get('response_preview', 'N/A')[:50]}...", "green")
                    else:
                        print_colored(f"❌ {provider}: {result['status']}", "red")
                        if "error" in result:
                            print_colored(f"   Erreur: {result['error']}", "red")

                return True
            else:
                print_colored(f"❌ Erreur: {response.status_code}", "red")
                return False

    except Exception as e:
        print_colored(f"❌ Erreur: {e}", "red")
        return False


async def test_council_query_simple():
    """Test 4: Requête simple au Council (sans review)"""
    print_colored("\n💬 Test 4: Requête Simple (sans review)", "blue")

    query = "Explique en une phrase ce qu'est le machine learning."
    print_colored(f"Question: {query}", "yellow")

    try:
        start_time = time.time()

        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(
                f"{API_BASE}/api/council/query",
                json={
                    "query": query,
                    "enable_review": False
                }
            )

            elapsed = time.time() - start_time

            if response.status_code == 200:
                data = response.json()

                print_colored(f"\n✅ Réponse reçue en {elapsed:.2f}s", "green")
                print_colored(f"\n📝 Réponse finale:", "blue")
                print(f"{data['final_response'][:200]}...")

                print_colored(f"\n👥 Opinions individuelles:", "blue")
                for model, opinion in data["opinions"].items():
                    print_colored(f"  {model}: {opinion[:100]}...", "green")

                print_colored(f"\n⏱️  Temps d'exécution: {data['metadata']['execution_time']:.2f}s", "green")
                print_colored(f"👤 Chairman: {data['metadata']['chairman']}", "green")
                print_colored(f"👥 Membres: {', '.join(data['metadata']['council_members'])}", "green")

                return True
            else:
                error = response.json()
                print_colored(f"❌ Erreur: {response.status_code}", "red")
                print_colored(f"   {error.get('detail', 'Unknown error')}", "red")
                return False

    except Exception as e:
        print_colored(f"❌ Erreur: {e}", "red")
        return False


async def test_council_query_with_review():
    """Test 5: Requête avec review croisée (optionnel - plus long)"""
    print_colored("\n🔍 Test 5: Requête avec Review Croisée (optionnel)", "blue")
    print_colored("⚠️  Ce test peut prendre 30-60 secondes", "yellow")

    # Demander confirmation
    response = input("Lancer ce test? (y/n): ")
    if response.lower() != 'y':
        print_colored("Test ignoré", "yellow")
        return None

    query = "Quelle est la meilleure approche pour tester une API REST?"
    print_colored(f"Question: {query}", "yellow")

    try:
        start_time = time.time()

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{API_BASE}/api/council/query",
                json={
                    "query": query,
                    "enable_review": True
                }
            )

            elapsed = time.time() - start_time

            if response.status_code == 200:
                data = response.json()

                print_colored(f"\n✅ Réponse reçue en {elapsed:.2f}s", "green")
                print_colored(f"\n📝 Réponse finale:", "blue")
                print(f"{data['final_response'][:300]}...")

                if data.get("rankings"):
                    print_colored(f"\n⭐ Rankings disponibles:", "blue")
                    for reviewer, ranking in data["rankings"].items():
                        print_colored(f"  {reviewer}: {ranking.get('parsed', False)}", "green")

                print_colored(f"\n⏱️  Temps d'exécution: {data['metadata']['execution_time']:.2f}s", "green")

                return True
            else:
                error = response.json()
                print_colored(f"❌ Erreur: {response.status_code}", "red")
                print_colored(f"   {error.get('detail', 'Unknown error')}", "red")
                return False

    except Exception as e:
        print_colored(f"❌ Erreur: {e}", "red")
        return False


async def test_council_config():
    """Test 6: Configuration du Council"""
    print_colored("\n⚙️  Test 6: Configuration Council", "blue")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE}/api/council/config")

            if response.status_code == 200:
                config = response.json()

                print_colored(f"✅ Configuration chargée:", "green")
                print(f"   Default council: {', '.join(config['default_council'])}")
                print(f"   Chairman: {config['chairman']}")
                print(f"   Review enabled: {config['enable_review']}")
                print(f"   Anonymize models: {config['anonymize_models']}")
                print(f"   Timeouts: Stage1={config['timeouts']['stage1']}s, "
                      f"Stage2={config['timeouts']['stage2']}s, "
                      f"Stage3={config['timeouts']['stage3']}s")

                return True
            else:
                print_colored(f"❌ Erreur: {response.status_code}", "red")
                return False

    except Exception as e:
        print_colored(f"❌ Erreur: {e}", "red")
        return False


async def main():
    """Execute tous les tests"""
    print_colored("\n" + "="*60, "blue")
    print_colored("🧪 LLM COUNCIL - SUITE DE TESTS", "blue")
    print_colored("="*60, "blue")
    print_colored(f"API: {API_BASE}", "yellow")
    print_colored(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "yellow")

    results = []

    # Test 1: Health
    results.append(("Health Check", await test_council_health()))

    # Test 2: Providers list
    results.append(("Providers List", await test_providers_list()))

    # Test 3: Connectivity
    results.append(("Providers Connectivity", await test_providers_connectivity()))

    # Test 4: Query simple
    results.append(("Simple Query", await test_council_query_simple()))

    # Test 5: Query avec review (optionnel)
    review_result = await test_council_query_with_review()
    if review_result is not None:
        results.append(("Query with Review", review_result))

    # Test 6: Config
    results.append(("Config", await test_council_config()))

    # Résumé
    print_colored("\n" + "="*60, "blue")
    print_colored("📊 RÉSUMÉ DES TESTS", "blue")
    print_colored("="*60, "blue")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        color = "green" if result else "red"
        print_colored(f"{status} - {name}", color)

    print_colored("\n" + "-"*60, "blue")
    percentage = (passed / total * 100) if total > 0 else 0
    print_colored(f"Résultat: {passed}/{total} tests réussis ({percentage:.1f}%)",
                  "green" if passed == total else "yellow")

    if passed == total:
        print_colored("\n🎉 Tous les tests sont passés avec succès!", "green")
    elif passed > 0:
        print_colored(f"\n⚠️  {total - passed} test(s) en échec", "yellow")
    else:
        print_colored("\n❌ Tous les tests ont échoué", "red")

    print_colored("="*60 + "\n", "blue")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_colored("\n\n⚠️  Tests interrompus par l'utilisateur", "yellow")
    except Exception as e:
        print_colored(f"\n❌ Erreur fatale: {e}", "red")
