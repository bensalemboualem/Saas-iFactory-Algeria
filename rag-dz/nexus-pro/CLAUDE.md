# CLAUDE.md - Nexus AI Platform pour IA Factory Algérie

> **Version**: 1.0.0  
> **Statut**: Production-Ready  
> **Stack**: FastAPI + React/Next.js + PostgreSQL/Supabase + Redis + Qdrant

---

## 🎯 Mission

Fusionner **BMAD Method** + **Archon** + **bolt.diy** en une plateforme unifiée pour le marché algérien.

```
┌─────────────────────────────────────────────────────────────────┐
│                         UTILISATEUR                              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    META-ORCHESTRATOR (P0)                        │
│         Gouvernance · Routage · Sessions · Conflits              │
│                         Port: 8100                               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  BMAD RUNNER  │   │  ARCHON SYNC  │   │ BOLT EXECUTOR │
│     (P1)      │   │     (P0)      │   │     (P0)      │
│   Workflows   │   │   KB + Tasks  │   │  SEUL WRITER  │
│    :8052      │   │    :8051      │   │    :8053      │
└───────────────┘   └───────────────┘   └───────────────┘
```

---

## 🤖 Les 9 Orchestrateurs

### Priorité P0 (Critique)

| Agent | Port | Rôle | Droits |
|-------|------|------|--------|
| **meta-orchestrator** | 8100 | Gouvernance globale, routage, sessions, conflits | Read + Lock |
| **intake-triage** | - | Qualification demandes, génère `requirements/*.md` | Write `requirements/` |
| **archon-sync** | 8051 | Source de vérité KB + Tasks | Write Tasks (Archon) |
| **bolt-executor** | 8053 | **SEUL WRITER** - Implémente le code | Write **CODE** |
| **validator-qa** | 8054 | Tests, validation, droit de **VETO** | Write `tests/` + VETO |

### Priorité P1 (Important)

| Agent | Port | Rôle | Droits |
|-------|------|------|--------|
| **bmad-runner** | 8052 | 21 agents BMAD, workflows agile | Write `PRPs/`, `docs/` |
| **context-curator** | - | Conventions, patterns, `project-context.md` | Write `project-context.md` |
| **security-auditor** | - | Audit sécurité, droit de **VETO** | Read + VETO |

### Priorité P2 (Optimisation)

| Agent | Port | Rôle | Droits |
|-------|------|------|--------|
| **cost-model-router** | - | Optimisation coût/latence LLM | Read only |

---

## 🔒 Single-Writer Rule (CRITIQUE)

**Un seul agent peut écrire du code à la fois: `bolt-executor`**

### Workflow d'écriture
```
1. Task créée dans Archon (status: todo)
2. Meta-orchestrator assigne à bolt-executor
3. bolt-executor demande LOCK sur les fichiers
4. Meta vérifie: pas déjà locké, pas protégé sans validation
5. LOCK accordé → Task passe à "doing"
6. bolt-executor écrit
7. validator-qa vérifie (tests, lint, sécurité)
8. Si OK → LOCK libéré → Task passe à "done"
9. Si KO → Retour à bolt-executor avec issues
```

### Dossiers Protégés (Validation obligatoire)
```yaml
critical:
  - migrations/          # security-auditor + validator-qa
  - auth/                # security-auditor
  - services/chargily/   # security-auditor + validator-qa
  - agents/gov/          # security-auditor

important:
  - config/
  - middleware/
  - models/
```

---

## 🇩🇿 Adaptations Algérie

### Paiement
```python
# TOUJOURS Chargily, JAMAIS Stripe
from services.chargily import ChargilyService
# Toujours en DZD
```

### Multi-tenant
```python
# tenant_id OBLIGATOIRE via JWT
# JAMAIS via header X-Tenant-ID
# RLS activé sur TOUTES les tables
```

### Langues
```python
LANGUAGES = ["fr", "ar", "darija", "en"]
# RTL support obligatoire pour l'arabe
```

