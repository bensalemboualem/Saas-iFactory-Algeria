# IAFactory - Enterprise AI Platform Suite

**Version:** 2.0.0
**Dernière mise à jour:** Décembre 2024
**Mainteneur:** IAFactory Team

---

## Vue d'ensemble

IAFactory est une suite complète de plateformes d'intelligence artificielle conçue pour l'entreprise moderne. Elle comprend quatre projets majeurs interconnectés qui couvrent l'éducation, la création de contenu vidéo, la gestion scolaire, et l'orchestration IA avancée.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          IAFACTORY ECOSYSTEM                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │   IAFACTORY     │  │   IAFACTORY     │  │   ONESTSCHOOLED │              │
│  │    ACADEMY      │  │ VIDEO-PLATFORM  │  │   (BBC School)  │              │
│  │   ───────────   │  │   ───────────   │  │   ───────────   │              │
│  │ LMS & E-learning│  │ AI Video Gen.   │  │ School Mgmt.    │              │
│  │ FastAPI + React │  │ Multi-Agent AI  │  │ Laravel/PHP     │              │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘              │
│           │                    │                    │                        │
│           └────────────────────┼────────────────────┘                        │
│                                │                                             │
│                    ┌───────────▼───────────┐                                 │
│                    │       RAG-DZ          │                                 │
│                    │   (NEXUS AI PLATFORM) │                                 │
│                    │   ─────────────────   │                                 │
│                    │  Meta-Orchestrator    │                                 │
│                    │  9 Agents | 27 Apps   │                                 │
│                    │  BMAD + Archon + Bolt │                                 │
│                    └───────────────────────┘                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Projets

| Projet | Description | Stack | Port(s) | Status |
|--------|-------------|-------|---------|--------|
| [iafactory-academy](./iafactory-academy/) | Plateforme e-learning avec gestion de cours, paiements Stripe, et certifications | FastAPI, React, PostgreSQL, Redis | 8000, 3000 | Production |
| [iafactory-video-platform](./iafactory-video-platform/) | Création vidéo automatisée avec 40+ providers IA | FastAPI, Next.js, FFmpeg, Multi-AI | 8001, 3000 | Production |
| [onestschooled](./onestschooled/) | Système de gestion scolaire BBC School Algérie | Laravel, PHP, MySQL | 80, 443 | Production |
| [rag-dz](./rag-dz/) | Meta-orchestrateur IA Nexus avec 27 applications | FastAPI, Supabase, Qdrant, Multi-Agent | 8100, 8181 | Développement |

---

## Architecture Globale

### Stack Technologique

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND LAYER                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  React 18  │  Next.js 15  │  Vite  │  TailwindCSS  │  TypeScript 5.3        │
│  Zustand   │  TanStack Query  │  React Hook Form  │  Zod                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  FastAPI 0.109  │  Laravel 8+  │  SQLAlchemy 2.0  │  Pydantic V2            │
│  Celery 5.3     │  Redis 7     │  JWT Auth        │  WebSocket              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  PostgreSQL 16  │  Supabase  │  MySQL  │  Qdrant (Vector)  │  Redis Cache   │
│  MinIO (S3)     │  AWS S3    │  Alembic Migrations                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AI/ML PROVIDERS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  LLMs:    OpenAI │ Anthropic │ Groq │ DeepSeek │ Mistral │ Google          │
│  Images:  DALL-E 3 │ Flux │ SDXL │ Leonardo │ Ideogram                      │
│  Videos:  Runway │ Pika │ Luma │ Kling                                      │
│  Audio:   ElevenLabs │ OpenAI TTS │ Whisper │ Suno │ Udio                   │
│  Avatars: HeyGen │ D-ID │ Synthesia │ SadTalker                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Intégrations Spécifiques Algérie

| Service | Utilisation | Provider |
|---------|-------------|----------|
| Paiements | E-commerce, abonnements | Chargily (pas Stripe) |
| Langues | Interface utilisateur | FR, AR, Darija, EN |
| APIs Gouvernementales | Vérifications | CNAS, CNRC, Sonelgaz, CASNOS |

---

## Installation Rapide

