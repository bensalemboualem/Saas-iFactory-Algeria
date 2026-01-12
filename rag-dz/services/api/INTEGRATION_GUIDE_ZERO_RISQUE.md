# 🚀 GUIDE INTÉGRATION - ARCHITECTURE ZÉRO RISQUE

**Généré le**: 23 décembre 2024
**Objectif**: Déployer SafeLLMRouter + RateLimiter + Chargily en 4h

---

## 📋 CHECKLIST PRÉ-REQUIS

Avant de commencer, vérifier:

```bash
✅ PostgreSQL opérationnel (port 5432)
✅ Redis opérationnel (port 6379)
✅ Services API FastAPI lancé (port 8000)
✅ Variables d'environnement configurées (.env)
✅ Clés API rotées (18 clés exposées supprimées)
```

---

## 🔐 ÉTAPE 1: ROTATION CLÉS API (30 min) - PRIORITÉ ABSOLUE

### 1.1 Supprimer .env.ready du repo

```bash
# Retirer du tracking Git
git rm --cached apps/video-studio/.env.ready

# Supprimer physiquement
rm -f apps/video-studio/.env.ready

# Ajouter à .gitignore
echo "**/.env.ready" >> .gitignore
echo "**/.env.local" >> .gitignore

# Commit
git add .gitignore
git commit -m "security: remove exposed API keys from repo"
git push
```

### 1.2 Régénérer TOUTES les clés

**Providers à régénérer** (18 clés exposées):

1. **Anthropic**: https://console.anthropic.com/settings/keys
   - Révoquer `sk-ant-api03-KXm...`
   - Générer nouvelle clé

2. **OpenAI**: https://platform.openai.com/api-keys
   - Révoquer `sk-proj-ysv...`
   - Générer nouvelle clé

3. **Groq**: https://console.groq.com/keys
   - Régénérer clé

4. **OpenRouter** (PRIORITAIRE): https://openrouter.ai/keys
   - Régénérer clé

5. Continuer pour les 14 autres (Gemini, Mistral, DeepSeek, etc.)

### 1.3 Créer .env.local sécurisé

```bash
# services/api/.env.local
cat > services/api/.env.local <<EOF
# IA Factory Algeria - Production Keys
# GÉNÉRÉ: $(date)
# ⚠️ NE JAMAIS COMMIT CE FICHIER

# === LLM PROVIDERS ===
ANTHROPIC_API_KEY=sk-ant-VOTRE_NOUVELLE_CLE
OPENAI_API_KEY=sk-VOTRE_NOUVELLE_CLE
GROQ_API_KEY=gsk_VOTRE_NOUVELLE_CLE
OPENROUTER_API_KEY=sk-or-v1-VOTRE_NOUVELLE_CLE
GEMINI_API_KEY=AIza...
MISTRAL_API_KEY=...
DEEPSEEK_API_KEY=...

# === DATABASE ===
POSTGRES_URL=postgresql://user:pass@localhost:5432/iafactory_dz
REDIS_URL=redis://localhost:6379/0

# === PAYMENT CHARGILY ===
CHARGILY_API_KEY=test_YOUR_KEY  # Changer en 'live_' pour prod
CHARGILY_SECRET_KEY=test_YOUR_SECRET
CHARGILY_WEBHOOK_SECRET=YOUR_WEBHOOK_SECRET
CHARGILY_MODE=test  # Changer en 'live' pour prod

# === BUDGET PROTECTION ===
DAILY_BUDGET_USD=50.0

# === APP ===
API_SECRET_KEY=$(openssl rand -hex 32)
FRONTEND_URL=http://localhost:3000
API_URL=http://localhost:8000
EOF

# Sécuriser
chmod 600 services/api/.env.local
```

---

## 💾 ÉTAPE 2: MIGRATIONS DATABASE (15 min)

### 2.1 Appliquer migration

```bash
cd services/api

# Vérifier connexion PostgreSQL
psql $POSTGRES_URL -c "SELECT version();"

# Appliquer migration
psql $POSTGRES_URL -f migrations/005_billing_tiers.sql

# Vérifier tables créées
psql $POSTGRES_URL -c "\dt"
# Doit montrer:
# - user_tiers
# - llm_usage_logs
# - payment_transactions
```

### 2.2 Tester insertion

```sql
-- Test user_tiers
INSERT INTO user_tiers (user_id, tier, subscribed_at, expires_at)
VALUES (1, 'free', NULL, NULL)
ON CONFLICT (user_id) DO NOTHING;

-- Vérifier
SELECT * FROM user_tiers;

-- Test llm_usage_logs
INSERT INTO llm_usage_logs (user_id, provider, model, tokens_input, tokens_output, cost_usd)
VALUES (1, 'groq', 'llama-3.3-70b', 100, 800, 0.0);

-- Vérifier
SELECT * FROM llm_usage_logs ORDER BY created_at DESC LIMIT 5;
```

