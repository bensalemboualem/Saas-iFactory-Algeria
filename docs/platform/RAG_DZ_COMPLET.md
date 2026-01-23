# RAG-DZ - Analyse Exhaustive Complete

> **Projet**: rag-dz
> **Localisation**: D:\IAFactory\rag-dz\
> **Date d'analyse**: 29 Decembre 2025
> **Type**: Plateforme SaaS IA Fullstack Monorepo

---

## Table des Matieres

1. [Vue d'Ensemble](#1-vue-densemble)
2. [Applications IA](#2-applications-ia)
3. [Agents IA](#3-agents-ia)
4. [Workflows](#4-workflows)
5. [Architecture RAG](#5-architecture-rag)
6. [Integrations LLM](#6-integrations-llm)
7. [Frontend](#7-frontend)
8. [Systeme Multilingue](#8-systeme-multilingue)
9. [Auth & Securite](#9-auth--securite)
10. [Bases de Donnees](#10-bases-de-donnees)
11. [Docker & Infrastructure](#11-docker--infrastructure)
12. [API Endpoints](#12-api-endpoints)

---

## 1. Vue d'Ensemble

### Description
Plateforme SaaS d'Intelligence Artificielle complete pour le marche algerien, integrant RAG (Retrieval-Augmented Generation), chatbots, generation video IA, CRM, et agents specialises.

### Statistiques
| Metrique | Valeur |
|----------|--------|
| **Applications** | 28 apps |
| **Agents IA** | 15+ agents |
| **Routers API** | 70+ endpoints |
| **Services** | 35+ services |
| **Frontends** | 4 UIs |

### Stack Technique

| Couche | Technologies |
|--------|--------------|
| **Backend** | Python 3.11+, FastAPI 0.111.0, SQLAlchemy, Pydantic |
| **Frontend** | React 18, Next.js 14, Vite 4, TypeScript 5, TailwindCSS |
| **Base de donnees** | PostgreSQL 16 (pgvector), Redis 7, Qdrant, Meilisearch |
| **IA/ML** | OpenAI, Anthropic Claude, Groq, Gemini, DeepSeek, Ollama |
| **Embeddings** | sentence-transformers, cross-encoder (reranking) |
| **Voice** | Twilio, ElevenLabs, Google TTS |
| **Video** | Replicate, Stability AI |
| **Paiements** | Chargily (Algerie) |
| **Orchestration** | Docker Compose, n8n |
| **Monitoring** | Prometheus, Grafana |

---

## 2. Applications IA

### Liste Complete des Applications

| # | Application | Chemin | Description | Stack |
|---|-------------|--------|-------------|-------|
| 1 | **api-portal** | `apps/api-portal/` | Portail developpeurs API | React |
| 2 | **bmad** | `apps/bmad/` | BMAD Method - Brainstorming & Architecture | React |
| 3 | **can2025** | `apps/can2025/` | Application CAN 2025 Algerie | React |
| 4 | **cockpit** | `apps/cockpit/` | Tableau de bord administrateur | React |
| 5 | **council** | `apps/council/` | LLM Council - Deliberation multi-IA | React |
| 6 | **crm-ia** | `apps/crm-ia/` | CRM avec assistant IA | React |
| 7 | **dev-portal** | `apps/dev-portal/` | Portail developpeurs | React |
| 8 | **dzirvideo** | `apps/dzirvideo/` | Generation video IA algerienne | React |
| 9 | **ia-agents** | `apps/ia-agents/` | Marketplace d'agents IA | React |
| 10 | **ia-chatbot** | `apps/ia-chatbot/` | Chatbot IA configurable | React |
| 11 | **ia-notebook** | `apps/ia-notebook/` | Notebook IA style NotebookLM | React |
| 12 | **ia-searcher** | `apps/ia-searcher/` | Moteur de recherche IA | React |
| 13 | **ia-voice** | `apps/ia-voice/` | Assistant vocal IA | React |
| 14 | **iafactory-landing** | `apps/iafactory-landing/` | Landing page principale | Next.js |
| 15 | **interview** | `apps/interview/` | Simulateur d'entretiens IA | React |
| 16 | **ithy** | `apps/ithy/` | Mixture of Agents (MoA) | React |
| 17 | **landing-pro** | `apps/landing-pro/` | Landing page pro | Next.js |
| 18 | **legal-assistant** | `apps/legal-assistant/` | Assistant juridique algerien | React |
| 19 | **marketing** | `apps/marketing/` | Outils marketing IA | React |
| 20 | **mcp-dashboard** | `apps/mcp-dashboard/` | Dashboard Model Context Protocol | React |
| 21 | **news** | `apps/news/` | Agregateur actualites IA | React |
| 22 | **pme-dz** | `apps/pme-dz/` | PME Copilot pour entreprises algeriennes | React |
| 23 | **prompt-creator** | `apps/prompt-creator/` | Generateur de prompts | React |
| 24 | **seo-dz-boost** | `apps/seo-dz-boost/` | SEO optimise Algerie | React |
| 25 | **shared** | `apps/shared/` | Composants partages | React |
| 26 | **sport** | `apps/sport/` | Actualites sportives IA | React |
| 27 | **video-studio** | `apps/video-studio/` | Studio video IA complet | React |
| 28 | **workflow-studio** | `apps/workflow-studio/` | Createur de workflows IA | React |

### Applications Phares

#### dzirvideo - Generation Video IA
```
Fonctionnalites:
- Generation video depuis texte
- Voix off IA (arabe, francais)
- Sous-titres automatiques
- Export multi-formats
APIs: Replicate, Stability AI, ElevenLabs
```

#### pme-dz - PME Copilot
```
Fonctionnalites:
- Analyse financiere PME
- Generation rapports
- Previsions IA
- Assistant comptable
APIs: OpenAI, Anthropic
```

#### legal-assistant - Assistant Juridique
```
Fonctionnalites:
- RAG sur code algerien
- Recherche jurisprudence
- Redaction documents
- Conseil juridique IA
```

---

## 3. Agents IA

### Liste Complete des Agents

| # | Agent | Chemin | Role | LLM |
|---|-------|--------|------|-----|
| 1 | **base_agent** | `agents/core/` | Agent de base abstrait | - |
| 2 | **ai_consultant** | `agents/business/consultant/` | Consultant business IA | OpenAI/Anthropic |
| 3 | **data_analyst** | `agents/business/data-analysis/` | Analyste de donnees | OpenAI |
| 4 | **customer_support** | `agents/business/customer-support/` | Support client IA | OpenAI |
| 5 | **financial_coach** | `agents/finance/` | Coach financier | OpenAI/Anthropic |
| 6 | **legal_team** | `agents/legal/` | Equipe juridique IA | Anthropic |
| 7 | **recruitment_team** | `agents/recruitment/` | Equipe recrutement | OpenAI |
| 8 | **real_estate_team** | `agents/real_estate/` | Equipe immobilier | OpenAI |
| 9 | **travel_agent** | `agents/travel/` | Agent de voyage | OpenAI |
| 10 | **teaching_team** | `agents/teaching/` | Equipe enseignement | OpenAI/Anthropic |
| 11 | **local_rag** | `agents/rag/local-rag/` | RAG local | Ollama |
| 12 | **chat_pdf** | `agents/rag/chat-pdf/` | Chat avec PDF | OpenAI |
| 13 | **video_operator** | `agents/video-operator/` | Operateur video IA | Replicate |
| 14 | **discovery_dz** | `agents/discovery-dz/` | Decouverte Algerie | OpenAI |
| 15 | **recruteur_dz** | `agents/recruteur-dz/` | Recruteur algerien | OpenAI |
| 16 | **ux_research** | `agents/ux-research/` | Recherche UX | OpenAI |

### Agents Specialises Backend

| Agent | Fichier | Description |
|-------|---------|-------------|
| **POLVA SuperAgent** | `services/super_agent_polva.py` | Super-agent orchestrateur |
| **Voice AI Agent** | `services/voice_ai_agent.py` | Agent vocal avance |
| **Workflow Orchestrator** | `services/workflow_orchestrator.py` | Orchestration workflows |
| **Conversational Orchestrator** | `services/conversational_orchestrator.py` | Conversations multi-tours |
| **BMAD Orchestrator** | `services/bmad_orchestrator.py` | Orchestration BMAD |
| **Bolt Orchestration** | `services/bolt_orchestration_service.py` | Integration Bolt.diy |

### Structure d'un Agent Type

```python
# agents/business/consultant/ai_consultant_agent.py
class AIConsultantAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-turbo")
        self.system_prompt = """
        Tu es un consultant IA expert...
        """

    async def analyze(self, query: str) -> str:
        # Logique d'analyse
        pass

    async def recommend(self, context: dict) -> list:
        # Recommendations
        pass
```

---

## 4. Workflows

### Workflows n8n

**Localisation**: `workflows/`

| Workflow | Description |
|----------|-------------|
| **sales/** | Workflows vente automatises |
| **delivery/** | Workflows livraison |

### Workflows Backend

| Service | Fichier | Description |
|---------|---------|-------------|
| **Workflow Orchestrator** | `workflow_orchestrator.py` | Orchestration principale |
| **Workflow State** | `workflow_state.py` | Gestion d'etat |
| **Bolt Workflow** | `bolt_workflow_service.py` | Integration Bolt |
| **Project Coordinator** | `project_coordinator.py` | Coordination projets |

### Pipeline de Workflow Type

```
1. ENTREE
   ├── Requete utilisateur
   └── Contexte session

2. PREPROCESSING
   ├── Tokenization
   ├── Detection intention
   └── Extraction entites

3. ROUTING
   ├── Selection agent
   ├── Selection LLM
   └── Allocation ressources

4. EXECUTION
   ├── RAG retrieval
   ├── Generation LLM
   └── Post-processing

5. SORTIE
   ├── Response formatee
   ├── Citations
   └── Actions suggerees
```

---

## 5. Architecture RAG

### Pipeline RAG Complete

```
┌─────────────────────────────────────────────────────────────┐
│                    INGESTION PIPELINE                        │
├─────────────────────────────────────────────────────────────┤
│  Documents → Chunking → Embeddings → Vector Store (Qdrant)  │
│                                                              │
│  Formats: PDF, DOCX, TXT, MD, HTML                          │
│  Chunking: 512 tokens, overlap 50                           │
│  Embeddings: paraphrase-multilingual-mpnet-base-v2          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    RETRIEVAL PIPELINE                        │
├─────────────────────────────────────────────────────────────┤
│  Query → Embedding → Vector Search → Reranking → Top-K      │
│                                                              │
│  Vector DB: Qdrant + PGVector (hybrid)                      │
│  Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2            │
│  Top-K: 10 documents                                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   GENERATION PIPELINE                        │
├─────────────────────────────────────────────────────────────┤
│  Context + Query → Prompt → LLM → Response + Citations      │
│                                                              │
│  LLM: Claude-3.5-Sonnet / GPT-4-Turbo / Llama-70B          │
│  Context Window: 128K tokens                                │
│  Citations: Source + Page + Confidence                      │
└─────────────────────────────────────────────────────────────┘
```

### Modules RAG

| Module | Fichier | Fonction |
|--------|---------|----------|
| **BigRAG Router** | `bigrag/bigrag_router.py` | RAG multi-pays |
| **Ingest Router** | `bigrag_ingest/ingest_router.py` | Ingestion documents |
| **Advanced RAG** | `services/advanced_rag.py` | RAG avance |
| **Context Optimizer** | `services/context_optimizer.py` | Optimisation contexte |
| **Reranker** | `services/reranker.py` | Reranking resultats |

### Configuration RAG

```python
# config.py
embedding_model = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
embedding_device = "cpu"  # ou "cuda"
embedding_batch_size = 32

use_reranking = True
reranking_model = "cross-encoder/ms-marco-MiniLM-L-6-v2"
reranking_top_k = 10

use_pgvector = True  # Hybrid search
```

---

## 6. Integrations LLM

### Providers Supportes

| Provider | Modeles | Usage | API Key Env |
|----------|---------|-------|-------------|
| **OpenAI** | GPT-4-Turbo, GPT-3.5-Turbo | Chat, Embeddings | `OPENAI_API_KEY` |
| **Anthropic** | Claude-3.5-Sonnet, Claude-3-Opus | Chat, Analysis | `ANTHROPIC_API_KEY` |
| **Groq** | Llama-3.3-70B, Mixtral | Fast inference | `GROQ_API_KEY` |
| **Google** | Gemini Pro, Gemini Flash | Multimodal | `GOOGLE_GENERATIVE_AI_API_KEY` |
| **Mistral** | Mistral Large, Codestral | Code, Chat | `MISTRAL_API_KEY` |
| **DeepSeek** | DeepSeek-V3, DeepSeek-Coder | Economique | `DEEPSEEK_API_KEY` |
| **Ollama** | Llama, Mistral local | Local/Souverain | `OLLAMA_BASE_URL` |
| **OpenRouter** | Multi-providers | Fallback | `OPEN_ROUTER_API_KEY` |
| **Cohere** | Command-R+ | Reranking | `COHERE_API_KEY` |
| **Together** | Various OSS | Economique | `TOGETHER_API_KEY` |

### Multi-LLM Router

```python
# multi_llm/multi_llm_router.py
class MultiLLMRouter:
    providers = {
        "openai": OpenAIProvider(),
        "anthropic": AnthropicProvider(),
        "groq": GroqProvider(),
        "gemini": GeminiProvider(),
        "ollama": OllamaProvider(),
    }

    async def route(self, query: str, preference: str = "auto"):
        # Selection automatique basee sur:
        # - Type de tache
        # - Latence requise
        # - Cout
        # - Disponibilite
```

### LLM Council (Deliberation Multi-IA)

```python
# routers/council.py
# Permet de consulter plusieurs LLM simultanement
# pour des decisions plus robustes

council_members = [
    {"provider": "anthropic", "model": "claude-3.5-sonnet"},
    {"provider": "openai", "model": "gpt-4-turbo"},
    {"provider": "gemini", "model": "gemini-pro"},
]

# Le "chairman" synthetise les reponses
chairman = "claude"
```

---

## 7. Frontend

### Applications Frontend

| App | Chemin | Framework | Port | Description |
|-----|--------|-----------|------|-------------|
| **ia-factory-ui** | `frontend/ia-factory-ui/` | Next.js 14 | 3000 | UI principale |
| **rag-ui** | `frontend/rag-ui/` | React + Vite | 5173 | Interface RAG |
| **archon-ui** | `frontend/archon-ui/` | React + Vite | 5174 | Interface Archon |
| **video-studio** | `frontend/video-studio/` | React + Vite | 3050 | Studio video |

### ia-factory-ui (Next.js 14)

**Dependencies principales**:
```json
{
  "next": "^14.1.0",
  "react": "^18.2.0",
  "next-intl": "^4.6.1",      // i18n
  "zustand": "^4.5.0",         // State management
  "framer-motion": "^11.0.3",  // Animations
  "recharts": "^2.12.0",       // Charts
  "lucide-react": "^0.323.0",  // Icons
  "tailwindcss": "^3.4.1"      // Styling
}
```

**Structure**:
```
ia-factory-ui/
├── src/
│   ├── app/                   # App Router (Next.js 14)
│   │   ├── [locale]/         # Routes i18n
│   │   ├── api/              # API Routes
│   │   └── layout.tsx
│   ├── components/           # Composants React
│   │   ├── ui/              # Composants UI (Radix)
│   │   ├── chat/            # Composants chat
│   │   └── dashboard/       # Composants dashboard
│   ├── lib/                  # Utilitaires
│   ├── store/               # Zustand stores
│   └── messages/            # Traductions i18n
```

### rag-ui (React + Vite)

**Dependencies principales**:
```json
{
  "react": "^18.2.0",
  "react-router-dom": "^6.8.1",
  "@tanstack/react-query": "^5.89.0",  // Data fetching
  "axios": "^1.6.0",
  "framer-motion": "^12.23.14",
  "react-dnd": "^16.0.1",              // Drag & drop
  "zod": "^4.1.9"                       // Validation
}
```

**Pages principales**:
- `/` - Dashboard
- `/chat` - Interface chat RAG
- `/knowledge` - Base de connaissances
- `/settings` - Configuration
- `/mcp` - Dashboard MCP

---

## 8. Systeme Multilingue

### Langues Supportees

| Langue | Code | Direction | Couverture |
|--------|------|-----------|------------|
| Francais | `fr` | LTR | 100% |
| Arabe | `ar` | RTL | 100% |
| Anglais | `en` | LTR | 100% |
| Darija (Algerien) | `dz` | RTL | Partiel |

### Implementation i18n

**Frontend (next-intl)**:
```typescript
// messages/fr.json
{
  "common": {
    "welcome": "Bienvenue sur IA Factory",
    "search": "Rechercher...",
    "submit": "Envoyer"
  },
  "chat": {
    "placeholder": "Posez votre question...",
    "thinking": "Reflexion en cours..."
  }
}
```

### Module Darija (NLP Algerien)

```python
# darija/darija_router.py
# Support du dialecte algerien (Darija)

@router.post("/translate")
async def translate_darija(text: str, target: str = "fr"):
    """Traduit depuis/vers le darija algerien"""
    pass

@router.post("/detect")
async def detect_dialect(text: str):
    """Detecte si le texte est en darija"""
    pass
```

---

## 9. Auth & Securite

### Systeme d'Authentification

| Composant | Implementation |
|-----------|----------------|
| **JWT Tokens** | python-jose, access + refresh |
| **Password Hashing** | passlib (bcrypt) |
| **API Keys** | SHA256 hash |
| **Rate Limiting** | Redis-based |

### Middleware Securite

```python
# main.py
app.add_middleware(RateLimitMiddleware)
# app.add_middleware(EnhancedAuthMiddleware)  # Desactive temporairement
app.add_middleware(TenantContextMiddleware)
app.add_middleware(RequestIDMiddleware)
```

### Rate Limiting

```python
# config.py
rate_limit_per_minute = 60
rate_limit_per_hour = 1000
rate_limit_burst = 10
enable_rate_limiting = True
```

### Endpoints Auth

| Endpoint | Methode | Description |
|----------|---------|-------------|
| `/auth/register` | POST | Inscription |
| `/auth/login` | POST | Connexion |
| `/auth/refresh` | POST | Refresh token |
| `/auth/logout` | POST | Deconnexion |
| `/auth/me` | GET | Profil utilisateur |

---

## 10. Bases de Donnees

### PostgreSQL (Principal)

**Configuration**:
```python
postgres_url = "postgresql://user:pass@iaf-postgres:5432/iafactory"
postgres_db = "iafactory_dz"
```

**Extensions**:
- `pgvector` - Recherche vectorielle
- `uuid-ossp` - Generation UUID

**Modeles Principaux**:

| Modele | Fichier | Description |
|--------|---------|-------------|
| `User` | `models/user.py` | Utilisateurs |
| `UserKey` | `models/user_key.py` | Cles API utilisateurs |
| `BillingModels` | `models/billing_models.py` | Facturation |
| `PMEModels` | `models/pme_models.py` | Donnees PME |
| `CRMProModels` | `models/crm_pro_models.py` | CRM avance |
| `BoltWorkflow` | `models/bolt_workflow.py` | Workflows Bolt |
| `Citation` | `models/citation.py` | Citations RAG |

### Qdrant (Vector DB)

**Configuration**:
```python
qdrant_host = "iaf-qdrant"
qdrant_port = 6333
```

**Collections**:
- `iafactory_documents` - Documents RAG
- `iafactory_embeddings` - Embeddings
- `user_knowledge_bases` - Bases par utilisateur

### Redis (Cache)

**Configuration**:
```python
redis_url = "redis://iaf-redis:6379/0"
```

**Usages**:
- Session cache
- Rate limiting counters
- Temporary data
- Pub/Sub messaging

### Meilisearch (Full-text)

**Configuration**:
```python
meili_url = "http://meilisearch:7700"
```

**Indexes**:
- Documents full-text
- Recherche hybride (vector + keyword)

---

## 11. Docker & Infrastructure

### Services Docker

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `iaf-postgres` | pgvector/pgvector:pg16 | 5432 | Base PostgreSQL |
| `iaf-redis` | redis:7-alpine | 6379 | Cache Redis |
| `iaf-qdrant` | qdrant/qdrant | 6333, 6334 | Vector DB |
| `iaf-backend` | custom FastAPI | 8000 | API Backend |
| `iaf-frontend` | custom Next.js | 3000 | Frontend principal |
| `iaf-rag-ui` | custom Vite | 5173 | UI RAG |
| `iaf-n8n` | n8n | 5678 | Workflow automation |
| `iaf-anythingllm` | AnythingLLM | 3001 | LLM interface |
| `iaf-ollama` | ollama | 11434 | LLM local |
| `iaf-adminer` | adminer | 8080 | DB admin |
| `iaf-prometheus` | prometheus | 9090 | Metrics |
| `iaf-grafana` | grafana | 3002 | Dashboards |
| `iaf-flowise` | flowise | 3004 | Flow builder |
| `iaf-firecrawl` | firecrawl | 3005 | Web scraper |

### Volumes Docker

```yaml
volumes:
  postgres-data:
  redis-data:
  qdrant-data:
  anythingllm-data:
  ollama-data:
  backend-cache:
  n8n-data:
  prometheus-data:
  grafana-data:
  flowise-data:
```

### Networks

```yaml
networks:
  iafactory-network:
    driver: bridge
```

### Profiles Docker

| Profile | Services Actives |
|---------|-----------------|
| `default` | Core services |
| `ai-local` | + Ollama |
| `full` | + rag-ui |
| `video` | + video-studio |
| `agents` | + Streamlit agents |
| `monitoring` | + Prometheus, Grafana |
| `extras` | + Flowise, Firecrawl |

---

## 12. API Endpoints

### Vue d'Ensemble (70+ Routers)

```python
# Routers inclus dans main.py
# Groupes par categorie

# CORE
- auth.router              # Authentification
- test.router              # Tests
- upload.router            # Upload fichiers
- query.router             # Requetes RAG

# RAG
- knowledge.router         # Base de connaissances
- bigrag_router            # BigRAG multi-pays
- ingest_router            # Ingestion documents
- rag_public.router        # RAG API publique

# AGENTS
- agents.router            # Gestion agents
- agent_chat.router        # Chat avec agents
- orchestrator.router      # Orchestration
- coordination.router      # Coordination

# BMAD
- bmad.router              # BMAD core
- bmad_chat.router         # BMAD chat
- bmad_openai.router       # BMAD OpenAI
- bmad_orchestration.router# BMAD orchestration

# BOLT
- bolt.router              # Bolt SuperPower
- bolt_auth.router         # Bolt Auth
- workflow.router          # Workflows

# VOICE
- voice.router             # Voice agent
- voice_ai.router          # Voice AI advanced
- stt_router               # Speech-to-Text
- tts_router               # Text-to-Speech

# COMMUNICATION
- twilio.router            # Twilio SMS
- whatsapp.router          # WhatsApp
- email_agent.router       # Email agent

# BUSINESS
- crm.router               # CRM basic
- crm_pro.router           # CRM PRO
- pme.router               # PME basic
- pme_v2.router            # PME PRO V2
- billing.router           # Facturation
- billing_v2.router        # Facturation V2
- payment.router           # Paiements Chargily
- credits.router           # Systeme credits

# INTEGRATIONS
- google.router            # Google Calendar/Gmail
- calendar.router          # Calendrier
- credentials.router       # Credentials management

# AI SPECIAL
- council.router           # LLM Council
- council_custom.router    # Council custom
- ithy.router              # Mixture of Agents
- multi_llm_router         # Multi-LLM
- streaming.router         # LLM Streaming
- polva.router             # POLVA SuperAgent

# VIDEO
- studio_video.router      # Studio video
- dzirvideo.router         # Dzir IA Video

# SPECIALIZED
- ocr_router               # OCR multilingue
- darija_router            # Darija NLP
- notebook_lm.router       # Notebook LM
- prompt_creator.router    # Prompt creator
- growth_grid.router       # Growth Grid
- legal_search.router      # Recherche juridique

# MCP
- mcp.router               # MCP core
- mcp_health.router        # MCP health
- mcp_metrics.router       # MCP metrics

# ADMIN
- admin_dashboard.router   # Dashboard admin
- tenants.router           # Multi-tenant
- team_seats_router        # Team seats
- promo_codes.router       # Codes promo
- catalog.router           # Catalogue apps
- analytics.router         # Analytics
- quota.router             # Quotas
```

### Endpoints Principaux

#### Auth
| Endpoint | Methode | Description |
|----------|---------|-------------|
| `POST /auth/register` | Inscription utilisateur |
| `POST /auth/login` | Connexion |
| `POST /auth/refresh` | Refresh token |
| `GET /auth/me` | Profil utilisateur |

#### RAG
| Endpoint | Methode | Description |
|----------|---------|-------------|
| `POST /api/query` | Requete RAG |
| `POST /api/upload` | Upload document |
| `GET /knowledge/bases` | Liste bases |
| `POST /knowledge/search` | Recherche |

#### Chat
| Endpoint | Methode | Description |
|----------|---------|-------------|
| `POST /chat/send` | Envoyer message |
| `GET /chat/history` | Historique |
| `WS /ws/chat` | WebSocket chat |

#### Voice
| Endpoint | Methode | Description |
|----------|---------|-------------|
| `POST /voice/stt` | Speech-to-Text |
| `POST /voice/tts` | Text-to-Speech |
| `POST /voice/call` | Initier appel |

#### Billing
| Endpoint | Methode | Description |
|----------|---------|-------------|
| `POST /payment/checkout` | Initier paiement |
| `POST /payment/webhook` | Webhook Chargily |
| `GET /credits/balance` | Solde credits |

---

## Resume Executif

### Points Forts

1. **Architecture Modulaire** - 28 apps independantes
2. **Multi-LLM** - 10+ providers supportes
3. **RAG Avance** - Hybrid search + reranking
4. **Localisation** - Francais, Arabe, Darija
5. **Souverainete** - Ollama pour LLM local
6. **Paiements** - Chargily integre (Algerie)

### A Ameliorer

1. Auth middleware desactive temporairement
2. Tests unitaires a completer
3. Documentation API a finaliser
4. Monitoring a deployer

### Metriques Cles

```
Code Backend:    ~50,000 lignes Python
Code Frontend:   ~30,000 lignes TypeScript
Routers API:     70+
Services:        35+
Agents IA:       15+
Applications:    28
```

---

*Document genere par Claude Code - Analyse PROMPT 2*
*Date: 29 Decembre 2025*
