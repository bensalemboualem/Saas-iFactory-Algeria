# 📋 CHECKLIST DE MIGRATION - RAG-DZ / IAFactory

**Créé**: 20 Décembre 2024  
**Dernière mise à jour**: `date +%Y-%m-%d`  
**Responsable**: [Votre nom]

---

## 🎯 OBJECTIF

Réduire la dette technique identifiée dans [docs/AUDIT.md](./AUDIT.md) selon le plan de 30 jours.

---

## 📊 PROGRESSION GLOBALE

| Phase | Status | Progression | Date |
|-------|--------|-------------|------|
| P0 - Critique | ✅ Terminé | ██████████ 100% | 20 déc 2024 |
| P1 - Réorganisation | ✅ Terminé | ██████████ 100% | 20 déc 2024 |
| P2 - Documentation | ✅ Terminé | ██████████ 100% | 20 déc 2024 |
| P3 - Tests & Refacto | 🔜 Planifié | ░░░░░░░░░░ 0% | Jan 2025 |

---

## 🔴 P0 - ACTIONS CRITIQUES (Semaine 1)

### Sécurité & Nettoyage

| # | Tâche | Commande/Script | Status | Notes |
|---|-------|-----------------|--------|-------|
| 1.1 | Supprimer `rag-compat/` | `rm -rf services/backend/rag-compat/` | ⬜ | 216 fichiers dupliqués |
| 1.2 | Supprimer `node_modules` commité | `git rm -r --cached apps/video-studio/frontend/node_modules/` | ⬜ | ~700MB économisés |
| 1.3 | Supprimer `.env.local` exposé | `git rm --cached apps/interview/.env.local` | ⬜ | Secrets critiques |
| 1.4 | Mettre à jour `.gitignore` | Voir script P0 | ⬜ | Prévention future |
| 1.5 | Corriger TODO billing signature | `services/api/app/billing/` | ⬜ | Vérifier implémentation |
| 1.6 | Externaliser admin key | `services/api/app/main.py` | ⬜ | Vers .env |

### Commande globale P0
```bash
# PowerShell
.\scripts\migration\p0-critical.ps1

# Ou Makefile
make migrate-p0
```

### ✅ Validation P0
- [ ] `git status` ne montre plus rag-compat
- [ ] `git status` ne montre plus node_modules
- [ ] `.gitignore` contient les nouvelles entrées
- [ ] Commit effectué: `git commit -m "chore: P0 migration - critical cleanup"`

---

## 🟠 P1 - RÉORGANISATION STRUCTURE (Semaine 2)

### Archivage Apps Vides

| # | Tâche | Status | Notes |
|---|-------|--------|-------|
| 2.1 | Créer `apps/_archived/` | ⬜ | Dossier archive |
| 2.2 | Déplacer 22 apps vides | ⬜ | Voir liste ci-dessous |
| 2.3 | Vérifier apps "borderline" | ⬜ | Décision manuelle |

**Apps à archiver (22):**
```
agriculture-dz, business-dz, commerce-dz, council, creative-studio,
dashboard-central, data-dz-dashboard, douanes-dz, dzirvideo-ai,
education-dz, finance-dz, industrie-dz, islam-dz, legal-assistant,
pme-dz, sante-dz, seo-dz-boost, transport-dz, api-packages,
pipeline-creator
```

### Consolidation Shared

| # | Tâche | Status | Notes |
|---|-------|--------|-------|
| 2.4 | Créer `packages/shared/` | ⬜ | Nouveau dossier |
| 2.5 | Copier `apps/shared/` | ⬜ | Consolidation |
| 2.6 | Copier `services/shared/` | ⬜ | Consolidation |
| 2.7 | Copier `shared/` racine | ⬜ | Consolidation |
| 2.8 | Mettre à jour imports | ⬜ | Refactoring |

### Docker-Compose Cleanup

| # | Tâche | Status | Notes |
|---|-------|--------|-------|
| 2.9 | Analyser 13 docker-compose | ⬜ | Identifier doublons |
| 2.10 | Créer `docker-compose.dev.yml` | ⬜ | Développement |
| 2.11 | Créer `docker-compose.staging.yml` | ⬜ | Pré-prod |
| 2.12 | Créer `docker-compose.prod.yml` | ⬜ | Production VPS |

### Conventions Nommage

| # | Tâche | Status | Notes |
|---|-------|--------|-------|
| 2.13 | Lister fichiers Python kebab-case | ⬜ | ~20 fichiers |
| 2.14 | Renommer → snake_case | ⬜ | Script généré |
| 2.15 | Mettre à jour imports | ⬜ | Refactoring |

### Commande globale P1
```bash
.\scripts\migration\p1-reorganize.ps1
# Ou: make migrate-p1
```

### ✅ Validation P1
- [ ] `apps/_archived/` contient 20+ apps
- [ ] `packages/shared/` existe et contient le code consolidé
- [ ] 3 docker-compose max dans `infrastructure/docker/`
- [ ] Plus de fichiers Python en kebab-case
- [ ] Commit: `git commit -m "chore: P1 migration - restructure"`

