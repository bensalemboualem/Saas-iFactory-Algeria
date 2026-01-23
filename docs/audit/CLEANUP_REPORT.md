# CLEANUP REPORT - iafactorychatgpt

> **Date**: 2026-01-17
> **Projet**: D:\iafactorychatgpt (Fork de LobeChat v2.0.0-next.179)

---

## RESUME EXECUTIF

| Catégorie | Problèmes | Espace récupérable |
|-----------|-----------|-------------------|
| Dossiers externes/dupliqués | 4 | ~500 MB |
| Fichiers de documentation obsolètes | 20+ | ~155 MB |
| Fichiers de log | 55 | ~1.5 MB |
| Archives .tar.gz | 8 | ~50 MB |
| Fichiers temporaires | 15+ | ~160 MB |
| **TOTAL ESTIMÉ** | **100+** | **~850 MB** |

---

## 1. LIENS AVEC D:\iafactory (PROJET EXTERNE)

### 1.1 Chemins absolus trouvés

⚠️ **ATTENTION**: Des références à `D:\IAFactory\` ont été trouvées dans les fichiers suivants:

| Fichier | Type |
|---------|------|
| `ANALYSE_EXHAUSTIVE_IAFACTORY.md` | Documentation externe |
| `BACKUPS/2026-01-02_144104/LISTE_PAGES.md` | Backup avec chemins externes |

**ACTION**: Ces fichiers font référence au projet externe D:\iafactory et devraient être supprimés.

### 1.2 Imports @iafactory/* trouvés

| Fichier | Import |
|---------|--------|
| `apps/api/src/routes/tools.ts` | `@iafactory/tools-registry`, `@iafactory/ai-engine`, `@iafactory/credits-system` |
| `apps/api/src/routes/tools.js` | Même imports (fichier dupliqué) |
| `test_prisma.js` | `@iafactory/database` |

**ACTION**: Ces imports référencent des packages locaux dans `packages/` - ce sont des dépendances internes au projet, PAS des liens externes.

### 1.3 URLs localhost trouvées

Les ports suivants sont référencés dans le projet:
- `localhost:3000` - Port principal (apps/web, documentation)
- `localhost:3001` - Gateway API
- `localhost:8000` - RAG API (rag-dz)
- `localhost:5173` - Vite dev server

**ACTION**: Ce sont des configurations de développement normales, pas de liens externes.

---

## 2. DOSSIERS COPIES (PAS SYMLINKS)

| Dossier | Type | Taille | Contenu |
|---------|------|--------|---------|
| `IAFactory/` | Répertoire | 184 MB | Copie de rag-dz + BACKUPS |
| `onestschooled/` | Répertoire vide | 16 KB | Vide |
| `iafactory-academy/` | Répertoire | 12 KB | frontend/ (quasi vide) |

### DÉTAILS

```
IAFactory/
├── BACKUPS/           # Backups obsolètes
└── rag-dz/            # DUPLIQUE avec apps/iafactory-core/rag-dz/

