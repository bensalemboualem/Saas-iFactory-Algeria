# Guide de Test Rapide - SaaS Zero Risque (30 min)

**Objectif**: Tester le système complet SANS rotation de clés (on les changera après validation).

---

## ÉTAPE 1: Configuration Minimale (5 min)

### 1.1 Créer .env.local pour tests

```bash
cd d:\IAFactory\rag-dz\services\api

# Créer .env.local avec configuration TEST (clés actuelles OK pour tests)
copy .env.example .env.local
# OU créer manuellement
```

Contenu minimal pour `.env.local`:

```bash
# === DATABASE ===
POSTGRES_URL=postgresql://postgres:password@localhost:5432/iafactory_dz
REDIS_URL=redis://localhost:6379/0

# === LLM PROVIDERS (clés actuelles - OK pour tests) ===
# Utiliser les clés existantes de .env.ready temporairement
GROQ_API_KEY=votre_cle_groq_actuelle
OPENROUTER_API_KEY=votre_cle_openrouter_actuelle
ANTHROPIC_API_KEY=votre_cle_anthropic_actuelle
OPENAI_API_KEY=votre_cle_openai_actuelle
GOOGLE_API_KEY=votre_cle_google_actuelle

# === CHARGILY (TEST MODE - pas besoin de compte réel) ===
CHARGILY_SECRET_KEY=sk_test_fake_for_testing_only
CHARGILY_PUBLIC_KEY=pk_test_fake_for_testing_only
CHARGILY_WEBHOOK_SECRET=whsec_fake_for_testing_only
CHARGILY_MODE=test

# === JWT ===
JWT_SECRET_KEY=test_secret_key_for_development_only_change_in_production

# === BUDGET ===
MAX_DAILY_BUDGET_USD=50.0

# === APP ===
ENVIRONMENT=development
```

### 1.2 Vérifier PostgreSQL et Redis tournent

```bash
# PostgreSQL (vérifier service actif)
# Windows: Services → PostgreSQL → Status: Running
# OU tester connexion:
psql -U postgres -c "SELECT version();"

# Redis (démarrer si nécessaire)
redis-server
# OU sur Windows:
# Services → Redis → Start
```

---

## ÉTAPE 2: Migration SQL (5 min)

```bash
cd d:\IAFactory\rag-dz\services\api

# Créer la base de données si elle n'existe pas
psql -U postgres -c "CREATE DATABASE iafactory_dz;"

# Appliquer la migration
psql -U postgres -d iafactory_dz -f migrations\005_billing_tiers.sql

# Vérifier que les tables sont créées
psql -U postgres -d iafactory_dz -c "\dt"
```

**Résultat attendu**:
```
            List of relations
 Schema |         Name          | Type  |  Owner
--------+-----------------------+-------+----------
 public | user_tiers            | table | postgres
 public | llm_usage_logs        | table | postgres
 public | payment_transactions  | table | postgres
```

---

## ÉTAPE 3: Créer User de Test (5 min)

```bash
# Se connecter à PostgreSQL
psql -U postgres -d iafactory_dz

# Vérifier si table users existe
\dt users

# Si table users n'existe pas, la créer:
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

# Créer user admin (mot de passe: admin123)
INSERT INTO users (email, hashed_password, is_superuser)
VALUES (
    'admin@iafactory.dz',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5hO.X7O5kX5K6',  -- "admin123"
    true
) ON CONFLICT (email) DO NOTHING;

# Créer user test FREE tier
INSERT INTO users (email, hashed_password)
VALUES (
    'test@iafactory.dz',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5hO.X7O5kX5K6',  -- "admin123"
    false
) ON CONFLICT (email) DO NOTHING;

# Associer tier FREE au user test
INSERT INTO user_tiers (user_id, tier)
SELECT id, 'free' FROM users WHERE email = 'test@iafactory.dz'
ON CONFLICT (user_id) DO NOTHING;

# Quitter psql
\q
```

---

## ÉTAPE 4: Démarrer l'API (2 min)

```bash
cd d:\IAFactory\rag-dz\services\api

# Installer dépendances si nécessaire
pip install -r requirements.txt

# Démarrer FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Vérifier que l'API tourne**:
```bash
# Dans un autre terminal
curl http://localhost:8000/health
```

Résultat attendu:
```json
{"status": "healthy", "timestamp": 1703347200, "service": "IAFactory"}
```

---

## ÉTAPE 5: Tests Manuels (10 min)

### Test 1: Login Admin

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"admin@iafactory.dz\",\"password\":\"admin123\"}"
```

**Copier le token** retourné:
```json
{"access_token": "eyJhbGc...", "token_type": "bearer"}
```

```bash
# Sauvegarder dans variable
set ADMIN_TOKEN=eyJhbGc...
```

### Test 2: Dashboard Admin

```bash
curl http://localhost:8000/api/admin/dashboard \
  -H "Authorization: Bearer %ADMIN_TOKEN%"
```

Résultat attendu:
```json
{
  "budget": {
    "spent_today_usd": 0.0,
    "limit_usd": 50.0,
    "remaining_usd": 50.0,
    "percent_used": 0.0
  },
  "users": {
    "active_count": 0,
    "free_count": 1,
    "student_count": 0,
    "pro_count": 0
  },
  "economics": {
    "revenue_dzd": 0,
    "costs_usd": 0.0,
    "profit_usd": 0.0,
    "margin_percent": 0.0
  }
}
```

### Test 3: Liste des Modèles Disponibles

```bash
# Login user test
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@iafactory.dz\",\"password\":\"admin123\"}"

# Copier token
set USER_TOKEN=eyJhbGc...

# Lister modèles
curl http://localhost:8000/api/v2/models \
  -H "Authorization: Bearer %USER_TOKEN%"
```

