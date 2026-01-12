# Guide de Déploiement - IAFactory Platform Suite

**Version:** 2.0.0
**Dernière mise à jour:** Décembre 2024

---

## Vue d'ensemble

Ce guide couvre le déploiement de l'ensemble des projets IAFactory:
- **iafactory-academy** - Plateforme e-learning
- **iafactory-video-platform** - Génération vidéo IA
- **onestschooled** - Gestion scolaire
- **rag-dz** - Meta-orchestrateur Nexus AI

---

## Prérequis Globaux

### Infrastructure

| Composant | Minimum | Recommandé | Production |
|-----------|---------|------------|------------|
| CPU | 4 cores | 8 cores | 16+ cores |
| RAM | 8 GB | 16 GB | 32+ GB |
| Stockage | 100 GB SSD | 250 GB NVMe | 500+ GB NVMe |
| Réseau | 100 Mbps | 500 Mbps | 1+ Gbps |

### Logiciels

```bash
# Versions minimales requises
Docker >= 24.0
Docker Compose >= 2.20
Git >= 2.40
Node.js >= 18.0
Python >= 3.11
PHP >= 7.4 (pour onestschooled)
```

### Services Cloud

| Service | Obligatoire | Description |
|---------|-------------|-------------|
| PostgreSQL | Oui | Base de données principale |
| Redis | Oui | Cache et queues |
| Supabase | Recommandé | Auth + DB managée |
| AWS S3 / MinIO | Oui | Stockage fichiers |
| Qdrant | Pour RAG | Base vectorielle |

---

## Architecture de Déploiement

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PRODUCTION ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                    ┌─────────────────────────────────┐                       │
│                    │         LOAD BALANCER           │                       │
│                    │         (Nginx/Traefik)         │                       │
│                    └─────────────┬───────────────────┘                       │
│                                  │                                           │
│     ┌────────────────────────────┼────────────────────────────┐             │
│     │                            │                            │             │
│     ▼                            ▼                            ▼             │
│  ┌──────────┐              ┌──────────┐              ┌──────────┐          │
│  │ Academy  │              │  Video   │              │  RAG-DZ  │          │
│  │  :8000   │              │  :8001   │              │  :8100   │          │
│  └────┬─────┘              └────┬─────┘              └────┬─────┘          │
│       │                         │                         │                 │
│       └─────────────────────────┼─────────────────────────┘                 │
│                                 │                                           │
│                    ┌────────────┴────────────┐                              │
│                    │                         │                              │
│              ┌─────┴─────┐             ┌─────┴─────┐                        │
│              │ PostgreSQL│             │   Redis   │                        │
│              │   :5432   │             │   :6379   │                        │
│              └───────────┘             └───────────┘                        │
│                                                                              │
│              ┌───────────┐             ┌───────────┐                        │
│              │  Qdrant   │             │   MinIO   │                        │
│              │   :6333   │             │   :9000   │                        │
│              └───────────┘             └───────────┘                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Déploiement Docker Compose

### 1. Configuration Globale

Créer un fichier `docker-compose.yml` à la racine de IAFactory:

```yaml
# D:\IAFactory\docker-compose.yml

version: '3.8'

services:
  # ============================================
  # DATABASES
  # ============================================
  postgres:
    image: postgres:16-alpine
    container_name: iafactory-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-iafactory}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-secure_password}
      POSTGRES_DB: ${POSTGRES_DB:-iafactory}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U iafactory"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - iafactory-network

  redis:
    image: redis:7-alpine
    container_name: iafactory-redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - iafactory-network

  qdrant:
    image: qdrant/qdrant:latest
    container_name: iafactory-qdrant
    restart: unless-stopped
    volumes:
      - qdrant_data:/qdrant/storage
    ports:
      - "6333:6333"
    networks:
      - iafactory-network

  minio:
    image: minio/minio:latest
    container_name: iafactory-minio
    restart: unless-stopped
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER:-minioadmin}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:-minioadmin}
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"
      - "9001:9001"
    networks:
      - iafactory-network

  # ============================================
  # IAFACTORY ACADEMY
  # ============================================
  academy-backend:
    build:
      context: ./iafactory-academy/backend
      dockerfile: Dockerfile
    container_name: academy-backend
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://iafactory:secure_password@postgres:5432/academy
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    ports:
      - "8000:8000"
    networks:
      - iafactory-network

  academy-frontend:
    build:
      context: ./iafactory-academy/frontend
      dockerfile: Dockerfile
    container_name: academy-frontend
    restart: unless-stopped
    environment:
      - VITE_API_URL=http://academy-backend:8000
    ports:
      - "3000:3000"
    networks:
      - iafactory-network

  # ============================================
  # IAFACTORY VIDEO PLATFORM
  # ============================================
  video-backend:
    build:
      context: ./iafactory-video-platform/backend
      dockerfile: Dockerfile
    container_name: video-backend
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://iafactory:secure_password@postgres:5432/video
      - REDIS_URL=redis://redis:6379/1
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    ports:
      - "8001:8000"
    networks:
      - iafactory-network

  video-frontend:
    build:
      context: ./iafactory-video-platform/frontend
      dockerfile: Dockerfile
    container_name: video-frontend
    restart: unless-stopped
    ports:
      - "3001:3000"
    networks:
      - iafactory-network

  video-worker:
    build:
      context: ./iafactory-video-platform/backend
      dockerfile: Dockerfile
    container_name: video-worker
    restart: unless-stopped
    command: celery -A app.tasks worker -l info -c 4
    depends_on:
      - redis
      - video-backend
    networks:
      - iafactory-network

  # ============================================
  # RAG-DZ (NEXUS)
  # ============================================
  nexus-api:
    build:
      context: ./rag-dz/services/api
      dockerfile: Dockerfile
    container_name: nexus-api
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://iafactory:secure_password@postgres:5432/nexus
      - REDIS_URL=redis://redis:6379/2
      - QDRANT_URL=http://qdrant:6333
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      qdrant:
        condition: service_started
    ports:
      - "8100:8000"
    networks:
      - iafactory-network

  nexus-archon:
    build:
      context: ./rag-dz/frontend/archon-ui/python
      dockerfile: Dockerfile
    container_name: nexus-archon
    restart: unless-stopped
    ports:
      - "8181:8181"
    networks:
      - iafactory-network

  nexus-archon-ui:
    build:
      context: ./rag-dz/frontend/archon-ui
      dockerfile: Dockerfile
    container_name: nexus-archon-ui
    restart: unless-stopped
    ports:
      - "3737:3000"
    networks:
      - iafactory-network

  nexus-bolt:
    build:
      context: ./rag-dz/bolt-diy
      dockerfile: Dockerfile
    container_name: nexus-bolt
    restart: unless-stopped
    ports:
      - "5173:5173"
    networks:
      - iafactory-network

  # ============================================
  # MONITORING
  # ============================================
  pgadmin:
    image: dpage/pgadmin4
    container_name: iafactory-pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@iafactory.dz
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    networks:
      - iafactory-network

  redis-commander:
    image: rediscommander/redis-commander
    container_name: iafactory-redis-commander
    restart: unless-stopped
    environment:
      REDIS_HOSTS: local:redis:6379
    ports:
      - "8081:8081"
    networks:
      - iafactory-network

networks:
  iafactory-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  qdrant_data:
  minio_data:
```

### 2. Script d'Initialisation DB

```sql
-- D:\IAFactory\init-db.sql

-- Créer les bases de données pour chaque projet
CREATE DATABASE academy;
CREATE DATABASE video;
CREATE DATABASE nexus;
CREATE DATABASE onestschooled;

-- Créer l'utilisateur
CREATE USER iafactory_app WITH ENCRYPTED PASSWORD 'app_secure_password';

-- Accorder les permissions
GRANT ALL PRIVILEGES ON DATABASE academy TO iafactory_app;
GRANT ALL PRIVILEGES ON DATABASE video TO iafactory_app;
GRANT ALL PRIVILEGES ON DATABASE nexus TO iafactory_app;
GRANT ALL PRIVILEGES ON DATABASE onestschooled TO iafactory_app;
```

