# 🔍 AUDIT GLOBAL - RAG-DZ / IAFactory SaaS Platform

**Date**: 20 Décembre 2024  
**Analysé par**: Claude Opus 4.5  
**Périmètre**: apps/, agents/, services/, workflows/, core/, infrastructure/

---

## 📊 RÉSUMÉ EXÉCUTIF

| Métrique | Valeur |
|----------|--------|
| **Applications** | 40 (27 HTML, 6 Next.js, 2 React/Vite, 5 Full-Stack) |
| **Agents IA** | 15 répertoires, 25+ sous-agents |
| **Services Backend** | 8 services FastAPI |
| **Workflows** | 3 (delivery, sales, support) |
| **Containers Docker VPS** | 50+ actifs |
| **Domaines actifs** | ~15 (iafactoryalgeria.com, iafactory.ch, etc.) |

---

## ⚠️ TABLEAU DE PRIORITÉS

### 🔴 P0 - CRITIQUE (À faire immédiatement)

| # | Problème | Localisation | Impact | Action |
|---|----------|--------------|--------|--------|
| 1 | **Duplication massive** | `services/backend/rag-compat/` | 216/219 fichiers identiques à `services/api/` (98%) | SUPPRIMER le dossier |
| 2 | **node_modules commité** | `apps/video-studio/frontend/` | 700MB+ dans le repo | Supprimer + .gitignore |
| 3 | **Secrets exposés** | `apps/interview/.env.local` | Credentials en clair | Supprimer + .gitignore |
| 4 | **TODO sécurité** | `services/api/app/billing/` | Signature non implémentée | Implémenter ou désactiver |
| 5 | **Admin key hardcodée** | `services/api/app/main.py` | Risque d'accès non autorisé | Externaliser en .env |

### 🟠 P1 - IMPORTANT (Semaine 1-2)

| # | Problème | Localisation | Impact | Action |
|---|----------|--------------|--------|--------|
| 6 | **22 apps vides** | `apps/{commerce,douanes,education,...}` | Confusion, bruit | Archiver dans `apps/_archived/` |
| 7 | **3 shared/ dispersés** | `apps/shared/`, `services/shared/`, `shared/` | Duplication logique | Consolider en `packages/shared/` |
| 8 | **13 docker-compose** | `infrastructure/docker/` | Maintenance impossible | Réduire à 3 fichiers max |
| 9 | **65% apps sans README** | Multiples | Onboarding difficile | Générer README template |
| 10 | **Conventions mixtes** | `~20 fichiers Python en kebab-case` | Incohérence | Renommer en snake_case |

### 🟡 P2 - AMÉLIORATION (Semaine 3-4)

| # | Problème | Localisation | Impact | Action |
|---|----------|--------------|--------|--------|
| 11 | **97.5% apps sans tests** | Toutes sauf api/ | Régression risquée | Ajouter tests critiques |
| 12 | **3 frameworks agents** | BaseAgent, ADK, Agno | Fragmentation | Créer adaptateur unifié |
| 13 | **LLM hardcodés** | 12 agents | Pas de switch provider | Injection de dépendance |
| 14 | **Prompts inline** | Agents | Pas de versioning | Externaliser en .md |
| 15 | **CSS dupliqué** | 6 locations | Maintenance difficile | Centraliser iafactory-unified.css |

---

## 🏗️ ARCHITECTURE ACTUELLE