---

## 🟡 P2 - DOCUMENTATION (Semaine 3)

### README.md

| # | App | Status | Notes |
|---|-----|--------|-------|
| 3.1 | video-studio | ⬜ | Prioritaire |
| 3.2 | marketing | ⬜ | Prod |
| 3.3 | can2025 | ⬜ | Prod |
| 3.4 | dzirvideo | ⬜ | Beta |
| 3.5 | crm-ia | ⬜ | Beta |
| 3.6 | ia-agents | ⬜ | Beta |
| 3.7 | prompt-creator | ⬜ | Dev |
| 3.8 | ia-notebook | ⬜ | Dev |
| ... | (autres) | ⬜ | Auto-généré |

### .env.example

| # | App/Service | Status | Notes |
|---|-------------|--------|-------|
| 3.9 | services/api/ | ⬜ | Variables critiques |
| 3.10 | apps/video-studio/backend | ⬜ | LLM keys |
| 3.11 | apps/interview | ⬜ | Après suppression .env.local |

### Prompts Agents

| # | Tâche | Status | Notes |
|---|-------|--------|-------|
| 3.12 | Créer `agents/prompts/` | ⬜ | Dossier centralisé |
| 3.13 | Externaliser prompts finance | ⬜ | vers .md |
| 3.14 | Externaliser prompts legal | ⬜ | vers .md |
| 3.15 | Externaliser prompts recruitment | ⬜ | vers .md |

### Documentation Architecture

| # | Tâche | Status | Notes |
|---|-------|--------|-------|
| 3.16 | Créer `docs/ARCHITECTURE.md` | ⬜ | Schéma global |
| 3.17 | Créer `docs/CONTRIBUTING.md` | ⬜ | Guidelines |
| 3.18 | Mettre à jour `README.md` racine | ⬜ | Getting started |

### Commande globale P2
```bash
.\scripts\migration\p2-documentation.ps1
# Ou: make migrate-p2
```

### ✅ Validation P2
- [ ] 100% apps ont un README.md
- [ ] Toutes apps configurables ont .env.example
- [ ] Prompts agents externalisés
- [ ] Commit: `git commit -m "docs: P2 migration - documentation complete"`

---

## 🔵 P3 - TESTS & REFACTORING (Semaine 4)

### Tests Critiques

| # | Module | Type | Status | Notes |
|---|--------|------|--------|-------|
| 4.1 | Auth API | Unit | ⬜ | JWT, permissions |
| 4.2 | Billing API | Unit | ⬜ | Credits, signature |
| 4.3 | Video Pipeline | Integration | ⬜ | Génération complète |
| 4.4 | Agent BaseAgent | Unit | ⬜ | Framework core |

### Refactoring Agents

| # | Tâche | Status | Notes |
|---|-------|--------|-------|
| 4.5 | Créer adapter ADK→BaseAgent | ⬜ | Unification |
| 4.6 | Créer adapter Agno→BaseAgent | ⬜ | Unification |
| 4.7 | Implémenter injection LLM | ⬜ | Dependency injection |
| 4.8 | Décider sort agents config-only | ⬜ | Archiver ou implémenter |

### ✅ Validation P3
- [ ] Tests auth passent
- [ ] Tests billing passent
- [ ] Pipeline video testé end-to-end
- [ ] Framework agents unifié
- [ ] Commit: `git commit -m "test: P3 migration - tests & refactoring"`

---

## 📈 MÉTRIQUES À SUIVRE

| Métrique | Avant | Actuel | Cible |
|----------|-------|--------|-------|
| Fichiers dupliqués | 216 | ? | 0 |
| Apps vides | 22 | ? | 0 (archivées) |
| README coverage | 35% | ? | 100% |
| Test coverage | 2.5% | ? | 30% |
| Docker-compose files | 13 | ? | 3 |
| Frameworks agents | 3 | ? | 1 |

---

## 📝 NOTES DE PROGRESSION

### Semaine 1 (16-22 déc)
```
[ Date ] - [ Action ] - [ Résultat ]
```

### Semaine 2 (23-29 déc)
```
[ Date ] - [ Action ] - [ Résultat ]
```

### Semaine 3 (30 déc - 5 jan)
```
[ Date ] - [ Action ] - [ Résultat ]
```

### Semaine 4 (6-19 jan)
```
[ Date ] - [ Action ] - [ Résultat ]
```

---

## 🆘 BLOCAGES & QUESTIONS

| Date | Problème | Status | Solution |
|------|----------|--------|----------|
| - | - | - | - |

---

## ✅ VALIDATION FINALE

- [ ] P0 complété et validé
- [ ] P1 complété et validé
- [ ] P2 complété et validé
- [ ] P3 complété et validé
- [ ] Tests de régression passent
- [ ] VPS déployé avec nouvelle structure
- [ ] Documentation à jour
- [ ] Équipe briefée sur nouvelles conventions

---

*Dernière mise à jour automatique via `make migrate-status`*
