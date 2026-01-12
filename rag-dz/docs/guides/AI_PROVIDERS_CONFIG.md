# 🤖 Configuration des Providers AI

Guide complet pour configurer tous les providers IA dans RAG.dz

## 📊 État Actuel

### ✅ Backend RAG.dz
- **Provider:** Anthropic Claude
- **Modèle:** claude-3-5-sonnet-20241022
- **Status:** ✅ Actif et fonctionnel

### ✅ Bolt.diy
- **Providers configurés:** Tous (10+ providers)
- **Status:** ✅ Prêt à l'emploi

### ✅ BMAD/Archon
- **Intégration:** Backend API
- **Status:** ✅ Actif via routes `/api/bmad/*`

---

## 🔑 Providers Configurés

### 1. **Anthropic Claude** (Principal - Recommandé)
```bash
ANTHROPIC_API_KEY=sk-ant-api03-KXm...
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
```

**Modèles disponibles:**
- `claude-3-5-sonnet-20241022` (Recommandé)
- `claude-3-opus-20240229` (Le plus puissant)
- `claude-3-sonnet-20240229`
- `claude-3-haiku-20240307` (Le plus rapide)

**Avantages:**
- ✅ Meilleure compréhension contextuelle
- ✅ Excellente qualité de génération
- ✅ Support multilingue (FR/AR/EN)
- ✅ 200K tokens de contexte
- ✅ Recommandé pour BMAD/Archon

---

### 2. **OpenAI GPT**
```bash
OPENAI_API_KEY=sk-proj-ysv...
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo
```

**Modèles disponibles:**
- `gpt-4-turbo` (Le plus performant)
- `gpt-4` (Stable)
- `gpt-3.5-turbo` (Économique)

**Avantages:**
- ✅ Rapide et fiable
- ✅ Bon rapport qualité/prix (3.5-turbo)
- ✅ Excellente documentation

---

### 3. **DeepSeek** (Économique)
```bash
DEEPSEEK_API_KEY=sk-e2d...
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-chat
```

**Avantages:**
- ✅ Très économique (5-10x moins cher)
- ✅ Bonnes performances
- ✅ Support du code

---

### 4. **Groq** (Le Plus Rapide)
```bash
GROQ_API_KEY=gsk_mw3...
LLM_PROVIDER=groq
LLM_MODEL=llama-3.1-70b-versatile
```

**Modèles disponibles:**
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`
- `gemma-7b-it`

**Avantages:**
- ✅ Vitesse extrême (500+ tokens/sec)
- ✅ Gratuit (avec limites)
- ✅ Parfait pour développement

---

### 5. **Google Gemini**
```bash
GOOGLE_GENERATIVE_AI_API_KEY=AIza...
LLM_PROVIDER=google
LLM_MODEL=gemini-1.5-pro
```

**Avantages:**
- ✅ Multimodal (texte + images)
- ✅ Grand contexte (1M tokens)
- ✅ Gratuit (avec limites)

---

### 6. **Autres Providers Disponibles**

**Mistral AI:**
```bash
MISTRAL_API_KEY=U4TD...
# Modèles: mistral-large, mistral-medium, mistral-small
```

**Cohere:**
```bash
COHERE_API_KEY=bAVV...
# Modèles: command-r-plus, command-r
```

**Together AI:**
```bash
TOGETHER_API_KEY=99ac...
# Nombreux modèles open-source
```

**OpenRouter (Meta-routing):**
```bash
OPEN_ROUTER_API_KEY=sk-or-v1-b096...
# Accès à tous les providers via une seule API
```

---

## 🔧 Configuration par Service

### Backend RAG.dz (`.env` racine)

```bash
# ==============================================
# Cloud LLM Configuration
# ==============================================
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
ENABLE_LLM=true

# Clés API
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-proj-...
DEEPSEEK_API_KEY=sk-e2d...
GROQ_API_KEY=gsk_mw3...
GOOGLE_GENERATIVE_AI_API_KEY=AIza...
```

### Bolt.diy (`bolt-diy/.env.local`)

Toutes les clés AI sont déjà configurées dans le fichier existant.

---

## 🎯 Changer de Provider

### Via Variables d'Environnement

**1. Modifier `.env`:**
```bash
# Passer à OpenAI GPT-4
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo

# Ou passer à DeepSeek
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-chat

