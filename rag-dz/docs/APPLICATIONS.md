# Catalogue des Applications - RAG-DZ / Nexus AI Platform

**Version:** 2.0.0
**Total Applications:** 27
**Dernière mise à jour:** Décembre 2024

---

## Vue d'ensemble

Le projet RAG-DZ (Nexus AI Platform) contient 27 applications intégrées, organisées par catégorie et niveau de maturité.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        NEXUS AI APPLICATIONS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                       PRODUCTION (10 apps)                           │    │
│  │  CRM-IA │ DZIRVideo │ IA-Chatbot │ Landing-Pro │ Video-Studio        │    │
│  │  Copilot │ IAFactory-Landing │ Chat-PDF │ Hybrid-Search │ Local-RAG  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                       BETA (10 apps)                                 │    │
│  │  API-Portal │ Dev-Portal │ IA-Notebook │ IA-Searcher │ IA-Voice      │    │
│  │  Ithy │ Legal-Assistant │ Marketing │ MCP-Dashboard │ Workflow-Studio│    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                       ALPHA (7 apps)                                 │    │
│  │  CAN2025 │ Cockpit │ Interview │ News │ SEO-DZ-Boost │ Sport         │    │
│  │  PME-Onboarding                                                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Légende des Statuts

| Statut | Description | Couleur |
|--------|-------------|---------|
| **Fonctionnel** | En production, entièrement opérationnel | 🟢 |
| **Partiel** | Beta, fonctionnalités de base opérationnelles | 🟡 |
| **Ébauche** | Alpha, en développement actif | 🔴 |
| **Template** | Modèle réutilisable | 🔵 |
| **Archivé** | Non maintenu | ⚫ |

---

## Applications par Catégorie

### 1. Applications IA Core

#### 1.1 IA Chatbot
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/ia-chatbot/` |
| **Statut** | 🟢 Fonctionnel |
| **Stack** | HTML + JavaScript + CSS |
| **Description** | Interface chatbot conversationnelle avec support multi-modèles |

**Fonctionnalités:**
- Chat en temps réel
- Historique de conversation
- Support markdown
- Export des conversations
- Intégration multi-LLM (OpenAI, Anthropic, Groq)

**Points d'entrée:**
```
apps/ia-chatbot/
├── index.html          # Interface principale
├── js/
│   ├── chat.js         # Logique chat
│   └── api.js          # Appels API
└── css/
    └── style.css       # Styles
```

---

#### 1.2 IA Voice
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/ia-voice/` |
| **Statut** | 🟡 Partiel |
| **Stack** | React + Whisper + ElevenLabs |
| **Description** | Assistant vocal avec STT (Speech-to-Text) et TTS (Text-to-Speech) |

**Fonctionnalités:**
- Transcription vocale (Whisper)
- Synthèse vocale (ElevenLabs, OpenAI TTS)
- Commandes vocales
- Mode conversation continue

---

#### 1.3 IA Searcher
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/ia-searcher/` |
| **Statut** | 🟡 Partiel |
| **Stack** | React + FastAPI + Qdrant |
| **Description** | Moteur de recherche sémantique augmenté par IA |

**Fonctionnalités:**
- Recherche sémantique vectorielle
- Recherche hybride (texte + vecteurs)
- Filtres avancés
- Résumés automatiques des résultats

---

#### 1.4 Ithy
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/ithy/` |
| **Statut** | 🟡 Partiel |
| **Stack** | Next.js + FastAPI |
| **Description** | Agrégateur de modèles IA - interface unifiée pour tous les LLMs |

**Fonctionnalités:**
- Comparaison de modèles
- Routing intelligent
- Benchmarking automatique
- Gestion des coûts par modèle

---

#### 1.5 IA Notebook
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/ia-notebook/` |
| **Statut** | 🟡 Partiel |
| **Stack** | React + FastAPI |
| **Description** | Clone de NotebookLM - génération de podcasts et résumés à partir de documents |

**Fonctionnalités:**
- Upload de documents (PDF, DOCX, TXT)
- Génération de résumés
- Création de podcasts audio
- Q&A sur documents

---

### 2. Applications Business

#### 2.1 CRM-IA
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/crm-ia/` |
| **Statut** | 🟢 Fonctionnel |
| **Stack** | FastAPI + SQLite + React |
| **Description** | CRM intelligent pour PME avec assistance IA |

**Fonctionnalités:**
- Gestion contacts et entreprises
- Pipeline de ventes
- Scoring leads automatique
- Suggestions IA de next-best-action
- Rapports et analytics

**API Endpoints:**
```
POST   /api/contacts          # Créer un contact
GET    /api/contacts          # Lister les contacts
PUT    /api/contacts/{id}     # Modifier un contact
DELETE /api/contacts/{id}     # Supprimer un contact
POST   /api/ai/score-lead     # Scorer un lead
POST   /api/ai/suggest-action # Suggestion d'action
```

---