### Agents GOV (existants à compléter)
- CNAS: `agents/gov/cnas.py` - parsers incomplets
- Sonelgaz: `agents/gov/sonelgaz.py` - parsers incomplets
- CASNOS, CNRC, Impôts: à implémenter

---

## 📋 Exécution des PRPs

### Ordre obligatoire
```
PRP-001 → PRP-002 → PRP-003 → PRP-004 → PRP-005 → PRP-006
```

### Format des commits
```
feat(PRP-XXX): description courte
fix(PRP-XXX): correction
docs(PRP-XXX): documentation
test(PRP-XXX): tests
```

### Règles
1. Lire le PRP en entier AVANT de commencer
2. Exécuter les tâches dans l'ordre (T1 → T2 → ...)
3. Marquer chaque tâche DONE avant de passer à la suivante
4. Si blocage → créer `questions/[date]-question.md`
5. Ne JAMAIS skip une tâche

---

## 📁 Structure du Projet

```
nexus-iafactory/
├── CLAUDE.md                 # Ce fichier
├── README.md                 # Documentation utilisateur
├── docker-compose.yml        # Orchestration services
├── .env.example              # Variables d'environnement
│
├── .claude/
│   ├── PERMISSIONS.md        # Matrice droits/locks
│   ├── agents/               # 9 orchestrateurs
│   │   ├── meta-orchestrator.md
│   │   ├── intake-triage.md
│   │   ├── archon-sync.md
│   │   ├── bolt-executor.md
│   │   ├── validator-qa.md
│   │   ├── bmad-runner.md
│   │   ├── context-curator.md
│   │   ├── security-auditor.md
│   │   └── cost-model-router.md
│   └── commands/
│       ├── project-init.md
│       └── prp-execute.md
│
├── PRPs/                     # Plans d'exécution
│   ├── PRP-001-project-setup.md
│   ├── PRP-002-meta-orchestrator.md
│   ├── PRP-003-archon-integration.md
│   ├── PRP-004-bmad-integration.md
│   ├── PRP-005-bolt-integration.md
│   └── PRP-006-iafactory-adaptation.md
│
├── orchestrators/            # Code des orchestrateurs
│   ├── meta/
│   ├── bmad/
│   ├── archon/
│   ├── bolt/
│   └── shared/
│
├── scripts/
│   ├── start.sh
│   ├── stop.sh
│   └── health-check.sh
│
└── docs/
    ├── architecture.md
    ├── deployment.md
    └── api-reference.md
```

---

## ⚡ Commandes Disponibles

| Commande | Description |
|----------|-------------|
| `/project-init` | Initialise la structure Nexus |
| `/prp:execute PRP-XXX` | Exécute un PRP spécifique |
| `/status` | État de tous les services |
| `/audit` | Audit complet du projet |
| `/health` | Health check rapide |

---

## 🚨 Points Critiques

### Sécurité
- [ ] Clés API: JAMAIS dans le code, toujours `.env`
- [ ] RLS Supabase: TOUJOURS activé
- [ ] Secrets scan: Avant chaque commit

### Performance
- [ ] Utiliser DeepSeek pour tâches simples (coût)
- [ ] Claude/GPT-4o pour tâches complexes (qualité)
- [ ] Cache Redis pour KB queries fréquentes

### Qualité
- [ ] Tests obligatoires pour chaque feature
- [ ] Lint (black/eslint) avant commit
- [ ] Type hints Python / TypeScript strict

---

## 🚀 Démarrage

```bash
# 1. Copier les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API

# 2. Démarrer les services
./scripts/start.sh

# 3. Vérifier la santé
./scripts/health-check.sh

# 4. Accéder aux services
# Meta-Orchestrator: http://localhost:8100
# Archon UI:         http://localhost:3737
# Bolt.diy:          http://localhost:5173
```

---

## 📞 En cas de problème

1. Vérifier les logs: `docker compose logs -f [service]`
2. Redémarrer: `./scripts/stop.sh && ./scripts/start.sh`
3. Reset complet: `docker compose down -v && ./scripts/start.sh`

---

*Document généré pour IA Factory Algérie*  
*Consolidation BMAD + Archon + bolt.diy*
