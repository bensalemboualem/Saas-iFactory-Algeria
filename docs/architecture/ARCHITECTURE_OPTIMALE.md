# Architecture Optimale - IAFactory Multi-Region

> **Objectif**: Partager le code entre rag-dz (Algerie) et Helvetia (Suisse)
> **Date**: 29 Decembre 2025
> **Base**: RAG_DZ_COMPLET.md (28 apps, 15 agents, 70+ endpoints)

---

## Table des Matieres

1. [Contraintes & Exigences](#1-contraintes--exigences)
2. [Option A: Monorepo](#2-option-a-monorepo)
3. [Option B: Package Partage](#3-option-b-package-partage)
4. [Comparaison Detaillee](#4-comparaison-detaillee)
5. [Recommandation Finale](#5-recommandation-finale)
6. [Structure Proposee](#6-structure-proposee)
7. [Configuration par Environnement](#7-configuration-par-environnement)
8. [Commandes Deploiement](#8-commandes-deploiement)
9. [Plan de Migration](#9-plan-de-migration)

---

## 1. Contraintes & Exigences

### Contraintes Techniques

| Contrainte | Description |
|------------|-------------|
| **Code IDENTIQUE** | Les 28 apps, 15 agents et workflows DOIVENT etre partages |
| **Deploiement SEPARE** | 2 VPS independants (Alger + Geneve) |
| **Config DIFFERENTE** | Langues, env vars, API keys, domaines |
| **Souverainete donnees** | Donnees DZ restent en Algerie, CH restent en Suisse |

### Differences par Region

| Aspect | Algerie (rag-dz) | Suisse (Helvetia) |
|--------|------------------|-------------------|
| **Domaine** | iafactory-algeria.com | iafactory.ch |
| **VPS** | Alger (Icosnet/OVH) | Geneve (Infomaniak) |
| **Langues UI** | FR, AR, EN, Darija | FR, DE, IT, EN |
| **Paiements** | Chargily (DZD) | Stripe (CHF/EUR) |
| **LLM Local** | Ollama (souverain) | Ollama (souverain) |
| **Timezone** | Africa/Algiers | Europe/Zurich |
| **Legal** | Code Commerce DZ | Code des Obligations CH |

### Ce qui est PARTAGE (IDENTIQUE)

```
PARTAGE (100% identique):
├── 28 Applications IA
│   ├── api-portal, bmad, can2025, cockpit, council...
│   ├── crm-ia, dev-portal, dzirvideo, ia-agents...
│   ├── ia-chatbot, ia-notebook, ia-searcher, ia-voice...
│   ├── legal-assistant, marketing, mcp-dashboard...
│   ├── pme-dz, prompt-creator, seo-dz-boost...
│   └── video-studio, workflow-studio
├── 15+ Agents IA
│   ├── consultant, data-analyst, customer-support
│   ├── financial-coach, legal-team, recruitment-team
│   ├── real-estate, travel, teaching, local-rag
│   ├── chat-pdf, video-operator, discovery
│   └── POLVA, Voice AI, Workflow Orchestrator
├── 70+ API Endpoints
├── Architecture RAG
├── Multi-LLM Router
└── Frontend Components
```

### Ce qui est DIFFERENT (par region)

```
DIFFERENT (specifique region):
├── .env (variables d'environnement)
├── docker-compose.yml (ports, volumes)
├── nginx.conf (domaines, SSL)
├── messages/ (traductions i18n)
├── legal/ (documents juridiques)
├── payment/ (provider: Chargily vs Stripe)
└── branding/ (logos, couleurs)
```

---

## 2. Option A: Monorepo

### Description

Un seul repository contenant tout le code avec des dossiers de deploiement separes.

### Structure

```
iafactory-platform/
│
├── core/                          # CODE PARTAGE (identique)
│   ├── apps/                      # 28 applications
│   │   ├── api-portal/
│   │   ├── bmad/
│   │   ├── crm-ia/
│   │   ├── dzirvideo/
│   │   ├── ia-chatbot/
│   │   ├── legal-assistant/
│   │   ├── pme/                   # Renomme de pme-dz
│   │   ├── video-studio/
│   │   └── ... (28 apps)
│   │
│   ├── agents/                    # 15+ agents
│   │   ├── business/
│   │   ├── finance/
│   │   ├── legal/
│   │   ├── rag/
│   │   └── ... (15 agents)
│   │
│   ├── services/                  # Backend API
│   │   └── api/
│   │       ├── app/
│   │       │   ├── routers/       # 70+ routers
│   │       │   ├── services/      # 35+ services
│   │       │   ├── models/
│   │       │   ├── bigrag/
│   │       │   ├── multi_llm/
│   │       │   └── ...
│   │       ├── requirements.txt
│   │       └── Dockerfile
│   │
│   ├── frontend/                  # 4 frontends
│   │   ├── main-ui/              # Renomme de ia-factory-ui
│   │   ├── rag-ui/
│   │   ├── archon-ui/
│   │   └── video-studio/
│   │
│   ├── workflows/                 # n8n workflows
│   └── infrastructure/            # SQL, configs partagees
│
├── deployments/                   # CONFIGS SPECIFIQUES
│   │
│   ├── algeria/                   # Config Algerie
│   │   ├── .env                   # Variables DZ
│   │   ├── .env.production
│   │   ├── docker-compose.yml     # Stack DZ
│   │   ├── docker-compose.prod.yml
│   │   ├── nginx/
│   │   │   └── nginx.conf         # iafactory-algeria.com
│   │   ├── messages/              # i18n (fr, ar, en, darija)
│   │   │   ├── fr.json
│   │   │   ├── ar.json
│   │   │   ├── en.json
│   │   │   └── dz.json            # Darija
│   │   ├── legal/                 # Documents juridiques DZ
│   │   ├── branding/              # Logos, assets DZ
│   │   └── scripts/
│   │       ├── deploy.sh
│   │       ├── backup.sh
│   │       └── restore.sh
│   │
│   └── switzerland/               # Config Suisse
│       ├── .env                   # Variables CH
│       ├── .env.production
│       ├── docker-compose.yml     # Stack CH
│       ├── docker-compose.prod.yml
│       ├── nginx/
│       │   └── nginx.conf         # iafactory.ch
│       ├── messages/              # i18n (fr, de, it, en)
│       │   ├── fr.json
│       │   ├── de.json
│       │   ├── it.json
│       │   └── en.json
│       ├── legal/                 # Documents juridiques CH
│       ├── branding/              # Logos, assets CH
│       └── scripts/
│           ├── deploy.sh
│           ├── backup.sh
│           └── restore.sh
│
├── shared/                        # Utilitaires partages
│   ├── scripts/
│   │   ├── setup.sh              # Setup initial
│   │   ├── test.sh               # Tests
│   │   └── lint.sh               # Linting
│   └── templates/
│       ├── env.template          # Template .env
│       └── docker-compose.template.yml
│
├── docs/                          # Documentation
│   ├── architecture.md
│   ├── deployment.md
│   ├── contributing.md
│   └── api/
│
├── package.json                   # Workspace root
├── pnpm-workspace.yaml           # pnpm workspaces
├── turbo.json                    # Turborepo config
└── README.md
```

### Avantages Monorepo

| Avantage | Description |
|----------|-------------|
| **Simplicite** | Un seul repo a gerer |
| **Coherence** | Code toujours synchronise |
| **Refactoring** | Facile de modifier partout |
| **CI/CD** | Un seul pipeline |
| **Dependencies** | Partagees (pnpm workspaces) |

### Inconvenients Monorepo

| Inconvenient | Description |
|--------------|-------------|
| **Taille** | Repo volumineux |
| **Clonage** | Long sur connexion lente |
| **Permissions** | Tout ou rien |
| **Complexite CI** | Build complet a chaque push |

---

## 3. Option B: Package Partage

### Description

Le code core est publie comme package npm/pip, importe dans 2 repos separes.

### Structure

```
REPOSITORY 1: @iafactory/core (npm) + iafactory-core (pip)
─────────────────────────────────────────────────────────
iafactory-core/
├── packages/
│   ├── apps/                      # 28 applications
│   │   ├── package.json
│   │   └── src/
│   ├── agents/                    # 15+ agents
│   │   ├── setup.py
│   │   └── src/
│   ├── api/                       # Backend API
│   │   ├── setup.py
│   │   └── src/
│   ├── frontend-components/       # Composants React
│   │   ├── package.json
│   │   └── src/
│   └── workflows/                 # Workflows
│       └── src/
├── package.json
├── setup.py
├── pyproject.toml
└── README.md

PUBLICATION:
- npm: @iafactory/apps, @iafactory/components
- pip: iafactory-core, iafactory-agents, iafactory-api


REPOSITORY 2: rag-dz (Algerie)
──────────────────────────────
rag-dz/
├── package.json                   # Import @iafactory/*
├── requirements.txt               # Import iafactory-*
├── .env
├── .env.production
├── docker-compose.yml
├── nginx/
├── messages/                      # i18n DZ
├── legal/
├── branding/
├── scripts/
└── README.md


REPOSITORY 3: helvetia (Suisse)
────────────────────────────────
helvetia/
├── package.json                   # Import @iafactory/*
├── requirements.txt               # Import iafactory-*
├── .env
├── .env.production
├── docker-compose.yml
├── nginx/
├── messages/                      # i18n CH
├── legal/
├── branding/
├── scripts/
└── README.md
```

### Avantages Package

| Avantage | Description |
|----------|-------------|
| **Separation** | Repos independants |
| **Versioning** | Versions semantiques |
| **Permissions** | Acces granulaire |
| **Legers** | Repos deployment legers |

### Inconvenients Package

| Inconvenient | Description |
|--------------|-------------|
| **Complexite** | 3 repos a gerer |
| **Synchronisation** | Versions a maintenir |
| **Publication** | Pipeline npm/pip |
| **Debugging** | Plus difficile |
| **Dev local** | npm link / pip -e |

---

## 4. Comparaison Detaillee

### Tableau Comparatif

| Critere | Monorepo | Package | Gagnant |
|---------|----------|---------|---------|
| **Simplicite setup** | Simple | Complexe | Monorepo |
| **Synchronisation code** | Automatique | Manuelle (versions) | Monorepo |
| **Temps CI/CD** | Long (tout rebuild) | Court (incremental) | Package |
| **Taille clone** | ~500 MB | ~50 MB chacun | Package |
| **Dev local** | Immediat | npm link requis | Monorepo |
| **Permissions** | Tout ou rien | Granulaire | Package |
| **Versioning** | Git tags | Semver | Package |
| **Debugging** | Facile | Difficile | Monorepo |
| **Scaling equipe** | Moyen | Bon | Package |
| **Open source** | Un seul repo | Core separable | Package |

### Score

| Option | Score /10 | Commentaire |
|--------|-----------|-------------|
| **Monorepo** | 8/10 | Ideal pour equipe reduite, iteration rapide |
| **Package** | 6/10 | Bon pour grande equipe, mais complexe |

---

## 5. Recommandation Finale

### RECOMMANDATION: Option A - Monorepo

**Pourquoi ?**

1. **Equipe reduite** - Vous etes probablement 1-5 developpeurs
2. **Iteration rapide** - Modifications instantanees partout
3. **Coherence garantie** - Pas de desync entre regions
4. **Setup simple** - Un clone, tout fonctionne
5. **Debug facile** - Tout le code accessible

### Architecture Recommandee

```
┌─────────────────────────────────────────────────────────────┐
│                    MONOREPO IAFACTORY                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                    core/                             │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │    │
│  │  │  apps/  │ │ agents/ │ │services/│ │frontend/│   │    │
│  │  │   28    │ │   15+   │ │   api   │ │    4    │   │    │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘   │    │
│  │                    CODE PARTAGE                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                  │
│            ┌──────────────┴──────────────┐                  │
│            │                             │                  │
│  ┌─────────▼─────────┐     ┌─────────────▼─────────┐       │
│  │ deployments/      │     │ deployments/          │       │
│  │ algeria/          │     │ switzerland/          │       │
│  │                   │     │                       │       │
│  │ ├── .env         │     │ ├── .env              │       │
│  │ ├── docker-compose│     │ ├── docker-compose    │       │
│  │ ├── nginx/       │     │ ├── nginx/            │       │
│  │ ├── messages/    │     │ ├── messages/         │       │
│  │ │   ├── fr.json  │     │ │   ├── fr.json       │       │
│  │ │   ├── ar.json  │     │ │   ├── de.json       │       │
│  │ │   └── dz.json  │     │ │   └── it.json       │       │
│  │ ├── legal/       │     │ ├── legal/            │       │
│  │ └── branding/    │     │ └── branding/         │       │
│  │                   │     │                       │       │
│  │  VPS ALGER       │     │  VPS GENEVE           │       │
│  │  iafactory-      │     │  iafactory.ch         │       │
│  │  algeria.com     │     │                       │       │
│  └───────────────────┘     └───────────────────────┘       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Structure Proposee

### Arborescence Complete

```
iafactory-platform/
│
├── core/                                    # CODE PARTAGE
│   │
│   ├── apps/                               # 28 Applications
│   │   ├── api-portal/
│   │   │   ├── src/
│   │   │   ├── package.json
│   │   │   └── README.md
│   │   ├── bmad/
│   │   ├── cockpit/
│   │   ├── council/
│   │   ├── crm/                            # Renomme de crm-ia
│   │   ├── dev-portal/
│   │   ├── video-gen/                      # Renomme de dzirvideo
│   │   ├── agents-marketplace/             # Renomme de ia-agents
│   │   ├── chatbot/                        # Renomme de ia-chatbot
│   │   ├── notebook/                       # Renomme de ia-notebook
│   │   ├── searcher/                       # Renomme de ia-searcher
│   │   ├── voice/                          # Renomme de ia-voice
│   │   ├── landing/                        # Renomme de iafactory-landing
│   │   ├── interview/
│   │   ├── ithy/
│   │   ├── landing-pro/
│   │   ├── legal-assistant/
│   │   ├── marketing/
│   │   ├── mcp-dashboard/
│   │   ├── news/
│   │   ├── pme/                            # Renomme de pme-dz
│   │   ├── prompt-creator/
│   │   ├── seo-boost/                      # Renomme de seo-dz-boost
│   │   ├── shared/
│   │   ├── sport/
│   │   ├── video-studio/
│   │   ├── workflow-studio/
│   │   └── can2025/                        # App specifique (a evaluer)
│   │
│   ├── agents/                             # 15+ Agents IA
│   │   ├── core/
│   │   │   ├── base_agent.py
│   │   │   └── __init__.py
│   │   ├── business/
│   │   │   ├── consultant/
│   │   │   ├── data-analysis/
│   │   │   └── customer-support/
│   │   ├── finance/
│   │   │   └── financial_coach.py
│   │   ├── legal/
│   │   │   └── legal_team.py
│   │   ├── recruitment/
│   │   ├── real_estate/
│   │   ├── travel/
│   │   ├── teaching/
│   │   ├── rag/
│   │   │   ├── local-rag/
│   │   │   ├── chat-pdf/
│   │   │   └── hybrid-search/
│   │   ├── video-operator/
│   │   ├── discovery/                      # Renomme de discovery-dz
│   │   ├── recruiter/                      # Renomme de recruteur-dz
│   │   ├── ux-research/
│   │   └── templates/
│   │
│   ├── services/                           # Backend API
│   │   └── api/
│   │       ├── app/
│   │       │   ├── main.py
│   │       │   ├── config.py
│   │       │   ├── routers/               # 70+ routers
│   │       │   ├── services/              # 35+ services
│   │       │   ├── models/
│   │       │   ├── bigrag/
│   │       │   ├── bigrag_ingest/
│   │       │   ├── multi_llm/
│   │       │   ├── ocr/
│   │       │   ├── darija/                # NLP dialectes
│   │       │   ├── voice/
│   │       │   ├── mcp/
│   │       │   └── team_seats/
│   │       ├── requirements.txt
│   │       ├── Dockerfile
│   │       └── alembic/
│   │
│   ├── frontend/                           # 4 Frontends
│   │   ├── main-ui/                       # Next.js principal
│   │   │   ├── src/
│   │   │   │   ├── app/
│   │   │   │   ├── components/
│   │   │   │   └── lib/
│   │   │   ├── public/
│   │   │   ├── package.json
│   │   │   └── next.config.js
│   │   ├── rag-ui/                        # React + Vite
│   │   ├── archon-ui/
│   │   └── video-studio/
│   │
│   ├── workflows/                          # n8n Workflows
│   │   ├── sales/
│   │   ├── delivery/
│   │   └── templates/
│   │
│   └── infrastructure/                     # Configs partagees
│       ├── sql/
│       │   ├── init.sql
│       │   └── pgvector_migration.sql
│       └── observability/
│           └── prometheus.yml
│
├── deployments/                            # CONFIGS PAR REGION
│   │
│   ├── algeria/                           # ALGERIE
│   │   ├── .env.example
│   │   ├── .env.production.example
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.prod.yml
│   │   ├── nginx/
│   │   │   ├── nginx.conf
│   │   │   └── ssl/
│   │   ├── messages/
│   │   │   ├── fr.json
│   │   │   ├── ar.json
│   │   │   ├── en.json
│   │   │   └── dz.json
│   │   ├── legal/
│   │   │   ├── cgu.md
│   │   │   ├── privacy.md
│   │   │   └── mentions-legales.md
│   │   ├── branding/
│   │   │   ├── logo.svg
│   │   │   ├── favicon.ico
│   │   │   └── colors.css
│   │   └── scripts/
│   │       ├── deploy.sh
│   │       ├── backup.sh
│   │       ├── restore.sh
│   │       └── ssl-renew.sh
│   │
│   └── switzerland/                       # SUISSE
│       ├── .env.example
│       ├── .env.production.example
│       ├── docker-compose.yml
│       ├── docker-compose.prod.yml
│       ├── nginx/
│       │   ├── nginx.conf
│       │   └── ssl/
│       ├── messages/
│       │   ├── fr.json
│       │   ├── de.json
│       │   ├── it.json
│       │   └── en.json
│       ├── legal/
│       │   ├── agb.md                     # Conditions generales (DE)
│       │   ├── datenschutz.md             # Privacy (DE)
│       │   └── impressum.md
│       ├── branding/
│       │   ├── logo.svg
│       │   ├── favicon.ico
│       │   └── colors.css
│       └── scripts/
│           ├── deploy.sh
│           ├── backup.sh
│           ├── restore.sh
│           └── ssl-renew.sh
│
├── shared/                                 # UTILITAIRES
│   ├── scripts/
│   │   ├── setup.sh
│   │   ├── test.sh
│   │   ├── lint.sh
│   │   └── build-all.sh
│   └── templates/
│       ├── env.template
│       └── docker-compose.template.yml
│
├── docs/                                   # DOCUMENTATION
│   ├── README.md
│   ├── architecture.md
│   ├── deployment.md
│   ├── contributing.md
│   ├── api/
│   │   └── openapi.yaml
│   └── guides/
│       ├── algeria.md
│       └── switzerland.md
│
├── .github/                               # CI/CD
│   └── workflows/
│       ├── test.yml
│       ├── build.yml
│       ├── deploy-algeria.yml
│       └── deploy-switzerland.yml
│
├── package.json                           # Root workspace
├── pnpm-workspace.yaml
├── turbo.json
├── .gitignore
├── .dockerignore
└── README.md
```

---

## 7. Configuration par Environnement

### Variables d'Environnement

#### deployments/algeria/.env.example

```bash
# ═══════════════════════════════════════════════════════════
# IAFACTORY ALGERIA - CONFIGURATION
# ═══════════════════════════════════════════════════════════

# ── REGION ──
REGION=algeria
REGION_CODE=DZ
TIMEZONE=Africa/Algiers
DEFAULT_LANGUAGE=fr
SUPPORTED_LANGUAGES=fr,ar,en,dz

# ── DOMAIN ──
DOMAIN=iafactory-algeria.com
API_URL=https://api.iafactory-algeria.com
APP_URL=https://app.iafactory-algeria.com

# ── DATABASE ──
POSTGRES_HOST=iaf-postgres
POSTGRES_PORT=5432
POSTGRES_USER=iafactory_dz
POSTGRES_PASSWORD=CHANGE_ME_SECURE_PASSWORD
POSTGRES_DB=iafactory_dz

# ── REDIS ──
REDIS_URL=redis://iaf-redis:6379/0

# ── QDRANT ──
QDRANT_HOST=iaf-qdrant
QDRANT_PORT=6333

# ── LLM PROVIDERS ──
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
GROQ_API_KEY=gsk_xxx
GOOGLE_GENERATIVE_AI_API_KEY=AIzaSy-xxx
DEEPSEEK_API_KEY=sk-xxx

# ── OLLAMA (LOCAL/SOUVERAIN) ──
OLLAMA_BASE_URL=http://iaf-ollama:11434
OLLAMA_MODEL=llama3.2

# ── PAIEMENTS (ALGERIE = CHARGILY) ──
PAYMENT_PROVIDER=chargily
CHARGILY_API_KEY=xxx
CHARGILY_SECRET_KEY=xxx
CHARGILY_WEBHOOK_SECRET=xxx
CHARGILY_MODE=test
PAYMENT_CURRENCY=DZD

# ── COMMUNICATION ──
TWILIO_ACCOUNT_SID=xxx
TWILIO_AUTH_TOKEN=xxx
TWILIO_PHONE_NUMBER=+213xxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+213xxx

# ── SECURITY ──
API_SECRET_KEY=CHANGE_ME_MIN_32_CHARS
JWT_SECRET_KEY=CHANGE_ME_MIN_32_CHARS
ALLOWED_ORIGINS=https://app.iafactory-algeria.com,https://iafactory-algeria.com

# ── FEATURES ──
ENABLE_DARIJA=true
ENABLE_ARABIC_RTL=true
LEGAL_FRAMEWORK=algeria
```

#### deployments/switzerland/.env.example

```bash
# ═══════════════════════════════════════════════════════════
# IAFACTORY SWITZERLAND - CONFIGURATION
# ═══════════════════════════════════════════════════════════

# ── REGION ──
REGION=switzerland
REGION_CODE=CH
TIMEZONE=Europe/Zurich
DEFAULT_LANGUAGE=fr
SUPPORTED_LANGUAGES=fr,de,it,en

# ── DOMAIN ──
DOMAIN=iafactory.ch
API_URL=https://api.iafactory.ch
APP_URL=https://app.iafactory.ch

# ── DATABASE ──
POSTGRES_HOST=iaf-postgres
POSTGRES_PORT=5432
POSTGRES_USER=iafactory_ch
POSTGRES_PASSWORD=CHANGE_ME_SECURE_PASSWORD
POSTGRES_DB=iafactory_ch

# ── REDIS ──
REDIS_URL=redis://iaf-redis:6379/0

# ── QDRANT ──
QDRANT_HOST=iaf-qdrant
QDRANT_PORT=6333

# ── LLM PROVIDERS ──
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
GROQ_API_KEY=gsk_xxx
GOOGLE_GENERATIVE_AI_API_KEY=AIzaSy-xxx

# ── OLLAMA (LOCAL/SOUVERAIN) ──
OLLAMA_BASE_URL=http://iaf-ollama:11434
OLLAMA_MODEL=llama3.2

# ── PAIEMENTS (SUISSE = STRIPE) ──
PAYMENT_PROVIDER=stripe
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_PUBLIC_KEY=pk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
PAYMENT_CURRENCY=CHF

# ── COMMUNICATION ──
TWILIO_ACCOUNT_SID=xxx
TWILIO_AUTH_TOKEN=xxx
TWILIO_PHONE_NUMBER=+41xxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+41xxx

# ── SECURITY ──
API_SECRET_KEY=CHANGE_ME_MIN_32_CHARS
JWT_SECRET_KEY=CHANGE_ME_MIN_32_CHARS
ALLOWED_ORIGINS=https://app.iafactory.ch,https://iafactory.ch

# ── FEATURES ──
ENABLE_DARIJA=false
ENABLE_ARABIC_RTL=false
LEGAL_FRAMEWORK=switzerland
```

### Docker Compose par Region

#### deployments/algeria/docker-compose.yml

```yaml
# IAFACTORY ALGERIA - Docker Compose
version: '3.8'

services:
  iaf-postgres:
    image: pgvector/pgvector:pg16
    container_name: iaf-dz-postgres
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
      TZ: ${TIMEZONE}
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ../../core/infrastructure/sql/init.sql:/docker-entrypoint-initdb.d/01-init.sql:ro
    ports:
      - "5432:5432"
    networks:
      - iaf-network

  iaf-redis:
    image: redis:7-alpine
    container_name: iaf-dz-redis
    volumes:
      - redis-data:/data
    ports:
      - "6379:6379"
    networks:
      - iaf-network

  iaf-qdrant:
    image: qdrant/qdrant:latest
    container_name: iaf-dz-qdrant
    volumes:
      - qdrant-data:/qdrant/storage
    ports:
      - "6333:6333"
    networks:
      - iaf-network

  iaf-backend:
    build:
      context: ../../core/services/api
      dockerfile: Dockerfile
    container_name: iaf-dz-backend
    env_file:
      - .env
    environment:
      - REGION=algeria
    volumes:
      - ../../core/services/api:/app
      - ../../core/agents:/agents:ro
    ports:
      - "8000:8000"
    depends_on:
      - iaf-postgres
      - iaf-redis
      - iaf-qdrant
    networks:
      - iaf-network

  iaf-frontend:
    build:
      context: ../../core/frontend/main-ui
      dockerfile: Dockerfile
      args:
        - NEXT_PUBLIC_API_URL=${API_URL}
        - NEXT_PUBLIC_REGION=${REGION}
    container_name: iaf-dz-frontend
    environment:
      - NEXT_PUBLIC_API_URL=${API_URL}
    volumes:
      - ./messages:/app/messages:ro
      - ./branding:/app/public/branding:ro
    ports:
      - "3000:3000"
    networks:
      - iaf-network

  iaf-ollama:
    image: ollama/ollama:latest
    container_name: iaf-dz-ollama
    volumes:
      - ollama-data:/root/.ollama
    ports:
      - "11434:11434"
    networks:
      - iaf-network

  iaf-nginx:
    image: nginx:alpine
    container_name: iaf-dz-nginx
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - iaf-backend
      - iaf-frontend
    networks:
      - iaf-network

volumes:
  postgres-data:
  redis-data:
  qdrant-data:
  ollama-data:

networks:
  iaf-network:
    driver: bridge
```

---

## 8. Commandes Deploiement

### Scripts Deploy

#### shared/scripts/deploy.sh

```bash
#!/bin/bash
# Deploy script for IAFactory Platform

set -e

REGION=$1
ENVIRONMENT=${2:-production}

if [ -z "$REGION" ]; then
    echo "Usage: ./deploy.sh <algeria|switzerland> [production|staging]"
    exit 1
fi

echo "═══════════════════════════════════════════════════"
echo "  DEPLOYING IAFACTORY - $REGION ($ENVIRONMENT)"
echo "═══════════════════════════════════════════════════"

DEPLOY_DIR="deployments/$REGION"

if [ ! -d "$DEPLOY_DIR" ]; then
    echo "Error: Deployment directory not found: $DEPLOY_DIR"
    exit 1
fi

cd "$DEPLOY_DIR"

# Load environment
if [ "$ENVIRONMENT" == "production" ]; then
    ENV_FILE=".env.production"
else
    ENV_FILE=".env"
fi

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Environment file not found: $ENV_FILE"
    exit 1
fi

export $(cat $ENV_FILE | grep -v '^#' | xargs)

echo "1. Pulling latest images..."
docker-compose pull

echo "2. Building custom images..."
docker-compose build --no-cache

echo "3. Stopping old containers..."
docker-compose down

echo "4. Starting new containers..."
if [ "$ENVIRONMENT" == "production" ]; then
    docker-compose -f docker-compose.prod.yml up -d
else
    docker-compose up -d
fi

echo "5. Running migrations..."
docker-compose exec -T iaf-backend alembic upgrade head

echo "6. Health check..."
sleep 10
curl -f http://localhost:8000/health || exit 1

echo "═══════════════════════════════════════════════════"
echo "  DEPLOYMENT COMPLETE!"
echo "  Region: $REGION"
echo "  Environment: $ENVIRONMENT"
echo "  API: $API_URL"
echo "  App: $APP_URL"
echo "═══════════════════════════════════════════════════"
```

### Commandes Rapides

```bash
# ═══════════════════════════════════════════════════════
# DEVELOPPEMENT LOCAL
# ═══════════════════════════════════════════════════════

# Cloner le monorepo
git clone https://github.com/iafactory/iafactory-platform.git
cd iafactory-platform

# Setup Algerie (dev)
cd deployments/algeria
cp .env.example .env
docker-compose up -d

# Setup Suisse (dev)
cd deployments/switzerland
cp .env.example .env
docker-compose up -d


# ═══════════════════════════════════════════════════════
# DEPLOIEMENT PRODUCTION
# ═══════════════════════════════════════════════════════

# Algerie
./shared/scripts/deploy.sh algeria production

# Suisse
./shared/scripts/deploy.sh switzerland production


# ═══════════════════════════════════════════════════════
# BACKUP
# ═══════════════════════════════════════════════════════

# Backup Algerie
./deployments/algeria/scripts/backup.sh

# Backup Suisse
./deployments/switzerland/scripts/backup.sh


# ═══════════════════════════════════════════════════════
# MISE A JOUR CODE
# ═══════════════════════════════════════════════════════

# Pull + Deploy les 2 regions
git pull origin main
./shared/scripts/deploy.sh algeria production
./shared/scripts/deploy.sh switzerland production
```

---

## 9. Plan de Migration

### Phase 1: Preparation (1-2 jours)

```bash
# 1. Creer le nouveau repo
mkdir iafactory-platform
cd iafactory-platform
git init

# 2. Creer la structure
mkdir -p core/{apps,agents,services,frontend,workflows,infrastructure}
mkdir -p deployments/{algeria,switzerland}
mkdir -p shared/{scripts,templates}
mkdir -p docs
```

### Phase 2: Migration Code (2-3 jours)

```bash
# 1. Copier le code core depuis rag-dz
cp -r ../rag-dz/apps/* core/apps/
cp -r ../rag-dz/agents/* core/agents/
cp -r ../rag-dz/services/* core/services/
cp -r ../rag-dz/frontend/* core/frontend/
cp -r ../rag-dz/workflows/* core/workflows/
cp -r ../rag-dz/infrastructure/* core/infrastructure/

# 2. Renommer les dossiers specifiques DZ
mv core/apps/pme-dz core/apps/pme
mv core/apps/seo-dz-boost core/apps/seo-boost
mv core/agents/discovery-dz core/agents/discovery
mv core/agents/recruteur-dz core/agents/recruiter

# 3. Nettoyer les references "dz" dans le code
# (garder darija comme module optionnel)
```

### Phase 3: Configuration (1 jour)

```bash
# 1. Creer les configs Algeria
cp ../rag-dz/.env deployments/algeria/.env.example
cp ../rag-dz/docker-compose.yml deployments/algeria/

# 2. Creer les configs Switzerland (adapter)
cp deployments/algeria/.env.example deployments/switzerland/.env.example
# Modifier: REGION, langues, paiements, domaine

# 3. Creer les traductions
mkdir -p deployments/algeria/messages
mkdir -p deployments/switzerland/messages
```

### Phase 4: Test (1-2 jours)

```bash
# 1. Test local Algeria
cd deployments/algeria
docker-compose up -d
# Verifier: http://localhost:3000

# 2. Test local Switzerland
cd ../switzerland
docker-compose up -d
# Verifier: http://localhost:3001

# 3. Tests automatises
./shared/scripts/test.sh
```

### Phase 5: Deploiement (1 jour)

```bash
# 1. Push vers GitHub
git add .
git commit -m "feat: monorepo multi-region architecture"
git push origin main

# 2. Deploy Algerie
./shared/scripts/deploy.sh algeria production

# 3. Deploy Suisse
./shared/scripts/deploy.sh switzerland production

# 4. Verification finale
curl https://api.iafactory-algeria.com/health
curl https://api.iafactory.ch/health
```

### Checklist Migration

- [ ] Backup complet de rag-dz
- [ ] Creer nouveau repo iafactory-platform
- [ ] Migrer code core
- [ ] Renommer dossiers generiques
- [ ] Creer configs Algeria
- [ ] Creer configs Switzerland
- [ ] Creer traductions FR/AR/EN/DZ
- [ ] Creer traductions FR/DE/IT/EN
- [ ] Tester localement Algeria
- [ ] Tester localement Switzerland
- [ ] Setup CI/CD GitHub Actions
- [ ] Deploy production Algeria
- [ ] Deploy production Switzerland
- [ ] Verifier health checks
- [ ] Mettre a jour DNS
- [ ] Archiver ancien rag-dz

---

## Resume

### Architecture Choisie: MONOREPO

```
iafactory-platform/
├── core/                    # CODE PARTAGE (28 apps, 15 agents)
├── deployments/
│   ├── algeria/            # Config DZ (Chargily, ar/fr/dz)
│   └── switzerland/        # Config CH (Stripe, de/fr/it)
├── shared/                  # Scripts, templates
└── docs/                    # Documentation
```

### Avantages

1. **Un seul repo** - Simplicite de gestion
2. **Code synchronise** - Modifications instantanees
3. **Deploy independant** - 2 VPS separes
4. **Config flexible** - .env par region
5. **Souverainete** - Donnees locales

### Prochaines Etapes

1. **Valider** cette architecture avec l'equipe
2. **Executer** le plan de migration (5-7 jours)
3. **Tester** les 2 deployments
4. **Documenter** les procedures

---

*Document genere par Claude Code - PROMPT 4*
*Date: 29 Decembre 2025*