#### 2.2 PME-DZ Suite
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/pme-dz/` |
| **Statut** | 🟡 Partiel |
| **Stack** | Multiple |
| **Description** | Suite d'outils pour PME algériennes |

**Sous-applications:**

| App | Chemin | Statut | Description |
|-----|--------|--------|-------------|
| Copilot | `pme-dz/copilot/` | 🟢 Fonctionnel | Assistant IA pour décisions business |
| Growth | `pme-dz/growth/` | 🟡 Partiel | Analytics et croissance |
| Onboarding | `pme-dz/onboarding/` | 🔴 Ébauche | Onboarding clients |

---

#### 2.3 Legal Assistant
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/legal-assistant/` |
| **Statut** | 🟡 Partiel |
| **Stack** | FastAPI + RAG |
| **Description** | Assistant juridique spécialisé droit algérien |

**Fonctionnalités:**
- Recherche dans les textes de loi DZ
- Génération de contrats
- Conseil juridique IA
- Base de connaissances juridique

---

### 3. Applications Vidéo

#### 3.1 DZIRVideo
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/dzirvideo/` |
| **Statut** | 🟢 Fonctionnel |
| **Stack** | Python + FFmpeg + Multi-AI |
| **Description** | Génération vidéo automatisée avec multi-providers |

**Fonctionnalités:**
- Génération de scripts
- Génération d'images (DALL-E, Flux, SDXL)
- Génération de vidéos (Runway, Pika, Luma)
- Voix off (ElevenLabs, OpenAI TTS)
- Montage automatique FFmpeg
- Export multi-format

**Pipeline:**
```
apps/dzirvideo/
├── src/
│   ├── pipeline.py           # Pipeline principal
│   ├── pipeline_v2.py        # Pipeline V2
│   ├── generators/
│   │   ├── image_generator.py
│   │   ├── video_generator.py
│   │   └── audio_generator.py
│   └── processors/
│       └── ffmpeg_processor.py
└── config/
    └── providers.yaml        # Configuration providers
```

---

#### 3.2 Video Studio
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/video-studio/` |
| **Statut** | 🟢 Fonctionnel |
| **Stack** | FastAPI + Next.js |
| **Description** | Studio de production vidéo professionnel |

**Fonctionnalités:**
- Interface timeline visuelle
- Preview en temps réel
- Multi-pistes audio/vidéo
- Effets et transitions
- Export haute qualité

---

### 4. Applications Marketing & Landing

#### 4.1 IAFactory Landing
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/iafactory-landing/` |
| **Statut** | 🟢 Fonctionnel |
| **Stack** | HTML + CSS + JS |
| **Description** | Landing page principale IAFactory |

---

#### 4.2 Landing Pro
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/landing-pro/` |
| **Statut** | 🟢 Fonctionnel |
| **Stack** | Next.js + i18n |
| **Description** | Landing page multilingue professionnelle |

**Fonctionnalités:**
- Support FR/AR/EN
- SEO optimisé
- Analytics intégrés
- A/B testing

---

#### 4.3 Marketing
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/marketing/` |
| **Statut** | 🟡 Partiel |
| **Stack** | React + Vite |
| **Description** | Outils marketing automation |

---

### 5. Applications Développeur

#### 5.1 API Portal
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/api-portal/` |
| **Statut** | 🟡 Partiel |
| **Stack** | React + FastAPI |
| **Description** | Portail de gestion des clés API pour développeurs |

**Fonctionnalités:**
- Génération de clés API
- Dashboard usage
- Documentation interactive
- Rate limiting

---

#### 5.2 Dev Portal
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/dev-portal/` |
| **Statut** | 🟡 Partiel |
| **Stack** | React |
| **Description** | Portail documentation développeurs |

---

#### 5.3 MCP Dashboard
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/mcp-dashboard/` |
| **Statut** | 🟡 Partiel |
| **Stack** | React |
| **Description** | Dashboard de gestion des serveurs MCP (Model Context Protocol) |

---

### 6. Applications Spécialisées

