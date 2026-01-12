#!/usr/bin/env python3
"""
Script de diagnostic rapide - IA Factory Algeria
Vérifie que tout est prêt pour les tests
"""
import os
import sys
from pathlib import Path

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def check_redis():
    """Vérifier Redis"""
    print(f"\n{BLUE}[1/5] Vérification Redis...{RESET}")
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        print(f"{GREEN}✅ Redis: Connecté et fonctionne{RESET}")
        return True
    except ImportError:
        print(f"{RED}❌ Redis: Module Python pas installé{RESET}")
        print(f"{YELLOW}   → Installer: pip install redis{RESET}")
        return False
    except Exception as e:
        print(f"{RED}❌ Redis: Pas accessible (pas démarré?){RESET}")
        print(f"{YELLOW}   → Démarrer: docker run -d -p 6379:6379 redis:7-alpine{RESET}")
        return False

def check_postgres():
    """Vérifier PostgreSQL"""
    print(f"\n{BLUE}[2/5] Vérification PostgreSQL...{RESET}")
    try:
        import asyncpg
        print(f"{GREEN}✅ PostgreSQL: Module asyncpg installé{RESET}")

        # Check .env.local for DATABASE_URL
        env_file = Path(".env.local")
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith("DATABASE_URL="):
                        print(f"{GREEN}✅ PostgreSQL: DATABASE_URL configurée{RESET}")
                        return True

        print(f"{YELLOW}⚠️  PostgreSQL: DATABASE_URL pas dans .env.local{RESET}")
        print(f"{YELLOW}   → Ajouter: DATABASE_URL=postgresql://postgres:postgres@localhost:5432/iafactory_dz{RESET}")
        return False

    except ImportError:
        print(f"{RED}❌ PostgreSQL: Module asyncpg pas installé{RESET}")
        print(f"{YELLOW}   → Installer: pip install asyncpg{RESET}")
        return False

def check_api_keys():
    """Vérifier clés API essentielles"""
    print(f"\n{BLUE}[3/5] Vérification clés API...{RESET}")

    env_file = Path(".env.local")
    if not env_file.exists():
        print(f"{RED}❌ Fichier .env.local n'existe pas{RESET}")
        print(f"{YELLOW}   → Créer: touch .env.local{RESET}")
        return False

    keys_found = {
        'GROQ_API_KEY': False,
        'DATABASE_URL': False,
        'REDIS_URL': False,
        'JWT_SECRET_KEY': False
    }

    with open(env_file) as f:
        content = f.read()
        for key in keys_found.keys():
            if f"{key}=" in content and not f"{key}=your_" in content:
                keys_found[key] = True

    # Vérifier clés essentielles
    all_ok = True

    if keys_found['GROQ_API_KEY']:
        print(f"{GREEN}✅ GROQ_API_KEY: Configurée{RESET}")
    else:
        print(f"{RED}❌ GROQ_API_KEY: Manquante ou invalide{RESET}")
        print(f"{YELLOW}   → Obtenir sur: https://console.groq.com/keys{RESET}")
        all_ok = False

    if keys_found['DATABASE_URL']:
        print(f"{GREEN}✅ DATABASE_URL: Configurée{RESET}")
    else:
        print(f"{YELLOW}⚠️  DATABASE_URL: Manquante{RESET}")
        all_ok = False

    if keys_found['REDIS_URL']:
        print(f"{GREEN}✅ REDIS_URL: Configurée{RESET}")
    else:
        print(f"{YELLOW}⚠️  REDIS_URL: Manquante (défaut: redis://localhost:6379/0){RESET}")

    if keys_found['JWT_SECRET_KEY']:
        print(f"{GREEN}✅ JWT_SECRET_KEY: Configurée{RESET}")
    else:
        print(f"{YELLOW}⚠️  JWT_SECRET_KEY: Manquante{RESET}")
        print(f"{YELLOW}   → Générer: python -c 'import secrets; print(secrets.token_urlsafe(64))'{RESET}")

    return all_ok

def check_dependencies():
    """Vérifier dépendances Python critiques"""
    print(f"\n{BLUE}[4/5] Vérification dépendances Python...{RESET}")

    required = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'redis': 'Redis',
        'asyncpg': 'AsyncPG',
        'httpx': 'HTTPX',
        'pydantic': 'Pydantic'
    }

    missing = []
    for module, name in required.items():
        try:
            __import__(module)
            print(f"{GREEN}✅ {name}: Installé{RESET}")
        except ImportError:
            print(f"{RED}❌ {name}: Manquant{RESET}")
            missing.append(module)

    if missing:
        print(f"\n{YELLOW}   → Installer manquants: pip install {' '.join(missing)}{RESET}")
        return False

    return True

