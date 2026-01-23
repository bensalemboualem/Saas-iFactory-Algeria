# IA Factory - rag-dz

## Commandes
cd infrastructure/docker && docker-compose up -d : Démarrer
./scripts/deploy/ : Scripts de déploiement

## Structure Projet (Mise à jour 19/12/2025 - Phase 2)
```
rag-dz/ (21 dossiers racine)
├── apps/                   # 39 applications par secteur
│   ├── agriculture-dz/    # agri, irrigation
│   ├── api-packages/      # packaging API
│   ├── api-portal/        # portail API
│   ├── bmad/              # BMAD workflow
│   ├── can2025/           # CAN 2025
│   ├── commerce-dz/       # commerce
│   ├── council/           # conseil
│   ├── creative-studio/   # studio créatif
│   ├── crm-ia/            # CRM IA
│   ├── dev-portal/        # portail dev
│   ├── dzirvideo*/        # vidéo IA
│   ├── education-dz/      # formation
│   ├── finance-dz/        # finance
│   ├── ia-*/              # agents, chatbot, notebook, searcher, voice
│   ├── interview/         # interview
│   ├── ithy/              # Ithy
│   ├── legal-assistant/   # assistant juridique
│   ├── marketing/         # marketing (production)
│   ├── news/, sport/      # médias
│   ├── pipeline-creator/  # créateur pipeline
│   ├── pme-dz/            # PME copilot
│   ├── prompt-creator/    # créateur prompts
│   ├── sante-dz/          # santé
│   ├── seo-dz-boost/      # SEO
│   ├── shared/            # composants partagés
│   └── transport-dz/      # transport
├── services/               # 8 services backend
│   ├── api/               # API FastAPI principale (port 8000)
│   ├── backend/           # billing, key-service, rag-compat, voice
│   ├── connectors/        # connecteurs DZ
│   ├── data-dashboard/    # dashboard data
│   ├── fiscal-assistant/  # assistant fiscal
│   ├── ithy/              # intégration Ithy
│   ├── legal-assistant/   # assistant juridique
│   └── voice-assistant/   # assistant vocal
├── infrastructure/         # Consolidé (docker, n8n, nginx, observability, sql)
├── agents/                 # Agents IA
├── frontend/               # UIs React
├── ia-factory/             # Core IA Factory
├── ia-factory-automation/  # Automatisation
├── scripts/                # Scripts dev et déploiement
├── config/                 # Configuration
├── core/                   # Modules core
├── docs/                   # Documentation
├── templates/              # Templates
├── tests/                  # Tests
└── workflows/              # Workflows n8n
```

## Fichiers racine
- .env, .env.example, .env.local, .env.production
- .gitignore, CLAUDE.md, README.md
- Makefile, requirements.txt

## Style Code
- JavaScript ES6+, pas jQuery
- Python avec type hints
- Gestion erreurs try/catch

## Theme UI
Mode sombre: bg slate-900, text slate-100
Accent: blue-500, success emerald-500, error red-500

## i18n
fr (LTR), ar (RTL), en (LTR)

## Tokens - IMPORTANT
1. /clear entre chaque tache
2. Lire fichiers specifiques seulement
3. grep pour chercher

## NE JAMAIS FAIRE
- Modifier fichiers non mentionnes
- Supprimer code sans demander
- Hardcoder credentials
- Toucher aux apps/ sans autorisation explicite

## VERIFICATION OBLIGATOIRE (Tolérance Zéro)
Avant chaque commit/déploiement :
1. Vérifier que services/api/ existe et contient app/main.py
2. Vérifier que CLAUDE.md et README.md sont intacts
3. Vérifier que docker-compose.yml est valide
4. Vérifier qu'aucun fichier .env n'est exposé