---

## 🔧 ÉTAPE 3: INTÉGRER ROUTES FASTAPI (30 min)

### 3.1 Ajouter imports dans main.py

```python
# services/api/app/main.py

from app.routers import chat_safe, payment, admin_dashboard
from app.middleware.rate_limiter import rate_limit_middleware

# Ajouter routers
app.include_router(chat_safe.router)
app.include_router(payment.router)
app.include_router(admin_dashboard.router)

# Ajouter middleware rate limiting
app.middleware("http")(rate_limit_middleware)
```

### 3.2 Redémarrer API

```bash
# Tuer processus existant
pkill -f "uvicorn.*app.main:app"

# Relancer avec .env.local
cd services/api
export $(cat .env.local | xargs)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Vérifier logs
# Doit montrer: "Application startup complete"
```

### 3.3 Tester endpoints

```bash
# Health check
curl http://localhost:8000/health

# Models disponibles (avec auth)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://localhost:8000/api/v2/models

# Chat (avec auth)
curl -X POST http://localhost:8000/api/v2/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Bonjour, comment tu vas?",
    "model": "gpt-4o"
  }'

# Dashboard admin (avec superuser)
curl -H "Authorization: Bearer ADMIN_JWT_TOKEN" \
     http://localhost:8000/admin/dashboard
```

---

## 💳 ÉTAPE 4: CONFIGURER CHARGILY (1h)

### 4.1 Créer compte Chargily

1. Aller sur https://pay.chargily.com
2. S'inscrire avec email algérien
3. Vérifier identité (CIB ou EDAHABIA)
4. Activer mode développeur

### 4.2 Obtenir clés API

Dans dashboard Chargily:
- API Key (test): `test_pk_xxxxx`
- Secret Key (test): `test_sk_xxxxx`
- Webhook Secret: Générer dans "Webhooks"

Ajouter à `.env.local`:
```bash
CHARGILY_API_KEY=test_pk_xxxxx
CHARGILY_SECRET_KEY=test_sk_xxxxx
CHARGILY_WEBHOOK_SECRET=whsec_xxxxx
CHARGILY_MODE=test
```

### 4.3 Configurer webhook Chargily

Dans dashboard Chargily → Webhooks:

**URL**: `https://api.iafactoryalgeria.com/payment/webhook/chargily`
**Events**: Cocher "checkout.paid", "checkout.failed", "checkout.expired"
**Secret**: Copier et mettre dans CHARGILY_WEBHOOK_SECRET

### 4.4 Tester paiement en mode TEST

```bash
# Créer checkout test
curl -X POST http://localhost:8000/payment/subscribe/student \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# Response:
# {
#   "checkout_url": "https://pay.chargily.net/test/checkout/xxxxx",
#   "amount": 1590
# }

# Ouvrir checkout_url dans navigateur
# Utiliser carte de test Chargily:
# Numéro: 4242 4242 4242 4242
# Expiry: 12/25
# CVV: 123

# Vérifier webhook reçu dans logs backend
# Vérifier user_tiers mis à jour
psql $POSTGRES_URL -c "SELECT * FROM user_tiers WHERE user_id = 1;"
```

---

## 🔍 ÉTAPE 5: TESTER ROUTING (1h)

### 5.1 Test tier FREE (Groq uniquement)

```python
# Test script: test_routing.py
import requests

API_URL = "http://localhost:8000"

# User FREE (tier = 'free')
headers_free = {"Authorization": "Bearer FREE_USER_JWT"}

# Doit utiliser Groq (provider = "groq")
for i in range(3):
    response = requests.post(
        f"{API_URL}/api/v2/chat",
        headers=headers_free,
        json={"prompt": f"Test {i+1}", "model": "gpt-4o"}
    )
    data = response.json()
    print(f"Request {i+1}: Provider = {data['provider']}, Cost = ${data['cost']}")
    assert data["provider"] == "groq", "FREE tier doit utiliser Groq uniquement!"
    assert data["cost"] == 0, "Groq doit être gratuit!"

# 4ème requête doit être refusée (quota 3/jour)
response = requests.post(f"{API_URL}/api/v2/chat", headers=headers_free, json={"prompt": "Test 4"})
assert response.status_code == 429, "Quota FREE non respecté!"
print("✅ Tier FREE: OK (100% Groq, quota 3/jour)")
```

### 5.2 Test tier STUDENT (85% Groq / 15% OpenRouter)

