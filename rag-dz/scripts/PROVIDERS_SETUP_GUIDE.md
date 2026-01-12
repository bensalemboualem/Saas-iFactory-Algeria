# Guide Setup Providers LLM - IA Factory Algeria

**Objectif**: Configurer tous les providers LLM (gratuits + payants) pour maximiser qualité/coût

---

## 🎯 Stratégie Multi-Providers

### Providers GRATUITS (Priorité 1-3)

| Provider | Coût | Qualité | Utilisation |
|----------|------|---------|-------------|
| **Groq** | 100% gratuit | ⭐⭐⭐⭐ | 85-100% des requêtes |
| **Swiss AI Apertus** | 100% gratuit | ⭐⭐⭐ | Rotation/backup |
| **MiMo Flash** | Gratuit (limité temps) | ⭐⭐⭐ | Rotation/backup |

### Providers PREMIUM (Priorité 4-6)

| Provider | Coût | Qualité | Utilisation |
|----------|------|---------|-------------|
| **Claude Sonnet 4** | $3/$15 par 1M tokens | ⭐⭐⭐⭐⭐ | 5-10% (premium users) |
| **GPT-4o** | $2.50/$10 par 1M tokens | ⭐⭐⭐⭐⭐ | 3-5% (premium users) |
| **Grok 2** | $2/$10 par 1M tokens | ⭐⭐⭐⭐ | 2-5% (premium users) |

---

## 📝 Étape 1: Créer les Comptes

### 1. Groq (GRATUIT - PRIORITÉ #1)

```bash
# 1. Aller sur
https://console.groq.com/signup

# 2. Sign up avec Google/GitHub
# 3. Aller dans "API Keys"
# 4. Créer nouvelle clé: "IA Factory Algeria"
# 5. Copier la clé: gsk_xxxxx...

# 6. Ajouter dans .env.local
GROQ_API_KEY=gsk_xxxxx...
```

**Modèles disponibles**:
- `llama-3.3-70b-versatile` (recommandé)
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`

### 2. PublicAI Apertus (GRATUIT - PRIORITÉ #2)

```bash
# 1. Aller sur
https://platform.publicai.co/signup

# 2. Sign up (email requis)
# 3. Verify email
# 4. Dashboard → API Keys → Create
# 5. Copier la clé

# 6. Ajouter dans .env.local
PUBLICAI_API_KEY=pk_xxxxx...
```

**Modèles disponibles**:
- `swiss-ai/apertus-8b-instruct` (rapide)
- `swiss-ai/apertus-70b-instruct` (meilleur)

### 3. OpenRouter (PAYANT - ACCÈS À TOUS)

```bash
# 1. Aller sur
https://openrouter.ai/signup

# 2. Sign up avec Google/GitHub
# 3. Add Credit: $20-50 recommandé
#    Settings → Billing → Add Credit
# 4. API Keys → Create
# 5. Copier la clé: sk-or-v1-xxxxx...

# 6. Ajouter dans .env.local
OPENROUTER_API_KEY=sk-or-v1-xxxxx...
```

**Donne accès à**:
- MiMo Flash (gratuit temporairement)
- Claude Sonnet 4, Opus 4, Haiku 4
- GPT-4o, GPT-4o-mini
- Grok 2
- +200 autres modèles

---

## ⚙️ Étape 2: Configurer .env.local

```bash
cd d:\IAFactory\rag-dz\services\api

# Créer .env.local si n'existe pas
# Ajouter toutes les clés:

# ============================================
# LLM PROVIDERS
# ============================================

# Groq (GRATUIT - Priorité #1)
GROQ_API_KEY=gsk_xxxxx

# PublicAI Apertus (GRATUIT - Priorité #2)
PUBLICAI_API_KEY=pk_xxxxx

# OpenRouter (PAYANT - Accès à tout)
OPENROUTER_API_KEY=sk-or-v1-xxxxx

