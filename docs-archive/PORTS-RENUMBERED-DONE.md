#  Renumérotation Ports Terminée - 11 janvier 2026

## Statut : COMPLET

**94 fichiers modifiés** - Aucun conflit de ports

## Nouveaux ports par projet

### iafactory-gateway (inchangé)
- API : 3001
- PostgreSQL : 5432 (partagé)
- Redis : 6379 (partagé)

### iafactory-academy
- Backend : 8200 (était 8000)
- Frontend : 3100 (était 3000)
- PostgreSQL : 5434 (était 5432)
- Redis : 6381 (était 6379)

### iafactory-ai-tools
- Backend : 8220 (était 8001/8002)
- Frontend : 3110 (était 3000)
- PostgreSQL : 5435
- Redis : 6382
- MinIO : 9002-9003 (était 9000-9001)

### iafactory-video-platform
- Backend : 8240 (était 8000)
- Frontend : 3120 (était 3000)
- PostgreSQL : 5436
- Redis : 6383
- Celery Flower : 5556 (était 5555)
- MinIO : 9004-9005 (était 9000-9001)

### rag-dz
- Backend API : 8180 (inchangé)
- Archon Server : 8181 (inchangé)
- Archon UI : 3737 (inchangé)
- RAG UI : 5173 (inchangé)
- Bolt : 5174 (inchangé)
- PostgreSQL : 5433 (était 5432)
- Redis : 6380 (était 6379)
- Qdrant : 6334 (était 6333)
- Ollama : 11435 (était 11434)
- Meilisearch : 7701 (était 7700)

## Prochaines étapes

1. Tester chaque projet individuellement avec Docker
2. Désactiver les services billing de rag-dz (Phase 1 - Jour 2)
3. Centraliser providers IA dans gateway (Phase 1 - Jour 3)

**Backup disponible** : D:\IAFactory-backup-2025-01-11-04h00\