#### 6.1 Prompt Creator
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/prompt-creator/` |
| **Statut** | 🟡 Partiel |
| **Stack** | React |
| **Description** | Générateur et optimiseur de prompts IA |

---

#### 6.2 Workflow Studio
| Attribut | Valeur |
|----------|--------|
| **Chemin** | `apps/workflow-studio/` |
| **Statut** | 🟡 Partiel |
| **Stack** | React + ReactFlow |
| **Description** | Éditeur visuel de workflows IA |

**Fonctionnalités:**
- Éditeur drag-and-drop
- Connexion de nœuds
- Exécution de workflows
- Export/Import

---

### 7. Applications en Développement

| App | Chemin | Statut | Description |
|-----|--------|--------|-------------|
| CAN 2025 | `apps/can2025/` | 🔴 Ébauche | Application CAN 2025 Algérie |
| Cockpit | `apps/cockpit/` | 🔴 Ébauche | Dashboard monitoring global |
| Interview | `apps/interview/` | 🔴 Ébauche | Simulation d'entretiens |
| News | `apps/news/` | 🔴 Ébauche | Agrégateur de news IA |
| SEO DZ Boost | `apps/seo-dz-boost/` | 🔴 Ébauche | Optimisation SEO Algérie |
| Sport | `apps/sport/` | 🔴 Ébauche | Application sport IA |

---

## Services Backend Associés

| Service | Chemin | Description | Statut |
|---------|--------|-------------|--------|
| API Principale | `services/api/` | API REST FastAPI (90+ routers) | 🟢 |
| Browser Automation | `services/browser-automation/` | Agents Playwright | 🟡 |
| Connectors | `services/connectors/` | Connecteurs externes | 🟡 |
| Fiscal Assistant | `services/fiscal-assistant/` | Assistant fiscal DZ | 🟡 |
| Voice Assistant | `services/voice-assistant/` | STT/TTS Whisper | 🟡 |
| Billing | `services/backend/billing/` | Facturation Chargily | 🟢 |
| Key Service | `services/backend/key-service/` | Gestion clés API | 🟡 |

---

## Agents Associés

### Business Agents
| Agent | Fichier | Statut |
|-------|---------|--------|
| AI Consultant | `agents/business/consultant/ai_consultant_agent.py` | 🟢 |
| Customer Support | `agents/business/customer-support/customer_support_agent.py` | 🟢 |
| Data Analyst | `agents/business/data-analysis/ai_data_analyst.py` | 🟢 |

### RAG Agents
| Agent | Fichier | Statut |
|-------|---------|--------|
| Chat PDF | `agents/rag/chat-pdf/chat_pdf.py` | 🟢 |
| Hybrid Search | `agents/rag/hybrid-search/main.py` | 🟢 |
| Local RAG | `agents/rag/local-rag/local_rag_agent.py` | 🟢 |

### Specialized Agents
| Agent | Fichier | Statut |
|-------|---------|--------|
| Financial Coach | `agents/finance/financial_coach.py` | 🟢 |
| Legal Team | `agents/legal/legal_team.py` | 🟢 |
| Real Estate | `agents/real_estate/real_estate_team.py` | 🟢 |
| Recruitment | `agents/recruitment/recruitment_team.py` | 🟢 |
| Teaching | `agents/teaching/teaching_team.py` | 🟢 |
| Travel | `agents/travel/travel_agent.py` | 🟢 |

---

## Démarrage Rapide par Application

### CRM-IA
```bash
cd apps/crm-ia
pip install -r requirements.txt
uvicorn app:app --reload --port 8002
```

### DZIRVideo
```bash
cd apps/dzirvideo
pip install -r requirements.txt
python src/pipeline.py --input "Créer une vidéo sur l'IA"
```

### Video Studio
```bash
cd apps/video-studio

# Backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8003

# Frontend (nouveau terminal)
cd frontend && npm install && npm run dev
```

### IA Chatbot
```bash
# Simple - ouvrir dans un navigateur
cd apps/ia-chatbot
open index.html

# Ou avec un serveur local
python -m http.server 8080
```

---

## Configuration Commune

### Variables d'Environnement

Chaque application peut avoir son propre `.env`, mais les clés communes sont:

```bash
# LLM APIs
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
GROQ_API_KEY=gsk_xxx

# Base de données
DATABASE_URL=postgresql://user:pass@localhost:5432/nexus

# Redis
REDIS_URL=redis://localhost:6379

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx

# Stockage
S3_BUCKET=nexus-assets
S3_REGION=eu-west-3
```

---

## Ports par Défaut

| Application | Port | URL |
|-------------|------|-----|
| Meta-Orchestrator | 8100 | http://localhost:8100 |
| Archon Server | 8181 | http://localhost:8181 |
| Archon UI | 3737 | http://localhost:3737 |
| Bolt.diy | 5173 | http://localhost:5173 |
| API Principale | 8000 | http://localhost:8000 |
| CRM-IA | 8002 | http://localhost:8002 |
| Video Studio | 8003 | http://localhost:8003 |
| IA Chatbot | 8080 | http://localhost:8080 |

---

## Feuille de Route

### Q1 2025
- [ ] Stabiliser les 10 applications en production
- [ ] Compléter la documentation API
- [ ] Ajouter tests E2E

### Q2 2025
- [ ] Passer les 10 apps beta en production
- [ ] Unifier l'authentification
- [ ] Dashboard analytics global

### Q3 2025
- [ ] Compléter les apps en ébauche
- [ ] Application mobile
- [ ] Multi-tenant complet

---

## Contribution

Pour contribuer à une application:

1. Fork le repository
2. Créer une branche: `git checkout -b feature/app-name/feature-description`
3. Commiter: `git commit -m "feat(app-name): description"`
4. Push et créer une PR

---

*Catalogue généré le 31 décembre 2024*