### Prérequis

- **Docker** >= 24.0
- **Docker Compose** >= 2.20
- **Node.js** >= 18.0 (pour le développement frontend)
- **Python** >= 3.11 (pour le développement backend)
- **Git**

### Démarrage Global

```bash
# Cloner le repository
git clone https://github.com/iafactory/iafactory.git
cd iafactory

# Copier les fichiers d'environnement
cp iafactory-academy/backend/.env.example iafactory-academy/backend/.env
cp iafactory-video-platform/backend/.env.example iafactory-video-platform/backend/.env
cp rag-dz/.env.example rag-dz/.env

# Démarrer tous les services (mode développement)
docker-compose -f docker-compose/docker-compose.dev.yml up -d

# Ou démarrer un projet spécifique
cd iafactory-academy && docker-compose up -d
```

### Ports par Défaut

| Service | Port | Description |
|---------|------|-------------|
| Academy Backend | 8000 | API FastAPI |
| Academy Frontend | 3000 | React Vite |
| Video Backend | 8001 | API FastAPI |
| Video Frontend | 3001 | Next.js |
| RAG-DZ Meta | 8100 | Meta-Orchestrator |
| RAG-DZ Archon | 8181 | Archon Server |
| RAG-DZ Bolt | 5173 | Bolt.diy IDE |
| PostgreSQL | 5432/5433 | Base de données |
| Redis | 6379/6380 | Cache & Queue |
| Qdrant | 6333 | Vector Database |

---

## Documentation

### Index Principal

| Document | Description |
|----------|-------------|
| [ARCHITECTURE_OPTIMALE.md](./ARCHITECTURE_OPTIMALE.md) | Architecture système détaillée |
| [INVENTAIRE_COMPLET.md](./INVENTAIRE_COMPLET.md) | Inventaire des 27+ applications |
| [PLAN_MIGRATION_DETAILLE.md](./PLAN_MIGRATION_DETAILLE.md) | Plan de migration vers production |
| [DOCKER_COMPOSE_MULTI_ENV.md](./DOCKER_COMPOSE_MULTI_ENV.md) | Configuration Docker multi-environnement |
| [SECURITY_REMEDIATION.md](./SECURITY_REMEDIATION.md) | Guide de sécurisation |

### Par Projet

| Projet | Documentation |
|--------|---------------|
| iafactory-academy | [README](./iafactory-academy/README.md) · [Architecture](./iafactory-academy/docs/architecture.md) · [API](./iafactory-academy/docs/api.md) |
| iafactory-video-platform | [README](./iafactory-video-platform/README.md) · [Architecture](./iafactory-video-platform/docs/architecture.md) · [Agents](./iafactory-video-platform/docs/agents.md) |
| onestschooled | [README](./onestschooled/README.md) · [Installation](./onestschooled/docs/installation.md) · [Modules](./onestschooled/docs/modules.md) |
| rag-dz | [README](./rag-dz/README.md) · [CLAUDE.md](./rag-dz/CLAUDE.md) · [Applications](./rag-dz/docs/applications.md) |

### Audits & Diagnostics

| Document | Description |
|----------|-------------|
| [AUDIT_IAFACTORY.md](./AUDIT_IAFACTORY.md) | Audit global de la plateforme |
| [AUDIT_ONESTSCHOOL.md](./AUDIT_ONESTSCHOOL.md) | Audit système scolaire |
| [DIAGNOSTIC_BMAD_ARCHON_BOLT.md](./DIAGNOSTIC_BMAD_ARCHON_BOLT.md) | Diagnostic des orchestrateurs |
| [ANALYSE_EXHAUSTIVE_IAFACTORY.md](./ANALYSE_EXHAUSTIVE_IAFACTORY.md) | Analyse complète du codebase |

---

## Structure des Répertoires

