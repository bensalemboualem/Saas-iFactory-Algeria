# 💰 Solutions Économiques pour AI Providers

**Date**: 2025-01-20
**Objectif**: Trouver la solution la moins chère pour Bolt + BMAD Agents

---

## 📊 Comparaison des Coûts (par 1M tokens)

| Provider | Input | Output | Performance | Free Tier | Recommandation |
|----------|-------|--------|-------------|-----------|----------------|
| **Groq** | **GRATUIT** | **GRATUIT** | Ultra rapide (500 tok/s) | 14,400 req/day | ✅ **MEILLEUR CHOIX** |
| **Cohere** | $0.15 | $0.60 | Rapide | 1000 req/mois | ✅ Bon backup |
| **DeepSeek** | $0.14 | $0.28 | Correct | Non | ✅ Déjà utilisé |
| **OpenRouter** | Variable | Variable | Routage intelligent | Credits gratuits | ⚠️ Dépend du model |
| **Together** | $0.20 | $0.20 | Rapide | $25 credits | ⚠️ Payant |
| **Gemini** | $0.075 | $0.30 | Bon | 15 req/min gratuit | ⚠️ Rate limited |
| **Mistral** | $0.25 | $0.25 | Correct | Non | ❌ Payant |
| **Claude** | $3.00 | $15.00 | Excellent mais cher | Non | ❌ TRÈS CHER |
| **OpenAI** | $0.15-5.00 | $0.60-15.00 | Excellent mais cher | Non | ❌ CHER |

---

## 🎯 SOLUTION RECOMMANDÉE

### Architecture à 2 niveaux:

```
┌─────────────────────────────────────────┐
│         BOLT.DIY (Frontend)             │
│  Provider: GROQ (GRATUIT)               │
│  Model: llama-3.3-70b-versatile         │
│  Usage: Génération de code Bolt         │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│    BACKEND BMAD (Agents Experts)        │
│  Provider: DEEPSEEK ($0.14/$0.28)       │
│  Model: deepseek-chat                   │
│  Usage: Conversations agents BMAD       │
└─────────────────────────────────────────┘
```

### Pourquoi cette solution?

1. **GROQ pour Bolt** (Frontend) ✅
   - **100% GRATUIT** (14,400 requêtes/jour)
   - **Ultra rapide** (500 tokens/seconde)
   - Modèles puissants: Llama 3.3 70B, Mixtral 8x7B
   - Parfait pour génération de code

2. **DEEPSEEK pour BMAD** (Backend) ✅
   - **Très économique** ($0.14 input, $0.28 output)
   - Bon pour conversations (agents)
   - Déjà configuré et testé
   - 20x moins cher que Claude

**Coût estimé mensuel**: **~$5-10** (seulement BMAD agents)

---

## 🔧 Configuration GROQ pour Bolt

### Étape 1: Vérifier la Clé Groq

Tu as déjà la clé dans `.env.local`:
```env
GROQ_API_KEY=gsk_YOUR_GROQ_API_KEY_HERE
```

### Étape 2: Configurer Bolt pour Groq

1. Ouvre Bolt: http://localhost:5174
2. Clique sur **Settings** (⚙️)
3. Section "**Provider**": Sélectionne **Groq**
4. Section "**Model**": Sélectionne **llama-3.3-70b-versatile**
5. Ferme les settings

**Modèles Groq disponibles**:
- `llama-3.3-70b-versatile` (Meilleur, 128k context)
- `llama-3.1-70b-versatile` (Très bon)
- `mixtral-8x7b-32768` (Rapide)
- `gemma2-9b-it` (Léger)

### Étape 3: Tester

1. Tape un message dans Bolt (sans agent BMAD)
2. Vérifie que Groq répond rapidement
3. Si erreur, vérifie les logs:
   ```bash
   docker logs ragdz-bolt-diy -f
   ```

---

## 🚀 Configuration OLLAMA Local (Pour VPS)

### Architecture VPS avec Ollama

