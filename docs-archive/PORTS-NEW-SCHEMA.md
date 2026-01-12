# 🔢 Nouveau Schéma de Ports IAFactory

**Appliqué le** : 11 janvier 2026, 07h30

## 🌐 CORE (Mutualisé - toujours actif)

| Service | Port | Projet |
|---------|------|--------|
| Gateway API | **3001** | iafactory-gateway |
| PostgreSQL shared | **5432** | shared (optionnel) |
| Redis shared | **6379** | shared (optionnel) |

---

## 📦 PROJET 1 : rag-dz (Range: 8180-8199, 3737, 5173-5174)

| Service | Ancien port | Nouveau port |
|---------|-------------|--------------|
| Backend API | 8180 | **8180** (inchangé) |
| Archon Server | 8181 | **8181** (inchangé) |
| Archon UI | 3737 | **3737** (inchangé) |
| RAG UI | 5173 | **5173** (inchangé) |
| Bolt | 5174 | **5174** (inchangé) |
| PostgreSQL | 5432 | **5433** |
| Redis | 6379 | **6380** |
| Qdrant | 6333 | **6334** |
| Ollama | 11434 | **11435** |
| Meilisearch | 7700 | **7701** |

---

## 📦 PROJET 2 : iafactory-academy (Range: 8200-8219, 3100)

| Service | Ancien port | Nouveau port |
|---------|-------------|--------------|
| Backend | 8000 | **8200** |
| Frontend | 3000 | **3100** |
| PostgreSQL | 5432 | **5434** |
| Redis | 6379 | **6381** |

---

## 📦 PROJET 3 : iafactory-ai-tools (Range: 8220-8239, 3110)

| Service | Ancien port | Nouveau port |
|---------|-------------|--------------|
| Backend | 8001 | **8220** |
| Frontend | 3000 | **3110** |
| PostgreSQL | 5432 | **5435** |
| Redis | 6379 | **6382** |
| MinIO API | 9000 | **9002** |
| MinIO Console | 9001 | **9003** |

---

## 📦 PROJET 4 : iafactory-video-platform (Range: 8240-8259, 3120)

| Service | Ancien port | Nouveau port |
|---------|-------------|--------------|
| Backend | 8000 | **8240** |
| Frontend | 3000 | **3120** |
| PostgreSQL | 5432 | **5436** |
| Redis | 6379 | **6383** |
| Celery Flower | 5555 | **5556** |
| MinIO API | 9000 | **9004** |
| MinIO Console | 9001 | **9005** |

---

## 🌍 STACK ALGERIA (Range: 8300-8319, 3300)

| Service | Ancien port | Nouveau port |
|---------|-------------|--------------|
| Backend | 8000 | **8300** |
| Frontend | 3000 | **3300** |
| PostgreSQL | 5432 | **5437** |
| Redis | 6379 | **6384** |
| Qdrant | 6333 | **6335** |

---

## 🇨🇭 STACK SWITZERLAND (Range: 8320-8339, 3320)

| Service | Ancien port | Nouveau port |
|---------|-------------|--------------|
| Backend | 8000 | **8320** |
| Frontend | 3000 | **3320** |
| PostgreSQL | 5432 | **5438** |
| Redis | 6379 | **6385** |
| Qdrant | 6333 | **6336** |