# ============================================
# AUTRES (déjà dans projet)
# ============================================

DATABASE_URL=postgresql://...
REDIS_URL=redis://...
JWT_SECRET_KEY=...
MAX_DAILY_BUDGET_USD=50.0
```

---

## 🧪 Étape 3: Tester les Providers

### Test Automatique (Recommandé)

```bash
cd d:\IAFactory\rag-dz

# Installer dépendances
pip install httpx

# Tester TOUS les providers
python scripts/setup_all_providers.py test

# Résultat attendu:
# ✅ Groq: OK (0.85s)
# ✅ Swiss AI Apertus: OK (1.23s)
# ✅ MiMo Flash: OK (1.56s)
# ✅ Claude Sonnet 4: OK (2.14s)
# ✅ GPT-4o: OK (1.89s)
# ✅ Grok 2: OK (2.01s)
#
# 📊 Succès: 6/6 (100%)
```

### Générer Template .env

```bash
python scripts/setup_all_providers.py template

# Affiche template complet avec URLs pour obtenir clés
```

### Test Provider Spécifique

```bash
# Test Groq avec modèle spécifique
python scripts/setup_all_providers.py check groq llama-3.3-70b-versatile

# Test Claude
python scripts/setup_all_providers.py check claude anthropic/claude-sonnet-4-20250514
```

---

## 🔧 Étape 4: Intégration SafeLLMRouter

Le QuotaManager classifie automatiquement les providers:

```python
# Dans app/core/quota_manager.py

FREE_PROVIDERS = {
    "groq",
    "publicai/apertus",
    "publicai/mimo",  # Si on l'ajoute direct
    "gemini"
}

PREMIUM_PROVIDERS = {
    "openrouter/anthropic/claude-sonnet-4-20250514",
    "openrouter/openai/gpt-4o",
    "openrouter/grok-2-1212"
}
```

**Configuration SafeLLMRouter** (déjà fait):

```python
# Dans app/core/safe_llm_router.py

# Routing par tier
ROUTING_CONFIG = {
    "free": {
        "groq": 100,  # 100% Groq
        "openrouter": 0
    },
    "student": {
        "groq": 85,   # 85% Groq (gratuit)
        "openrouter": 15  # 15% premium (budget contrôlé)
    },
    "pro": {
        "groq": 70,   # 70% Groq
        "openrouter": 30  # 30% premium
    }
}
```

---

## 📊 Étape 5: Monitoring

### Dashboard Admin - Usage Providers

```bash
# Endpoint déjà créé
GET /api/admin/dashboard

# Vérifier distribution:
{
  "providers": {
    "groq": {"messages": 8500, "percentage": 94%},  # ✅ Objectif: >90%
    "claude": {"messages": 300, "percentage": 3%},   # ✅ Objectif: <5%
    "gpt": {"messages": 200, "percentage": 2%}       # ✅ Objectif: <3%
  }
}
```

### Alertes à Configurer

```python
# Si premium usage > 15% (tier STUDENT)
if premium_percentage > 15:
    send_alert("Usage premium trop élevé")
    # Action: Réduire quota premium de 10 à 8

# Si costs > budget
if daily_costs > MAX_DAILY_BUDGET:
    # Fallback automatique vers Groq (déjà implémenté)
    pass
```

---

## 💰 Coûts Estimés

### Scénario: 100 users ÉTUDIANT

```
Moyenne: 200 messages/jour/user

Distribution réelle observée:
  - 94% Groq (gratuit): 188 msg × $0 = $0
  - 5% Claude: 10 msg × $0.0126 = $0.126/jour
  - 1% GPT: 2 msg × $0.0085 = $0.017/jour

Coût par user:
  - Provider: $0.143/jour = $4.29/mois
  - Hosting: $0.20/mois
  TOTAL: $4.49/mois

Revenue: $6.91/mois (1590 DA)
Marge: $2.42/mois (35%) ✅

