# Démarrage Rapide - Tests SaaS Zero Risque

**Status**: ✅ Code intégré et prêt
**Prochaine étape**: Tests avant rotation de clés

---

## Ce qui a été fait

✅ **SafeLLMRouter** intégré ([app/core/safe_llm_router.py](services/api/app/core/safe_llm_router.py))
✅ **RateLimiter** intégré ([app/middleware/rate_limiter.py](services/api/app/middleware/rate_limiter.py))
✅ **Payment Router** intégré ([app/routers/payment.py](services/api/app/routers/payment.py))
✅ **Admin Dashboard** intégré ([app/routers/admin_dashboard.py](services/api/app/routers/admin_dashboard.py))
✅ **Chat Safe** intégré ([app/routers/chat_safe.py](services/api/app/routers/chat_safe.py))
✅ **Migration SQL** prête ([migrations/005_billing_tiers.sql](services/api/migrations/005_billing_tiers.sql))
✅ **Routers** enregistrés dans [main.py](services/api/app/main.py:92-94)
✅ **Scripts de test** créés
✅ **Scripts de rotation clés** prêts (pour après tests)

---

## Démarrage Immédiat (3 commandes)

### Option 1: Script Automatique (Recommandé)

```bash
cd d:\IAFactory\rag-dz\services\api
quick_start.bat
```

Ce script va:
1. Vérifier/créer `.env.local`
2. Vérifier PostgreSQL et Redis
3. Créer la base de données
4. Appliquer la migration SQL
5. Démarrer l'API sur http://localhost:8000

### Option 2: Manuel

```bash
cd d:\IAFactory\rag-dz\services\api

# 1. Créer .env.local (copier les clés actuelles)
notepad .env.local

# 2. Appliquer migration
psql -U postgres -c "CREATE DATABASE iafactory_dz;"
psql -U postgres -d iafactory_dz -f migrations\005_billing_tiers.sql

# 3. Démarrer API
uvicorn app.main:app --reload --port 8000
```

---

## Vérification Rapide (1 min)

```bash
# Test 1: API tourne
curl http://localhost:8000/health

# Test 2: Docs accessibles
start http://localhost:8000/docs

# Test 3: Nouveaux endpoints visibles
# Chercher dans /docs:
# - "Payment Chargily"
# - "Admin Dashboard"
# - "Chat Safe"
```

---

## Tests Complets (10 min)

Voir le guide détaillé: [QUICK_TEST_GUIDE.md](services/api/QUICK_TEST_GUIDE.md)

Résumé:
1. **Login admin**: `POST /api/auth/login`
2. **Dashboard**: `GET /api/admin/dashboard`
3. **Chat FREE tier**: `POST /api/v2/chat`
4. **Rate limiting**: 4 messages → 429 Error
5. **Usage logs**: Vérifier table `llm_usage_logs`

---

## Après Tests Réussis

1. **Documenter résultats**
   - Screenshots dashboard
   - Logs API
   - Résultats tests

2. **Rotation clés API** (20 min)
   ```bash
   scripts\rotate_api_keys.bat
   python scripts\verify_keys_rotation.py
   ```

3. **Setup Chargily Production**
   - Créer compte: https://chargily.com
   - Obtenir clés LIVE
   - Configurer webhook

4. **Déploiement VPS** (optionnel)
   ```bash
   services\api\deploy_zero_risque.bat
   ```

---

## Structure Fichiers Créés

```
rag-dz/
├── services/api/
│   ├── app/
│   │   ├── core/
│   │   │   └── safe_llm_router.py       ✅ NOUVEAU
│   │   ├── middleware/
│   │   │   └── rate_limiter.py          ✅ NOUVEAU
│   │   ├── routers/
│   │   │   ├── payment.py               ✅ NOUVEAU
│   │   │   ├── admin_dashboard.py       ✅ NOUVEAU
│   │   │   ├── chat_safe.py             ✅ NOUVEAU
│   │   │   └── __init__.py              ✅ MODIFIÉ
│   │   └── main.py                      ✅ MODIFIÉ (3 routers ajoutés)
│   ├── migrations/
│   │   └── 005_billing_tiers.sql        ✅ NOUVEAU
│   ├── quick_start.bat                  ✅ NOUVEAU
│   ├── deploy_zero_risque.bat           ✅ NOUVEAU
│   ├── test_zero_risque.py              ✅ NOUVEAU
│   ├── QUICK_TEST_GUIDE.md              ✅ NOUVEAU
│   └── INTEGRATION_COMPLETE.md          ✅ NOUVEAU
├── scripts/
│   ├── rotate_api_keys.bat              ✅ NOUVEAU (pour après)
│   ├── verify_keys_rotation.py          ✅ NOUVEAU (pour après)
│   └── GUIDE_ROTATION_RAPIDE.md         ✅ NOUVEAU (pour après)
└── DEMARRAGE_RAPIDE.md                  ✅ CE FICHIER
```

---

## Endpoints Disponibles

### Chat avec Zero Risk
- `POST /api/v2/chat` - Chat avec SafeLLMRouter
- `GET /api/v2/models` - Modèles disponibles par tier
- `GET /api/v2/usage/today` - Stats usage user

### Payment Chargily
- `POST /api/payment/subscribe/{tier}` - Créer checkout (student/pro)
- `POST /api/payment/webhook/chargily` - Webhook Chargily
- `GET /api/payment/status` - Status abonnement
- `POST /api/payment/cancel` - Annuler abonnement

### Admin Dashboard
- `GET /api/admin/dashboard` - Dashboard complet
- `GET /api/admin/costs/breakdown` - Breakdown coûts
- `POST /api/admin/budget/update` - Modifier budget cap
- `POST /api/admin/users/{id}/ban` - Ban user

---

## Configuration Minimale .env.local

Pour tests, minimum requis:

```bash
# DATABASE
POSTGRES_URL=postgresql://postgres:password@localhost:5432/iafactory_dz
REDIS_URL=redis://localhost:6379/0

# LLM (utiliser clés actuelles - OK pour tests)
GROQ_API_KEY=votre_cle_actuelle
OPENROUTER_API_KEY=votre_cle_actuelle

# CHARGILY (fake pour tests)
CHARGILY_SECRET_KEY=sk_test_fake
CHARGILY_MODE=test

# APP
JWT_SECRET_KEY=test_secret_dev_only
MAX_DAILY_BUDGET_USD=50.0
```

---

## Support

- **Guide test détaillé**: [QUICK_TEST_GUIDE.md](services/api/QUICK_TEST_GUIDE.md)
- **Guide rotation clés**: [scripts/GUIDE_ROTATION_RAPIDE.md](scripts/GUIDE_ROTATION_RAPIDE.md)
- **Integration complète**: [INTEGRATION_COMPLETE.md](services/api/INTEGRATION_COMPLETE.md)

---

## Timeline

| Étape | Durée | Status |
|-------|-------|--------|
| Intégration code | - | ✅ FAIT |
| Tests SaaS | 30 min | 🔄 EN COURS |
| Rotation clés | 20 min | ⏳ APRÈS TESTS |
| Setup Chargily LIVE | 15 min | ⏳ APRÈS ROTATION |
| Déploiement VPS | 30 min | ⏳ OPTIONNEL |

---

**Prêt?** Exécutez:
```bash
cd d:\IAFactory\rag-dz\services\api
quick_start.bat
```

Temps estimé jusqu'à production: **1h15** (tests + rotation + Chargily)
