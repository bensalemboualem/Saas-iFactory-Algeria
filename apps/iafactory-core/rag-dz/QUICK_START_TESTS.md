# 🚀 Quick Start - Tests Backend (30 minutes)

**Date**: 2024-12-23
**Objectif**: Valider que tous les endpoints "Zero Risque" fonctionnent

---

## ✅ Étape 1: Démarrer l'API (2 min)

### Terminal 1 - API Server

```bash
cd d:\IAFactory\rag-dz\services\api

# Activer environnement virtuel (si applicable)
# .venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Démarrer l'API
uvicorn app.main:app --reload --port 8000
```

**Résultat attendu:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## ✅ Étape 2: Tests Basiques Sans Auth (5 min)

### Terminal 2 - Tests Rapides

```bash
# Test 1: Health Check API
curl http://localhost:8000/health

# Résultat attendu:
# {"status":"healthy","timestamp":1734970000.0,"service":"IAFactory"}

# Test 2: Health Check Quotas
curl http://localhost:8000/api/quota/health

# Résultat attendu:
# {"status":"healthy","redis":"connected","quota_manager":"initialized"}

# Test 3: Info Quotas Publique (pas d'auth)
curl http://localhost:8000/api/quota/quotas/info

# Résultat attendu: JSON avec détails FREE/STUDENT/PRO
```

**Si ces 3 tests passent → Backend de base fonctionne! ✅**

---

## ✅ Étape 3: Créer User Test (5 min)

```bash
# Créer un compte test
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@iafactory.dz",
    "password": "Test1234!",
    "name": "Test User"
  }'

# Login et récupérer token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@iafactory.dz",
    "password": "Test1234!"
  }' > token.json

# Extraire le token (copie la valeur "access_token")
# Windows PowerShell:
cat token.json | ConvertFrom-Json | Select-Object -ExpandProperty access_token

# Linux/Mac:
cat token.json | jq -r '.access_token'
```

**Copie le token dans une variable:**

```bash
# Windows CMD:
set TEST_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGc...

# PowerShell:
$env:TEST_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."

# Linux/Mac:
export TEST_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## ✅ Étape 4: Tests Avec Auth (10 min)

```bash
# Test 4: Usage Quota
curl http://localhost:8000/api/quota/usage \
  -H "Authorization: Bearer $TEST_TOKEN"

# Résultat attendu:
# {
#   "messages_today": 0,
#   "messages_limit": 3,
#   "messages_remaining": 3,
#   "premium_today": 0,
#   "premium_limit": 0,
#   "tier": "free"
# }

# Test 5: Liste Modèles
curl http://localhost:8000/api/v2/models \
  -H "Authorization: Bearer $TEST_TOKEN"

# Résultat: Liste des modèles disponibles

# Test 6: Chat Simple (Groq)
curl -X POST http://localhost:8000/api/v2/chat \
  -H "Authorization: Bearer $TEST_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Dis juste OK pour tester"}
    ]
  }'

# Résultat attendu:
# {
#   "response": "OK",
#   "provider": "groq",
#   "quota_info": {...}
# }
```

**Si test 6 marche → Routing LLM fonctionne! ✅**

---

## ✅ Étape 5: Test Suite Complète (8 min)

```bash
cd d:\IAFactory\rag-dz\services\api

# Option A: Sans tokens (tests limités)
python test_zero_risque.py

# Option B: Avec tokens (tests complets)
set TEST_USER_TOKEN=%TEST_TOKEN%
set ADMIN_TOKEN=%ADMIN_TOKEN%  # Si tu as un admin
python test_zero_risque.py
```

**8 tests seront exécutés:**
1. ✅ Health Check
2. ⚠️  Admin Dashboard (skip si pas ADMIN_TOKEN)
3. ✅ Chat FREE tier
4. ✅ Rate Limiting
5. ⚠️  Payment Checkout (skip si Chargily pas configuré)
6. ✅ Models Endpoint
7. ✅ Usage Stats
8. ✅ Subscription Status

**Résultat attendu:**
```
===========================================================
  TEST SUMMARY