### 3. Fichier .env Global

```bash
# D:\IAFactory\.env

# ============================================
# GLOBAL
# ============================================
COMPOSE_PROJECT_NAME=iafactory
ENVIRONMENT=production

# ============================================
# DATABASE
# ============================================
POSTGRES_USER=iafactory
POSTGRES_PASSWORD=super_secure_password_change_me
POSTGRES_DB=iafactory

# ============================================
# REDIS
# ============================================
REDIS_PASSWORD=redis_secure_password

# ============================================
# MINIO
# ============================================
MINIO_ROOT_USER=iafactory
MINIO_ROOT_PASSWORD=minio_secure_password

# ============================================
# AI PROVIDERS
# ============================================
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
GROQ_API_KEY=gsk_xxx

# ============================================
# OTHER PROVIDERS
# ============================================
ELEVENLABS_API_KEY=xxx
CHARGILY_API_KEY=xxx
CHARGILY_SECRET=xxx

# ============================================
# SUPABASE (optionnel)
# ============================================
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx
SUPABASE_SERVICE_KEY=xxx

# ============================================
# SENTRY (monitoring)
# ============================================
SENTRY_DSN=https://xxx@sentry.io/xxx
```

### 4. Lancement

```bash
# Construire toutes les images
docker-compose build

# Démarrer les services de base
docker-compose up -d postgres redis qdrant minio

# Attendre que les services soient prêts
sleep 30

# Démarrer les applications
docker-compose up -d

# Vérifier le statut
docker-compose ps

# Voir les logs
docker-compose logs -f
```

---

## Configuration Nginx (Reverse Proxy)

```nginx
# /etc/nginx/sites-available/iafactory.dz

# Academy
server {
    listen 443 ssl http2;
    server_name academy.iafactory.dz;

    ssl_certificate /etc/letsencrypt/live/iafactory.dz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/iafactory.dz/privkey.pem;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
    }
}

# Video Platform
server {
    listen 443 ssl http2;
    server_name video.iafactory.dz;

    ssl_certificate /etc/letsencrypt/live/iafactory.dz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/iafactory.dz/privkey.pem;

    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 300s;  # Pour les longues opérations vidéo
    }

    location / {
        proxy_pass http://127.0.0.1:3001;
        proxy_set_header Host $host;
    }
}

# Nexus AI Platform
server {
    listen 443 ssl http2;
    server_name nexus.iafactory.dz;

    ssl_certificate /etc/letsencrypt/live/iafactory.dz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/iafactory.dz/privkey.pem;

    location /api/ {
        proxy_pass http://127.0.0.1:8100;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /archon/ {
        proxy_pass http://127.0.0.1:8181;
        proxy_set_header Host $host;
    }

    location /bolt/ {
        proxy_pass http://127.0.0.1:5173;
        proxy_set_header Host $host;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location / {
        proxy_pass http://127.0.0.1:3737;
        proxy_set_header Host $host;
    }
}
```

---

## SSL avec Let's Encrypt

```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx

# Obtenir les certificats
sudo certbot --nginx -d academy.iafactory.dz \
                     -d video.iafactory.dz \
                     -d nexus.iafactory.dz

# Configurer le renouvellement automatique
sudo crontab -e
# Ajouter:
0 3 * * * /usr/bin/certbot renew --quiet
```

---

## Migrations

### Academy

```bash
docker-compose exec academy-backend alembic upgrade head
```

### Video Platform

```bash
docker-compose exec video-backend alembic upgrade head
```

### RAG-DZ

```bash
docker-compose exec nexus-api alembic upgrade head
```

### OneStSchooled

```bash
# Si utilisant Docker
docker-compose exec onestschooled php artisan migrate --seed

# Sinon, manuellement
cd onestschooled
php artisan migrate:fresh --seed --path=database/migrations/tenant
```