```
┌─────────────────────────────────────────────────────────────────┐
│                        VPS 46.224.3.125                         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    NGINX (Reverse Proxy)                 │   │
│  │  *.iafactoryalgeria.com  |  *.iafactory.ch  |  api.*    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│  ┌───────────┬───────────┬───────────┬───────────┬──────────┐  │
│  │ marketing │ video-std │ bolt-diy  │ api       │ whisper  │  │
│  │ (static)  │ (Next.js) │ (bolt.new)│ (FastAPI) │ (AI)     │  │
│  └───────────┴───────────┴───────────┴───────────┴──────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              DATABASES & STORAGE                         │   │
│  │  PostgreSQL │ MongoDB │ Redis │ Qdrant │ MinIO          │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 INVENTAIRE DÉTAILLÉ

### 🖥️ Applications (40)

#### ✅ Apps Production-Ready (8)
| App | Stack | Tests | README | Status |
|-----|-------|-------|--------|--------|
| `video-studio` | Next.js 14 + FastAPI | ✅ | ✅ | 🟢 Prod |
| `marketing` | React/Vite | ❌ | ✅ | 🟢 Prod |
| `can2025` | Next.js | ❌ | ✅ | 🟢 Prod |
| `news` | Next.js | ❌ | ✅ | 🟢 Prod |
| `sport` | Next.js | ❌ | ✅ | 🟢 Prod |
| `dzirvideo` | Full-Stack | ❌ | ✅ | 🟡 Beta |
| `ia-agents` | Next.js | ❌ | ✅ | 🟡 Beta |
| `crm-ia` | Full-Stack | ❌ | ✅ | 🟡 Beta |

#### ⚠️ Apps En Développement (10)
| App | Stack | Notes |
|-----|-------|-------|
| `prompt-creator` | React | Interface fonctionnelle |
| `ia-notebook` | React | Jupyter-like |
| `ia-chatbot` | HTML/JS | Basique |
| `ia-searcher` | HTML/JS | POC |
| `ia-voice` | HTML/JS | POC |
| `interview` | Next.js | **⚠️ .env.local exposé** |
| `api-portal` | HTML | Documentation |
| `dev-portal` | HTML | Documentation |
| `landing-pro` | HTML | Template |
| `ithy` | Full-Stack | En cours |

#### 🔴 Apps Coquilles Vides (22) → À ARCHIVER
```
agriculture-dz, business-dz, commerce-dz, council, creative-studio,
dashboard-central, data-dz-dashboard, douanes-dz, dzirvideo-ai,
education-dz, finance-dz, industrie-dz, islam-dz, legal-assistant,
pme-dz, sante-dz, seo-dz-boost, transport-dz, bmad, api-packages,
billing-credits (partiel), pipeline-creator
```

---

### 🤖 Agents IA (15 répertoires)

#### Architecture Agents
```
agents/
├── core/                    # Framework de base
│   ├── base_agent.py        # Classe abstraite BaseAgent
│   ├── agent_config.py      # Configuration YAML
│   ├── multi_agent_team.py  # Orchestration multi-agents
│   └── tool_registry.py     # Gestion des outils
│
├── rag/                     # RAG spécialisé
│   ├── finance-agent/       # 🟠 Google ADK (incompatible)
│   └── legal-agent/         # BaseAgent
│
├── business/
│   ├── consultant/          # 🟠 Google ADK
│   └── analyst/             # BaseAgent
│
├── finance/                 # BaseAgent ✅
├── legal/                   # BaseAgent ✅
├── real_estate/             # BaseAgent ✅
├── recruitment/             # BaseAgent ✅
├── teaching/                # BaseAgent ✅
├── travel/                  # BaseAgent ✅
│
├── discovery-dz/            # 🔴 Config only (pas de code)
├── recruteur-dz/            # 🔴 Config only
├── ux-research/             # 🔴 Config only
├── iafactory-operator/      # Agno framework
└── video-operator/          # Agno framework
```

#### Problèmes Agents
| Problème | Agents affectés | Solution |
|----------|-----------------|----------|
| 3 frameworks incompatibles | business/consultant, rag/finance, video-operator | Adaptateur unifié |
| LLM hardcodé | 12 agents | Injection dépendances |
| Prompts inline | Tous | Externaliser en .md |
| Couplage Streamlit | 5 agents | Séparer UI/Logic |
| Config-only sans code | 3 agents | Implémenter ou archiver |

---

### ⚙️ Services Backend (8)

| Service | Port | Status | Tests | Notes |
|---------|------|--------|-------|-------|
| `api/` | 8000 | 🟢 Prod | ✅ 8 fichiers | Service principal |
| `backend/rag-compat/` | - | 🔴 DUPLI | ✅ | **SUPPRIMER** |
| `connectors/` | - | 🟡 Dev | ❌ | N8N, Make, Zapier |
| `data-dashboard/` | - | 🟡 Dev | ❌ | Pas de persistence |
| `fiscal-assistant/` | - | 🟡 Dev | ❌ | Lois fiscales DZ |
| `ithy/` | - | 🟡 Dev | ❌ | Moteur recherche |
| `legal-assistant/` | - | 🟡 Dev | ❌ | Lois DZ |
| `voice-assistant/` | - | 🟡 Dev | ❌ | STT/TTS |

#### Duplication Critique
```
services/api/           ←──── 98% IDENTIQUE ────→   services/backend/rag-compat/
   └── 219 fichiers                                    └── 216 fichiers
