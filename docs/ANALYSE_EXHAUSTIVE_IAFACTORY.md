# Analyse Exhaustive IAFactory

> **Date d'analyse**: 29 Decembre 2025
> **Localisation**: D:\IAFactory\
> **Projets analyses**: 8
> **Projets actifs**: 3
> **Projets vides**: 5

---

## Sommaire

1. [rag-dz](#1-rag-dz) - Plateforme RAG principale
2. [iafactory-academy](#2-iafactory-academy) - LMS e-learning
3. [onestschooled](#3-onestschooled) - SaaS gestion scolaire
4. [Helvetia](#4-helvetia) - VIDE
5. [iafactory-video-studio](#5-iafactory-video-studio) - VIDE
6. [iafactory-video-studio-pro](#6-iafactory-video-studio-pro) - VIDE
7. [bmad-agent](#7-bmad-agent) - VIDE
8. [bolt-diy-fresh](#8-bolt-diy-fresh) - VIDE
9. [Synthese](#synthese)

---

## 1. rag-dz

### Identification

| Attribut | Valeur |
|----------|--------|
| **Type** | Fullstack (Monorepo) |
| **Objectif** | Plateforme SaaS d'IA pour le marche algerien - RAG, Chatbots, Video IA, CRM, Agents |
| **Maturite** | Production-ready |

### Technologies Principales

| Categorie | Technologies |
|-----------|--------------|
| **Backend** | Python 3.11+, FastAPI 0.111.0, SQLAlchemy |
| **Frontend** | React 18, Next.js 14, Vite, TypeScript, Tailwind CSS |
| **Base de donnees** | PostgreSQL 16 (pgvector), Redis 7, Qdrant |
| **IA/ML** | OpenAI, Anthropic Claude, Groq, Gemini, DeepSeek, Ollama |
| **Embeddings** | sentence-transformers, cross-encoder (reranking) |
| **Orchestration** | Docker Compose, n8n (workflows) |
| **Monitoring** | Prometheus, Grafana |

### Structure du Projet

```
rag-dz/
├── apps/                      # ~30 applications par secteur
│   ├── api-portal/           # Portail API
│   ├── can2025/              # CAN 2025
│   ├── crm-ia/               # CRM IA
│   ├── dzirvideo/            # Video IA
│   ├── ia-chatbot/           # Chatbot IA
│   ├── ia-notebook/          # Notebook IA
│   ├── iafactory-landing/    # Landing page
│   ├── legal-assistant/      # Assistant juridique
│   ├── marketing/            # Marketing
│   ├── mcp-dashboard/        # Dashboard MCP
│   ├── pme-dz/               # PME Copilot
│   ├── seo-dz-boost/         # SEO Algerie
│   ├── video-studio/         # Studio Video
│   └── workflow-studio/      # Studio Workflows
├── services/                  # Backend microservices
│   └── api/                  # API FastAPI principale
│       └── app/
│           ├── bigrag/       # RAG avance
│           ├── core/         # Configuration
│           ├── darija/       # Support dialecte algerien
│           ├── digital_twin/ # Jumeau numerique
│           ├── life_assistant/ # Assistant vie
│           ├── llm_router/   # Routage LLM
│           ├── mcp/          # Model Context Protocol
│           ├── models/       # Modeles SQLAlchemy
│           ├── multi_llm/    # Multi-LLM
│           ├── ocr/          # OCR
│           ├── routers/      # Routes API
│           ├── security/     # Securite
│           ├── services/     # Logique metier
│           ├── voice/        # Voice features
│           └── voice_agent/  # Agent vocal
├── frontend/                  # Applications frontend
│   ├── ia-factory-ui/        # UI principale (Next.js)
│   ├── rag-ui/               # UI RAG (React/Vite)
│   ├── archon-ui/            # UI Archon
│   └── video-studio/         # UI Video Studio
├── agents/                    # Agents IA par domaine
│   ├── business/             # Agents business
│   ├── legal/                # Agent juridique
│   ├── finance/              # Agent finance
│   ├── rag/                  # Agent RAG
│   ├── real_estate/          # Agent immobilier
│   ├── recruitment/          # Agent recrutement
│   └── video-operator/       # Operateur video
├── infrastructure/            # Infra Docker, SQL
│   └── sql/                  # Scripts init PostgreSQL
├── workflows/                 # Workflows n8n
├── templates/                 # Templates UI
└── bmad/                      # BMAD Method integration
```

### Backend API (FastAPI)

**Port**: 8000

**Routes principales**:
- `/health` - Health check
- `/api/v1/chat` - Chat RAG
- `/api/v1/documents` - Gestion documents
- `/api/v1/embeddings` - Embeddings
- `/api/v1/knowledge` - Base de connaissances
- `/api/v1/voice` - Voice features
- `/api/v1/mcp` - MCP endpoints

### Frontend Applications

| Application | Port | Framework |
|-------------|------|-----------|
| ia-factory-ui | 3000 | Next.js 14 |
| rag-ui | 5173 | React + Vite |
| Video Studio | 3050 | Next.js |

### Services Docker

| Service | Port | Image |
|---------|------|-------|
| iaf-postgres | 5432 | pgvector/pgvector:pg16 |
| iaf-redis | 6379 | redis:7-alpine |
| iaf-qdrant | 6333/6334 | qdrant/qdrant |
| iaf-backend | 8000 | FastAPI custom |
| iaf-frontend | 3000 | Next.js custom |
| iaf-rag-ui | 5173 | Vite custom |
| iaf-n8n | 5678 | n8n |
| iaf-anythingllm | 3001 | AnythingLLM |
| iaf-ollama | 11434 | Ollama |
| iaf-adminer | 8080 | Adminer |
| iaf-prometheus | 9090 | Prometheus |
| iaf-grafana | 3002 | Grafana |
| iaf-flowise | 3004 | Flowise |
| iaf-firecrawl | 3005 | Firecrawl |

### Dependances Backend Principales

```
fastapi==0.111.0
uvicorn==0.30.0
pydantic==2.7.3
redis==5.0.7
psycopg==3.2.1
qdrant-client==1.11.1
sentence-transformers==2.7.0
torch==2.3.1
openai==1.35.0
anthropic==0.28.0
twilio==9.0.0
supabase==2.10.0
elasticsearch==8.15.1
```

### Configuration (.env)

**Variables cles**:
- `API_SECRET_KEY` - Cle API
- `POSTGRES_PASSWORD` - Password PostgreSQL
- `LLM_PROVIDER` - anthropic/openai/groq/deepseek
- `EMBEDDING_MODEL` - sentence-transformers/paraphrase-multilingual-mpnet-base-v2
- `USE_RERANKING` - true
- `QDRANT_HOST` / `QDRANT_PORT`
- Cles API: OPENAI, ANTHROPIC, GROQ, GOOGLE, MISTRAL, DEEPSEEK

### Services Externes

- **LLM Cloud**: OpenAI, Anthropic Claude, Groq, Google Gemini, Mistral, DeepSeek
- **Communication**: Twilio (SMS, WhatsApp)
- **BDD Cloud**: Supabase
- **Orchestration**: n8n
- **Video IA**: Replicate, Stability AI, ElevenLabs

---

## 2. iafactory-academy

### Identification

| Attribut | Valeur |
|----------|--------|
| **Type** | Fullstack |
| **Objectif** | Plateforme e-learning avec gestion de cours, paiements Stripe, certifications |
| **Maturite** | MVP en developpement |

### Technologies Principales

| Categorie | Technologies |
|-----------|--------------|
| **Backend** | Python 3.11+, FastAPI 0.109.0, SQLAlchemy 2.0, Alembic |
| **Frontend** | React 18.3, TypeScript 5.3, Vite 5, TailwindCSS 3.4 |
| **Base de donnees** | PostgreSQL 16, Redis 7 |
| **Task Queue** | Celery 5.3.6, Flower |
| **Paiements** | Stripe |
| **Email** | SendGrid |
| **Storage** | AWS S3 |

### Structure du Projet

```
iafactory-academy/
├── backend/
│   ├── app/
│   │   ├── api/              # Routes API
│   │   ├── core/             # Config, security, dependencies
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── tasks/            # Celery tasks
│   ├── alembic/              # DB migrations
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   └── src/
│       ├── api/              # API clients
│       ├── components/       # UI components
│       ├── pages/            # Route pages
│       ├── lib/              # Utilities
│       ├── store/            # Zustand stores
│       └── types/            # TypeScript types
├── docs/                     # Documentation
├── deploy/                   # Deployment configs
├── demo/                     # Demo content
├── supabase/                 # Supabase config
└── docker-compose.yml
```

### Backend API (FastAPI)

**Port**: 8000

**Modules principaux**:
- Authentification JWT (access + refresh tokens)
- Gestion des cours, modules, lecons
- Inscriptions etudiants
- Paiements Stripe
- Certifications
- Progression tracking

### Frontend (React/Vite)

**Port**: 3000

**Dependances principales**:
```json
{
  "@tanstack/react-query": "^5.17.19",
  "@stripe/react-stripe-js": "^2.4.0",
  "@supabase/supabase-js": "^2.89.0",
  "zustand": "^4.4.7",
  "react-router-dom": "^6.21.3",
  "react-hook-form": "^7.49.3",
  "zod": "^3.22.4",
  "recharts": "^2.10.4",
  "framer-motion": "^10.18.0"
}
```

### Services Docker

| Service | Port | Description |
|---------|------|-------------|
| postgres | 5433 | PostgreSQL 16 |
| redis | 6385 | Redis 7 |
| backend | 8000 | FastAPI |
| celery_worker | - | Celery worker |
| celery_beat | - | Celery scheduler |
| flower | 5555 | Celery monitoring |
| pgadmin | 5050 | PostgreSQL admin |
| redis-commander | 8081 | Redis admin |

### Dependances Backend

```
fastapi==0.109.0
sqlalchemy==2.0.25
alembic==1.13.1
celery==5.3.6
redis==5.0.1
stripe==8.0.0
sendgrid==6.11.0
boto3==1.34.26
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
sentry-sdk[fastapi]==1.40.0
```

### Configuration (.env)

**Variables cles**:
- `SECRET_KEY`, `JWT_SECRET_KEY` - Securite
- `DATABASE_URL` - PostgreSQL
- `REDIS_URL` - Cache
- `STRIPE_SECRET_KEY`, `STRIPE_PUBLIC_KEY` - Paiements
- `SENDGRID_API_KEY` - Emails
- `AWS_*` - S3 Storage
- API Keys IA: OPENAI, ANTHROPIC, GROQ, GEMINI, MISTRAL, DEEPSEEK

### Services Externes

- **Paiements**: Stripe
- **Email**: SendGrid
- **Storage**: AWS S3
- **Monitoring**: Sentry
- **BDD Cloud**: Supabase

---

## 3. onestschooled

### Identification

| Attribut | Valeur |
|----------|--------|
| **Type** | Fullstack (Laravel Monolith) |
| **Objectif** | SaaS de gestion scolaire multi-tenant (administration, eleves, profs, parents) |
| **Maturite** | Production (v12 Laravel) |

### Technologies Principales

| Categorie | Technologies |
|-----------|--------------|
| **Backend** | PHP 8.2+, Laravel 12, Laravel Modules |
| **Frontend** | Blade, Bootstrap 5, Vite, SASS |
| **Base de donnees** | MySQL |
| **Multi-tenant** | stancl/tenancy |
| **Paiements** | Stripe, PayPal |
| **Notifications** | Firebase, Twilio, Pusher |

### Structure du Projet

```
onestschooled/
├── app/
│   ├── Http/
│   │   ├── Controllers/
│   │   │   ├── Academic/      # Gestion academique
│   │   │   ├── Accounts/      # Comptabilite
│   │   │   ├── Admin/         # Administration
│   │   │   ├── Api/           # API endpoints
│   │   │   ├── Attendance/    # Presence
│   │   │   ├── Auth/          # Authentification
│   │   │   ├── Examination/   # Examens
│   │   │   ├── Fees/          # Frais
│   │   │   ├── Frontend/      # Site public
│   │   │   ├── Leave/         # Conges
│   │   │   ├── Library/       # Bibliotheque
│   │   │   ├── OnlineExamination/ # Examens en ligne
│   │   │   ├── ParentPanel/   # Portail parents
│   │   │   └── ChatbotController.php # Chatbot IA
│   │   └── Middleware/
│   ├── Models/
│   │   ├── Academic/
│   │   ├── Accounts/
│   │   ├── Attendance/
│   │   ├── Examination/
│   │   └── Fees/
│   └── Services/
├── Modules/                    # Laravel Modules
│   ├── MainApp/               # Module principal
│   ├── Forums/                # Forums
│   ├── Installer/             # Installation
│   ├── LiveChat/              # Chat en direct
│   ├── MultiBranch/           # Multi-etablissement
│   └── PushNotification/      # Notifications push
├── routes/
│   ├── web.php                # Routes web
│   ├── api.php                # Routes API
│   ├── admin.php              # Routes admin
│   ├── academic.php           # Routes academiques
│   ├── examination.php        # Routes examens
│   ├── fees.php               # Routes frais
│   ├── student-panel.php      # Portail etudiant
│   └── parent-panel.php       # Portail parent
├── resources/
│   ├── views/                 # Blade templates
│   └── js/
├── config/
├── database/
│   └── migrations/
└── frontend-html/             # Templates HTML statiques
```

### Modules Fonctionnels

| Module | Description |
|--------|-------------|
| **Academic** | Gestion classes, sections, sujets |
| **Accounts** | Comptabilite, budgets |
| **Attendance** | Presence eleves et staff |
| **Examination** | Examens, notes, bulletins |
| **Fees** | Frais de scolarite, paiements |
| **Library** | Gestion bibliotheque |
| **Leave** | Gestion des conges |
| **OnlineExamination** | Examens en ligne |
| **Forums** | Forums de discussion |
| **LiveChat** | Chat en direct |
| **MultiBranch** | Multi-etablissement |
| **PushNotification** | Notifications Firebase |

### API Endpoints

**Routes API** (`routes/api.php`):
- `/api/public/v1/*` - API publique
- Authentification Sanctum
- API mobile pour parents/eleves

### Dependances Composer

```json
{
  "laravel/framework": "^12.0",
  "laravel/sanctum": "^4.1",
  "nwidart/laravel-modules": "^10.0",
  "stancl/tenancy": "^3.7",
  "stripe/stripe-php": "^10.19",
  "srmklive/paypal": "~1.0",
  "kreait/laravel-firebase": "^6.0",
  "twilio/sdk": "^7.12",
  "barryvdh/laravel-dompdf": "^3.1.1",
  "intervention/image": "^2.7",
  "maatwebsite/excel": "^3.1"
}
```

### Configuration (.env)

**Variables cles**:
- `APP_SAAS=true` - Mode SaaS multi-tenant
- `DB_CONNECTION=mysql` - MySQL
- `STRIPE_KEY`, `STRIPE_SECRET` - Paiements Stripe
- `FIREBASE_*` - Notifications push
- `PUSHER_*` - Temps reel
- `TWILIO_*` - SMS (optionnel)

### Services Externes

- **Paiements**: Stripe, PayPal
- **Notifications**: Firebase Cloud Messaging
- **Temps reel**: Pusher
- **SMS**: Twilio
- **Maps**: Google Maps

---

## 4. Helvetia

### Statut: VIDE

Le dossier `D:\IAFactory\Helvetia\` existe mais ne contient aucun fichier.

**Hypothese**: Projet prevu pour le marche suisse (non demarre ou deplace).

---

## 5. iafactory-video-studio

### Statut: VIDE

Le dossier `D:\IAFactory\iafactory-video-studio\` existe mais ne contient aucun fichier.

**Note**: Les fonctionnalites Video Studio sont integrees dans `rag-dz/apps/video-studio/` et `rag-dz/frontend/video-studio/`.

---

## 6. iafactory-video-studio-pro

### Statut: VIDE

Le dossier `D:\IAFactory\iafactory-video-studio-pro\` existe mais ne contient aucun fichier.

**Note**: Version pro non demarree. Les fonctionnalites de base sont dans `rag-dz`.

---

## 7. bmad-agent

### Statut: VIDE

Le dossier `D:\IAFactory\bmad-agent\` existe mais ne contient aucun fichier.

**Note**: L'integration BMAD Method est presente dans `rag-dz/bmad/` et via le package npm `bmad-method` dans `rag-dz/package.json`.

---

## 8. bolt-diy-fresh

### Statut: VIDE

Le dossier `D:\IAFactory\bolt-diy-fresh\` existe mais ne contient aucun fichier.

**Hypothese**: Clone de Bolt.diy prevu mais non initialise.

---

## Synthese

### Vue d'Ensemble

| Projet | Type | Stack | Statut | Port Backend | Port Frontend |
|--------|------|-------|--------|--------------|---------------|
| **rag-dz** | Fullstack | FastAPI + React/Next.js | Actif | 8000 | 3000, 5173 |
| **iafactory-academy** | Fullstack | FastAPI + React | Actif | 8000 | 3000 |
| **onestschooled** | Monolith | Laravel 12 | Actif | 80/443 | Blade SSR |
| Helvetia | - | - | VIDE | - | - |
| iafactory-video-studio | - | - | VIDE | - | - |
| iafactory-video-studio-pro | - | - | VIDE | - | - |
| bmad-agent | - | - | VIDE | - | - |
| bolt-diy-fresh | - | - | VIDE | - | - |

### Tableau Comparatif des Projets Actifs

| Critere | rag-dz | iafactory-academy | onestschooled |
|---------|--------|-------------------|---------------|
| **Langage Backend** | Python | Python | PHP |
| **Framework Backend** | FastAPI | FastAPI | Laravel 12 |
| **Frontend** | React/Next.js | React/Vite | Blade/Bootstrap |
| **BDD Principale** | PostgreSQL | PostgreSQL | MySQL |
| **BDD Vectorielle** | Qdrant, PGVector | Qdrant | - |
| **Cache** | Redis | Redis | Redis (optionnel) |
| **Paiements** | Chargily (DZ) | Stripe | Stripe, PayPal |
| **IA/LLM** | Multi-provider | Multi-provider | Chatbot custom |
| **Multi-tenant** | Non | Non | Oui (stancl/tenancy) |
| **i18n** | fr, ar, en | fr, ar, en, de, it | Multi-langue |

### Redondances Identifiees

1. **Authentification JWT**
   - `rag-dz`: Implementation custom avec python-jose
   - `iafactory-academy`: Implementation similaire
   - **Recommandation**: Extraire en package partage

2. **Integration LLM**
   - Les deux projets Python ont des configurations LLM similaires
   - **Recommandation**: Creer un module `iaf-llm-client` partage

3. **Gestion des cours/formations**
   - `iafactory-academy`: Module complet de e-learning
   - `onestschooled`: Module academique
   - **Recommandation**: Evaluer la fusion ou le partage

4. **Video Studio**
   - Code present dans `rag-dz/apps/video-studio/`
   - Dossiers vides `iafactory-video-studio` et `iafactory-video-studio-pro`
   - **Recommandation**: Supprimer les dossiers vides

5. **BMAD Method**
   - Integration dans `rag-dz/bmad/`
   - Dossier vide `bmad-agent`
   - **Recommandation**: Supprimer le dossier vide

### Integrations Possibles

1. **rag-dz <-> iafactory-academy**
   - Utiliser le RAG de rag-dz pour alimenter les contenus de cours
   - Chatbot IA pour support etudiant
   - Generation automatique de quiz avec LLM

2. **rag-dz <-> onestschooled**
   - API RAG pour chatbot scolaire (deja present: `ChatbotController.php`)
   - Assistant IA pour parents/eleves
   - Generation de rapports avec LLM

3. **iafactory-academy <-> onestschooled**
   - Partage du module de paiements Stripe
   - SSO entre les plateformes
   - Synchronisation des donnees eleves

### Architecture Finale Recommandee

```
IAFactory Ecosystem
│
├── CORE SERVICES (Shared)
│   ├── iaf-auth-service/        # Auth centralisee (JWT, OAuth)
│   ├── iaf-llm-gateway/         # Gateway LLM multi-provider
│   ├── iaf-storage-service/     # Storage S3/local unifie
│   └── iaf-notification-hub/    # Notifications (email, SMS, push)
│
├── APPLICATIONS
│   ├── rag-dz/                  # Plateforme IA Algerie (CONSERVER)
│   ├── iafactory-academy/       # LMS e-learning (CONSERVER)
│   └── onestschooled/           # SaaS scolaire (CONSERVER)
│
├── A NETTOYER (SUPPRIMER)
│   ├── Helvetia/                # Vide
│   ├── iafactory-video-studio/  # Vide (dans rag-dz)
│   ├── iafactory-video-studio-pro/ # Vide
│   ├── bmad-agent/              # Vide (dans rag-dz)
│   └── bolt-diy-fresh/          # Vide
│
└── INFRASTRUCTURE
    ├── Docker Compose unifie
    ├── PostgreSQL cluster (multi-DB)
    ├── Redis cluster
    ├── Traefik reverse proxy
    └── Monitoring (Prometheus/Grafana)
```

### Actions Recommandees

#### Immediate (Nettoyage)
- [ ] Supprimer `Helvetia/` (vide)
- [ ] Supprimer `iafactory-video-studio/` (vide)
- [ ] Supprimer `iafactory-video-studio-pro/` (vide)
- [ ] Supprimer `bmad-agent/` (vide)
- [ ] Supprimer `bolt-diy-fresh/` (vide)

#### Court terme (Optimisation)
- [ ] Unifier les configurations Docker
- [ ] Creer un `.env.shared` pour les cles API communes
- [ ] Harmoniser les ports pour eviter les conflits
- [ ] Documenter les dependances inter-projets

#### Moyen terme (Integration)
- [ ] Extraire les modules partages (auth, LLM client)
- [ ] Mettre en place un API Gateway (Traefik/Kong)
- [ ] Centraliser les logs et metriques
- [ ] Implementer SSO entre les applications

### Ports Utilises

| Port | Service | Projet |
|------|---------|--------|
| 3000 | Frontend Next.js | rag-dz, iafactory-academy |
| 3001 | AnythingLLM | rag-dz |
| 3002 | Grafana | rag-dz |
| 3004 | Flowise | rag-dz |
| 3005 | Firecrawl | rag-dz |
| 5050 | pgAdmin | iafactory-academy |
| 5173 | Vite dev | rag-dz, iafactory-academy |
| 5432 | PostgreSQL | rag-dz |
| 5433 | PostgreSQL | iafactory-academy |
| 5555 | Flower | iafactory-academy |
| 5678 | n8n | rag-dz |
| 6333/6334 | Qdrant | rag-dz |
| 6379 | Redis | rag-dz |
| 6385 | Redis | iafactory-academy |
| 8000 | FastAPI Backend | rag-dz, iafactory-academy |
| 8080 | Adminer | rag-dz |
| 8081 | Redis Commander | iafactory-academy |
| 9090 | Prometheus | rag-dz |
| 11434 | Ollama | rag-dz |

---

*Document genere automatiquement par Claude Code - IAFactory Analysis*