```
┌─────────────────────────────────────────┐
│              VPS SERVER                 │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Docker Container: Ollama         │ │
│  │  - llama3.2:3b (léger, rapide)    │ │
│  │  - deepseek-r1:7b (reasoning)     │ │
│  │  - qwen2.5-coder:7b (code)        │ │
│  │  Port: 11434                      │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Backend RAG.dz (Port 8180)       │ │
│  │  - BMAD Agents → Ollama local     │ │
│  │  - Pas de coût API externe!       │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Bolt.DIY (Port 5174)             │ │
│  │  - Provider: Groq (gratuit)       │ │
│  │  - Ou Ollama local en backup      │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Étape 1: Installer Ollama sur VPS

```bash
# Sur ton VPS
curl -fsSL https://ollama.com/install.sh | sh

# Ou via Docker (recommandé)
docker run -d \
  --name ollama \
  --gpus all \
  -v ollama_data:/root/.ollama \
  -p 11434:11434 \
  ollama/ollama
```

### Étape 2: Télécharger Modèles

```bash
# Modèles recommandés pour BMAD agents
docker exec ollama ollama pull llama3.2:3b       # 2GB, rapide
docker exec ollama ollama pull qwen2.5-coder:7b  # 4GB, bon pour code
docker exec ollama ollama pull deepseek-r1:7b    # 4GB, reasoning

# Alternative économique
docker exec ollama ollama pull gemma2:2b         # 1.5GB, très léger
```

### Étape 3: Configurer Backend pour Ollama

Modifie `backend/rag-compat/app/routers/bmad_chat.py`:

```python
def get_ollama_client():
    """Client Ollama local"""
    from openai import OpenAI

    ollama_url = os.getenv("OLLAMA_API_BASE_URL", "http://ollama:11434/v1")

    return OpenAI(
        api_key="ollama",  # Ollama n'a pas besoin de vraie clé
        base_url=ollama_url
    )

@router.post("/chat")
async def chat_with_agent(request: ChatRequest):
    # Choisir le provider
    use_ollama = os.getenv("USE_OLLAMA", "false").lower() == "true"

    if use_ollama:
        client = get_ollama_client()
        model = "llama3.2:3b"  # Ou autre
    else:
        client = get_deepseek_client()
        model = "deepseek-chat"

    # Appel API identique
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
```

### Étape 4: Variables d'Environnement VPS

```env
# .env sur VPS
USE_OLLAMA=true
OLLAMA_API_BASE_URL=http://ollama:11434/v1

# Backup Groq si Ollama down
GROQ_API_KEY=gsk_YOUR_GROQ_API_KEY_HERE
```

---

## 📋 Plan de Migration VPS

### Option A: 100% Gratuit avec Ollama Local

**Avantages**:
- ✅ Coût API: **$0/mois**
- ✅ Pas de rate limits
- ✅ Données privées (sur ton serveur)
- ✅ Latence basse

**Inconvénients**:
- ❌ Besoin GPU (ou CPU puissant)
- ❌ Plus lent que cloud APIs
- ❌ Maintenance serveur

**Requirements VPS**:
- 16GB RAM minimum
- 50GB disk (pour modèles)
- GPU recommandé (mais pas obligatoire)
- Docker + Docker Compose

### Option B: Hybride Ollama + Groq

**Architecture**:
```
Bolt Frontend → Groq (GRATUIT, rapide)
BMAD Agents simples → Ollama local (GRATUIT)
BMAD Agents complexes → Groq ou DeepSeek (backup)
```

**Avantages**:
- ✅ Meilleur des 2 mondes
- ✅ Fallback si Ollama down
- ✅ Coût ~$2-5/mois

---

## 🎯 Recommandation Finale

### Pour MAINTENANT (Dev local):

```yaml
Bolt.DIY:
  provider: Groq
  model: llama-3.3-70b-versatile
  cost: GRATUIT

BMAD Backend:
  provider: DeepSeek
  model: deepseek-chat
  cost: ~$5-10/mois
