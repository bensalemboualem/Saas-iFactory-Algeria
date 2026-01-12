# Guide de Déploiement - IAFactory Video Platform

**Version:** 1.0.0
**Dernière mise à jour:** Décembre 2024

---

## Prérequis

### Système

| Composant | Minimum | Recommandé |
|-----------|---------|------------|
| OS | Ubuntu 20.04+ / Debian 11+ | Ubuntu 22.04 LTS |
| CPU | 4 cores | 8+ cores |
| RAM | 8 GB | 16+ GB |
| Stockage | 100 GB SSD | 500+ GB NVMe |
| Réseau | 100 Mbps | 1 Gbps |

### Logiciels

- **Docker** >= 24.0
- **Docker Compose** >= 2.20
- **Git**
- **Make** (optionnel, pour les commandes simplifiées)

### Services Externes Requis

| Service | Obligatoire | Description |
|---------|-------------|-------------|
| OpenAI API | Oui | LLM & DALL-E |
| ElevenLabs | Recommandé | Voix de haute qualité |
| Supabase | Oui (prod) | Base de données managée |
| AWS S3 / MinIO | Oui | Stockage des assets |
| Runway / Pika | Optionnel | Génération vidéo |

---

## Installation

### 1. Cloner le Repository

```bash
git clone https://github.com/iafactory/iafactory-video-platform.git
cd iafactory-video-platform
```

### 2. Configuration de l'Environnement

```bash
# Copier le fichier d'exemple
cp backend/.env.example backend/.env

# Éditer les variables
nano backend/.env
```

### 3. Variables d'Environnement

```bash
# ============================================
# APPLICATION
# ============================================
APP_NAME=iafactory-video
APP_ENV=production  # development | staging | production
DEBUG=false
SECRET_KEY=your-super-secret-key-min-32-chars

# ============================================
# DATABASE
# ============================================
DATABASE_URL=postgresql://user:password@localhost:5432/video_platform
# Ou Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your-supabase-key
SUPABASE_SERVICE_KEY=your-service-key

# ============================================
# REDIS
# ============================================
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# ============================================
# STORAGE
# ============================================
STORAGE_TYPE=s3  # local | s3 | minio
S3_BUCKET=iafactory-video-assets
S3_REGION=eu-west-3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key

# Pour MinIO (développement)
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# ============================================
# AI PROVIDERS - LLM
# ============================================
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
GROQ_API_KEY=gsk_xxx

# ============================================
# AI PROVIDERS - IMAGES
# ============================================
FLUX_API_KEY=your-flux-key
LEONARDO_API_KEY=your-leonardo-key
STABILITY_API_KEY=your-stability-key

# ============================================
# AI PROVIDERS - VIDEO
# ============================================
RUNWAY_API_KEY=your-runway-key
PIKA_API_KEY=your-pika-key
LUMA_API_KEY=your-luma-key

# ============================================
# AI PROVIDERS - VOICE
# ============================================
ELEVENLABS_API_KEY=your-elevenlabs-key

# ============================================
# AI PROVIDERS - AVATAR
# ============================================
HEYGEN_API_KEY=your-heygen-key
DID_API_KEY=your-did-key

# ============================================
# AI PROVIDERS - MUSIC
# ============================================
SUNO_API_KEY=your-suno-key

# ============================================
# PLATFORM OAUTH (Publication)
# ============================================
YOUTUBE_CLIENT_ID=your-client-id
YOUTUBE_CLIENT_SECRET=your-client-secret
TIKTOK_CLIENT_KEY=your-client-key
TIKTOK_CLIENT_SECRET=your-client-secret
INSTAGRAM_APP_ID=your-app-id
INSTAGRAM_APP_SECRET=your-app-secret
LINKEDIN_CLIENT_ID=your-client-id
LINKEDIN_CLIENT_SECRET=your-client-secret

# ============================================
# MONITORING
# ============================================
SENTRY_DSN=https://xxx@sentry.io/xxx
LOG_LEVEL=INFO
```

---

## Déploiement avec Docker

### Mode Développement

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

### Mode Production

```bash
# Utiliser le fichier de production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8001:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.tasks worker -l info -c 4
    environment:
      - CELERY_BROKER_URL=${CELERY_BROKER_URL}
    depends_on:
      - redis
      - api
    volumes:
      - ./backend:/app

  beat:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.tasks beat -l info
    depends_on:
      - redis
      - worker

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://api:8000
    depends_on:
      - api

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-postgres}
      POSTGRES_DB: ${DB_NAME:-video_platform}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5433:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6380:6379"
    volumes:
      - redis_data:/data

  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data

volumes:
  postgres_data:
  redis_data:
  minio_data:
```

### docker-compose.prod.yml

```yaml
version: '3.8'

services:
  api:
    restart: always
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '2'
          memory: 4G
    environment:
      - DEBUG=false
      - LOG_LEVEL=WARNING

  worker:
    restart: always
    deploy:
      replicas: 4
      resources:
        limits:
          cpus: '4'
          memory: 8G

  frontend:
    restart: always
    environment:
      - NODE_ENV=production

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - api
      - frontend
```

---

## Déploiement Manuel (Sans Docker)

### Backend

```bash
cd backend

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Migrations
alembic upgrade head

# Démarrer l'API
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Démarrer les workers Celery (dans un autre terminal)
celery -A app.tasks worker -l info -c 4

# Démarrer le scheduler (dans un autre terminal)
celery -A app.tasks beat -l info
```

### Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Build
npm run build

# Démarrer
npm start
```

---

## Configuration Nginx

```nginx
# /etc/nginx/sites-available/video.iafactory.dz

upstream api_backend {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

upstream frontend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name video.iafactory.dz;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name video.iafactory.dz;

    # SSL
    ssl_certificate /etc/letsencrypt/live/video.iafactory.dz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/video.iafactory.dz/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;

    # Logs
    access_log /var/log/nginx/video.access.log;
    error_log /var/log/nginx/video.error.log;

    # API
    location /api/ {
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Timeouts for long-running operations
        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Static files
    location /static/ {
        alias /var/www/video.iafactory.dz/static/;
        expires 30d;
    }

    # Upload limit
    client_max_body_size 500M;
}
```

---

## SSL avec Let's Encrypt

```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx

# Obtenir le certificat
sudo certbot --nginx -d video.iafactory.dz

# Renouvellement automatique
sudo certbot renew --dry-run
```

---

## Migrations de Base de Données

```bash
# Créer une nouvelle migration
alembic revision --autogenerate -m "Description de la migration"

# Appliquer les migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Monitoring

### Logs

```bash
# Logs Docker
docker-compose logs -f api

# Logs système
tail -f /var/log/nginx/video.error.log

# Logs applicatifs
tail -f /var/log/video-platform/app.log
```

### Métriques

L'API expose des métriques Prometheus sur `/metrics`:

```bash
# Ajouter à prometheus.yml
scrape_configs:
  - job_name: 'video-platform'
    static_configs:
      - targets: ['localhost:8001']
```

### Health Checks

```bash
# API Health
curl http://localhost:8001/health

# Réponse attendue
{
    "status": "healthy",
    "database": "connected",
    "redis": "connected",
    "storage": "connected"
}
```

---

## Sauvegarde

### Base de Données

```bash
# Backup PostgreSQL
pg_dump -U postgres video_platform > backup_$(date +%Y%m%d).sql

# Restore
psql -U postgres video_platform < backup_20241201.sql
```

### Assets (S3/MinIO)

```bash
# Sync avec AWS CLI
aws s3 sync s3://iafactory-video-assets ./backup/assets/

# Ou avec MinIO Client
mc mirror myminio/video-assets ./backup/assets/
```

### Script de Backup Complet

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/video-platform/$DATE"

mkdir -p $BACKUP_DIR

# Database
pg_dump -U postgres video_platform | gzip > $BACKUP_DIR/database.sql.gz

# Redis
redis-cli BGSAVE
cp /var/lib/redis/dump.rdb $BACKUP_DIR/redis.rdb

# Config files
cp -r /app/backend/.env $BACKUP_DIR/

# Upload to S3
aws s3 sync $BACKUP_DIR s3://iafactory-backups/video-platform/$DATE/

# Cleanup old backups (keep 30 days)
find /backup/video-platform -type d -mtime +30 -exec rm -rf {} \;

echo "Backup completed: $BACKUP_DIR"
```

### Cron pour Backups Automatiques

```bash
# Éditer crontab
crontab -e

# Ajouter (tous les jours à 2h du matin)
0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
```

---

## Mise à Jour

### Procédure Standard

```bash
# 1. Backup
./scripts/backup.sh

# 2. Pull des changements
git pull origin main

# 3. Rebuild des images
docker-compose build

# 4. Migrations
docker-compose run --rm api alembic upgrade head

# 5. Redémarrage sans downtime
docker-compose up -d --no-deps api
docker-compose up -d --no-deps worker

# 6. Vérification
docker-compose ps
curl http://localhost:8001/health
```

### Rollback

```bash
# Revenir à la version précédente
git checkout <previous-tag>

# Rollback migration
docker-compose run --rm api alembic downgrade -1

# Rebuild et redémarrer
docker-compose build
docker-compose up -d
```

---

## Troubleshooting

### Problèmes Courants

| Problème | Solution |
|----------|----------|
| Container ne démarre pas | `docker-compose logs <service>` |
| Erreur de connexion DB | Vérifier DATABASE_URL et que postgres est up |
| Workers bloqués | `docker-compose restart worker` |
| Out of memory | Augmenter RAM ou réduire workers |
| Timeout API | Augmenter `proxy_read_timeout` dans nginx |

### Commandes Utiles

```bash
# État des containers
docker-compose ps

# Ressources utilisées
docker stats

# Entrer dans un container
docker-compose exec api bash

# Vider le cache Redis
docker-compose exec redis redis-cli FLUSHALL

# Purger les tâches Celery
docker-compose exec worker celery -A app.tasks purge

# Vérifier les migrations
docker-compose exec api alembic current
```

---

## Checklist de Déploiement

### Avant le Déploiement

- [ ] Variables d'environnement configurées
- [ ] Clés API valides et testées
- [ ] Base de données accessible
- [ ] Redis accessible
- [ ] Stockage S3/MinIO configuré
- [ ] SSL certificats en place
- [ ] Backups configurés

### Après le Déploiement

- [ ] Health checks passent
- [ ] API accessible via HTTPS
- [ ] Frontend charge correctement
- [ ] Workers fonctionnent
- [ ] Logs sans erreurs critiques
- [ ] Monitoring actif
- [ ] Premier test de génération réussi

---

## Contacts

- **Support technique:** devops@iafactory.dz
- **Urgences:** +213 xxx xxx xxx
