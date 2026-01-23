# AUDIT COMPLET PROJETS IAFACTORY - INVENTAIRE DOCKER
**Date:** 2025-12-27
**Total Containers:** 41 | **Volumes:** 57 | **Images Custom:** ~20

---

## 1. PROJETS ACTIFS (Containers Running)

| Container | Image | Importance | Complet. | Verdict |
|-----------|-------|------------|----------|---------|
| `iafactoryrag` | mintplexlabs/anythingllm | CRITIQUE | 95% | ✅ GARDER |
| `iafactory-video-frontend` | iafactory-video-studio-frontend | CRITIQUE | 85% | ✅ GARDER |
| `iafactory-video-backend` | iafactory-video-studio-backend | CRITIQUE | 85% | ✅ GARDER |
| `iafactory-video-db` | postgres:16-alpine | CRITIQUE | 100% | ✅ GARDER |
| `iafactory-video-redis` | redis:7-alpine | CRITIQUE | 100% | ✅ GARDER |
| `iaf-browser-automation` | browser-automation | IMPORTANT | 70% | ✅ GARDER |
| `videostudio-postgres` | postgres:16-alpine | IMPORTANT | 100% | ⚠️ DOUBLON |
| `videostudio-redis` | redis:7-alpine | SECONDAIRE | 100% | ⚠️ DOUBLON |
| `videostudio-n8n` | n8nio/n8n | IMPORTANT | 100% | ✅ GARDER |
| `videostudio-adminer` | adminer | SECONDAIRE | 100% | 🔄 OPTIONNEL |
| `videostudio-minio` | minio/minio | IMPORTANT | 100% | ✅ GARDER |
| `reels-automation-reels-app-1` | reels-automation-reels-app | IMPORTANT | 60% | ✅ GARDER |
| `iaf-dz-postgres-local` | pgvector/pgvector:pg16 | CRITIQUE | 100% | ✅ GARDER |
| `iaf-dz-redis-local` | redis:7-alpine | CRITIQUE | 100% | ✅ GARDER |
| `iaf-dz-qdrant-local` | qdrant/qdrant | CRITIQUE | 100% | ✅ GARDER |
| `ia-factory-redis` | redis:7-alpine | IMPORTANT | 100% | ✅ GARDER |
| `ia-factory-qdrant` | qdrant/qdrant | IMPORTANT | 100% | ✅ GARDER |

**Total Running: 17 containers**

---

## 2. PROJETS ARRETES A GARDER

### 2.1 rag-dz (Backend/Frontend)

| Container | Status | Dernière activité | Verdict |
|-----------|--------|-------------------|---------|
| `rag-dz-backend-local-1` | Exited 9j | Code existe | ⚠️ SAUVEGARDER |
| `rag-dz-frontend-local-1` | Exited 7j | Code existe | ⚠️ SAUVEGARDER |
| `rag-dz-db-local-1` | Exited 7j | Volume postgres | ⚠️ BACKUP DB |
| `iaf-dz-backend-local` | Exited 5j | Image 11GB ! | 🔄 REBUILD |
| `iaf-dz-docs-local` | Exited 9j | Docs frontend | 🔄 REBUILD |

**Volumes associés:**
- `rag-dz_postgres_data` (47.74MB) - ⚠️ SAUVEGARDER
- `rag-dz_qdrant_data` (357B) - peut reconstruire
- `ragdz-postgres-data` (77.95MB) - ⚠️ SAUVEGARDER
- `ragdz-qdrant-data` (415.6MB) - ⚠️ SAUVEGARDER
- `iaf-dz-qdrant-data` (1.54GB) - ⚠️ SAUVEGARDER

### 2.2 ia-factory-automation

| Container | Status | Importance | Verdict |
|-----------|--------|------------|---------|
| `ia-factory-automation` | Exited 5j | CRITIQUE | 🔄 REBUILD |
| `ia-factory-celery` | Exited 5j | CRITIQUE | 🔄 REBUILD |
| `ia-factory-beat` | Exited 5j | CRITIQUE | 🔄 REBUILD |
| `ia-factory-postgres` | Created | CRITIQUE | ⚠️ VÉRIFIER |