# Ou passer à Groq (rapide)
LLM_PROVIDER=groq
LLM_MODEL=llama-3.1-70b-versatile
```

**2. Redémarrer le backend:**
```bash
docker-compose restart backend
```

**3. Vérifier:**
```bash
docker exec ragdz-backend python -c "from app.clients.cloud_llm import CloudLLMClient; client = CloudLLMClient(); print('Provider:', client.provider); print('Model:', client.model)"
```

---

## 💰 Coûts Estimés

### Par Provider (pour 1M tokens)

| Provider | Input | Output | Total (1M tokens) |
|----------|-------|--------|-------------------|
| **GPT-4 Turbo** | $10 | $30 | ~$40 |
| **GPT-3.5 Turbo** | $0.50 | $1.50 | ~$2 |
| **Claude Sonnet** | $3 | $15 | ~$18 |
| **Claude Haiku** | $0.25 | $1.25 | ~$1.50 |
| **DeepSeek** | $0.14 | $0.28 | ~$0.42 |
| **Groq** | Gratuit* | Gratuit* | Gratuit* |
| **Gemini** | Gratuit* | Gratuit* | Gratuit* |

*Avec limites quotidiennes

### 💡 Recommandations Économiques

1. **Développement:** Groq (gratuit) ou DeepSeek (très économique)
2. **Production petit volume:** Claude Haiku ou GPT-3.5-turbo
3. **Production qualité:** Claude Sonnet ou GPT-4
4. **Production gros volume:** DeepSeek ou Claude Haiku

---

## 🧪 Tester un Provider

### Via API

```bash
# Test avec curl
curl -X POST http://localhost:8180/api/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ragdz_dev_demo_key_..." \
  -d '{
    "query": "Bonjour, comment vas-tu ?",
    "max_results": 3
  }'
```

### Via Python (dans le container)

```bash
docker exec -it ragdz-backend python
```

```python
from app.clients.cloud_llm import CloudLLMClient

client = CloudLLMClient()
print(f"Provider: {client.provider}")
print(f"Model: {client.model}")
print(f"Available: {client.is_available()}")

# Test de génération
response = client.generate(
    prompt="Dis bonjour en français",
    temperature=0.7,
    max_tokens=100
)
print(f"Response: {response}")
```

---

## 🔒 Sécurité des Clés API

### ⚠️ IMPORTANT

- ✅ **NE JAMAIS** commiter `.env` dans Git
- ✅ Utiliser `.env.example` comme template
- ✅ Ajouter `.env` au `.gitignore`
- ✅ Utiliser des clés différentes dev/prod
- ✅ Rotation régulière des clés

### Protéger vos clés:

```bash
# .gitignore (déjà configuré)
.env
.env.local
.env.*.local
**/.env.local
```

---

## 🐛 Debugging

### Le LLM ne fonctionne pas?

**1. Vérifier la configuration:**
```bash
docker exec ragdz-backend env | grep -E "LLM|ANTHROPIC|OPENAI"
```

**2. Vérifier la connexion:**
```bash
docker exec ragdz-backend python -c "
from app.clients.cloud_llm import CloudLLMClient
client = CloudLLMClient()
print('Available:', client.is_available())
print('Provider:', client.provider)
"
```

**3. Vérifier les logs:**
```bash
docker logs ragdz-backend --tail 50 | grep -i "llm\|anthropic\|openai"
```

**4. Tester manuellement:**
```bash
# OpenAI
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"Hello"}]}'

# Anthropic
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-3-5-sonnet-20241022","max_tokens":100,"messages":[{"role":"user","content":"Hello"}]}'
```

---

## 📚 Ressources

### Documentation Officielle

- **Anthropic:** https://docs.anthropic.com/
- **OpenAI:** https://platform.openai.com/docs
- **DeepSeek:** https://platform.deepseek.com/docs
- **Groq:** https://console.groq.com/docs
- **Google AI:** https://ai.google.dev/docs

### Obtenir des API Keys

- **Anthropic:** https://console.anthropic.com/
- **OpenAI:** https://platform.openai.com/api-keys
- **DeepSeek:** https://platform.deepseek.com/api_keys
- **Groq:** https://console.groq.com/keys
- **Google:** https://makersuite.google.com/app/apikey

---

## ✅ Configuration Actuelle Vérifiée

✅ Backend RAG.dz → Anthropic Claude Sonnet 3.5
✅ Bolt.diy → Tous providers configurés
✅ BMAD → Utilise le backend (Claude)
✅ Archon → Utilise le backend (Claude)

**Tout est prêt à l'emploi!** 🚀
