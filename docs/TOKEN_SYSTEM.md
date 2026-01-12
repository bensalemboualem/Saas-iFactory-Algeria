# SYSTEME DE TOKENS IA FACTORY

**Date:** 30 Decembre 2025

---

## Resume

Le systeme de tokens IA Factory permet aux clients DZ d'acheter des tokens en DZD via Chargily et de consommer l'IA (Groq, OpenRouter, DeepSeek, etc.) avec deduction automatique.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   CLIENT DZ     │────>│  IA FACTORY     │────>│   PROVIDERS     │
│                 │     │                 │     │                 │
│ Paie DZD        │     │ Gere tokens     │     │ Groq (1x)       │
│ (Chargily)      │     │ Route requetes  │     │ DeepSeek (1x)   │
│ CIB/EDAHABIA    │     │ Applique rates  │     │ OpenAI (3-5x)   │
└─────────────────┘     └─────────────────┘     │ Claude (3.5-6x) │
                                                └─────────────────┘
```

---

## Fichiers Implementes

### Migration SQL

| Fichier | Description |
|---------|-------------|
| `migrations/009_token_system.sql` | Tables base (balances, licences, usage_logs) |
| `migrations/013_token_packs_purchase.sql` | Packs, achats, provider rates |

### Services Python

| Fichier | Description |
|---------|-------------|
| `app/tokens/repository.py` | Repository PostgreSQL (balance, redeem, deduct) |
| `app/tokens/router.py` | API endpoints (/api/tokens/*) |
| `app/tokens/llm_proxy.py` | Proxy LLM avec deduction auto et rates |
| `app/tokens/purchase_service.py` | Service achat via Chargily |
| `app/services/chargily_service.py` | Client Chargily (checkout, webhook) |

---

## Tables de Donnees

### tenant_token_balances
```sql
tenant_id UUID PRIMARY KEY
balance_tokens INTEGER        -- Solde actuel
total_purchased INTEGER       -- Total achete
total_consumed INTEGER        -- Total consomme
last_purchase_at TIMESTAMPTZ
last_usage_at TIMESTAMPTZ
```

### token_packs
```sql
id UUID PRIMARY KEY
slug VARCHAR(50) UNIQUE       -- 'starter', 'pro', 'business', etc.
name VARCHAR(100)             -- 'Pack Pro'
tokens INTEGER                -- 500000
bonus_tokens INTEGER          -- 50000 (promo)
price_dzd INTEGER             -- 20000
price_chf DECIMAL             -- 20.00
is_active BOOLEAN
is_featured BOOLEAN
```

### token_purchases
```sql
id UUID PRIMARY KEY
tenant_id UUID
pack_id UUID
tokens_amount INTEGER
bonus_amount INTEGER
amount_dzd INTEGER
payment_provider VARCHAR(20)  -- 'chargily', 'stripe'
payment_status VARCHAR(20)    -- 'pending', 'paid', 'failed'
chargily_checkout_id VARCHAR
created_at TIMESTAMPTZ
paid_at TIMESTAMPTZ
```

### provider_rates
```sql
id UUID PRIMARY KEY
provider VARCHAR(50)          -- 'groq', 'openai', 'anthropic'
model_pattern VARCHAR(100)    -- 'gpt-4.*', NULL = tous
rate DECIMAL(5,2)             -- 1.0 = 1:1, 3.0 = x3
is_active BOOLEAN
priority INTEGER
```

### token_usage_logs
```sql
id UUID PRIMARY KEY
tenant_id UUID
provider VARCHAR(50)
model VARCHAR(100)
tokens_input INTEGER
tokens_output INTEGER
tokens_total INTEGER (GENERATED)
cost_tokens INTEGER           -- Tokens deduits (avec rate)
balance_before INTEGER
balance_after INTEGER
latency_ms INTEGER
metadata JSONB
created_at TIMESTAMPTZ
```

---

## API Endpoints

### Consultation

| Endpoint | Methode | Description |
|----------|---------|-------------|
| `/api/tokens/balance` | GET | Solde actuel du tenant |
| `/api/tokens/history` | GET | Historique utilisation |
| `/api/tokens/packs` | GET | Liste des packs disponibles |
| `/api/tokens/purchases` | GET | Historique des achats |
| `/api/tokens/health` | GET | Health check |

### Achat

| Endpoint | Methode | Description |
|----------|---------|-------------|
| `/api/tokens/purchase` | POST | Creer checkout Chargily |
| `/api/tokens/redeem` | POST | Echanger code licence |
| `/api/tokens/webhook/chargily` | POST | Webhook paiement |

---

## Packs de Tokens

| Pack | Tokens | Bonus | Total | Prix DZD | Prix CHF |
|------|--------|-------|-------|----------|----------|
| starter | 100,000 | 0 | 100,000 | 5,000 | 5.00 |
| pro | 500,000 | 50,000 | 550,000 | 20,000 | 20.00 |
| business | 2,000,000 | 300,000 | 2,300,000 | 70,000 | 70.00 |
| dev | 5,000,000 | 1,000,000 | 6,000,000 | 150,000 | 150.00 |
| enterprise | 20,000,000 | 5,000,000 | 25,000,000 | 500,000 | 500.00 |

---

## Multiplicateurs par Provider

Les tokens IA Factory sont convertis selon le provider utilise:

### Economiques (1x - 1.5x)
| Provider | Model | Rate | Description |
|----------|-------|------|-------------|
| groq | * | 1.0x | Tarif standard |
| groq | llama-3.3.* | 0.8x | Reduction 20% |
| deepseek | * | 1.0x | Tarif standard |
| deepseek | deepseek-chat | 0.9x | Reduction 10% |
| mistral | mistral-small.* | 1.0x | Economique |
| google | gemini-1.5-flash.* | 1.2x | Economique |

### Standards (2x - 3x)
| Provider | Model | Rate | Description |
|----------|-------|------|-------------|
| openrouter | * | 2.0x | Tarif standard |
| openrouter | llama.* | 1.5x | Llama via OR |
| openai | * | 3.0x | Tarif standard |
| openai | gpt-4o-mini | 1.5x | Economique |
| mistral | mistral-large.* | 3.0x | Premium |
| google | gemini-1.5-pro.* | 3.0x | Pro |
| anthropic | claude-3-sonnet.* | 3.0x | Sonnet |

### Premium (4x - 6x)
| Provider | Model | Rate | Description |
|----------|-------|------|-------------|
| openai | gpt-4o | 4.0x | Premium |
| openai | gpt-4-turbo.* | 5.0x | Turbo |
| openrouter | gpt-4.* | 5.0x | GPT-4 via OR |
| openrouter | claude-3.* | 4.0x | Claude via OR |
| anthropic | * | 3.5x | Tarif standard |
| anthropic | claude-3.5-sonnet.* | 3.5x | Sonnet 3.5 |
| anthropic | claude-3-opus.* | 6.0x | Opus (max) |

---

## Flux Achat (Chargily)

```
1. Client → POST /api/tokens/purchase {pack_slug: "pro"}
2. Backend → Cree enregistrement token_purchases (status: pending)
3. Backend → ChargilyService.create_checkout(amount_dzd, metadata)
4. Backend ← Chargily: {checkout_id, checkout_url}
5. Backend → UPDATE token_purchases SET chargily_checkout_id
6. Backend → Return {checkout_url: "https://pay.chargily.net/..."}