Résultat attendu (tier FREE):
```json
{
  "models": [
    {
      "id": "llama-3.3-70b-versatile",
      "name": "Llama 3.3 70B",
      "provider": "groq",
      "tier_required": "free"
    }
  ],
  "user_tier": "free"
}
```

### Test 4: Chat avec SafeLLMRouter (FREE tier)

```bash
curl -X POST http://localhost:8000/api/v2/chat \
  -H "Authorization: Bearer %USER_TOKEN%" \
  -H "Content-Type: application/json" \
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"Bonjour! Dis moi quel provider tu utilises.\"}]}"
```

Résultat attendu:
```json
{
  "response": "Bonjour! Je suis alimenté par Groq...",
  "provider": "groq",
  "model": "llama-3.3-70b-versatile",
  "tokens_input": 15,
  "tokens_output": 50,
  "cost_usd": 0.0
}
```

### Test 5: Vérifier Rate Limiting

```bash
# Envoyer 4 messages rapidement (FREE = 3/jour max)
for /L %i in (1,1,4) do (
  curl -X POST http://localhost:8000/api/v2/chat ^
    -H "Authorization: Bearer %USER_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"messages\":[{\"role\":\"user\",\"content\":\"Test %i\"}]}"

  timeout /t 1
)
```

**4ème message doit retourner**:
```json
{
  "detail": "Limite quotidienne atteinte (3 messages/jour pour tier FREE)"
}
```

### Test 6: Vérifier Usage Logs dans DB

```bash
psql -U postgres -d iafactory_dz -c "SELECT * FROM llm_usage_logs ORDER BY created_at DESC LIMIT 5;"
```

Résultat attendu:
```
 id | user_id | provider | tokens_input | tokens_output | cost_usd | created_at
----+---------+----------+--------------+---------------+----------+------------
  3 |       2 | groq     |           15 |            50 |     0.00 | 2024-12-23...
  2 |       2 | groq     |           15 |            50 |     0.00 | 2024-12-23...
  1 |       2 | groq     |           15 |            50 |     0.00 | 2024-12-23...
```

---

## ÉTAPE 6: Tests Automatisés (3 min)

```bash
cd d:\IAFactory\rag-dz\services\api

# Définir tokens pour tests
set ADMIN_TOKEN=votre_admin_token_ici
set TEST_USER_TOKEN=votre_user_token_ici

# Exécuter suite de tests
python test_zero_risque.py
```

**Résultat attendu**:
```
✅ [TEST 1/8] Health Check
✅ [TEST 2/8] Admin Dashboard
✅ [TEST 3/8] Chat with FREE tier
✅ [TEST 4/8] Rate Limiting
⚠️  [TEST 5/8] Payment Checkout (skipped - Chargily not configured)
✅ [TEST 6/8] Available Models
✅ [TEST 7/8] Usage Stats
✅ [TEST 8/8] Subscription Status

Passed: 7/8 tests
```

---

## Checklist de Validation

Avant de passer en production (et rotation clés), vérifier:

- [ ] API démarre sans erreur (`uvicorn app.main:app`)
- [ ] `/health` retourne 200 OK
- [ ] `/docs` accessible et affiche tous les endpoints
- [ ] Login admin fonctionne
- [ ] Dashboard admin accessible
- [ ] Chat avec tier FREE utilise 100% Groq
- [ ] Rate limiting bloque après 3 messages (tier FREE)
- [ ] Logs écrits dans `llm_usage_logs` table
- [ ] Pas d'erreur dans les logs API
- [ ] Redis accessible (`redis-cli ping`)
- [ ] PostgreSQL tables créées (user_tiers, llm_usage_logs, payment_transactions)

---

## Problèmes Courants

### API ne démarre pas: "ModuleNotFoundError: No module named 'app.routers.payment'"

**Cause**: Nouveau router non trouvé

**Solution**:
```bash
# Vérifier que les fichiers existent
dir services\api\app\routers\payment.py
dir services\api\app\routers\admin_dashboard.py
dir services\api\app\routers\chat_safe.py
dir services\api\app\core\safe_llm_router.py
dir services\api\app\middleware\rate_limiter.py
```

Si manquants, vérifier que les fichiers générés précédemment sont bien présents.

### API démarre mais erreur 500 sur /api/v2/chat

**Cause**: SafeLLMRouter ne trouve pas les clés API

**Solution**:
```bash
# Vérifier .env.local contient:
type services\api\.env.local | findstr GROQ_API_KEY
type services\api\.env.local | findstr OPENROUTER_API_KEY

# Copier clés depuis .env.ready si nécessaire
```

### PostgreSQL: "relation users does not exist"

**Cause**: Table users pas créée

**Solution**:
```bash
# Appliquer migration users (si existe)
psql -U postgres -d iafactory_dz -f migrations\001_create_users_table.sql

# OU créer manuellement (voir Étape 3)
```

### Redis: "Connection refused"

**Cause**: Redis ne tourne pas

**Solution**:
```bash
# Windows: Démarrer service Redis
net start Redis

# OU démarrer manuellement
redis-server

# Tester
redis-cli ping
# Doit retourner: PONG
```

---

## Prochaine Étape

Une fois TOUS les tests passent:

1. **Documenter les résultats** (screenshot dashboard, logs, etc.)
2. **Préparer Chargily compte réel** (si pas encore fait)
3. **ROTATION DES CLÉS API** avec les scripts créés:
   ```bash
   scripts\rotate_api_keys.bat
   python scripts\verify_keys_rotation.py
   ```

4. **Push vers production**

---

**Temps total**: 30 minutes ⏱️

**Questions?** Vérifiez les logs API:
```bash
# Dans le terminal où uvicorn tourne
# Les logs s'affichent en temps réel
```