```python
# User STUDENT (tier = 'student')
headers_student = {"Authorization": "Bearer STUDENT_USER_JWT"}

groq_count = 0
openrouter_count = 0

# Envoyer 100 requêtes
for i in range(100):
    response = requests.post(
        f"{API_URL}/api/v2/chat",
        headers=headers_student,
        json={"prompt": f"Test {i+1}", "model": "gpt-4o"}
    )
    data = response.json()

    if data["provider"] == "groq":
        groq_count += 1
    elif data["provider"] == "openrouter":
        openrouter_count += 1

groq_percent = groq_count / 100 * 100
print(f"Groq: {groq_count}/100 ({groq_percent}%)")
print(f"OpenRouter: {openrouter_count}/100 ({100 - groq_percent}%)")

# Tolérance ±5%
assert 80 <= groq_percent <= 90, "Routing STUDENT doit être ~85% Groq"
print("✅ Tier STUDENT: OK (85% Groq / 15% OpenRouter)")
```

### 5.3 Test budget cap (fallback automatique)

```python
# Simuler budget dépassé
import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.set("budget:today:usd", "51.0")  # > 50 (limite)

# Requête avec user PRO (normalement OpenRouter)
response = requests.post(
    f"{API_URL}/api/v2/chat",
    headers={"Authorization": "Bearer PRO_USER_JWT"},
    json={"prompt": "Test budget cap", "model": "gpt-4o"}
)
data = response.json()

assert data["provider"] == "groq", "Doit fallback sur Groq si budget cap dépassé!"
assert data.get("budget_fallback") == True
print("✅ Budget cap: OK (auto-switch Groq)")

# Reset budget
r.delete("budget:today:usd")
```

---

## 📊 ÉTAPE 6: DASHBOARD ADMIN (30 min)

### 6.1 Accès dashboard

```bash
# Ouvrir dans navigateur (avec admin JWT)
https://api.iafactoryalgeria.com/admin/dashboard

# Ou via curl
curl -H "Authorization: Bearer ADMIN_JWT" \
     http://localhost:8000/admin/dashboard | jq
```

### 6.2 Métriques affichées

Le dashboard doit montrer:

```json
{
  "budget": {
    "spent_usd": 5.23,
    "limit_usd": 50.0,
    "remaining_usd": 44.77,
    "percent_used": 10.5,
    "alert_level": "ok"
  },
  "users": {
    "active_today": 12,
    "avg_cost_per_user": 0.44,
    "abusive_count": 0,
    "abusive_users": []
  },
  "providers": [
    {
      "provider": "groq",
      "requests_count": 150,
      "cost_total": 0.0
    },
    {
      "provider": "openrouter",
      "requests_count": 30,
      "cost_total": 5.23
    }
  ],
  "economics": {
    "revenue_usd": 20.73,
    "costs_usd": 5.23,
    "profit_usd": 15.50,
    "margin_percent": 74.8
  },
  "alerts": []
}
```

### 6.3 Surveiller alertes

Si budget > 90%, alerte apparaît:

```json
{
  "alerts": [
    {
      "level": "critical",
      "message": "Budget quotidien à 92.3%! Basculement auto sur Groq imminent.",
      "action": "Augmenter DAILY_BUDGET_USD ou attendre minuit"
    }
  ]
}
```

---

## 🧪 ÉTAPE 7: TESTS FINAUX (1h)

### 7.1 Test complet user journey

```bash
# 1. Signup
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.dz", "password": "secure123"}'

# 2. Login
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.dz", "password": "secure123"}' | jq -r .access_token)

# 3. Chat FREE (3 messages)
for i in {1..3}; do
  curl -X POST http://localhost:8000/api/v2/chat \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"prompt\": \"Test $i\"}"
done

# 4. 4ème message doit échouer (quota)
curl -X POST http://localhost:8000/api/v2/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test 4"}'
# Expected: 429 Too Many Requests

# 5. Créer checkout upgrade STUDENT
CHECKOUT=$(curl -X POST http://localhost:8000/payment/subscribe/student \
  -H "Authorization: Bearer $TOKEN" | jq -r .checkout_url)

echo "Ouvrir dans navigateur: $CHECKOUT"
# Payer avec carte test Chargily

# 6. Vérifier abonnement activé
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/payment/subscription/status
# Expected: {"tier": "student", "is_active": true}

# 7. Chat STUDENT (200 messages possibles)
curl -X POST http://localhost:8000/api/v2/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test post-upgrade", "model": "claude-sonnet-4"}'
# Expected: provider = "groq" ou "openrouter" (85%/15%)
```

### 7.2 Test rate limiting

```bash
# Envoyer 20 requêtes en 10 secondes (trop rapide)
for i in {1..20}; do
  curl -X POST http://localhost:8000/api/v2/chat \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"prompt\": \"Spam $i\"}" &
done

# Doit recevoir 429 après 10 requêtes (limite STUDENT = 10/min)
```

### 7.3 Test fallback providers

