# Nexus AI Platform

> Plateforme IA unifiée pour IA Factory Algérie  
> Fusion de BMAD Method + Archon + bolt.diy

---

## 🎯 Vue d'ensemble

Nexus combine trois projets open-source majeurs:

| Projet | Rôle | Stars |
|--------|------|-------|
| **BMAD Method** | 21 agents + 50 workflows agile | 26.5k |
| **Archon** | Knowledge Base + RAG + Task Management | 13.5k |
| **bolt.diy** | IDE web + 19 LLM providers | 18.8k |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    META-ORCHESTRATOR                         │
│              Gouvernance · Routage · Sessions                │
│                        :8100                                 │
└─────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  BMAD RUNNER  │  │  ARCHON SYNC  │  │ BOLT EXECUTOR │
│   Workflows   │  │   KB + Tasks  │  │  Code Writer  │
│    :8052      │  │    :8051      │  │    :8053      │
└───────────────┘  └───────────────┘  └───────────────┘
```

---

## 🚀 Quick Start

### 1. Cloner le projet

```bash
git clone https://github.com/iafactory/nexus-platform.git
cd nexus-platform
```

### 2. Configurer l'environnement

```bash
cp .env.example .env
# Éditer .env avec vos clés API
```

### 3. Démarrer

```bash
./scripts/start.sh
```

### 4. Accéder aux services

| Service | URL |
|---------|-----|
| Meta-Orchestrator | http://localhost:8100 |
| Archon UI | http://localhost:3737 |
| Archon API | http://localhost:8181 |
| Bolt.diy | http://localhost:5173 |

---

## 📋 PRPs (Plans d'exécution)

| PRP | Description | Effort |
|-----|-------------|--------|
| PRP-001 | Project Setup | 2-3h |
| PRP-002 | Meta-Orchestrator | 4-5h |
| PRP-003 | Archon Integration | 4-5h |
| PRP-004 | BMAD Integration | 3-4h |
| PRP-005 | Bolt Integration | 3-4h |
| PRP-006 | IA Factory Adaptation | 6-8h |

**Total**: ~25-30 heures

---

## 🤖 Les 9 Orchestrateurs

### P0 - Critique
- **meta-orchestrator**: Gouvernance globale
- **intake-triage**: Qualification demandes
- **archon-sync**: KB + Tasks (source de vérité)
- **bolt-executor**: **SEUL WRITER** du code
- **validator-qa**: Tests + VETO

### P1 - Important
- **bmad-runner**: Workflows BMAD
- **context-curator**: Conventions projet
- **security-auditor**: Sécurité + VETO

### P2 - Optimisation
- **cost-model-router**: Optimisation coûts LLM

---

## 🇩🇿 Adaptations Algérie

- **Paiement**: Chargily (DZD) - pas Stripe
- **Langues**: Français, Arabe, Darija
- **APIs GOV**: CNAS, Sonelgaz, CASNOS, CNRC
- **Conformité**: RLS, multi-tenant, JWT

---

## 📖 Documentation

- [Architecture détaillée](./docs/architecture.md)
- [Guide de déploiement](./docs/deployment.md)
- [API Reference](./docs/api-reference.md)
- [CLAUDE.md](./CLAUDE.md) - Instructions pour Claude Code

---

## 🛠️ Commandes utiles

```bash
# Démarrer
./scripts/start.sh

# Arrêter
./scripts/stop.sh

# Health check
./scripts/health-check.sh

# Logs
docker compose logs -f [service]

# Reset complet
docker compose down -v && ./scripts/start.sh
```

---

## 📄 Licence

- BMAD Method: MIT
- Archon: ACL v1.2 (non-commercial as-a-service)
- bolt.diy: MIT

---

## 🤝 Contribution

Voir [CONTRIBUTING.md](./CONTRIBUTING.md)

---

*Développé pour IA Factory Algérie*