**Code source:** `ia-factory/automation/` - Existe ✅
**Docker-compose:** `ia-factory/automation/docker-compose.yml` ✅
**Verdict:** 🔄 PEUT ÊTRE RECONSTRUIT

### 2.3 bolt-diy (Multiples versions)

| Container | Image | Status | Verdict |
|-----------|-------|--------|---------|
| `bolt-diy-fresh-app-dev-1` | 1e1843b846ae | Exited 3sem | ❌ SUPPRIMER |
| `bolt-diy-fresh-app-prod-1` | bolt-ai:production | Exited 3sem | ⚠️ SAUVEGARDER |

**Volumes:**
- `bolt-diy-fresh_postgres_data` (48MB) - ⚠️ BACKUP avant suppression
- `bolt-diy-fresh_qdrant_data` (357B) - Peut supprimer
- `bolt-diy-fresh_archon_postgres_data` (47.79MB) - ⚠️ BACKUP

### 2.4 dzirvideo / dziria-app

| Container | Image | Taille | Status | Verdict |
|-----------|-------|--------|--------|---------|
| `dzirvideo` | dzirvideo-dzirvideo | 4.87GB | Exited 12j | ⚠️ SAUVEGARDER |
| `dziria-app-dev-1` | 1e1843b846ae | 3.31GB | Exited 3sem | ❌ SUPPRIMER |

**Code source:** `apps/dzirvideo/` - Existe ✅
**Verdict:** Image énorme mais code existe, peut rebuilder

### 2.5 IAFactory School

| Container | Image | Status | Verdict |
|-----------|-------|--------|---------|
| `iafactory-backend` | ia-factory-school-backend | Exited 2sem | 🔄 REBUILD |
| `iafactory-frontend` | ia-factory-school-frontend | Exited 2sem | 🔄 REBUILD |
| `iafactory-qdrant` | qdrant/qdrant | Exited 2sem | 🔄 RESTART |

**Volume:** `ia-factory-school_qdrant_data` (281.2MB) - ⚠️ SAUVEGARDER

### 2.6 Video Operator

| Container | Image | Taille | Status | Verdict |
|-----------|-------|--------|--------|---------|
| `iafactory-video-operator` | video-operator-video-operator | 8.66GB | Exited 12j | ⚠️ ÉNORME |

**Volumes:**
- `video-operator_video_uploads` (0B)
- `video-operator_video_outputs` (0B)
**Code source:** `agents/video-operator/` - Existe ✅
**Verdict:** Image de 13.3GB ! 🔄 Peut rebuilder depuis code

---

## 3. AGENTS & WORKFLOWS

### 3.1 Agents BMAD (19 agents via npm package)
**Location:** `node_modules/bmad-method/`
- Installé via npm, pas de containers dédiés
- Utilisé par les slash commands Claude

### 3.2 Agents Custom IAFactory

| Agent | Location | Status | Type |
|-------|----------|--------|------|
| Archon | `frontend/archon-ui/` | Code exist | Submodule Git |
| Video Operator | `agents/video-operator/` | Container stopped | Python API |
| IAFactory Operator | `agents/iafactory-operator/` | docker-compose exist | A démarrer |
| Discovery DZ | `agents/discovery-dz/` | Config only | Claude skill |
| UX Research | `agents/ux-research/` | Config only | Claude skill |
| Recruteur DZ | `agents/recruteur-dz/` | Config only | Claude skill |

### 3.3 Agents RAG Templates

| Agent | Location | Complet |
|-------|----------|---------|
| Local RAG | `agents/rag/local-rag/` | ✅ |
| Finance Agent | `agents/rag/finance-agent/` | ✅ |
| Chat PDF | `agents/rag/chat-pdf/` | ✅ |
| Hybrid Search | `agents/rag/hybrid-search/` | ✅ |
| Voice Support | `agents/rag/voice-support/` | ✅ |