apps/iafactory-core/   # 184 MB - Même contenu
└── rag-dz/
```

⚠️ **DUPLICATION MAJEURE**: `IAFactory/rag-dz/` et `apps/iafactory-core/rag-dz/` sont identiques!

---

## 3. PACKAGE.JSON - DEPENDANCES

✅ **Aucune dépendance vers ../iafactory** trouvée.

Les dépendances `workspace:*` référencent des packages locaux:
- `@lobechat/*` → packages/ (projet LobeChat)
- `@lobehub/*` → packages/ (projet LobeChat)

Les packages ajoutés pour iafactory sont dans `packages/`:
- `packages/ai-engine/`
- `packages/chargily-pay/`
- `packages/credits-system/`
- `packages/tools-registry/`

---

## 4. FICHIERS .ENV - ANALYSE

| Fichier | Liens externes | Secrets exposés |
|---------|----------------|-----------------|
| `.env` | ❌ Aucun | ⚠️ DATABASE_URL, KEY_VAULTS_SECRET |
| `apps/gateway/.env` | ❌ Aucun | ⚠️ **CLÉS API EXPOSÉES** (GROQ, OPENROUTER, DEEPSEEK, OPENAI) |
| `apps/web/.env` | ❌ Aucun | ✅ Secrets factices pour dev |

### ⚠️ ALERTE SÉCURITÉ

Le fichier `apps/gateway/.env` contient des **clés API réelles**:
```
GROQ_API_KEY=gsk_mw3p2...
OPENROUTER_API_KEY=sk-or-v1-b096b9...
DEEPSEEK_API_KEY=sk-e2d7d2...
OPENAI_API_KEY=sk-proj-ysvcis...
```

**ACTION URGENTE**: Révoquer ces clés et les remplacer par des variables d'environnement.

---

## 5. FICHIERS À SUPPRIMER

### 5.1 Dossiers Legacy (Priorité HAUTE)

```bash
# ~250 MB à récupérer
rm -rf _LEGACY_ARCHIVE/         # 52 MB
rm -rf BACKUPS/                  # 14 MB
rm -rf IAFactory/                # 184 MB (DUPLIQUÉ)
```

### 5.2 Dossiers quasi-vides

```bash
# Dossiers vides ou quasi-vides
rm -rf onestschooled/           # 16 KB (vide)
rm -rf iafactory-academy/       # 12 KB (presque vide)
```

### 5.3 Archives .tar.gz (hors node_modules)

```bash
# ~50 MB à récupérer
rm -f iafactory-lite.tar.gz
rm -f iafactory-source.tar.gz
rm -f apps/iafactory-core/rag-dz/apps/dzirvideo/dzirvideo-*.tar.gz
```

### 5.4 Fichiers de log (~1.5 MB)

```bash
# Logs à la racine
rm -f api-dev.err.log
rm -f api-dev.out.log
rm -f bolt-dev.err.log
rm -f bolt-dev.out.log

# Logs dans apps/web/ (45+ fichiers)
rm -f apps/web/*.log

# Logs dans apps/iafactory-core/
rm -f apps/iafactory-core/rag-dz/apps/dzirvideo/*.log
```

### 5.5 Fichiers temporaires/diagnostic (~160 MB)

```bash
# Fichiers volumineux à la racine
rm -f ARBO_COMPLETE.txt              # 124 MB
rm -f scan_full_report.txt           # 30 MB
rm -f file_type_counts.txt           # 1.7 MB
rm -f tree_depth3.txt                # 93 KB

# Scripts obsolètes
rm -f *.bat                          # start-*.bat, restart-*.bat
rm -f *.ps1                          # archive_*.ps1
rm -f backup_folders.txt
rm -f env_files.txt
rm -f TOOLS_ALL.txt
```

### 5.6 Documentation externe iafactory

```bash
# Documentation qui devrait être dans un repo séparé
rm -rf documentation/                # 1.1 MB (documentation iafactory-algeria)

# Fichiers .md spécifiques à iafactory
rm -f ANALYSE_EXHAUSTIVE_IAFACTORY.md
rm -f ARCHITECTURE_OPTIMALE.md
rm -f AUDIT_ALL_BY_CATEGORY.md
rm -f AUDIT_IAFACTORY.md
rm -f AUDIT_ONESTSCHOOL.md
rm -f BMAD_ARCHON_BOLT.md
rm -f DATABASE_SCHEMAS.md
rm -f DEPLOYMENT_GUIDE.md
rm -f DIAGNOSTIC_BMAD_ARCHON_BOLT.md
rm -f DOCKER_COMPOSE_MULTI_ENV.md
rm -f IAFACTORY_MEMORY.md
rm -f IAFACTORY_VIDEO_PLATFORM.md
rm -f MASTER_STRATEGIC_PLAN.md
rm -f MEMOIRE_PROJET_CHAT_BOLT.md
rm -f PLAN_MIGRATION_DETAILLE.md
rm -f RAG_DZ_COMPLET.md
rm -f RESTART_INSTRUCTIONS.md
rm -f REVOCATION_URGENTE_CLES_API.md
rm -f SCAN_COMPLET_IAFACTORY.md
rm -f SECURITY_REMEDIATION.md
rm -f TOKEN_SYSTEM.md
```

### 5.7 Dossiers applicatifs externes

```bash
# Applications iafactory qui ne font pas partie de LobeChat
rm -rf landing-bolt-style/           # 97 MB
rm -rf landing-genspark-pro/         # 124 KB
```

---

## 6. SCRIPT DE NETTOYAGE COMPLET

```bash
#!/bin/bash
# cleanup_iafactorychatgpt.sh
# À exécuter depuis D:\iafactorychatgpt

echo "=== CLEANUP iafactorychatgpt ==="

# 1. Dossiers legacy et dupliqués
rm -rf _LEGACY_ARCHIVE/
rm -rf BACKUPS/
rm -rf IAFactory/
rm -rf onestschooled/
rm -rf iafactory-academy/

# 2. Archives
rm -f iafactory-lite.tar.gz
rm -f iafactory-source.tar.gz
rm -f apps/iafactory-core/rag-dz/apps/dzirvideo/dzirvideo-*.tar.gz

# 3. Logs
rm -f *.log
rm -f apps/web/*.log
rm -f apps/iafactory-core/rag-dz/apps/dzirvideo/*.log

# 4. Fichiers temporaires volumineux
rm -f ARBO_COMPLETE.txt
rm -f scan_full_report.txt
rm -f file_type_counts.txt
rm -f tree_depth3.txt
rm -f backup_folders.txt
rm -f env_files.txt
rm -f TOOLS_ALL.txt

# 5. Scripts obsolètes
rm -f *.bat
rm -f *.ps1

# 6. Documentation externe
rm -rf documentation/

# 7. Landing pages externes
rm -rf landing-bolt-style/
rm -rf landing-genspark-pro/

# 8. Fichiers MD iafactory
rm -f ANALYSE_EXHAUSTIVE_IAFACTORY.md
rm -f ARCHITECTURE_OPTIMALE.md
rm -f AUDIT_*.md
rm -f BMAD_ARCHON_BOLT.md
rm -f DATABASE_SCHEMAS.md
rm -f DEPLOYMENT_GUIDE.md
rm -f DIAGNOSTIC_BMAD_ARCHON_BOLT.md
rm -f DOCKER_COMPOSE_MULTI_ENV.md
rm -f IAFACTORY_*.md
rm -f MASTER_STRATEGIC_PLAN.md
rm -f MEMOIRE_PROJET_CHAT_BOLT.md
rm -f PLAN_MIGRATION_DETAILLE.md
rm -f RAG_DZ_COMPLET.md
rm -f RESTART_INSTRUCTIONS.md
rm -f REVOCATION_URGENTE_CLES_API.md
rm -f SCAN_COMPLET_IAFACTORY.md
rm -f SECURITY_REMEDIATION.md
rm -f TOKEN_SYSTEM.md

echo "=== CLEANUP TERMINÉ ==="
echo "Espace récupéré: ~850 MB"
```

---

## 7. RECOMMANDATIONS

### Priorité HAUTE (Faire immédiatement)

1. **RÉVOQUER LES CLÉS API** dans `apps/gateway/.env`
2. Supprimer `IAFactory/` (duplication de 184 MB)
3. Supprimer `_LEGACY_ARCHIVE/` et `BACKUPS/`

### Priorité MOYENNE

4. Supprimer les fichiers `.log`
5. Supprimer les archives `.tar.gz`
6. Supprimer les fichiers temporaires volumineux

### Priorité BASSE

7. Nettoyer la documentation externe
8. Évaluer si `apps/iafactory-core/` doit rester ou être dans un repo séparé
9. Évaluer si `apps/api/` et `apps/gateway/` sont nécessaires

---

## 8. STRUCTURE RECOMMANDÉE APRÈS NETTOYAGE

```
D:\iafactorychatgpt\
├── .claude/            # Config Claude
├── .github/            # GitHub workflows
├── apps/
│   └── desktop/        # App Electron (LobeChat)
├── docs/               # Documentation LobeChat
├── e2e/                # Tests E2E
├── locales/            # i18n
├── packages/           # Monorepo packages
│   ├── agent-runtime/
│   ├── database/
│   ├── model-runtime/
│   └── ...
├── scripts/            # Scripts build
├── src/                # Code source principal
├── .env                # Config environnement
├── package.json
├── README.md
└── tsconfig.json
```

---

## FIN DU RAPPORT
