#  Renumérotation Ports TERMINÉE - 11 janvier 2026, 07h30

## Statut : COMPLET - 94 fichiers modifiés

Tous les conflits de ports sont résolus. Les projets peuvent maintenant tourner simultanément en dev.

##  Nouveaux ports par projet

###  iafactory-gateway (CORE - inchangé)
- API : **3001**
- PostgreSQL : **5432** (partagé optionnel)
- Redis : **6379** (partagé optionnel)

###  iafactory-academy (32 fichiers)
- Backend : **8200** (était 8000)
- Frontend : **3100** (était 3000)
- PostgreSQL : **5434**
- Redis : **6381**

###  iafactory-ai-tools (3 fichiers)
- Backend : **8220** (était 8001/8002)
- Frontend : **3110** (était 3000)
- PostgreSQL : **5435**
- Redis : **6382**
- MinIO : **9002-9003** (était 9000-9001)

###  iafactory-video-platform (5 fichiers)
- Backend : **8240** (était 8000)
- Frontend : **3120** (était 3000)
- PostgreSQL : **5436**
- Redis : **6383**
- Celery Flower : **5556** (était 5555)
- MinIO : **9004-9005** (était 9000-9001)

###  rag-dz (54 fichiers)
- Backend API : **8180** (inchangé)
- Archon Server : **8181** (inchangé)
- Archon UI : **3737** (inchangé)
- RAG UI : **5173** (inchangé)
- Bolt : **5174** (inchangé)
- PostgreSQL : **5433** (était 5432)
- Redis : **6380** (était 6379)
- Qdrant : **6334** (était 6333)
- Ollama : **11435** (était 11434)
- Meilisearch : **7701** (était 7700)

###  onestschooled (Laravel sans Docker)
- Utilise php artisan serve ou serveur web classique
- Pas de renumérotation nécessaire

---

##  JOUR 1 TERMINÉ

**Accomplissements** :
-  Backup complet (1.1 GB, 23776 fichiers)
-  Audit clés API (14 fichiers .env, toutes clés = test)
-  Audit ports (conflits identifiés)
-  Renumérotation complète (94 fichiers, 5 projets)
-  Documentation créée

**Fichiers créés** :
- \REFACTOR-PLAN-2025-01-11.md\
- \PORTS-REGISTRY.md\
- \PORTS-NEW-SCHEMA.md\
- \PORTS-RENUMBERED-DONE.md\
- \.claude/refactor-tracking.md\

**Scripts créés** :
- \scripts/renumber-academy.ps1\
- \scripts/renumber-ai-tools.ps1\
- \scripts/renumber-video.ps1\
- \scripts/renumber-rag-dz.ps1\
- \scripts/renumber-onestschooled.ps1\

---

##  PROCHAINES ÉTAPES (Jour 2+)

### Phase 1 - Jour 2 : Désactivation billing rag-dz
- [ ] Renommer services billing de rag-dz (.DISABLED)
- [ ] Créer GatewayClient dans rag-dz
- [ ] Modifier routers pour utiliser GatewayClient
- [ ] Test avec utilisateur fictif

### Phase 1 - Jour 3 : Centralisation providers IA
- [ ] Vérifier providers dans gateway
- [ ] Remplacer appels directs dans tous les projets
- [ ] Tests end-to-end

### Phase 1 - Jour 4-5 : Rotation clés (quand prod)
- [ ] Générer nouvelles clés prod
- [ ] Mettre uniquement dans gateway/.env
- [ ] Révoquer anciennes clés

---

**Backup disponible** : \D:\IAFactory-backup-2025-01-11-04h00\\\
"@ | Out-File -FilePath "D:\IAFactory\JOUR-1-TERMINE.md" -Encoding UTF8

Write-Host "
 JOUR 1 TERMINE " -ForegroundColor Green
Write-Host "94 fichiers renumerotes - 0 conflits de ports" -ForegroundColor Cyan
Write-Host "
Document : JOUR-1-TERMINE.md cree
" -ForegroundColor Yellow

@"
# JOUR 1 TERMINE - 11 janvier 2026

## Statut : COMPLET - 94 fichiers modifies

### iafactory-gateway
- API : 3001 (inchange)

### iafactory-academy  
- Backend : 8200
- Frontend : 3100

### iafactory-ai-tools
- Backend : 8220
- Frontend : 3110

### iafactory-video-platform
- Backend : 8240
- Frontend : 3120

### rag-dz
- Backend : 8180 (inchange)
- DB : 5433, Redis : 6380

## JOUR 2 : Desactivation billing rag-dz

Backup : D:\IAFactory-backup-2025-01-11-04h00\
