# DOCKER COMPOSE MULTI-ENVIRONNEMENT - IAFACTORY

**PROMPT 8** - Configuration Docker complete pour monorepo multi-region
**Date**: 2025-12-29
**Regions**: Algeria (DZ) + Switzerland (CH)

---

## TABLE DES MATIERES

1. [Vue d'Ensemble](#1-vue-densemble)
2. [Fichiers Generes](#2-fichiers-generes)
3. [Architecture des Ports](#3-architecture-des-ports)
4. [Guide d'Utilisation](#4-guide-dutilisation)
5. [Variables d'Environnement](#5-variables-denvironnement)
6. [Profiles Docker](#6-profiles-docker)
7. [Commandes Rapides](#7-commandes-rapides)
8. [Deploiement Production](#8-deploiement-production)

---

## 1. VUE D'ENSEMBLE

### Architecture Multi-Region

```
                    ┌─────────────────────────────────────────────────┐
                    │              IAFACTORY PLATFORM                  │
                    │                 (MONOREPO)                       │
                    └─────────────────────────────────────────────────┘
                                          │
              ┌───────────────────────────┴───────────────────────────┐
              │                                                        │
    ┌─────────▼─────────┐                              ┌──────────────▼──────────────┐
    │   ALGERIA (DZ)    │                              │    SWITZERLAND (CH)         │
    │                   │                              │                             │
    │  ┌─────────────┐  │                              │  ┌─────────────┐           │
    │  │ PostgreSQL  │  │                              │  │ PostgreSQL  │           │
    │  │ Port: 5432  │  │                              │  │ Port: 5433  │           │
    │  └─────────────┘  │                              │  └─────────────┘           │
    │  ┌─────────────┐  │                              │  ┌─────────────┐           │
    │  │   Redis     │  │                              │  │   Redis     │           │
    │  │ Port: 6379  │  │                              │  │ Port: 6380  │           │
    │  └─────────────┘  │                              │  └─────────────┘           │
    │  ┌─────────────┐  │                              │  ┌─────────────┐           │
    │  │   Qdrant    │  │                              │  │   Qdrant    │           │
    │  │ Port: 6333  │  │                              │  │ Port: 6335  │           │
    │  └─────────────┘  │                              │  └─────────────┘           │
    │  ┌─────────────┐  │                              │  ┌─────────────┐           │
    │  │  Backend    │  │                              │  │  Backend    │           │
    │  │ Port: 8000  │  │                              │  │ Port: 8001  │           │
    │  └─────────────┘  │                              │  └─────────────┘           │
    │  ┌─────────────┐  │                              │  ┌─────────────┐           │
    │  │  Frontend   │  │                              │  │  Frontend   │           │
    │  │ Port: 3000  │  │                              │  │ Port: 3001  │           │
    │  └─────────────┘  │                              │  └─────────────┘           │
    │                   │                              │                             │
    │  Chargily (DZD)   │                              │  Stripe (CHF)              │
    │  fr/ar/en/darija  │                              │  fr/de/it/en               │
    │  Africa/Algiers   │                              │  Europe/Zurich             │
    │                   │                              │                             │
    └───────────────────┘                              └─────────────────────────────┘
```

### Differences Cles

| Aspect | Algeria (DZ) | Switzerland (CH) |
|--------|-------------|------------------|
| **Timezone** | Africa/Algiers | Europe/Zurich |
| **Paiement** | Chargily (DZD) | Stripe (CHF) |
| **Langues** | fr, ar, en, darija | fr, de, it, en |
| **Legal** | Code Commerce DZ | LPD-CH + GDPR |
| **Darija** | Active | Desactive |
| **RTL Arabic** | Active | Desactive |

---

## 2. FICHIERS GENERES

### Structure des Fichiers

```
D:\IAFactory\docker-compose\
├── docker-compose.algeria.yml           # Dev Algeria
├── docker-compose.algeria.prod.yml      # Prod Algeria
├── docker-compose.switzerland.yml       # Dev Switzerland
├── docker-compose.switzerland.prod.yml  # Prod Switzerland
└── DOCKER_COMPOSE_MULTI_ENV.md          # Ce fichier
```

### Destination dans le Monorepo

```
iafactory-platform/
├── deployments/
│   ├── algeria/
│   │   ├── docker-compose.yml           # <- docker-compose.algeria.yml
│   │   ├── docker-compose.prod.yml      # <- docker-compose.algeria.prod.yml
│   │   ├── .env.example
│   │   ├── .env.production.example
│   │   └── ...
│   └── switzerland/
│       ├── docker-compose.yml           # <- docker-compose.switzerland.yml
│       ├── docker-compose.prod.yml      # <- docker-compose.switzerland.prod.yml
│       ├── .env.example
│       ├── .env.production.example
│       └── ...
```

---

## 3. ARCHITECTURE DES PORTS

### Ports Development (Execution Simultanee Possible)

| Service | Algeria (DZ) | Switzerland (CH) |
|---------|-------------|------------------|
| **PostgreSQL** | 5432 | 5433 |
| **Redis** | 6379 | 6380 |
| **Qdrant HTTP** | 6333 | 6335 |
| **Qdrant gRPC** | 6334 | 6336 |
| **Meilisearch** | 7700 | 7701 |
| **Backend API** | 8000 | 8001 |
| **Frontend Main** | 3000 | 3001 |
| **Frontend RAG** | 5173 | 5174 |
| **n8n Workflow** | 5678 | 5679 |
| **Adminer** | 8080 | 8081 |
| **Prometheus** | 9090 | 9091 |
| **Grafana** | 3002 | 3003 |
| **Ollama** | 11434 | 11435 |
| **AnythingLLM** | 3001 | 3005 |
| **Agent Consultant** | 8501 | 8504 |
| **Agent Data** | 8502 | 8505 |
| **Agent Support** | 8503 | 8506 |

### Ports Production (VPS Separes)

En production, chaque region a son propre VPS, donc les ports sont standards:

| Service | Port Interne | Port Expose |
|---------|-------------|-------------|
| PostgreSQL | 5432 | 127.0.0.1:5432 |
| Redis | 6379 | 127.0.0.1:6379 |
| Backend | 8000 | 127.0.0.1:8000 |
| Frontend | 3000 | 127.0.0.1:3000 |
| Nginx | 80/443 | 0.0.0.0:80/443 |

---

## 4. GUIDE D'UTILISATION

### 4.1 Development Local

#### Lancer Algeria uniquement

```bash
cd deployments/algeria
cp .env.example .env
# Editer .env avec vos valeurs

# Services essentiels
docker-compose up -d

# Avec RAG UI
docker-compose --profile full up -d

# Avec agents IA
docker-compose --profile agents up -d

# Avec monitoring
docker-compose --profile monitoring up -d

# Tout
docker-compose --profile full --profile agents --profile monitoring up -d
```

#### Lancer Switzerland uniquement

```bash
cd deployments/switzerland
cp .env.example .env
# Editer .env avec vos valeurs

docker-compose up -d
```

#### Lancer les DEUX simultanement

```bash
# Terminal 1 - Algeria
cd deployments/algeria
docker-compose up -d

# Terminal 2 - Switzerland
cd deployments/switzerland
docker-compose up -d

# Verifier
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### 4.2 Verifier les Services

```bash
# Health checks
curl http://localhost:8000/health  # Algeria API
curl http://localhost:8001/health  # Switzerland API

# Ouvrir les frontends
start http://localhost:3000        # Algeria Frontend
start http://localhost:3001        # Switzerland Frontend
```

---

## 5. VARIABLES D'ENVIRONNEMENT

### 5.1 Variables Communes (les deux regions)

```env
# LLM Providers
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
GROQ_API_KEY=gsk_xxx
DEEPSEEK_API_KEY=sk-xxx
GOOGLE_GENERATIVE_AI_API_KEY=AIzaSy-xxx

# Security
API_SECRET_KEY=change-me-min-32-chars
JWT_SECRET_KEY=change-me-jwt-secret

# Embeddings
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
EMBEDDING_DEVICE=cpu

# Reranking
USE_RERANKING=true
RERANKING_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
```

### 5.2 Variables Specifiques Algeria

```env
# Region
REGION=algeria
REGION_CODE=DZ
TIMEZONE=Africa/Algiers

# Database
POSTGRES_USER=iafactory_dz
POSTGRES_DB=iafactory_dz

# Payment - Chargily
PAYMENT_PROVIDER=chargily
CHARGILY_API_KEY=xxx
CHARGILY_SECRET_KEY=xxx
CHARGILY_MODE=test
PAYMENT_CURRENCY=DZD

# Features
ENABLE_DARIJA=true
ENABLE_ARABIC_RTL=true
LEGAL_FRAMEWORK=algeria
```

### 5.3 Variables Specifiques Switzerland

```env
# Region
REGION=switzerland
REGION_CODE=CH
TIMEZONE=Europe/Zurich

# Database
POSTGRES_USER=iafactory_ch
POSTGRES_DB=iafactory_ch

# Payment - Stripe
PAYMENT_PROVIDER=stripe
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_PUBLIC_KEY=pk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
PAYMENT_CURRENCY=CHF

# Features
ENABLE_DARIJA=false
ENABLE_ARABIC_RTL=false
LEGAL_FRAMEWORK=switzerland

# Compliance
GDPR_COMPLIANT=true
LPD_CH_COMPLIANT=true
```

---

## 6. PROFILES DOCKER

Les profiles permettent de lancer des groupes de services optionnels.

### Profiles Disponibles

| Profile | Services | Usage |
|---------|----------|-------|
| **default** | postgres, redis, qdrant, meilisearch, backend, frontend | Services essentiels |
| **full** | + rag-ui | Frontend RAG additionnel |
| **agents** | + consultant, data-analysis, customer-support | Agents Streamlit |
| **automation** | + n8n | Workflows automatises |
| **monitoring** | + prometheus, grafana | Observabilite |
| **admin** | + adminer | Administration DB |
| **ai-local** | + ollama | LLM local souverain |
| **extras** | + anythingllm | Outils RAG additionnels |

### Exemples d'Utilisation

```bash
# Services essentiels seulement
docker-compose up -d

# Avec agents IA
docker-compose --profile agents up -d

# Avec tout sauf monitoring
docker-compose --profile full --profile agents --profile automation --profile admin up -d

# Stack complete
docker-compose --profile full --profile agents --profile automation --profile monitoring --profile admin --profile ai-local up -d
```

---

## 7. COMMANDES RAPIDES

### Development

```bash
# === ALGERIA ===
# Demarrer
cd deployments/algeria && docker-compose up -d

# Logs backend
docker-compose logs -f iaf-backend

# Rebuild apres modification
docker-compose up -d --build iaf-backend

# Arreter
docker-compose down

# Supprimer les volumes (ATTENTION: perte de donnees)
docker-compose down -v


# === SWITZERLAND ===
# Demarrer
cd deployments/switzerland && docker-compose up -d

# Logs
docker-compose logs -f iaf-backend

# Arreter
docker-compose down
```

### Production

```bash
# === ALGERIA (sur VPS Alger) ===
cd deployments/algeria
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml logs -f

# === SWITZERLAND (sur VPS Geneve) ===
cd deployments/switzerland
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml logs -f
```

### Maintenance

```bash
# Backup PostgreSQL
docker-compose exec iaf-postgres pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup.sql

# Restore PostgreSQL
docker-compose exec -T iaf-postgres psql -U $POSTGRES_USER $POSTGRES_DB < backup.sql

# Nettoyer les images non utilisees
docker system prune -a

# Voir l'utilisation disque
docker system df
```

---

## 8. DEPLOIEMENT PRODUCTION

### 8.1 Pre-requis VPS

| Ressource | Minimum | Recommande |
|-----------|---------|------------|
| **RAM** | 8 GB | 16 GB |
| **CPU** | 4 cores | 8 cores |
| **Disque** | 100 GB SSD | 200 GB SSD |
| **OS** | Ubuntu 22.04 LTS | Ubuntu 24.04 LTS |
| **Docker** | 24.0+ | Latest |

### 8.2 Checklist Deploiement

```
[ ] VPS provisionne (Alger pour DZ, Geneve pour CH)
[ ] Docker et Docker Compose installes
[ ] Repository clone
[ ] .env.production configure avec vraies valeurs
[ ] Secrets securises (pas de valeurs par defaut)
[ ] DNS configure (A records)
[ ] Certificats SSL (Let's Encrypt via Certbot)
[ ] Firewall configure (80, 443 ouverts)
[ ] Backup automatique configure
[ ] Monitoring actif
```

### 8.3 Script de Deploiement

```bash
#!/bin/bash
# deploy.sh <region> <environment>

REGION=$1
ENV=${2:-production}

echo "Deploying IAFactory $REGION ($ENV)..."

cd deployments/$REGION

# Pull latest
git pull origin main

# Build and start
if [ "$ENV" == "production" ]; then
    docker-compose -f docker-compose.prod.yml pull
    docker-compose -f docker-compose.prod.yml up -d --build
else
    docker-compose pull
    docker-compose up -d --build
fi

# Health check
sleep 30
curl -f http://localhost:8000/health || exit 1

echo "Deployment complete!"
```

### 8.4 Configuration Nginx (Production)

Fichier: `deployments/algeria/nginx/nginx.prod.conf`

```nginx
events {
    worker_connections 1024;
}

http {
    # SSL Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=general:10m rate=30r/s;

    # API Backend
    upstream backend {
        server iaf-backend:8000;
    }

    # Frontend
    upstream frontend {
        server iaf-frontend:3000;
    }

    # HTTP -> HTTPS redirect
    server {
        listen 80;
        server_name iafactory-algeria.com api.iafactory-algeria.com app.iafactory-algeria.com;
        return 301 https://$host$request_uri;
    }

    # Main App
    server {
        listen 443 ssl http2;
        server_name app.iafactory-algeria.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        location / {
            limit_req zone=general burst=50 nodelay;
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

    # API
    server {
        listen 443 ssl http2;
        server_name api.iafactory-algeria.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        location / {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_read_timeout 300s;
        }

        location /ws {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

---

## RESUME

### Fichiers Crees

| Fichier | Taille | Description |
|---------|--------|-------------|
| `docker-compose.algeria.yml` | ~450 lignes | Dev stack Algeria |
| `docker-compose.switzerland.yml` | ~450 lignes | Dev stack Switzerland |
| `docker-compose.algeria.prod.yml` | ~350 lignes | Prod stack Algeria |
| `docker-compose.switzerland.prod.yml` | ~350 lignes | Prod stack Switzerland |

### Services par Region

| Service | Algeria | Switzerland |
|---------|---------|-------------|
| PostgreSQL + PGVector | iaf-dz-postgres | iaf-ch-postgres |
| Redis | iaf-dz-redis | iaf-ch-redis |
| Qdrant | iaf-dz-qdrant | iaf-ch-qdrant |
| Meilisearch | iaf-dz-meilisearch | iaf-ch-meilisearch |
| Backend API | iaf-dz-backend | iaf-ch-backend |
| Frontend | iaf-dz-frontend | iaf-ch-frontend |
| n8n | iaf-dz-n8n | iaf-ch-n8n |
| Prometheus | iaf-dz-prometheus | iaf-ch-prometheus |
| Grafana | iaf-dz-grafana | iaf-ch-grafana |

### Prochaines Etapes

1. **Copier les fichiers** dans `deployments/{algeria,switzerland}/`
2. **Creer les .env.example** avec les templates fournis
3. **Tester localement** les deux stacks
4. **Deployer en production** sur VPS separes

---

*Document genere par Claude Code - PROMPT 8*
*Date: 29 Decembre 2025*