===========================================================
✅ Passed: 6/8
⚠️  Failed: 2/8 (Chargily pas encore configuré - normal)
===========================================================
```

---

## ✅ Étape 6: Test Providers LLM (5 min)

```bash
cd d:\IAFactory\rag-dz

# Tester tous les providers
python scripts/setup_all_providers.py test
```

**Résultat attendu:**
```
🚀 TEST DE TOUS LES PROVIDERS LLM

🔄 Test 🇺🇸 Groq (Meta Llama)...
✅ 🇺🇸 Groq (Meta Llama): OK (0.85s)

🔄 Test 🇨🇭 Algerian AI Apertus (PublicAI)...
⚠️  Clé manquante ou provider down

📊 RÉSUMÉ DES TESTS
Providers testés: 6
Succès: 1-3/6 (selon configuration)
```

---

## 🎯 Checklist Validation

### Minimum Viable (Tier FREE fonctionne):
- [x] API démarre sans erreur
- [x] `/health` → 200 OK
- [x] `/api/quota/health` → Redis OK
- [x] Création user → Token OK
- [x] `/api/v2/chat` → Groq répond
- [x] Quota décrémente après message

**Si ces 6 ✅ → Tu peux lancer en BETA! 🚀**

### Optimal (Tiers STUDENT/PRO + Payment):
- [ ] Groq + 1 autre provider gratuit configuré
- [ ] Claude/GPT (OpenRouter) configuré
- [ ] Chargily API keys configurées
- [ ] Payment checkout créé
- [ ] Admin dashboard accessible

---

## ❌ Troubleshooting Rapide

### Problème: API ne démarre pas

```bash
# Vérifier dépendances
pip install -r requirements.txt

# Vérifier .env.local existe
ls .env.local  # Ou: dir .env.local (Windows)

# Vérifier Redis tourne
redis-cli ping  # Devrait répondre PONG

# Si Redis pas installé:
docker run -d -p 6379:6379 redis:7-alpine
```

### Problème: "groq" provider not found

```bash
# Ajouter clé Groq dans .env.local
echo "GROQ_API_KEY=gsk_xxxxx" >> .env.local

# Ou créer .env.local:
cat > .env.local << EOF
GROQ_API_KEY=gsk_xxxxx
DATABASE_URL=postgresql://...
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=your_secret_key_here
EOF
```

### Problème: 401 Unauthorized

```bash
# Token expiré, refaire login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@iafactory.dz","password":"Test1234!"}'
```

### Problème: Chat timeout

```bash
# Groq down? Tester directement:
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"

# Si marche pas → Utiliser fallback Gemini ou attendre Groq
```

---

## ✅ Critères de Succès

**READY TO LAUNCH BETA** si:
- ✅ 6/8 tests suite passent
- ✅ Chat Groq fonctionne
- ✅ Quotas comptent correctement
- ✅ Au moins 1 provider gratuit configuré

**READY FOR PRODUCTION** si:
- ✅ 8/8 tests suite passent
- ✅ 2+ providers gratuits configurés
- ✅ 1+ provider premium (Claude/GPT) configuré
- ✅ Chargily payment fonctionne
- ✅ Admin dashboard accessible

---

## 📊 Prochaines Étapes

**Après validation tests:**

1. **Rotation clés API** (20 min)
   ```bash
   scripts\rotate_api_keys.bat
   python scripts\verify_keys_rotation.py
   ```

2. **Deploy Production** (1h)
   ```bash
   cd services/api
   .\deploy_zero_risque.bat
   ```

3. **Monitoring** (ongoing)
   ```bash
   curl http://localhost:8000/api/admin/dashboard \
     -H "Authorization: Bearer $ADMIN_TOKEN"
   ```

---

**Date**: 2024-12-23
**Status**: ✅ **READY FOR TESTING**
**Temps estimé**: 30 minutes
**Prêt à tester?** 🚀