```bash
# Simuler panne OpenRouter (kill process ou firewall)
# Requête doit automatiquement utiliser Groq

curl -X POST http://localhost:8000/api/v2/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test fallback"}'
# Expected: {"provider": "groq", "fallback": true}
```

---

## 🚀 ÉTAPE 8: DÉPLOIEMENT PRODUCTION (1h)

### 8.1 Changer Chargily en mode LIVE

```bash
# .env.local
CHARGILY_MODE=live
CHARGILY_API_KEY=live_pk_VOTRE_VRAIE_CLE
CHARGILY_SECRET_KEY=live_sk_VOTRE_VRAIE_CLE
```

### 8.2 Augmenter budget si besoin

```bash
# Pour 100 users actifs/jour
DAILY_BUDGET_USD=200.0
```

### 8.3 Redémarrer services

```bash
# Backend API
systemctl restart iafactory-api

# Vérifier logs
journalctl -u iafactory-api -f

# Tester healthcheck
curl https://api.iafactoryalgeria.com/health
```

---

## 📈 MONITORING POST-LANCEMENT

### Dashboards à surveiller (H24 premier jour):

1. **Admin Dashboard**: https://api.iafactoryalgeria.com/admin/dashboard
   - Budget spent (toutes les heures)
   - Alertes (push notifications)
   - Users abusifs

2. **Logs backend**:
```bash
tail -f /var/log/iafactory/api.log | grep -E "Rate limit|Budget|Error"
```

3. **Redis monitoring**:
```bash
redis-cli INFO stats
redis-cli KEYS "budget:*"
redis-cli KEYS "ratelimit:*"
```

4. **PostgreSQL queries**:
```sql
-- Coûts temps réel
SELECT
    provider,
    COUNT(*) as requests,
    SUM(cost_usd) as total_cost
FROM llm_usage_logs
WHERE created_at >= NOW() - INTERVAL '1 hour'
GROUP BY provider;

-- Users top coûts
SELECT
    user_id,
    COUNT(*) as messages,
    SUM(cost_usd) as cost
FROM llm_usage_logs
WHERE created_at >= CURRENT_DATE
GROUP BY user_id
ORDER BY cost DESC
LIMIT 10;
```

---

## ⚠️ ALERTES À CONFIGURER

### Budget > 90%
```bash
# Script cron toutes les 15 min
*/15 * * * * /opt/scripts/check_budget.sh

# check_budget.sh
#!/bin/bash
BUDGET=$(redis-cli GET budget:today:usd)
if (( $(echo "$BUDGET > 45" | bc -l) )); then
  # Envoyer notification WhatsApp/Email
  curl -X POST https://api.whatsapp.com/send \
    -d "phone=+213XXXXXXXXX" \
    -d "message=⚠️ Budget at $(echo "scale=1; $BUDGET/50*100" | bc)%"
fi
```

### Users abusifs
```bash
# Alerte si >10 users dépassent 300 msg/jour
# Intégrer dans dashboard check
```

---

## ✅ CHECKLIST FINAL

```
☐ Clés API rotées (18 clés)
☐ .env.ready supprimé du Git
☐ .env.local créé et sécurisé
☐ Migrations PostgreSQL appliquées
☐ Redis opérationnel
☐ Routes FastAPI intégrées
☐ Middleware rate limiting actif
☐ Chargily configuré (test)
☐ Tests routing OK (FREE/STUDENT/PRO)
☐ Tests budget cap OK
☐ Tests fallback OK
☐ Dashboard admin accessible
☐ Monitoring configuré
☐ Chargily passé en LIVE
☐ Déployé en production
☐ Premier paiement test réussi
```

---

## 🆘 TROUBLESHOOTING

### Erreur "GROQ_API_KEY not configured"

```bash
# Vérifier .env.local chargé
echo $GROQ_API_KEY

# Si vide, charger manuellement
export $(cat services/api/.env.local | xargs)

# Redémarrer uvicorn
```

### Webhook Chargily non reçu

```bash
# Vérifier URL webhook publique (pas localhost!)
# Tester webhook manuellement
curl -X POST https://api.iafactoryalgeria.com/payment/webhook/chargily \
  -H "signature: test" \
  -H "Content-Type: application/json" \
  -d '{"type": "checkout.paid", "data": {}}'

# Vérifier logs nginx
tail -f /var/log/nginx/access.log | grep webhook
```

### Rate limit ne marche pas

```bash
# Vérifier Redis
redis-cli PING
# Expected: PONG

# Vérifier clés rate limit
redis-cli KEYS "ratelimit:*"

# Vérifier middleware chargé
curl -v http://localhost:8000/api/v2/chat
# Headers doivent montrer rate limit
```

---

**FIN DU GUIDE**

**Durée totale estimée**: 4h
**Prochaine étape**: Frontend ModelSelector + Pricing page (2h)
