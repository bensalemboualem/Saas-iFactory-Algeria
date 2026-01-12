# INVENTAIRE IA FACTORY - 30 Decembre 2025

---

## RAG-DZ (Projet Principal)

### Applications (27 trouvees)

| # | Nom | Chemin | Description | Statut |
|---|-----|--------|-------------|--------|
| 1 | API Portal | `apps/api-portal/` | Portail gestion cles API developpeurs | Partiel |
| 2 | CAN 2025 | `apps/can2025/` | Application CAN 2025 Algerie | Ebauche |
| 3 | Cockpit | `apps/cockpit/` | Dashboard monitoring | Ebauche |
| 4 | CRM IA | `apps/crm-ia/` | CRM avec IA pour PME (FastAPI+SQLite) | Fonctionnel |
| 5 | Dev Portal | `apps/dev-portal/` | Portail developpeurs | Partiel |
| 6 | DZIRVideo | `apps/dzirvideo/` | Generation video IA (multi-generateurs) | Fonctionnel |
| 7 | IA Agents | `apps/ia-agents/` | Hub agents IA | Partiel |
| 8 | IA Chatbot | `apps/ia-chatbot/` | Chatbot IA (HTML+JS) | Fonctionnel |
| 9 | IAFactory Landing | `apps/iafactory-landing/` | Landing page principale | Fonctionnel |
| 10 | IA Notebook | `apps/ia-notebook/` | Clone NotebookLM | Partiel |
| 11 | IA Searcher | `apps/ia-searcher/` | Moteur recherche IA | Partiel |
| 12 | IA Voice | `apps/ia-voice/` | Assistant vocal STT/TTS | Partiel |
| 13 | Interview | `apps/interview/` | Outil simulation entretiens | Ebauche |
| 14 | Ithy | `apps/ithy/` | Agregateur modeles IA | Partiel |
| 15 | Landing Pro | `apps/landing-pro/` | Landing page pro (i18n) | Fonctionnel |
| 16 | Legal Assistant | `apps/legal-assistant/` | Assistant juridique DZ | Partiel |
| 17 | Marketing | `apps/marketing/` | App marketing (React+Vite) | Partiel |
| 18 | MCP Dashboard | `apps/mcp-dashboard/` | Dashboard MCP serveurs | Partiel |
| 19 | News | `apps/news/` | Agregateur news IA | Ebauche |
| 20 | PME-DZ | `apps/pme-dz/` | Suite PME (5 sous-apps) | Partiel |
| 21 | PME-DZ/Copilot | `apps/pme-dz/copilot/` | Copilot PME | Fonctionnel |
| 22 | PME-DZ/Growth | `apps/pme-dz/growth/` | Growth Grid analytics | Partiel |
| 23 | PME-DZ/Onboarding | `apps/pme-dz/onboarding/` | Onboarding PME | Ebauche |
| 24 | Prompt Creator | `apps/prompt-creator/` | Generateur prompts IA | Partiel |
| 25 | SEO DZ Boost | `apps/seo-dz-boost/` | Optimisation SEO Algerie | Ebauche |
| 26 | Sport | `apps/sport/` | App sport IA | Ebauche |
| 27 | Video Studio | `apps/video-studio/` | Studio video IA (FastAPI+Next.js) | Fonctionnel |
| 28 | Workflow Studio | `apps/workflow-studio/` | Editeur workflows visuels | Partiel |
| - | _archived | `apps/_archived/` | Apps archivees (3+) | Archive |

### Services Backend (10 trouves)

