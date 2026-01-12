#!/usr/bin/env python3
"""
Script de configuration et test de TOUS les providers LLM
Pour IA Factory Algeria
"""

import os
import asyncio
import httpx
from typing import Dict, List
from datetime import datetime

# ============================================
# CONFIGURATION PROVIDERS
# ============================================

PROVIDERS_CONFIG = {
    "1_groq": {
        "name": "🇺🇸 Groq (Meta Llama)",
        "base_url": "https://api.groq.com/openai/v1",
        "env_var": "GROQ_API_KEY",
        "models": [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768"
        ],
        "test_model": "llama-3.3-70b-versatile",
        "cost": "GRATUIT",
        "priority": 1
    },

    "2_publicai_apertus": {
        "name": "🇨🇭 Swiss AI Apertus (PublicAI)",
        "base_url": "https://api.publicai.co/v1",
        "env_var": "PUBLICAI_API_KEY",
        "models": [
            "swiss-ai/apertus-8b-instruct",
            "swiss-ai/apertus-70b-instruct"
        ],
        "test_model": "swiss-ai/apertus-8b-instruct",
        "cost": "GRATUIT",
        "priority": 2,
        "headers_extra": {
            "User-Agent": "IAFactoryAlgeria/1.0"
        }
    },

    "3_openrouter_mimo": {
        "name": "🇨🇳 Xiaomi MiMo (via OpenRouter)",
        "base_url": "https://openrouter.ai/api/v1",
        "env_var": "OPENROUTER_API_KEY",
        "models": [
            "xiaomi/mimo-v2-flash:free",
            "xiaomi/mimo-v2-flash"
        ],
        "test_model": "xiaomi/mimo-v2-flash:free",
        "cost": "GRATUIT (limité temps)",
        "priority": 3,
        "headers_extra": {
            "HTTP-Referer": "https://iafactoryalgeria.com",
            "X-Title": "IA Factory Algeria"
        }
    },

    "4_openrouter_claude": {
        "name": "🇺🇸 Claude Sonnet 4 (via OpenRouter)",
        "base_url": "https://openrouter.ai/api/v1",
        "env_var": "OPENROUTER_API_KEY",
        "models": [
            "anthropic/claude-sonnet-4-20250514",
            "anthropic/claude-opus-4-20250514",
            "anthropic/claude-haiku-4-20250514"
        ],
        "test_model": "anthropic/claude-sonnet-4-20250514",
        "cost": "$3.00 input / $15.00 output (par 1M tokens)",
        "priority": 4
    },

    "5_openrouter_gpt": {
        "name": "🇺🇸 GPT-4o (via OpenRouter)",
        "base_url": "https://openrouter.ai/api/v1",
        "env_var": "OPENROUTER_API_KEY",
        "models": [
            "openai/gpt-4o",
            "openai/gpt-4o-mini"
        ],
        "test_model": "openai/gpt-4o",
        "cost": "$2.50 input / $10.00 output (par 1M tokens)",
        "priority": 5
    },

    "6_openrouter_grok": {
        "name": "🇺🇸 Grok 2 (via OpenRouter)",
        "base_url": "https://openrouter.ai/api/v1",
        "env_var": "OPENROUTER_API_KEY",
        "models": [
            "x-ai/grok-2-1212",
            "x-ai/grok-2"
        ],
        "test_model": "x-ai/grok-2-1212",
        "cost": "$2.00 input / $10.00 output (par 1M tokens)",
        "priority": 6
    }
}

# ============================================
# FONCTIONS TEST
# ============================================