### 3.4 Agents Business

| Agent | Location | Docker |
|-------|----------|--------|
| Consultant | `agents/business/consultant/` | ✅ Dockerfile |
| Data Analysis | `agents/business/data-analysis/` | ✅ Dockerfile |
| Customer Support | `agents/business/customer-support/` | ✅ Dockerfile |

### 3.5 Workflows n8n
- `workflows/delivery/n8n_workflow_media_reels.json` - Workflow Reels

---

## 4. VIDEO STUDIO - ANALYSE DUPLICATAS

### 4.1 Versions identifiées

| Version | Location | Containers | Status |
|---------|----------|------------|--------|
| **video-studio (rag-dz)** | `apps/video-studio/` | iafactory-video-* | ✅ RUNNING |
| **iafactory-video-studio** | `D:\IAFactory\iafactory-video-studio\` | Même que ci-dessus | Repo séparé |
| **iafactory-video-studio-pro** | `D:\IAFactory\iafactory-video-studio-pro\` | videostudio-* | ✅ RUNNING |
| **video-operator** | `agents/video-operator/` | iafactory-video-operator | Exited |

### 4.2 Containers Video (Analyse)

**PRODUCTION (Video Studio DZ):**
- `iafactory-video-frontend` - Port 3000
- `iafactory-video-backend` - Port 8000
- `iafactory-video-db` - postgres:16
- `iafactory-video-redis` - redis:7

**INFRASTRUCTURE (Video Studio Pro):**
- `videostudio-postgres` - Port 5432 (CONFLIT!)
- `videostudio-redis` - Port 6380 (différent)
- `videostudio-n8n` - Port 5678
- `videostudio-minio` - Port 9000
- `videostudio-adminer` - Port 8080

### 4.3 Recommandation
- ✅ GARDER: iafactory-video-* (prod DZ)
- ⚠️ CONSOLIDER: videostudio-* infrastructure vers apps/video-studio
- ❌ SUPPRIMER: video-operator container (13.3GB) - rebuilder si nécessaire

---

## 5. APPLICATIONS SaaS CH/DZ

### 5.1 Apps Actives

| App | Location | Container | Prête Prod |
|-----|----------|-----------|------------|
| Video Studio | `apps/video-studio/` | ✅ Running | 85% |
| Landing Pro | `apps/landing-pro/` | - | 90% |
| CRM IA | `apps/crm-ia/` | docker-compose | 60% |
| Marketing | `apps/marketing/` | - | 70% |
| PME DZ | `apps/pme-dz/` | docker-compose | 50% |
| SEO DZ Boost | `apps/seo-dz-boost/` | docker-compose | 60% |

### 5.2 Apps Templates (archives)

| App | Status | Verdict |
|-----|--------|---------|
| Agriculture DZ | Archivé | 🔄 Template |
| Commerce DZ | Archivé | 🔄 Template |
| Education DZ | Archivé | 🔄 Template |
| Finance DZ | Archivé | 🔄 Template |
| Santé DZ | Archivé | 🔄 Template |
| Transport DZ | Archivé | 🔄 Template |

### 5.3 Apps Spéciales

| App | Description | Status |
|-----|-------------|--------|
| CAN 2025 | Coupe Afrique | En dev |
| News | Portail news | En dev |
| Sport | Sports | En dev |
| Legal Assistant | Assistant juridique | 70% |
| Ithy | Recherche IA | 80% |

---

## 6. DONNEES CRITIQUES - VOLUMES

### 6.1 CRITIQUE (Ne jamais supprimer)

| Volume | Taille | Contenu | Action |
|--------|--------|---------|--------|
| `iafactory-openwebui-data` | 1.081GB | Configs OpenWebUI | ⚠️ BACKUP |
| `iaf-dz-qdrant-data` | 1.54GB | Embeddings prod | ⚠️ BACKUP |
| `iaf-dz-backend-cache` | 1.13GB | Cache RAG | ⚠️ BACKUP |
| `iaf-dz-ollama-data` | 4.661GB | Modèles Ollama | 🔄 Rebuild |
| `iafactory-video-studio-pro_postgres_data` | 80.19MB | DB Video | ⚠️ BACKUP |
| `ragdz-qdrant-data` | 415.6MB | Embeddings | ⚠️ BACKUP |
| `ia-factory-automation_qdrant-data` | 281.2MB | Embeddings | ⚠️ BACKUP |

### 6.2 IMPORTANT (Sauvegarder avant nettoyage)

| Volume | Taille | Contenu | Action |
|--------|--------|---------|--------|
| `iaf-grafana-data` | 140.2MB | Dashboards | ⚠️ BACKUP |
| `ragdz-grafana-data` | 140.2MB | Dashboards | ⚠️ BACKUP |
| `iaf-dz-postgres-data-local` | 92.69MB | DB locale | ⚠️ BACKUP |
| `iafactory-video-studio-pro_n8n_data` | 4.743MB | Workflows | ⚠️ BACKUP |
| `n8n_data` | 636.1kB | Workflows | ⚠️ BACKUP |

### 6.3 PEUT SUPPRIMER

| Volume | Taille | Raison |
|--------|--------|--------|
| `bolt-diy-fresh_redis_data` | 264B | Vide/inutile |
| `bolt-diy-fresh_qdrant_storage` | 357B | Quasi vide |
| `iaf-redis-data` | 264B | Vide |
| `rag-dz_redis_data` | 264B | Vide |
| Volumes anonymes (6) | Variable | Orphelins |

---

## 7. IMAGES DOCKER PERSONNALISEES

### 7.1 CRITIQUE (Garder/Sauvegarder)

| Image | Taille | Dockerfile | Action |
|-------|--------|------------|--------|
| `iafactory-video-studio-frontend` | 1.98GB | ✅ Exists | 🔄 REBUILD |
| `iafactory-video-studio-backend` | 822MB | ✅ Exists | 🔄 REBUILD |
| `rag-dz-iafactory-backend` | 17.8GB! | ✅ Exists | 🔄 REBUILD |
| `reels-automation-reels-app` | 748MB | ✅ Exists | 🔄 REBUILD |

### 7.2 PEUT SUPPRIMER

| Image | Taille | Raison |
|-------|--------|--------|
| `video-operator-video-operator` | 13.3GB | Énorme, code exists |
| `dzirvideo-dzirvideo` | 4.87GB | Code exists |
| `bolt-ai:development` | 4.34GB | Test version |
| `bolt-ai:production` | 4.36GB | ⚠️ Garder 1 version |
| `rag-dz-backend-local` | 11GB | Code exists |
| `<none>` images | Variable | Dangling |

### 7.3 Dockerfiles existants

```
agents/video-operator/Dockerfile ✅
agents/iafactory-operator/Dockerfile ❓
agents/business/consultant/Dockerfile ✅
agents/business/data-analysis/Dockerfile ✅
agents/business/customer-support/Dockerfile ✅
apps/video-studio/frontend/Dockerfile ✅
apps/video-studio/backend/Dockerfile ✅
services/browser-automation/Dockerfile ✅
```

---

## 8. FICHIERS DOCKER-COMPOSE

### 8.1 ACTIFS (Production/Dev)

| Fichier | Containers | Status |
|---------|------------|--------|
| `infrastructure/docker/docker-compose.yml` | Principal | ✅ ACTIF |
| `apps/video-studio/docker-compose.yml` | Video Studio | ✅ ACTIF |
| `ia-factory/automation/docker-compose.yml` | Automation | ⚠️ Stopped |
| `services/browser-automation/docker-compose.yml` | Browser | ✅ ACTIF |

### 8.2 VARIANTS (À consolider)

| Fichier | Usage |
|---------|-------|
| `docker-compose-local.yml` | Dev local |
| `docker-compose.production.yml` | Prod |
| `docker-compose.simple.yml` | Minimal |
| `docker-compose.essential.yml` | Essentiel |
| `docker-compose.minimal.yml` | Très minimal |
| `docker-compose.prod.yml` | Prod alt |
| `docker-compose.extras.yml` | Services extra |

### 8.3 AGENTS (Templates)

| Fichier | Agent |
|---------|-------|
| `agents/video-operator/docker-compose.yml` | Video Op |
| `agents/iafactory-operator/docker-compose.yml` | IAF Op |
| `agents/templates/rag-apps/*/docker-compose.yml` | RAG Apps |

### 8.4 OBSOLETES / A SUPPRIMER

| Fichier | Raison |
|---------|--------|
| `docker-compose-ai-agents-phase*.yml` | Phases terminées |
| `docker-compose.frontend.yml` | Doublon |
| `docker-compose.apps.yml` | Non utilisé |

---

## 9. VERDICT & RECOMMANDATIONS

### ✅ GARDER - CRITIQUE PRODUCTION (17)

```
iafactoryrag                    AnythingLLM principal
iafactory-video-frontend        Video Studio DZ
iafactory-video-backend         Video Studio DZ
iafactory-video-db              DB Video
iafactory-video-redis           Cache Video
iaf-browser-automation          Browser automation
iaf-dz-postgres-local           DB principale
iaf-dz-redis-local              Cache principal
iaf-dz-qdrant-local             Embeddings prod
ia-factory-redis                Cache automation
ia-factory-qdrant               Embeddings automation
videostudio-n8n                 Workflows n8n
videostudio-minio               Storage S3
videostudio-postgres            DB Video Pro
reels-automation-reels-app-1    Reels generator
```

### ⚠️ SAUVEGARDER AVANT NETTOYAGE (8)

```
rag-dz-backend-local-1          Données backend
rag-dz-db-local-1               Base postgres
bolt-diy-fresh-app-prod-1       Version prod bolt
iafactory-video-operator        Peut avoir configs
iafactory-backend               School backend
iafactory-frontend              School frontend
iafactory-openwebui             Configs OpenWebUI
iafactory-anythingllm           Configs AnythingLLM
```

### 🔄 PEUT ÊTRE RECONSTRUIT (7)

```
ia-factory-automation           Dockerfile exists
ia-factory-celery               Dockerfile exists
ia-factory-beat                 Dockerfile exists
dzirvideo                       Dockerfile exists
iaf-dz-backend-local            Dockerfile exists
iaf-dz-docs-local               Dockerfile exists
iafactory-qdrant                Image officielle
```

### ❌ SUPPRIMER (9)

```
private-gpt-*                   Non utilisé (3 containers)
bolt-diy-fresh-app-dev-1        Version dev obsolète
dziria-app-dev-1                Test obsolète
iaf-ollama                      Created jamais démarré
ia-factory-postgres             Created jamais démarré
postgres-iafactory              Created jamais démarré
videostudio-adminer             Optionnel (peut redémarrer si besoin)
videostudio-redis               Doublon avec iafactory-video-redis
```

---

## 10. PLAN DE SAUVEGARDE

### 10.1 Commandes de backup volumes critiques

```powershell
# Créer dossier backup
mkdir D:\IAFactory\BACKUPS\2025-12-27

# Backup volumes critiques
docker run --rm -v iafactory-openwebui-data:/data -v D:\IAFactory\BACKUPS\2025-12-27:/backup alpine tar czf /backup/openwebui-data.tar.gz /data

docker run --rm -v iaf-dz-qdrant-data:/data -v D:\IAFactory\BACKUPS\2025-12-27:/backup alpine tar czf /backup/qdrant-embeddings.tar.gz /data

docker run --rm -v iaf-dz-backend-cache:/data -v D:\IAFactory\BACKUPS\2025-12-27:/backup alpine tar czf /backup/backend-cache.tar.gz /data

docker run --rm -v iafactory-video-studio-pro_postgres_data:/data -v D:\IAFactory\BACKUPS\2025-12-27:/backup alpine tar czf /backup/video-postgres.tar.gz /data

docker run --rm -v ragdz-qdrant-data:/data -v D:\IAFactory\BACKUPS\2025-12-27:/backup alpine tar czf /backup/ragdz-qdrant.tar.gz /data

docker run --rm -v ia-factory-automation_qdrant-data:/data -v D:\IAFactory\BACKUPS\2025-12-27:/backup alpine tar czf /backup/automation-qdrant.tar.gz /data

docker run --rm -v iafactory-video-studio-pro_n8n_data:/data -v D:\IAFactory\BACKUPS\2025-12-27:/backup alpine tar czf /backup/n8n-workflows.tar.gz /data
```

### 10.2 Export images custom importantes

```powershell
# Sauvegarder images qu'on ne peut pas facilement rebuilder
docker save bolt-ai:production -o D:\IAFactory\BACKUPS\2025-12-27\bolt-ai-production.tar

# Les autres images ont des Dockerfiles, pas besoin de sauvegarder
```

### 10.3 Backup configurations

```powershell
# Copier les .env de tous les projets
xcopy /s /i "D:\IAFactory\rag-dz\.env*" "D:\IAFactory\BACKUPS\2025-12-27\configs\"
xcopy /s /i "D:\IAFactory\iafactory-video-studio\.env*" "D:\IAFactory\BACKUPS\2025-12-27\configs\video-studio\"
xcopy /s /i "D:\IAFactory\iafactory-video-studio-pro\.env*" "D:\IAFactory\BACKUPS\2025-12-27\configs\video-studio-pro\"
xcopy /s /i "D:\iafactoryrag\docker\.env*" "D:\IAFactory\BACKUPS\2025-12-27\configs\iafactoryrag\"
```

### 10.4 Script de nettoyage (après backup!)

```powershell
# ATTENTION: Exécuter seulement après backup complet!

# 1. Arrêter containers à supprimer
docker stop private-gpt-private-gpt-ollama-1 private-gpt-ollama-cpu-1 private-gpt-ollama-1
docker stop bolt-diy-fresh-app-dev-1 dziria-app-dev-1
docker stop iaf-ollama ia-factory-postgres postgres-iafactory

# 2. Supprimer containers
docker rm private-gpt-private-gpt-ollama-1 private-gpt-ollama-cpu-1 private-gpt-ollama-1
docker rm bolt-diy-fresh-app-dev-1 dziria-app-dev-1
docker rm iaf-ollama ia-factory-postgres postgres-iafactory

# 3. Supprimer images lourdes inutiles
docker rmi video-operator-video-operator
docker rmi dzirvideo-dzirvideo
docker rmi bolt-ai:development
docker rmi rag-dz-backend-local

# 4. Nettoyer images dangling
docker image prune -f

# 5. Nettoyer volumes orphelins (ATTENTION!)
docker volume prune -f

# 6. Nettoyer build cache
docker builder prune -f
```

### 10.5 Espace récupérable estimé

| Type | Taille estimée |
|------|----------------|
| Images à supprimer | ~35 GB |
| Volumes orphelins | ~2 GB |
| Build cache | ~21 GB |
| **TOTAL** | **~58 GB** |

---

## RESUME EXECUTIF

| Catégorie | Quantité | Action |
|-----------|----------|--------|
| ✅ Containers à GARDER | 17 | Continuer |
| ⚠️ À SAUVEGARDER | 8 | Backup puis décision |
| 🔄 RECONSTRUCTIBLES | 7 | Supprimer container, garder code |
| ❌ À SUPPRIMER | 9 | Supprimer après backup |
| Volumes CRITIQUES | 7 | Backup obligatoire |
| Images ÉNORMES | 4 | Supprimer (~35GB) |
| docker-compose ACTIFS | 4 | Garder |
| docker-compose OBSOLETES | 8+ | Archiver/supprimer |

**Prochaines étapes:**
1. Exécuter les commandes de backup section 10.1-10.3
2. Vérifier les backups sont complets
3. Exécuter le nettoyage section 10.4
4. Consolider les docker-compose variants