| # | Service | Chemin | Description | Statut |
|---|---------|--------|-------------|--------|
| 1 | API Principale | `services/api/` | API REST FastAPI (90+ routers) | Fonctionnel |
| 2 | Browser Automation | `services/browser-automation/` | Agents Playwright (CNAS, Sonelgaz) | Partiel |
| 3 | Connectors | `services/connectors/` | Connecteurs services externes | Partiel |
| 4 | Data Dashboard | `services/data-dashboard/` | Dashboard analytics | Ebauche |
| 5 | Fiscal Assistant | `services/fiscal-assistant/` | Assistant fiscal DZ | Partiel |
| 6 | Legal Assistant | `services/legal-assistant/` | Assistant juridique DZ | Partiel |
| 7 | Voice Assistant | `services/voice-assistant/` | STT/TTS Whisper | Partiel |
| 8 | Backend/Billing | `services/backend/billing/` | Systeme facturation Chargily | Fonctionnel |
| 9 | Backend/Key-Service | `services/backend/key-service/` | Gestion cles API (Node.js) | Partiel |
| 10 | Backend/Voice-Agent | `services/backend/voice-agent/` | Transcription Whisper | Partiel |

### Agents (40+ trouves)

| # | Categorie | Nom | Fichier | Statut |
|---|-----------|-----|---------|--------|
| **BUSINESS** |
| 1 | Business | Consultant | `agents/business/consultant/agent.py` | Fonctionnel |
| 2 | Business | AI Consultant | `agents/business/consultant/ai_consultant_agent.py` | Fonctionnel |
| 3 | Business | Customer Support | `agents/business/customer-support/customer_support_agent.py` | Fonctionnel |
| 4 | Business | Data Analyst | `agents/business/data-analysis/ai_data_analyst.py` | Fonctionnel |
| **FINANCE** |
| 5 | Finance | Financial Coach | `agents/finance/financial_coach.py` | Fonctionnel |
| 6 | Finance | Investment Agent | `agents/templates/finance-startups/ai_investment_agent/` | Template |
| 7 | Finance | Startup Trends | `agents/templates/finance-startups/ai_startup_trend_analysis_agent/` | Template |
| 8 | Finance | Deep Research | `agents/templates/finance-startups/ai_deep_research_agent/` | Template |
| 9 | Finance | System Architect | `agents/templates/finance-startups/ai_system_architect_r1/` | Template |
| **LEGAL** |
| 10 | Legal | Legal Team | `agents/legal/legal_team.py` | Fonctionnel |
| **REAL ESTATE** |
| 11 | Real Estate | Real Estate Team | `agents/real_estate/real_estate_team.py` | Fonctionnel |
| **RECRUITMENT** |
| 12 | Recruitment | Recruitment Team | `agents/recruitment/recruitment_team.py` | Fonctionnel |
| 13 | Recruitment | Recruteur DZ | `agents/recruteur-dz/` | Ebauche |
| **TEACHING** |
| 14 | Teaching | Teaching Team | `agents/teaching/teaching_team.py` | Fonctionnel |
| **TRAVEL** |
| 15 | Travel | Travel Agent | `agents/travel/travel_agent.py` | Fonctionnel |
| **RAG** |
| 16 | RAG | Chat PDF | `agents/rag/chat-pdf/chat_pdf.py` | Fonctionnel |
| 17 | RAG | Financial Coach | `agents/rag/finance-agent/ai_financial_coach_agent.py` | Fonctionnel |
| 18 | RAG | Hybrid Search | `agents/rag/hybrid-search/main.py` | Fonctionnel |
| 19 | RAG | Local RAG | `agents/rag/local-rag/local_rag_agent.py` | Fonctionnel |
| 20 | RAG | Voice Support | `agents/rag/voice-support/customer_support_voice_agent.py` | Fonctionnel |
| **PRODUCTIVITY** |
| 21 | Productivity | Journalist | `agents/templates/productivity/journalist/` | Template |
| 22 | Productivity | Meeting | `agents/templates/productivity/meeting/` | Template |
| 23 | Productivity | Product Launch | `agents/templates/productivity/product-launch/` | Template |
| 24 | Productivity | Web Scraping | `agents/templates/productivity/web-scraping/` | Template |
| 25 | Productivity | XAI Finance | `agents/templates/productivity/xai-finance/` | Template |
| **RAG APPS** |
| 26 | RAG Apps | Agentic RAG | `agents/templates/rag-apps/agentic_rag_with_reasoning/` | Template |
| 27 | RAG Apps | Autonomous RAG | `agents/templates/rag-apps/autonomous_rag/` | Template |
| 28 | RAG Apps | Hybrid Search | `agents/templates/rag-apps/hybrid_search_rag/` | Template |
| 29 | RAG Apps | Local RAG | `agents/templates/rag-apps/local_rag_agent/` | Template |
| 30 | RAG Apps | RAG as Service | `agents/templates/rag-apps/rag-as-a-service/` | Template |
| **OPERATEURS** |
| 31 | Operator | IAFactory Operator | `agents/iafactory-operator/` | Fonctionnel |
| 32 | Operator | Video Operator | `agents/video-operator/` | Fonctionnel |
| **CORE** |
| 33 | Core | Base Agent | `agents/core/base_agent.py` | Fonctionnel |
| **API SERVICES** |
| 34 | API | Email Agent | `services/api/app/services/email_agent_service.py` | Fonctionnel |
| 35 | API | Voice AI Agent | `services/api/app/services/voice_ai_agent.py` | Partiel |
| 36 | API | Super Agent Polva | `services/api/app/services/super_agent_polva.py` | Partiel |
| 37 | API | Agent Memory | `services/api/app/services/agent_memory.py` | Fonctionnel |
| **ARCHON** |
| 38 | Archon | Base Agent | `frontend/archon-ui/python/src/agents/base_agent.py` | Fonctionnel |
| 39 | Archon | Document Agent | `frontend/archon-ui/python/src/agents/document_agent.py` | Fonctionnel |
| 40 | Archon | RAG Agent | `frontend/archon-ui/python/src/agents/rag_agent.py` | Fonctionnel |

