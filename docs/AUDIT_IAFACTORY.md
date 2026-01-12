# AUDIT IA FACTORY - 30 Decembre 2025

## Resume Executif

Le projet IA Factory comprend **4 sous-projets principaux** avec un total de **~500+ fichiers Python** et **~200+ fichiers TypeScript/React**.

---

## 1. Stack Technique

| Composant | Technologie |
|-----------|-------------|
| **Backend** | FastAPI (Python 3.11+), SQLAlchemy |
| **Frontend** | React 18, Vite, TailwindCSS, Zustand |
| **Database** | PostgreSQL + Supabase + PGVector |
| **Cache** | Redis |
| **Vector DB** | Qdrant, Meilisearch |
| **AI/LLM** | OpenAI, Anthropic, DeepSeek, Groq, Gemini, Perplexity, Ollama |
| **Paiement** | Chargily (Algerie), Stripe (Suisse) |
| **Browser Automation** | Playwright |
| **Deployment** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |

---

## 2. Sous-Projets Identifies (4 principaux)

### 2.1 RAG-DZ (Principal)
| Element | Valeur |
|---------|--------|
| **Chemin** | `/rag-dz/` |
| **Description** | Plateforme SaaS IA pour le marche algerien |
| **Backend** | FastAPI (services/api/) |
| **Frontend** | Next.js + React (frontend/ia-factory-ui/) |
| **Statut** | En cours - Fonctionnel partiellement |

### 2.2 IAFactory Academy
| Element | Valeur |
|---------|--------|
| **Chemin** | `/iafactory-academy/` |
| **Description** | Plateforme e-learning avec RAG |
| **Backend** | FastAPI + Supabase |
| **Frontend** | React + Vite |
| **Statut** | Complet - Pret pour production |

### 2.3 IAFactory Video Platform
| Element | Valeur |
|---------|--------|
| **Chemin** | `/iafactory-video-platform/` |
| **Description** | Generation de videos IA automatisee |
| **Backend** | FastAPI + Celery |
| **Frontend** | React (minimal) |
| **Statut** | En cours - Structure definie |

### 2.4 OneStSchooled
| Element | Valeur |
|---------|--------|
| **Chemin** | `/onestschooled/` |
| **Description** | SaaS ecole virtuelle (Laravel) |
| **Backend** | Laravel PHP |
| **Frontend** | Blade + jQuery |
| **Statut** | Complet - Application tierce |

---

## 3. Applications Existantes (RAG-DZ)

| # | Nom | Chemin | Fonction | Statut |
|---|-----|--------|----------|--------|
| 1 | API Portal | `/rag-dz/apps/api-portal/` | Gestion cles API developpeurs | En cours |
| 2 | CRM IA | `/rag-dz/apps/crm-ia/` | CRM avec IA pour PME | En cours |
| 3 | Video Studio | `/rag-dz/apps/video-studio/` | Generation videos IA | En cours |
| 4 | IA Notebook | `/rag-dz/apps/ia-notebook/` | NotebookLM clone | Partiel |
| 5 | PME-DZ Copilot | `/rag-dz/apps/pme-dz/copilot/` | Assistant PME algerien | Fonctionnel |
| 6 | PME-DZ Growth | `/rag-dz/apps/pme-dz/growth/` | Growth Grid analytics | Partiel |
| 7 | CAN 2025 | `/rag-dz/apps/can2025/` | App CAN 2025 | Ébauche |
| 8 | SEO DZ Boost | `/rag-dz/apps/seo-dz-boost/` | SEO pour Algerie | Ébauche |
| 9 | DZIRVideo | `/rag-dz/apps/dzirvideo/` | Generation video DZ | Ébauche |
| 10 | Sport App | `/rag-dz/apps/sport/` | Application sport | Ébauche |

---

## 4. Services Backend (RAG-DZ)

| # | Service | Chemin | Fonction | Statut |
|---|---------|--------|----------|--------|
| 1 | API Principale | `/rag-dz/services/api/` | API REST FastAPI | Fonctionnel |
| 2 | Fiscal Assistant | `/rag-dz/services/fiscal-assistant/` | Assistant fiscal DZ | Partiel |
| 3 | Legal Assistant | `/rag-dz/services/legal-assistant/` | Assistant juridique DZ | Partiel |
| 4 | Voice Assistant | `/rag-dz/services/voice-assistant/` | Assistant vocal STT/TTS | Partiel |
| 5 | Browser Automation | `/rag-dz/services/browser-automation/` | Automatisation sites gov | Fonctionnel |
| 6 | Data Dashboard | `/rag-dz/services/data-dashboard/` | Dashboard analytics | Ébauche |
| 7 | Connectors | `/rag-dz/services/connectors/` | Connecteurs externes | Partiel |
| 8 | Backend Billing | `/rag-dz/services/backend/billing/` | Systeme facturation | Fonctionnel |
| 9 | Key Service | `/rag-dz/services/backend/key-service/` | Gestion cles API (Node.js) | Partiel |
| 10 | Voice Agent | `/rag-dz/services/backend/voice-agent/` | Transcription Whisper | Partiel |

---

## 5. Agents GOV (Browser Automation)