def check_file_structure():
    """Vérifier structure fichiers critiques"""
    print(f"\n{BLUE}[5/5] Vérification fichiers critiques...{RESET}")

    critical_files = [
        'app/main.py',
        'app/core/safe_llm_router.py',
        'app/core/quota_manager.py',
        'app/routers/quota.py',
        'app/routers/payment.py',
        'app/routers/chat_safe.py',
        'app/routers/admin_dashboard.py'
    ]

    all_exist = True
    for file_path in critical_files:
        path = Path(file_path)
        if path.exists():
            print(f"{GREEN}✅ {file_path}{RESET}")
        else:
            print(f"{RED}❌ {file_path}: MANQUANT{RESET}")
            all_exist = False

    return all_exist

def generate_env_template():
    """Générer template .env.local si manquant"""
    env_file = Path(".env.local")
    if env_file.exists():
        return

    print(f"\n{YELLOW}Génération template .env.local...{RESET}")

    template = """# IA Factory Algeria - Configuration Locale
# NE PAS COMMIT CE FICHIER!

# ============================================
# LLM PROVIDERS
# ============================================

# Groq (GRATUIT - Priorité #1)
GROQ_API_KEY=your_groq_api_key_here

# PublicAI Apertus (GRATUIT - Priorité #2)
PUBLICAI_API_KEY=your_publicai_api_key_here

# OpenRouter (PAYANT - Accès Claude/GPT/Grok)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# ============================================
# DATABASE & CACHE
# ============================================

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/iafactory_dz
REDIS_URL=redis://localhost:6379/0

# ============================================
# SECURITY
# ============================================

JWT_SECRET_KEY=your_secret_key_here_min_64_chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# ============================================
# PAYMENT (Chargily)
# ============================================

CHARGILY_API_KEY=your_chargily_api_key_here
CHARGILY_SECRET_KEY=your_chargily_secret_key_here
CHARGILY_WEBHOOK_SECRET=your_webhook_secret_here

# ============================================
# MONITORING
# ============================================

MAX_DAILY_BUDGET_USD=50.0
ADMIN_EMAIL=admin@iafactory.dz
"""

    with open(env_file, 'w') as f:
        f.write(template)

    print(f"{GREEN}✅ Template .env.local créé!{RESET}")
    print(f"{YELLOW}   → Éditer maintenant: code .env.local{RESET}")

def main():
    """Exécuter tous les checks"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  IA FACTORY ALGERIA - DIAGNOSTIC SYSTÈME{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

    results = {
        'redis': check_redis(),
        'postgres': check_postgres(),
        'api_keys': check_api_keys(),
        'dependencies': check_dependencies(),
        'files': check_file_structure()
    }

    # Résumé
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  RÉSUMÉ{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

    passed = sum(results.values())
    total = len(results)

    if passed == total:
        print(f"{GREEN}✅ SYSTÈME PRÊT! {passed}/{total} checks passés{RESET}")
        print(f"\n{GREEN}🚀 Prochaine étape:{RESET}")
        print(f"{GREEN}   uvicorn app.main:app --reload --port 8000{RESET}\n")
        return 0
    else:
        print(f"{YELLOW}⚠️  {passed}/{total} checks passés{RESET}")
        print(f"{YELLOW}   {total - passed} problème(s) à corriger avant de lancer l'API{RESET}\n")

        # Actions à faire
        print(f"{BLUE}ACTIONS RECOMMANDÉES:{RESET}\n")

        if not results['dependencies']:
            print(f"{YELLOW}1. Installer dépendances:{RESET}")
            print(f"   pip install -r requirements.txt\n")

        if not results['redis']:
            print(f"{YELLOW}2. Démarrer Redis:{RESET}")
            print(f"   docker run -d --name redis-iafactory -p 6379:6379 redis:7-alpine\n")

        if not results['api_keys']:
            print(f"{YELLOW}3. Configurer clés API:{RESET}")
            print(f"   - Obtenir GROQ_API_KEY: https://console.groq.com/keys")
            print(f"   - Éditer .env.local: code .env.local\n")

        if not results['postgres']:
            print(f"{YELLOW}4. Démarrer PostgreSQL:{RESET}")
            print(f"   docker run -d --name postgres-iafactory -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:15-alpine")
            print(f"   docker exec -it postgres-iafactory psql -U postgres -c 'CREATE DATABASE iafactory_dz;'\n")

        if not results['files']:
            print(f"{RED}5. Fichiers manquants - vérifier code source{RESET}\n")

        print(f"{BLUE}Après corrections, relancer:{RESET}")
        print(f"   python check_ready.py\n")

        return 1

if __name__ == "__main__":
    # Générer .env.local si n'existe pas
    if not Path(".env.local").exists():
        generate_env_template()

    sys.exit(main())