### Workflows/Pipelines (15+ trouves)

| # | Nom | Chemin | Description | Statut |
|---|-----|--------|-------------|--------|
| 1 | DZIRVideo Pipeline | `apps/dzirvideo/src/pipeline.py` | Pipeline generation video | Fonctionnel |
| 2 | DZIRVideo Pipeline V2 | `apps/dzirvideo/src/pipeline_v2.py` | Pipeline video v2 | Fonctionnel |
| 3 | Video Studio Pipeline | `apps/video-studio/backend/app/api/routes/pipeline.py` | API pipeline video | Fonctionnel |
| 4 | IAFactory Operator | `agents/iafactory-operator/pipeline/` | Analyzer, Executor, Planner | Fonctionnel |
| 5 | BMAD Workflows | `bmad/src/core/workflows/` | Brainstorming, Party Mode | Template |
| 6 | BMAD Workflow Builder | `bmad/src/modules/bmb/agents/workflow-builder.agent.yaml` | Constructeur workflows | Template |
| 7 | Landing Workflows | `apps/landing-pro/api/workflows/` | Workflows landing | Partiel |
| 8 | Workflow Studio | `apps/workflow-studio/` | Editeur visuel | Partiel |
| 9 | GitHub Actions | `.github/workflows/` | CI/CD | Fonctionnel |

### Modules Video (6 trouves)

| # | Nom | Chemin | Description | Statut |
|---|-----|--------|-------------|--------|
| 1 | DZIRVideo | `apps/dzirvideo/` | Generation complete (DALL-E, Sora, etc) | Fonctionnel |
| 2 | Video Studio | `apps/video-studio/` | Studio pro (FastAPI+Next.js) | Fonctionnel |
| 3 | Video Operator Agent | `agents/video-operator/` | Agent orchestration video | Fonctionnel |
| 4 | Frontend Video Studio | `frontend/video-studio/` | UI React video studio | Partiel |
| 5 | IA Factory UI Video | `frontend/ia-factory-ui/app/[locale]/video-studio/` | Page video dans UI principale | Partiel |
| 6 | Archived DZIRVideo AI | `apps/_archived/dzirvideo-ai/` | Version archivee | Archive |

### Frontends (5 trouves)