async def test_provider(
    provider_key: str,
    config: Dict,
    verbose: bool = True
) -> Dict:
    """
    Teste un provider spécifique
    """

    result = {
        "provider": provider_key,
        "name": config["name"],
        "status": "unknown",
        "error": None,
        "response_time": None,
        "response_preview": None
    }

    # Vérifier clé API
    api_key = os.getenv(config["env_var"])

    if not api_key:
        result["status"] = "missing_key"
        result["error"] = f"Clé API manquante: {config['env_var']}"
        if verbose:
            print(f"❌ {config['name']}: Clé manquante")
        return result

    if verbose:
        print(f"🔄 Test {config['name']}...")

    # Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Ajouter headers extra si définis
    if "headers_extra" in config:
        headers.update(config["headers_extra"])

    # Payload test
    payload = {
        "model": config["test_model"],
        "messages": [
            {
                "role": "user",
                "content": "Dis juste 'OK' pour confirmer que tu fonctionnes."
            }
        ],
        "max_tokens": 10,
        "temperature": 0.3
    }

    # Test requête
    start_time = datetime.now()

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{config['base_url']}/chat/completions",
                headers=headers,
                json=payload
            )

            elapsed = (datetime.now() - start_time).total_seconds()
            result["response_time"] = elapsed

            if response.status_code == 200:
                data = response.json()

                # Extraire réponse
                if "choices" in data and len(data["choices"]) > 0:
                    content = data["choices"][0]["message"]["content"]
                    result["response_preview"] = content[:50]
                    result["status"] = "success"

                    if verbose:
                        print(f"✅ {config['name']}: OK ({elapsed:.2f}s)")
                        print(f"   Réponse: {content}")
                else:
                    result["status"] = "error"
                    result["error"] = "Format réponse invalide"
                    if verbose:
                        print(f"⚠️  {config['name']}: Format invalide")

            elif response.status_code == 401:
                result["status"] = "invalid_key"
                result["error"] = "Clé API invalide"
                if verbose:
                    print(f"❌ {config['name']}: Clé invalide")

            elif response.status_code == 429:
                result["status"] = "rate_limited"
                result["error"] = "Rate limit dépassé"
                if verbose:
                    print(f"⚠️  {config['name']}: Rate limit")

            else:
                result["status"] = "error"
                result["error"] = f"HTTP {response.status_code}: {response.text[:100]}"
                if verbose:
                    print(f"❌ {config['name']}: Erreur {response.status_code}")

    except httpx.TimeoutException:
        result["status"] = "timeout"
        result["error"] = "Timeout après 30s"
        if verbose:
            print(f"⏱️  {config['name']}: Timeout")

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        if verbose:
            print(f"❌ {config['name']}: {str(e)}")

    return result


async def test_all_providers(verbose: bool = True) -> List[Dict]:
    """
    Teste tous les providers en parallèle
    """

    if verbose:
        print("\n" + "="*60)
        print("🚀 TEST DE TOUS LES PROVIDERS LLM")
        print("="*60 + "\n")

    # Tester tous en parallèle
    tasks = [
        test_provider(key, config, verbose)
        for key, config in PROVIDERS_CONFIG.items()
    ]

    results = await asyncio.gather(*tasks)

    return results


def print_summary(results: List[Dict]):
    """
    Affiche résumé des tests
    """

    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60 + "\n")

    success_count = sum(1 for r in results if r["status"] == "success")
    total_count = len(results)

    print(f"Providers testés: {total_count}")
    print(f"Succès: {success_count}/{total_count}")
    print(f"Taux de réussite: {success_count/total_count*100:.0f}%\n")

    # Détails par status
    by_status = {}
    for r in results:
        status = r["status"]
        if status not in by_status:
            by_status[status] = []
        by_status[status].append(r)

    # Succès
    if "success" in by_status:
        print("✅ OPÉRATIONNELS:")
        for r in by_status["success"]:
            print(f"   • {r['name']} ({r['response_time']:.2f}s)")
        print()

    # Clés manquantes
    if "missing_key" in by_status:
        print("🔑 CLÉS MANQUANTES:")
        for r in by_status["missing_key"]:
            config = PROVIDERS_CONFIG[r["provider"]]
            print(f"   • {r['name']}")
            print(f"     Variable: {config['env_var']}")
            print(f"     Action: Créer compte et obtenir clé API")
        print()

    # Clés invalides
    if "invalid_key" in by_status:
        print("❌ CLÉS INVALIDES:")
        for r in by_status["invalid_key"]:
            config = PROVIDERS_CONFIG[r["provider"]]
            print(f"   • {r['name']}")
            print(f"     Variable: {config['env_var']}")
            print(f"     Action: Régénérer clé API")
        print()

    # Erreurs
    if "error" in by_status:
        print("⚠️  ERREURS:")
        for r in by_status["error"]:
            print(f"   • {r['name']}")
            print(f"     Erreur: {r['error']}")
        print()

    # Rate limits
    if "rate_limited" in by_status:
        print("⏸️  RATE LIMITED:")
        for r in by_status["rate_limited"]:
            print(f"   • {r['name']}")
            print(f"     Action: Attendre ou augmenter quota")
        print()