```
**Action**: Supprimer `services/backend/rag-compat/` immédiatement.

---

### 🔄 Workflows (3)

| Workflow | Status | Fichiers | Notes |
|----------|--------|----------|-------|
| `delivery/ClientOnboarding` | 🟡 POC | 2 | Async Python |
| `sales/LeadPipeline` | 🟡 POC | 1 | Scoring algorithm |
| `support/` | 🔴 Vide | 0 | À implémenter |

---

## ✅ 5 FORCES MAJEURES

1. **Architecture modulaire solide** - Séparation claire apps/agents/services/core
2. **Stack technique moderne** - Next.js 14, FastAPI, Docker, LLMs multiples
3. **Couverture domaines large** - Finance, Legal, Education, Video, CRM, etc.
4. **Infrastructure VPS opérationnelle** - 50+ containers, nginx configuré, SSL
5. **Framework agents extensible** - BaseAgent abstrait, multi-agent teams

---

## 🔴 5 FAIBLESSES URGENTES

1. **Duplication massive** - `rag-compat/` = 98% copie de `api/` (216 fichiers)
2. **Sécurité** - Secrets exposés (.env.local), TODO billing signature
3. **Fragmentation agents** - 3 frameworks incompatibles, LLM hardcodés
4. **Manque de tests** - 97.5% apps sans tests, régression garantie
5. **22 apps vides** - Bruit, confusion, maintenance impossible

---

## 📅 PLAN D'ACTION 30 JOURS

### Semaine 1 : Nettoyage Critique (P0)
- [ ] Supprimer `services/backend/rag-compat/`
- [ ] Supprimer `apps/video-studio/frontend/node_modules/` du repo
- [ ] Supprimer `apps/interview/.env.local` du repo
- [ ] Mettre à jour `.gitignore` global
- [ ] Corriger TODO sécurité billing

### Semaine 2 : Réorganisation Structure (P1)
- [ ] Créer `apps/_archived/` et y déplacer 22 apps vides
- [ ] Consolider `shared/` en `packages/shared/`
- [ ] Réduire docker-compose à 3 fichiers (dev, staging, prod)
- [ ] Renommer ~20 fichiers Python kebab→snake_case

### Semaine 3 : Documentation (P1)
- [ ] Générer README.md pour 26 apps sans documentation
- [ ] Créer `.env.example` pour toutes apps configurables
- [ ] Externaliser prompts agents vers `.md`
- [ ] Documenter architecture dans `docs/ARCHITECTURE.md`

### Semaine 4 : Refactoring Agents + Tests (P2)
- [ ] Créer adaptateur unifié BaseAgent/ADK/Agno
- [ ] Implémenter injection dépendances LLM
- [ ] Ajouter tests critiques (auth, billing, video pipeline)
- [ ] Décider sort des 3 agents config-only

---

## 📐 CONVENTIONS DE NOMMAGE

### Fichiers et Dossiers
| Contexte | Convention | Exemple |
|----------|------------|---------|
| Apps (dossiers) | `kebab-case` | `video-studio`, `ia-chatbot` |
| Python modules | `snake_case` | `agent_config.py`, `tool_registry.py` |
| Components React | `PascalCase` | `VideoPlayer.tsx`, `ChatWidget.jsx` |
| Config files | `kebab-case` | `docker-compose.yml`, `tsconfig.json` |

### Code
| Langage | Fonctions | Classes | Constantes |
|---------|-----------|---------|------------|
| Python | `snake_case` | `PascalCase` | `UPPER_SNAKE` |
| TypeScript | `camelCase` | `PascalCase` | `UPPER_SNAKE` |
| CSS | `kebab-case` | - | `--kebab-case` |

### Fichiers à Corriger (~20)
```
agents/rag/finance-agent/  → agents/rag/finance_agent/
agents/business/consultant/ → (OK si dossier, pas module)
scripts/deploy-*.sh        → (OK pour shell scripts)
```

---

## 🔧 STRUCTURE CIBLE PROPOSÉE

```
rag-dz/
├── apps/
│   ├── _archived/          # 22 apps inactives
│   ├── video-studio/       # Next.js + FastAPI
│   ├── marketing/          # React/Vite
│   ├── can2025/            # Next.js
│   └── ...                 # 8 apps actives
│
├── agents/
│   ├── core/               # Framework unifié
│   │   ├── base_agent.py
│   │   ├── adapters/       # ADK, Agno adapters
│   │   └── config/
│   └── domains/            # Agents métier
│       ├── finance/
│       ├── legal/
│       └── ...
│
├── packages/               # Nouveau: code partagé
│   ├── shared/             # Consolidation 3 shared/
│   ├── ui-components/
│   └── llm-clients/
│
├── services/
│   ├── api/                # Service principal
│   ├── connectors/
│   └── ...                 # 6 services (sans rag-compat)
│
├── infrastructure/
│   └── docker/
│       ├── docker-compose.dev.yml
│       ├── docker-compose.staging.yml
│       └── docker-compose.prod.yml
│
└── docs/
    ├── AUDIT.md            # Ce fichier
    ├── ARCHITECTURE.md
    └── CONTRIBUTING.md
```

---

## 📋 CHECKLIST DE SUIVI

### P0 - Critique
- [ ] `rm -rf services/backend/rag-compat/`
- [ ] `git rm -r --cached apps/video-studio/frontend/node_modules/`
- [ ] `git rm --cached apps/interview/.env.local`
- [ ] Update `.gitignore`
- [ ] Fix billing signature TODO

### P1 - Important
- [ ] Create `apps/_archived/`
- [ ] Move 22 empty apps
- [ ] Consolidate `shared/` → `packages/shared/`
- [ ] Reduce docker-compose files
- [ ] Fix naming conventions

### P2 - Amélioration
- [ ] Add critical tests
- [ ] Unify agent frameworks
- [ ] Implement LLM dependency injection
- [ ] Externalize prompts

---

## 📊 MÉTRIQUES POST-AUDIT

| Métrique | Avant | Cible |
|----------|-------|-------|
| Apps actives | 40 | 18 |
| Duplication services | 98% | 0% |
| Tests coverage | 2.5% | 30% |
| README coverage | 35% | 100% |
| Docker-compose files | 13 | 3 |

---

*Généré automatiquement par Claude Opus 4.5 - Audit IAFactory SaaS Platform*
*Pour questions: relancer l'audit avec `@workspace audit global`*