| # | Nom | Chemin | Stack | Statut |
|---|-----|--------|-------|--------|
| 1 | IA Factory UI | `frontend/ia-factory-ui/` | Next.js 14, React, i18n | Fonctionnel |
| 2 | Archon UI | `frontend/archon-ui/` | React + Python backend | Fonctionnel |
| 3 | RAG UI | `frontend/rag-ui/` | React | Partiel |
| 4 | Video Studio | `frontend/video-studio/` | React | Partiel |
| 5 | Shared Components | `frontend/shared/` | Composants partages | Partiel |

---

## IAFACTORY-ACADEMY

| Attribut | Valeur |
|----------|--------|
| **Stack** | FastAPI + React 18 + Vite + TailwindCSS |
| **Database** | PostgreSQL (Supabase) |
| **Paiement** | Stripe |
| **Auth** | JWT avec refresh tokens |
| **Completion** | ~85% |

### Fonctionnalites Implementees
- Gestion cours (CRUD complet)
- Modules et lecons hierarchiques
- Authentification JWT
- Paiements Stripe
- Certificats automatiques
- Progression tracking
- API RESTful documentee (Swagger)
- Upload S3
- Notifications email (SendGrid)
- Cache Redis
- Celery workers

### Fonctionnalites Manquantes
- Tests E2E
- Monitoring production
- Analytics avances
- Mobile app

### Modules Backend
| Module | Fichiers | Statut |
|--------|----------|--------|
| API | `api/` (auth, certificates, content, courses, enrollments, payments, rag, users) | Complet |
| Models | `models/` (content, course, enrollment, payment, resource, user) | Complet |
| Schemas | `schemas/` (base, content, course, enrollment, payment, resource, user) | Complet |
| Services | `services/` (auth, certificate, content, course, enrollment, payment, progress, rag/, user) | Complet |
| Tasks | `tasks/` (email_tasks) | Complet |

---

## ONESTSCHOOL

| Attribut | Valeur |
|----------|--------|
| **Stack** | Laravel (PHP 7.4+) + jQuery + Bootstrap 4 |
| **Type** | ERP ecole achete (Onest Drax) |
| **Database** | MySQL |
| **Completion** | ~95% (produit commercial) |

### Modules Integres
| Module | Description | Statut |
|--------|-------------|--------|
| Forums | Forums discussion | Inclus |
| Installer | Installation automatique | Inclus |
| LiveChat | Chat temps reel | Inclus |
| MainApp | Application principale | Inclus |
| MultiBranch | Multi-ecoles | Inclus |
| PushNotification | Notifications push | Inclus |

### Customisations IA Factory
| Customisation | Fichier | Statut |
|---------------|---------|--------|
| Chatbot BBC School | `BBCSchoolChatbotController.php` | Fonctionnel |
| Chatbot General | `ChatbotController.php` | Fonctionnel |
| OnestSchool AI | `OnestSchoolAIController.php` | Fonctionnel |
| Knowledge Base Seeder | `KnowledgeBaseSeeder.php` | Fonctionnel |
| Instagram Integration | `InstagramController.php` | Partiel |

### Integration IA Factory
- **API IA connectee**: Oui (via controllers custom)
- **DB partagee**: Non (MySQL separe)
- **Auth partagee**: Non

---

## IAFACTORY-VIDEO-PLATFORM

| Attribut | Valeur |
|----------|--------|
| **Stack** | FastAPI + Next.js 15 + React 19 + TailwindCSS |
| **Database** | PostgreSQL |
| **Queue** | Redis + Celery |
| **Video** | FFmpeg |
| **Completion** | ~70% |

### Fonctionnalites Implementees
- Creation NLP (description naturelle)
- Script IA (generation automatique)
- Multi-providers IA
- Montage automatique FFmpeg
- Publication multi-plateforme (API)
- Agents orchestration

### Fonctionnalites Manquantes
- UI complete frontend
- Tests E2E
- Monitoring
- Documentation utilisateur