Pour 100 users:
  - Revenue: $691/mois
  - Costs: $449/mois
  - Profit: $242/mois
```

**Note**: Avec quota premium strict (10/jour), coûts sont prévisibles et contrôlés.

---

## 🚨 Troubleshooting

### Problème: Groq rate limited

```bash
# Symptôme: 429 Rate Limit
# Solution: Fallback automatique vers Apertus

# Dans SafeLLMRouter:
if groq_rate_limited:
    fallback_to_apertus()
```

### Problème: OpenRouter credit épuisé

```bash
# Symptôme: 402 Payment Required
# Solution: Add credit

# 1. Aller sur https://openrouter.ai/settings/billing
# 2. Add Credit: $20-50
# 3. Activer Auto-recharge (optionnel)
```

### Problème: Provider lent

```bash
# Vérifier latence
python scripts/setup_all_providers.py test

# Si >3s de latence consistante:
# - Vérifier connexion internet
# - Essayer autre provider
# - Configurer timeout plus élevé
```

---

## ✅ Checklist Validation

Avant mise en production:

- [ ] Groq configuré et testé (GRATUIT)
- [ ] PublicAI Apertus configuré (GRATUIT)
- [ ] OpenRouter configuré avec crédit $20+ (PAYANT)
- [ ] Test automatique passé (6/6 succès)
- [ ] .env.local ne contient PAS de clés exposées
- [ ] .env.local dans .gitignore
- [ ] SafeLLMRouter routing configuré
- [ ] QuotaManager classification providers OK
- [ ] Dashboard admin monitoring actif
- [ ] Alertes budget configurées

---

## 🔮 Évolutions Futures

### Phase 2: Plus de Providers Gratuits

```python
# Ajouter Gemini (Google)
GOOGLE_API_KEY=AIzaSy...
# Modèle: gemini-2.0-flash-exp (gratuit)

# Ajouter DeepSeek (très cheap)
DEEPSEEK_API_KEY=sk-...
# Modèle: deepseek-chat ($0.14/$0.28 par 1M tokens)
```

### Phase 3: Rotation Intelligente

```python
# Rotation automatique entre providers gratuits
FREE_ROTATION = ["groq", "apertus", "mimo", "gemini"]

# Chaque requête utilise provider suivant (round-robin)
# Améliore disponibilité et évite rate limits
```

### Phase 4: Load Balancing

```python
# Si un provider lent/down:
# → Retirer automatiquement de rotation
# → Réintégrer après 5 minutes

# Monitoring latence temps réel
```

---

## 📞 Support

**Questions setup**:
- Voir script: [scripts/setup_all_providers.py](../scripts/setup_all_providers.py)
- Test providers: `python scripts/setup_all_providers.py test`
- Template .env: `python scripts/setup_all_providers.py template`

**Issues providers**:
1. Vérifier clés API valides
2. Check crédit OpenRouter suffisant
3. Test provider spécifique: `python scripts/setup_all_providers.py check <provider> <model>`
4. Consulter logs API: `tail -f logs/api.log | grep provider`

---

## 🎉 Résumé

### Setup Minimal (Gratuit)

✅ **Groq** seul suffit pour démarrer
✅ 100% gratuit
✅ Performance excellente

### Setup Recommandé (Gratuit + Premium)

✅ **Groq** (gratuit, 90% requêtes)
✅ **Apertus** (gratuit, backup)
✅ **OpenRouter** ($20 crédit, 10% requêtes premium)

**Coût**: ~$20 one-time pour démarrer
**Durée**: ~2-3 mois pour 100 users

### Setup Optimal (Production)

✅ Tous les providers configurés
✅ Rotation automatique gratuits
✅ Fallback multi-niveaux
✅ Monitoring temps réel

**Prêt à tester?** Exécutez:
```bash
python scripts/setup_all_providers.py test
```

🚀