```
D:\IAFactory\
├── iafactory-academy/           # Plateforme e-learning
│   ├── backend/                 # FastAPI + SQLAlchemy
│   ├── frontend/                # React + Vite
│   ├── docs/                    # Documentation technique
│   └── docker-compose.yml
│
├── iafactory-video-platform/    # Génération vidéo IA
│   ├── backend/                 # FastAPI + Multi-Agent
│   ├── frontend/                # Next.js 15
│   ├── docs/                    # Documentation agents
│   └── docker-compose.yml
│
├── onestschooled/               # Gestion scolaire Laravel
│   ├── app/                     # Application Laravel
│   ├── Modules/                 # Modules modulaires
│   ├── docs/                    # Documentation
│   └── docker-compose.yml
│
├── rag-dz/                      # Meta-orchestrateur Nexus
│   ├── orchestrators/           # 9 agents orchestrateurs
│   ├── agents/                  # 40+ agents spécialisés
│   ├── apps/                    # 27 applications
│   ├── services/                # Services backend
│   ├── bmad/                    # BMAD Method
│   ├── bolt-diy/                # IDE de génération
│   ├── PRPs/                    # Plans d'exécution
│   └── docs/                    # Documentation complète
│
├── docker-compose/              # Configurations Docker partagées
├── BACKUPS/                     # Sauvegardes
├── _archive/                    # Projets archivés
│
└── [Documentation racine]       # 17 fichiers .md
```

---

## Contribution

### Workflow Git

```bash
# Créer une branche feature
git checkout -b feature/nom-de-la-feature

# Commits atomiques avec messages clairs
git commit -m "feat(project): description courte"
git commit -m "fix(api): correction du bug X"
git commit -m "docs(readme): mise à jour documentation"

# Push et Pull Request
git push origin feature/nom-de-la-feature
```

### Conventions de Commits

| Préfixe | Description |
|---------|-------------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `docs` | Documentation |
| `style` | Formatage, pas de changement de code |
| `refactor` | Refactoring de code |
| `test` | Ajout ou modification de tests |
| `chore` | Maintenance, dépendances |

### Code Review

Avant toute fusion:
1. Tests passent (unitaires + intégration)
2. Documentation mise à jour
3. Review par au moins 1 développeur
4. Pas de secrets dans le code

---

## Sécurité

### Gestion des Secrets

**NE JAMAIS commiter de secrets dans le repository.**

```bash
# Fichiers à NE JAMAIS commiter
.env
.env.local
.env.production
*.pem
*.key
credentials.json
```

### Révocation d'urgence

En cas de fuite de clés API:
1. Consulter [REVOCATION_URGENTE_CLES_API.md](./REVOCATION_URGENTE_CLES_API.md)
2. Révoquer immédiatement sur le dashboard du provider
3. Générer de nouvelles clés
4. Mettre à jour les environnements sécurisés
5. Auditer les accès

### Checklist Sécurité

- [ ] Clés API dans variables d'environnement uniquement
- [ ] HTTPS activé en production
- [ ] CORS configuré correctement
- [ ] Rate limiting activé
- [ ] Logs d'audit actifs
- [ ] Backups chiffrés
- [ ] Accès base de données restreint

---

## Monitoring & Logs

### Services de Monitoring

| Service | URL | Description |
|---------|-----|-------------|
| pgAdmin | http://localhost:5050 | Administration PostgreSQL |
| Redis Commander | http://localhost:8081 | Monitoring Redis |
| Flower | http://localhost:5555 | Monitoring Celery |
| Archon UI | http://localhost:3737 | Dashboard RAG-DZ |

### Logs

```bash
# Voir les logs d'un service
docker logs -f iafactory-academy-backend

# Logs agrégés
docker-compose logs -f

# Logs avec filtrage
docker logs iafactory-academy-backend 2>&1 | grep ERROR
```

---

## Support

### Ressources

- **Issues:** GitHub Issues pour les bugs et suggestions
- **Wiki:** Documentation collaborative
- **Discussions:** GitHub Discussions pour les questions

### Contacts

- **Équipe technique:** tech@iafactory.dz
- **Support:** support@iafactory.dz
- **Sécurité:** security@iafactory.dz

---

## Licence

Copyright (c) 2024 IAFactory. Tous droits réservés.

Ce logiciel est propriétaire. Toute reproduction, distribution ou modification sans autorisation écrite est interdite.

---

<div align="center">

**Construit avec passion en Algérie**

</div>