### Agents Video
| Agent | Fichier | Fonction | Statut |
|-------|---------|----------|--------|
| Avatar Agent | `agents/avatar_agent.py` | Generation avatars | Partiel |
| Image Agent | `agents/image_agent.py` | Generation images | Fonctionnel |
| Montage Agent | `agents/montage_agent.py` | Montage video | Partiel |
| Orchestrator | `agents/orchestrator.py` | Orchestration pipeline | Fonctionnel |
| Publish Agent | `agents/publish_agent.py` | Publication reseaux | Partiel |
| Script Agent | `agents/script_agent.py` | Generation scripts | Fonctionnel |
| Video Agent | `agents/video_agent.py` | Generation video | Partiel |
| Voice Agent | `agents/voice_agent.py` | TTS/STT | Fonctionnel |

### Providers IA Configures
| Categorie | Providers |
|-----------|-----------|
| LLM | OpenAI, Anthropic, Groq, DeepSeek, Mistral, Google |
| Images | DALL-E 3, Flux, SDXL, Leonardo, Ideogram |
| Videos | Runway Gen-3, Pika Labs, Luma, Kling |
| Avatars | HeyGen, D-ID, Synthesia, SadTalker |
| Audio | ElevenLabs, OpenAI TTS, Whisper |
| Musique | Suno, Udio, MusicGen |

---

## Relations Entre Projets

### Partage de Code

| Source | Cible | Type | Details |
|--------|-------|------|---------|
| rag-dz | iafactory-academy | Reference | Imports dans anythingllm scripts |
| rag-dz | iafactory-video-platform | Reference | Config paths |
| rag-dz agents | rag-dz services | Import | Agents utilises par API |

### Bases de Donnees

| Projet | Database | Partage |
|--------|----------|---------|
| rag-dz | PostgreSQL + Supabase | Principal |
| iafactory-academy | PostgreSQL (Supabase) | Separe |
| onestschooled | MySQL | Separe |
| iafactory-video-platform | PostgreSQL | Separe |

### Authentification

| Projet | Methode | Partage |
|--------|---------|---------|
| rag-dz | JWT + API Keys | Principal |
| iafactory-academy | JWT | Separe |
| onestschooled | Laravel Session | Separe |
| iafactory-video-platform | JWT | Potentiel partage |

### Services Communs

| Service | Projets Utilisant |
|---------|-------------------|
| Chargily (Paiement DZ) | rag-dz |
| Stripe | iafactory-academy |
| OpenAI | Tous |
| Anthropic | Tous |
| Redis | rag-dz, iafactory-academy, iafactory-video-platform |
| PostgreSQL | rag-dz, iafactory-academy, iafactory-video-platform |

---

## Statistiques Globales

| Metrique | RAG-DZ | Academy | OneStSchool | Video Platform | Total |
|----------|--------|---------|-------------|----------------|-------|
| Apps/Modules | 27 | 1 | 6 | 1 | 35 |
| Agents | 40+ | 0 | 3 | 8 | 51+ |
| Services Backend | 10 | 1 | 1 | 1 | 13 |
| Fichiers Python | ~400 | ~50 | 0 | ~50 | ~500 |
| Fichiers PHP | 0 | 0 | ~200 | 0 | ~200 |
| Fichiers TS/TSX | ~100 | ~50 | 0 | ~30 | ~180 |
| Fichiers .env | 10+ | 5 | 1 | 2 | 18+ |

---

## Points Cles pour Decision Strategique

### Option A: Ameliorer RAG-DZ

**POUR:**
- 27 apps deja en place
- 40+ agents fonctionnels
- Chargily integre
- Stack maitrisee (FastAPI)
- 10 services backend

**CONTRE:**
- Code heterogene (HTML+JS, React, Next.js)
- Documentation incomplete
- Tests manquants
- Certains apps en ebauche

### Option B: Nouveau Projet + Pont

**POUR:**
- Architecture propre
- Separation claire
- Standards modernes

**CONTRE:**
- Duplication massive
- 40+ agents a remigrer
- 27 apps a reconstruire

### Option C: Hybride (Recommande)

**POUR:**
- RAG-DZ = Frontend/Apps (conserve)
- Nouveau Nexus = Backend unifie
- Migration progressive
- Agents reutilisables

**CONTRE:**
- Complexite temporaire
- 2 stacks en parallele

---

*Inventaire genere le 30 decembre 2025 par Claude Code*
