# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Unreleased]

### À venir
- Consolidation des 13 docker-compose en 3 fichiers (dev/staging/prod)
- Tests critiques pour auth, billing, video pipeline
- Unification des frameworks agents (BaseAgent/ADK/Agno)

---

## [2.0.0] - 2024-12-20

### 🚀 Migration Majeure - "Clean Repo Day"

Cette version représente une refonte complète de l'organisation du projet,
réduisant la dette technique accumulée et établissant des standards professionnels.

### Added
- `docs/AUDIT.md` - Rapport d'audit complet du projet
- `docs/MIGRATION_CHECKLIST.md` - Checklist de suivi de migration
- `packages/shared/` - Code partagé consolidé (39 fichiers)
- `apps/_archived/` - Archive des apps inactives avec README
- `scripts/migration/` - Scripts PowerShell réutilisables (P0, P1, P2)
- 15 nouveaux README.md pour les apps
- 9 nouveaux .env.example pour les apps configurables
- Nouvelles commandes Makefile: `migrate-p0`, `migrate-p1`, `migrate-p2`, `migrate-status`

### Removed
- `services/backend/rag-compat/` - **779 fichiers supprimés** (98% dupliqué de api/)
- `apps/video-studio/frontend/node_modules/` - **334 MB** retirés du repo
- `apps/interview/.env.local` - Secrets exposés supprimés
- 17 apps vides archivées (agriculture-dz, business-dz, commerce-dz, etc.)

### Changed
- Structure apps: 40 → 23 actives + 17 archivées
- Shared folders: 3 dispersés → 1 consolidé dans `packages/shared/`
- `.gitignore` renforcé (node_modules, .env, __pycache__, etc.)
- Tous les apps ont maintenant un README.md standardisé

### Security
- Suppression des credentials exposés dans .env.local
- Ajout de règles .gitignore pour prévenir les futures expositions
- Création de .env.example templates sécurisés

### Documentation
- Audit complet avec forces/faiblesses identifiées
- Plan d'action 30 jours documenté
- Conventions de nommage établies
- Structure cible proposée

### Tags de Rollback
- `pre-migration-p0` - État avant nettoyage critique
- `pre-migration-p1` - État avant réorganisation
- `pre-migration-p2` - État avant documentation

---

## [1.x.x] - Avant Migration

Version historique avant la migration majeure.
Voir tag `pre-migration-p0` pour l'état complet.

### Problèmes Corrigés
- Duplication massive (rag-compat = 98% copie de api/)
- node_modules commités (700MB+)
- Secrets exposés dans les fichiers .env
- 22 apps "coquilles vides" causant confusion
- 3 dossiers shared/ dispersés
- 13 fichiers docker-compose redondants
- Absence de README pour 65% des apps

---

## Statistiques de Migration

| Métrique | Avant | Après | Amélioration |
|----------|-------|-------|--------------|
| Taille repo | ~400 MB | ~60 MB | -85% |
| Fichiers dupliqués | 779 | 0 | -100% |
| Apps actives | 40 | 23 | Clarté |
| README coverage | 35% | 100% | +186% |
| Shared folders | 3 | 1 | Consolidé |
| Secrets exposés | 2+ | 0 | Sécurisé |

---

*Migration réalisée le 20 décembre 2024*
*Assistée par Claude Opus 4.5*