def generate_env_template():
    """
    Génère template .env avec toutes les clés
    """

    print("\n" + "="*60)
    print("📝 TEMPLATE .env.local")
    print("="*60 + "\n")

    print("# ============================================")
    print("# LLM PROVIDERS - IA Factory Algeria")
    print("# ============================================\n")

    providers_by_key = {}

    for key, config in PROVIDERS_CONFIG.items():
        env_var = config["env_var"]
        if env_var not in providers_by_key:
            providers_by_key[env_var] = []
        providers_by_key[env_var].append(config["name"])

    for env_var, names in providers_by_key.items():
        print(f"# {', '.join(names)}")
        current_value = os.getenv(env_var, "")
        if current_value:
            print(f"{env_var}={current_value[:10]}...")
        else:
            print(f"{env_var}=your_api_key_here")
        print()

    print("\n" + "="*60)
    print("📚 OBTENIR LES CLÉS API")
    print("="*60 + "\n")

    for env_var, names in providers_by_key.items():
        if env_var == "GROQ_API_KEY":
            print(f"{env_var}:")
            print(f"  → https://console.groq.com/keys")
            print(f"  → Gratuit, créer compte et générer clé\n")

        elif env_var == "PUBLICAI_API_KEY":
            print(f"{env_var}:")
            print(f"  → https://platform.publicai.co")
            print(f"  → Gratuit, sign up → API Keys\n")

        elif env_var == "OPENROUTER_API_KEY":
            print(f"{env_var}:")
            print(f"  → https://openrouter.ai/keys")
            print(f"  → Créer compte, add $20-50 crédit")
            print(f"  → Donne accès à: MiMo, Claude, GPT, Grok\n")


async def check_specific_model(
    provider: str,
    model: str,
    prompt: str = "Test"
) -> Dict:
    """
    Teste un modèle spécifique (pour debugging)
    """

    # Trouver config provider
    config = None
    for k, v in PROVIDERS_CONFIG.items():
        if provider in k:
            config = v
            break

    if not config:
        return {"error": f"Provider '{provider}' non trouvé"}

    # Override test model
    config["test_model"] = model

    return await test_provider(provider, config, verbose=True)


# ============================================
# MAIN
# ============================================

async def main():
    """
    Point d'entrée principal
    """

    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "test":
            # Test tous les providers
            results = await test_all_providers(verbose=True)
            print_summary(results)

            # Exit code
            success_count = sum(1 for r in results if r["status"] == "success")
            sys.exit(0 if success_count == len(results) else 1)

        elif command == "template":
            # Générer template .env
            generate_env_template()
            sys.exit(0)

        elif command == "check" and len(sys.argv) > 3:
            # Check modèle spécifique
            provider = sys.argv[2]
            model = sys.argv[3]
            result = await check_specific_model(provider, model)
            print(result)
            sys.exit(0)

        else:
            print("Usage:")
            print("  python setup_all_providers.py test       # Tester tous les providers")
            print("  python setup_all_providers.py template   # Générer template .env")
            print("  python setup_all_providers.py check <provider> <model>  # Tester modèle spécifique")
            sys.exit(1)

    else:
        # Par défaut: test tous
        results = await test_all_providers(verbose=True)
        print_summary(results)


if __name__ == "__main__":
    asyncio.run(main())