```

**Total mensuel**: **~$5-10** (vs $200+ avec Claude/OpenAI)

### Pour VPS (Production):

```yaml
Bolt.DIY:
  provider: Groq
  model: llama-3.3-70b-versatile
  cost: GRATUIT
  backup: Ollama local

BMAD Backend:
  provider: Ollama local
  models:
    - llama3.2:3b (conversations simples)
    - qwen2.5-coder:7b (code)
  cost: GRATUIT
  backup: DeepSeek ($5/mois)
```

**Total mensuel**: **$0-5** 🎉

---

## 📊 Comparaison Scénarios d'Usage

### Scénario 1: Utilisateur Léger (10 projets/mois)
| Solution | Coût |
|----------|------|
| Claude + OpenAI | ~$50-100 |
| Groq + DeepSeek | ~$5 |
| Groq + Ollama | **$0** ✅ |

### Scénario 2: Utilisateur Moyen (50 projets/mois)
| Solution | Coût |
|----------|------|
| Claude + OpenAI | ~$200-500 |
| Groq + DeepSeek | ~$15-25 |
| Groq + Ollama | **$0** ✅ |

### Scénario 3: Production (1000 utilisateurs/mois)
| Solution | Coût |
|----------|------|
| Claude + OpenAI | ~$10,000+ |
| Groq + DeepSeek | ~$300-500 |
| Groq + Ollama (VPS puissant) | **~$100** (coût VPS) ✅ |

---

## 🔧 Actions Immédiates

### 1. Maintenant (5 min):
```bash
# Configure Bolt pour Groq
# 1. Ouvre http://localhost:5174
# 2. Settings → Provider: Groq
# 3. Model: llama-3.3-70b-versatile
# 4. Teste un message
```

### 2. Aujourd'hui (30 min):
```bash
# Teste tous les providers disponibles
# Vérifie les rate limits et performances
```

### 3. Cette semaine (2h):
```bash
# Prépare configuration Ollama pour VPS
# Télécharge modèles optimaux
# Configure fallback Groq/DeepSeek
```

---

## 📝 Fichiers à Modifier

### 1. `backend/rag-compat/app/routers/bmad_chat.py`

Ajouter support Ollama:
```python
def get_ai_client():
    """Get AI client based on config"""
    provider = os.getenv("BMAD_PROVIDER", "deepseek")

    if provider == "ollama":
        return OpenAI(
            api_key="ollama",
            base_url=os.getenv("OLLAMA_API_BASE_URL", "http://ollama:11434/v1")
        ), "llama3.2:3b"
    elif provider == "groq":
        return OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        ), "llama-3.3-70b-versatile"
    else:  # deepseek (default)
        return get_deepseek_client(), "deepseek-chat"
```

### 2. `docker-compose.yml`

Ajouter service Ollama:
```yaml
ollama:
  image: ollama/ollama:latest
  container_name: ragdz-ollama
  volumes:
    - ollama_data:/root/.ollama
  ports:
    - "11434:11434"
  networks:
    - ragdz-network
  # Uncomment if you have GPU
  # deploy:
  #   resources:
  #     reservations:
  #       devices:
  #         - driver: nvidia
  #           count: 1
  #           capabilities: [gpu]

volumes:
  ollama_data:
```

### 3. `.env`

Ajouter configuration:
```env
# BMAD Provider Choice
BMAD_PROVIDER=deepseek  # ollama | groq | deepseek
OLLAMA_API_BASE_URL=http://ollama:11434/v1
USE_OLLAMA=false
```

---

## 🎉 Économies Réalisées

Avec configuration **Groq + DeepSeek**:
- **Claude/OpenAI**: $200-500/mois
- **Groq + DeepSeek**: $5-10/mois
- **Économie**: **~$190-490/mois** (95-98% moins cher)

Avec configuration **Groq + Ollama** sur VPS:
- **Claude/OpenAI**: $200-500/mois
- **Groq + Ollama**: $0/mois (+ $20-50 coût VPS)
- **Économie**: **~$150-450/mois** (75-90% moins cher)

---

**Auteur**: Claude Code Assistant
**Version**: 1.0
**Date**: 2025-01-20