---

## Backups

### Script de Backup

```bash
#!/bin/bash
# D:\IAFactory\scripts\backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/iafactory/$DATE"

mkdir -p $BACKUP_DIR

echo "=== Starting IAFactory Backup ==="

# PostgreSQL
echo "Backing up PostgreSQL..."
docker exec iafactory-postgres pg_dumpall -U iafactory | gzip > $BACKUP_DIR/postgres.sql.gz

# Redis
echo "Backing up Redis..."
docker exec iafactory-redis redis-cli BGSAVE
docker cp iafactory-redis:/data/dump.rdb $BACKUP_DIR/redis.rdb

# MinIO
echo "Backing up MinIO..."
docker exec iafactory-minio mc mirror /data $BACKUP_DIR/minio/

# Qdrant
echo "Backing up Qdrant..."
docker cp iafactory-qdrant:/qdrant/storage $BACKUP_DIR/qdrant/

# Upload to S3
echo "Uploading to S3..."
aws s3 sync $BACKUP_DIR s3://iafactory-backups/$DATE/

# Cleanup old backups (keep 30 days)
find /backup/iafactory -type d -mtime +30 -exec rm -rf {} \;

echo "=== Backup Complete ==="
```

### Cron

```bash
# Backup quotidien à 2h du matin
0 2 * * * /opt/iafactory/scripts/backup.sh >> /var/log/iafactory-backup.log 2>&1
```

---

## Monitoring

### Health Checks

```bash
# Vérifier tous les services
curl -s http://localhost:8000/health  # Academy
curl -s http://localhost:8001/health  # Video
curl -s http://localhost:8100/health  # Nexus
```

### Prometheus + Grafana

```yaml
# Ajouter à docker-compose.yml

prometheus:
  image: prom/prometheus
  container_name: iafactory-prometheus
  volumes:
    - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"
  networks:
    - iafactory-network

grafana:
  image: grafana/grafana
  container_name: iafactory-grafana
  environment:
    GF_SECURITY_ADMIN_PASSWORD: admin
  volumes:
    - grafana_data:/var/lib/grafana
  ports:
    - "3100:3000"
  networks:
    - iafactory-network
```

---

## Troubleshooting

### Problèmes Courants

| Problème | Solution |
|----------|----------|
| Container ne démarre pas | `docker-compose logs <service>` |
| Erreur de connexion DB | Vérifier les credentials dans .env |
| Port déjà utilisé | `lsof -i :<port>` puis tuer le processus |
| Out of memory | Augmenter la RAM ou réduire les workers |
| Permission denied | `chmod +x` sur les scripts |

### Logs Utiles

```bash
# Logs d'un service
docker-compose logs -f academy-backend

# Logs PostgreSQL
docker-compose logs -f postgres

# Logs Redis
docker-compose logs -f redis

# Tous les logs
docker-compose logs -f
```

### Redémarrage Propre

```bash
# Arrêter tout
docker-compose down

# Nettoyer les volumes (ATTENTION: perte de données)
docker-compose down -v

# Reconstruire et redémarrer
docker-compose build --no-cache
docker-compose up -d
```

---

## Checklist de Déploiement

### Pré-déploiement

- [ ] Clés API configurées (.env)
- [ ] Domaines DNS configurés
- [ ] Certificats SSL prêts
- [ ] Firewall configuré
- [ ] Backups configurés

### Déploiement

- [ ] Images Docker construites
- [ ] Bases de données migrées
- [ ] Services démarrés
- [ ] Health checks passent
- [ ] Logs sans erreurs

### Post-déploiement

- [ ] Tests fonctionnels
- [ ] Monitoring actif
- [ ] Alertes configurées
- [ ] Documentation mise à jour
- [ ] Équipe informée

---

## Contacts

- **DevOps:** devops@iafactory.dz
- **Urgences:** +213 xxx xxx xxx
- **Documentation:** docs.iafactory.dz

---

*Guide de déploiement IAFactory - Décembre 2024*