| Service | Fichier | Fonctionnalites | Statut |
|---------|---------|-----------------|--------|
| CNAS | `services/browser-automation/agents/cnas.py` | Attestation, historique, droits, carte Chifa | Structure OK - Parsers a completer |
| Sonelgaz | `services/browser-automation/agents/sonelgaz.py` | Factures, consommation, paiement | Structure OK - Parsers a completer |
| CASNOS | Reference uniquement | Non implemente | Planifie |
| CNRC | Reference uniquement | Non implemente | Planifie |
| Impots | Reference uniquement | Non implemente | Planifie |

---

## 6. Agents IA (Templates)

| # | Agent | Chemin | Fonction |
|---|-------|--------|----------|
| 1 | Consultant Business | `/rag-dz/agents/business/consultant/` | Consultant IA business |
| 2 | Customer Support | `/rag-dz/agents/business/customer-support/` | Support client IA |
| 3 | Data Analyst | `/rag-dz/agents/business/data-analysis/` | Analyse de donnees |
| 4 | Financial Coach | `/rag-dz/agents/finance/financial_coach.py` | Coach financier IA |
| 5 | Legal Team | `/rag-dz/agents/legal/legal_team.py` | Equipe juridique IA |
| 6 | Real Estate | `/rag-dz/agents/real_estate/real_estate_team.py` | Agent immobilier IA |
| 7 | Recruitment | `/rag-dz/agents/recruitment/recruitment_team.py` | Recrutement IA |
| 8 | Teaching Team | `/rag-dz/agents/teaching/teaching_team.py` | Equipe enseignement |
| 9 | Travel Agent | `/rag-dz/agents/travel/travel_agent.py` | Agent voyage |
| 10 | IAFactory Operator | `/rag-dz/agents/iafactory-operator/` | Orchestrateur principal |

---

## 7. Integrations Externes

### 7.1 Paiement

| Service | Configure | Fichier | Mode |
|---------|-----------|---------|------|
| Chargily | Oui | `services/api/app/services/chargily_service.py` | Test/Live |
| Stripe | Oui | `iafactory-academy/frontend/package.json` | Production |

### 7.2 LLM Providers

| Provider | Configure | Variables Env |
|----------|-----------|---------------|
| OpenAI | Oui | `OPENAI_API_KEY` |
| Anthropic Claude | Oui | `ANTHROPIC_API_KEY` |
| DeepSeek | Oui | `DEEPSEEK_API_KEY` |
| Groq | Oui | `GROQ_API_KEY` |
| Google Gemini | Oui | `GEMINI_API_KEY`, `GOOGLE_GENERATIVE_AI_API_KEY` |
| Perplexity | Oui | `PERPLEXITY_API_KEY` |
| Mistral | Oui | `MISTRAL_API_KEY` |
| Cohere | Oui | `COHERE_API_KEY` |
| Together AI | Oui | `TOGETHER_API_KEY` |
| OpenRouter | Oui | `OPEN_ROUTER_API_KEY` |
| Ollama (local) | Oui | `OLLAMA_BASE_URL` |

### 7.3 Databases

| Service | Configure | Variables Env |
|---------|-----------|---------------|
| PostgreSQL | Oui | `POSTGRES_URL`, `POSTGRES_PASSWORD` |
| Supabase | Oui | `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` |
| Redis | Oui | `REDIS_URL` |
| Qdrant | Oui | `QDRANT_HOST`, `QDRANT_PORT` |
| Meilisearch | Oui | `MEILI_URL`, `MEILI_MASTER_KEY` |

### 7.4 Services Externes

| Service | Configure | Usage |
|---------|-----------|-------|
| Twilio SMS | Oui | Notifications SMS |
| Twilio WhatsApp | Oui | Messages WhatsApp |
| Google OAuth | Oui | Authentification |
| n8n | Oui | Workflows automation |
| Replicate | Oui | Generation images/videos |
| ElevenLabs | Oui | TTS premium |
| Stability AI | Oui | Generation images |

---

## 8. Modeles de Donnees

### 8.1 RAG-DZ (PostgreSQL)

| Table | Description |
|-------|-------------|
| `users` | Utilisateurs avec auth bcrypt |
| `user_tiers` | Abonnements (free/student/pro/enterprise) |
| `llm_usage_logs` | Tracking usage LLM pour billing |
| `payment_transactions` | Historique paiements Chargily |
| `projects` | Projets utilisateurs |
| `knowledge_base` | Base de connaissances RAG |
| `orchestrator_state` | Etat orchestrateur workflows |
| `bmad_workflows` | Workflows BMAD |
| `tenants` | Multi-tenant RLS |
| `tokens` | Systeme tokens |
| `personal_lexicon` | Lexique personnel |
| `geneva_multicultural` | Donnees Suisse |
| `life_operations` | Operations vie |

### 8.2 IAFactory Academy (Supabase)

