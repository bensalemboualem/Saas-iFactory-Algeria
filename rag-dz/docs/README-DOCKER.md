# IAFactory RAG-DZ - Guide Docker

> Documentation complète pour déployer la stack IAFactory avec Docker.

## Table des matières

- [Prérequis](#prérequis)
- [Démarrage rapide](#démarrage-rapide)
- [Configurations disponibles](#configurations-disponibles)
- [Services et ports](#services-et-ports)
- [Profiles Docker](#profiles-docker)
- [Commandes utiles](#commandes-utiles)
- [Troubleshooting](#troubleshooting)

---

## Prérequis

- **Docker** >= 24.0
- **Docker Compose** >= 2.20
- **RAM** : 4 Go minimum (8 Go recommandé)
- **Disque** : 10 Go minimum

```bash
# Vérifier les versions
docker --version
docker compose version
```

---

## Démarrage rapide

### 1. Configurer l'environnement

```bash
# Copier le fichier d'exemple
cp .env.docker.example .env

# Éditer avec vos clés API (au minimum GROQ_API_KEY pour le LLM)
# Windows: notepad .env
# Linux/Mac: nano .env
```

### 2. Démarrer la stack minimale (RAG seulement)

```bash
docker compose -f docker-compose.minimal.yml up -d
```

**Services démarrés :**
- PostgreSQL + PGVector : `localhost:5432`
- Redis : `localhost:6379`
- Qdrant : `localhost:6333`
- AnythingLLM : `localhost:3001`

### 3. Démarrer la stack complète

```bash
docker compose up -d
```

**Services additionnels :**
- Backend API : `localhost:8000`
- Frontend : `localhost:3000`
- N8N Workflows : `localhost:5678`
- Adminer : `localhost:8080`

---

## Configurations disponibles

| Fichier | Usage | Commande |
|---------|-------|----------|
| `docker-compose.minimal.yml` | RAG uniquement (dev) | `docker compose -f docker-compose.minimal.yml up -d` |
| `docker-compose.yml` | Stack complète | `docker compose up -d` |

---

## Services et ports

### Stack Minimale

| Service | Port | Description | URL |
|---------|------|-------------|-----|
| PostgreSQL | 5432 | Base de données + PGVector | - |
| Redis | 6379 | Cache | - |
| Qdrant | 6333/6334 | Vector DB | http://localhost:6333/dashboard |
| AnythingLLM | 3001 | Interface RAG | http://localhost:3001 |

### Stack Complète

| Service | Port | Description | URL |
|---------|------|-------------|-----|
| iaf-backend | 8000 | API FastAPI | http://localhost:8000/docs |
| iaf-frontend | 3000 | Next.js UI | http://localhost:3000 |
| iaf-n8n | 5678 | Workflow automation | http://localhost:5678 |
| iaf-adminer | 8080 | Admin DB | http://localhost:8080 |

### Profiles optionnels

| Profile | Services | Commande |
|---------|----------|----------|
| `monitoring` | Prometheus + Grafana | `docker compose --profile monitoring up -d` |
| `video` | Video Studio | `docker compose --profile video up -d` |
| `agents` | AI Agents Streamlit | `docker compose --profile agents up -d` |
| `extras` | Flowise + Firecrawl | `docker compose --profile extras up -d` |
| `ai-local` | Ollama (LLM local) | `docker compose --profile ai-local up -d` |

---

## Profiles Docker

Démarrer des services spécifiques :

```bash
# Stack de base + monitoring
docker compose --profile monitoring up -d

# Stack de base + video studio
docker compose --profile video up -d

# Tout activer
docker compose --profile monitoring --profile video --profile agents --profile extras up -d
```

---

## Commandes utiles

### Gestion de base

```bash
# Démarrer
docker compose up -d

# Arrêter
docker compose down

# Voir les logs
docker compose logs -f

# Logs d'un service spécifique
docker compose logs -f iaf-backend

# Redémarrer un service
docker compose restart iaf-backend

# État des services
docker compose ps
```

### Maintenance

```bash
# Reconstruire les images
docker compose build --no-cache

# Nettoyer les volumes (ATTENTION: supprime les données)
docker compose down -v

# Nettoyer les images non utilisées
docker system prune -a
```

### Base de données

```bash
# Accéder à PostgreSQL
docker exec -it iaf-postgres psql -U iafactory -d iafactory

# Backup
docker exec iaf-postgres pg_dump -U iafactory iafactory > backup.sql

# Restore
docker exec -i iaf-postgres psql -U iafactory iafactory < backup.sql
```

### Redis

```bash
# CLI Redis
docker exec -it iaf-redis redis-cli

# Vider le cache
docker exec iaf-redis redis-cli FLUSHALL
```

---

## Troubleshooting

### Port déjà utilisé

```
Error: bind: address already in use
```

**Solution :**
```bash
# Trouver le processus
# Windows:
netstat -ano | findstr :5432
# Linux/Mac:
lsof -i :5432

# Changer le port dans docker-compose.yml
# ports:
#   - "5433:5432"  # Utiliser 5433 à la place
```

### Problème de mémoire

```
Container exited with code 137
```

**Solution :** Augmenter la mémoire Docker (Docker Desktop > Settings > Resources)

### Healthcheck échoue

```bash
# Vérifier les logs
docker compose logs iaf-postgres

# Vérifier la santé
docker inspect iaf-postgres | grep -A 10 Health
```

### Volumes corrompus

```bash
# Supprimer et recréer
docker compose down -v
docker compose up -d
```

### Reset complet

```bash
# Tout supprimer (ATTENTION: perte de données)
docker compose down -v --rmi all
docker volume prune -f
docker network prune -f

# Relancer
docker compose up -d
```

---

## Architecture réseau

```
                    ┌─────────────────────────────────────┐
                    │       iafactory-network             │
                    │                                     │
  ┌─────────────────┼─────────────────────────────────────┼────────────────┐
  │                 │                                     │                │
  │   ┌─────────┐   │   ┌─────────┐     ┌─────────┐       │   ┌─────────┐  │
  │   │ Backend │───┼───│ Postgres│     │  Redis  │       │   │ Frontend│  │
  │   │  :8000  │   │   │  :5432  │     │  :6379  │       │   │  :3000  │  │
  │   └────┬────┘   │   └─────────┘     └─────────┘       │   └─────────┘  │
  │        │        │                                     │                │
  │        │        │   ┌─────────┐     ┌─────────────┐   │                │
  │        └────────┼───│ Qdrant  │     │ AnythingLLM │   │                │
  │                 │   │  :6333  │     │   :3001     │   │                │
  │                 │   └─────────┘     └─────────────┘   │                │
  │                 │                                     │                │
  └─────────────────┴─────────────────────────────────────┴────────────────┘
```

---

## Support

- **Issues** : https://github.com/iafactory/rag-dz/issues
- **Email** : contact@iafactoryalgeria.com

---

*Généré le 2025-12-27 - IAFactory Algeria*