7. Client → Redirige vers checkout_url
8. Client → Paie sur Chargily (CIB/EDAHABIA)

9. Chargily → POST /api/tokens/webhook/chargily
   Payload: {type: "checkout.paid", data: {id, metadata}}
10. Backend → Verifie signature HMAC-SHA256
11. Backend → SELECT process_token_purchase(purchase_id)
    - UPDATE token_purchases SET status='paid', paid_at=NOW()
    - UPDATE tenant_token_balances SET balance += tokens
    - INSERT token_usage_logs (type: purchase)
12. Backend → Return {status: "success"}

13. Client → Redirige vers success_url
14. Client → GET /api/tokens/balance → {balance_tokens: 550000}
```

---

## Flux Consommation

```
1. App → proxy_openai_call(tenant_id, model="gpt-4o", messages=[...])

2. LLM Proxy:
   a. check_token_balance(tenant_id, estimated_tokens=500)
   b. Si balance < 500 → raise InsufficientTokensError

3. LLM Proxy → OpenAI API:
   a. client.chat.completions.create(model="gpt-4o", messages)
   b. Response: {usage: {prompt_tokens: 150, completion_tokens: 300}}

4. LLM Proxy:
   a. rate = get_provider_rate("openai", "gpt-4o") → 4.0
   b. cost = (150 + 300) * 4.0 = 1800 tokens

5. LLM Proxy → deduct_tokens_for_llm():
   a. SELECT deduct_tokens(tenant_id, 1800, "openai", "gpt-4o", ...)
   b. UPDATE tenant_token_balances SET balance = balance - 1800
   c. INSERT token_usage_logs

6. Return: {text: "...", tokens_input: 150, tokens_output: 300,
            cost_tokens: 1800, rate: 4.0}
```

---

## Codes de Test

```
IAFACTORY-WELCOME-1000      → 1,000 tokens (onboarding)
SUISSE-PRO-5000             → 5,000 tokens (prepaid CH)
ALGERIE-STARTER-500         → 500 tokens (trial DZ)
ENTERPRISE-UNLIMITED-50000  → 50,000 tokens (enterprise)
```

---

## Variables d'Environnement

```env
# Chargily
CHARGILY_API_KEY=your_api_key
CHARGILY_SECRET_KEY=your_secret_key
CHARGILY_WEBHOOK_SECRET=your_webhook_secret
CHARGILY_MODE=test  # ou 'live'

# URLs
FRONTEND_URL=https://iafactory.dz
API_URL=https://api.iafactory.dz

# Base de donnees
POSTGRES_URL=postgresql://user:pass@host:5432/db
```

---

## Comparaison avec Credits Existants

Le projet RAG-DZ a 2 systemes paralleles:

| Systeme | Fichiers | Usage |
|---------|----------|-------|
| **Tokens (nouveau)** | `app/tokens/*` | Multi-tenant, RLS, rates par provider |
| **Credits (existant)** | `app/services/credits_service.py` | Single-tenant, plans tarifaires |

### Recommandation

Unifier les 2 systemes en:
1. Gardant l'architecture Tokens (plus robuste, multi-tenant)
2. Important les plans tarifaires de Credits
3. Migrant les endpoints `/api/credits/*` vers `/api/tokens/*`

---

## Prochaines Etapes

1. [ ] Executer migration `013_token_packs_purchase.sql`
2. [ ] Tester flux achat avec Chargily test mode
3. [ ] Ajouter dashboard frontend tokens
4. [ ] Configurer webhook URL en production
5. [ ] Unifier avec systeme credits existant
6. [ ] Ajouter alertes low-balance (email/SMS)

---

*Documentation generee le 30 decembre 2025*