| Table | Description |
|-------|-------------|
| `users` | Utilisateurs (UUID, roles) |
| `courses` | Cours avec pricing CHF |
| `modules` | Modules de cours |
| `lessons` | Lecons (video, text, quiz) |
| `enrollments` | Inscriptions |
| `progress` | Progression apprenants |
| `payments` | Paiements Stripe |
| `certificates` | Certificats generes |
| `resources` | Ressources pedagogiques |
| `reviews` | Avis et notes |
| `bookmarks` | Favoris utilisateurs |

---

## 9. Variables d'Environnement Requises

### Obligatoires (Production)

```env
# Securite
API_SECRET_KEY=           # Min 32 caracteres
POSTGRES_PASSWORD=        # Password fort

# Database
POSTGRES_URL=             # Connection string complete
SUPABASE_URL=             # URL projet Supabase
SUPABASE_SERVICE_KEY=     # Cle service Supabase

# LLM (au moins un)
ANTHROPIC_API_KEY=        # Recommande pour production
OPENAI_API_KEY=           # Alternative

# Paiement
CHARGILY_API_KEY=         # Pour Algerie
CHARGILY_SECRET_KEY=
```

### Optionnelles

```env
# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Multi-LLM
DEEPSEEK_API_KEY=
GROQ_API_KEY=
GEMINI_API_KEY=
PERPLEXITY_API_KEY=

# Notifications
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# Video Generation
REPLICATE_API_KEY=
ELEVENLABS_API_KEY=
```

---

## 10. Points d'Attention

### Securite

| Issue | Severite | Action |
|-------|----------|--------|
| Cles API exposees dans docs | CRITIQUE | Rotation immediate requise |
| Password admin par defaut | HAUTE | Changer avant prod |
| CORS permissif (*) en dev | MOYENNE | Configurer pour prod |

### Code

| Issue | Localisation | Impact |
|-------|--------------|--------|
| Parsers GOV incomplets | `browser-automation/agents/` | Agents non fonctionnels |
| Tests unitaires manquants | Plusieurs services | Qualite non verifiee |
| Documentation API incomplete | `services/api/` | Integration difficile |

### Infrastructure

| Issue | Impact | Recommandation |
|-------|--------|----------------|
| Multi-tenant RLS partiel | Isolation donnees | Completer policies |
| Monitoring non configure | Visibilite | Activer Grafana |
| Backups non automatises | Perte donnees | Configurer cron |

---

## 11. Recommandations Immediates

### A Reutiliser Tel Quel

| Element | Raison |
|---------|--------|
| Service Chargily | Complet et fonctionnel |
| Schema DB Academy | RLS configure, production-ready |
| Multi-LLM Router | 10+ providers supportes |
| Templates agents IA | Bonne base reutilisable |
| Docker Compose configs | Multi-environnement configure |

### Necessite Refactoring

| Element | Action |
|---------|--------|
| Agents GOV | Completer parsers, ajouter tests |
| Services backend | Unifier patterns, ajouter validation |
| Frontend IA Factory UI | Migration Next.js 14, cleanup |

### A Creer

| Element | Priorite |
|---------|----------|
| Tests E2E | Haute |
| Documentation API OpenAPI | Haute |
| CI/CD pipeline complet | Moyenne |
| Monitoring/Alerting | Moyenne |
| Agents GOV supplementaires (CASNOS, CNRC, Impots) | Basse |

---

## 12. Arborescence Simplifiee

```
IAFactory/
├── .claude/                    # Config Claude Code
├── _archive/                   # Anciennes versions
│   ├── bmad-agent/
│   ├── bolt-diy-fresh/
│   ├── Helvetia/
│   └── iafactory-video-studio/
├── BACKUPS/                    # Sauvegardes
├── docker-compose/             # Configs Docker multi-env
│   ├── docker-compose.algeria.yml
│   ├── docker-compose.algeria.prod.yml
│   ├── docker-compose.switzerland.yml
│   └── docker-compose.switzerland.prod.yml
├── iafactory-academy/          # E-learning platform
│   ├── backend/                # FastAPI
│   ├── frontend/               # React + Vite
│   ├── demo/                   # Demos (iafactory-chat, openwebui)
│   └── supabase/               # Migrations
├── iafactory-video-platform/   # Video generation
│   ├── backend/                # FastAPI + Celery
│   ├── frontend/               # React
│   └── infrastructure/         # Docker, monitoring
├── onestschooled/              # Laravel SaaS ecole
├── rag-dz/                     # Plateforme principale DZ
│   ├── agents/                 # 15+ agents IA
│   ├── apps/                   # 10+ apps verticales
│   ├── frontend/               # UIs React/Next.js
│   ├── infrastructure/         # Docker, SQL
│   ├── services/               # 10+ microservices
│   └── scripts/                # Utilitaires
└── [Documentation .md files]   # 15+ fichiers doc racine
```

---

## 13. Statistiques

| Metrique | Valeur |
|----------|--------|
| Sous-projets | 4 |
| Fichiers Python | ~500+ |
| Fichiers TypeScript/React | ~200+ |
| Tables DB definies | ~25+ |
| Agents IA | 15+ |
| Apps verticales | 10+ |
| Microservices | 10+ |
| LLM Providers | 11 |
| Migrations SQL | 20+ |
| Variables env | 80+ |

---

*Audit genere le 30 decembre 2025 par Claude Code*
