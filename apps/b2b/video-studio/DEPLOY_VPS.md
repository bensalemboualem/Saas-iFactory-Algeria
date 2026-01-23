# 🚀 DÉPLOIEMENT VIDEO STUDIO SUR VPS HETZNER

## ✅ STATUT BACKEND

✅ **Backend FastAPI fonctionnel** - main.py complet avec:
- Routes video, audio, scripts, publish, tokens
- Middleware CORS configuré
- Health check endpoint
- Gestion des erreurs globale
- Documentation auto (/docs, /redoc)

✅ **Requirements.txt complet** - 61 dépendances dont:
- FastAPI 0.109.0
- SQLAlchemy 2.0.25 + AsyncPG
- Redis 5.0.1
- Anthropic (Claude)
- ElevenLabs 1.0.0
- fal-client 0.3.0
- FFmpeg-python

✅ **Docker-compose.yml prêt** - 4 services:
- Frontend (Next.js port 3000)
- Backend (FastAPI port 8000)
- PostgreSQL 16
- Redis 7

---

## 🎯 PLAN DE DÉPLOIEMENT (2-3 jours)

### JOUR 1: Configuration VPS (4h)

#### Étape 1: Connexion SSH et préparation
```bash
# Se connecter au VPS Hetzner
ssh root@VOTRE_IP_VPS

# Mettre à jour le système
apt update && apt upgrade -y

# Installer les outils de base
apt install -y git curl wget vim htop build-essential
```

#### Étape 2: Installer Docker & Docker Compose
```bash
# Installer Docker
curl -fsSL https://get.docker.com | sh

# Installer Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Vérifier
docker --version
docker-compose --version

# Démarrer Docker au boot
systemctl enable docker
systemctl start docker
```

#### Étape 3: Installer FFmpeg (pour le traitement vidéo)
```bash
apt install -y ffmpeg

# Vérifier
ffmpeg -version
```

#### Étape 4: Créer les dossiers
```bash
mkdir -p /opt/iafactory
cd /opt/iafactory
```

---

### JOUR 2: Déploiement Application (6h)

#### Étape 1: Cloner le repository
```bash
cd /opt/iafactory

# Option A: Depuis GitHub
git clone https://github.com/VOTRE_ORG/rag-dz.git
cd rag-dz/apps/video-studio

# Option B: Upload manuel avec scp (depuis votre machine locale)
# scp -r D:\IAFactory\rag-dz\apps\video-studio root@VOTRE_IP:/opt/iafactory/
```

#### Étape 2: Configurer les variables d'environnement
```bash
cd /opt/iafactory/rag-dz/apps/video-studio

# Copier le fichier exemple
cp .env.example .env

# Éditer le fichier
nano .env
```

**Remplir le .env avec vos vraies valeurs:**
```bash
# APIs IA (À OBTENIR)
FAL_KEY=fal_xxxxxxxxxxxxxxxxxx
REPLICATE_API_TOKEN=r8_xxxxxxxxxxxxxxxx
ELEVENLABS_API_KEY=sk_xxxxxxxxxxxxxxxx

# Database (laisser par défaut pour Docker)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/iafactory_video

# Redis (laisser par défaut pour Docker)
REDIS_URL=redis://redis:6379

# Auth (GÉNÉRER UN SECRET FORT)
JWT_SECRET=$(openssl rand -base64 32)
NEXTAUTH_SECRET=$(openssl rand -base64 32)

# Storage Cloudflare R2 (À CONFIGURER)
S3_BUCKET=iafactory-videos
S3_ACCESS_KEY=xxxxx
S3_SECRET_KEY=xxxxx
S3_ENDPOINT=https://xxxxx.r2.cloudflarestorage.com
S3_REGION=auto

# Stripe (À OBTENIR)
STRIPE_PUBLISHABLE_KEY=pk_live_xxxxx
STRIPE_SECRET_KEY=sk_live_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx

# Frontend URL
FRONTEND_URL=https://video-studio.iafactory.ch
NEXT_PUBLIC_API_URL=https://api.iafactory.ch
```

#### Étape 3: Build et lancer les containers
```bash
cd /opt/iafactory/rag-dz/apps/video-studio

# Build les images Docker
docker-compose build

# Lancer en arrière-plan
docker-compose up -d

# Vérifier que tout tourne
docker-compose ps

# Voir les logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Vous devriez voir:**
```
backend-1    | 🚀 Starting IAFactory Video Studio Pro v1.0.0
backend-1    | 📍 Environment: production
backend-1    | INFO:     Started server process [1]
backend-1    | INFO:     Uvicorn running on http://0.0.0.0:8000

frontend-1   | ready - started server on 0.0.0.0:3000
```

#### Étape 4: Vérifier que l'API fonctionne
```bash
# Test health check
curl http://localhost:8000/health

# Devrait retourner:
# {"status":"healthy","app":"IAFactory Video Studio Pro","version":"1.0.0","environment":"production"}

# Test documentation
curl http://localhost:8000/docs
```

---

### JOUR 3: Configuration Nginx + SSL (2h)

#### Étape 1: Installer Nginx
```bash
apt install -y nginx
```

#### Étape 2: Configurer Nginx comme reverse proxy
```bash
# Créer la config
nano /etc/nginx/sites-available/video-studio
```

**Contenu du fichier:**
```nginx
# Frontend Next.js
server {
    listen 80;
    server_name video-studio.iafactory.ch;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}

# Backend API
server {
    listen 80;
    server_name api.iafactory.ch;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Activer le site
ln -s /etc/nginx/sites-available/video-studio /etc/nginx/sites-enabled/

# Tester la config
nginx -t

# Recharger Nginx
systemctl reload nginx
```

#### Étape 3: Configurer le DNS
**Sur Cloudflare (ou votre registrar):**
```
Type A: video-studio.iafactory.ch -> VOTRE_IP_VPS
Type A: api.iafactory.ch -> VOTRE_IP_VPS
```

#### Étape 4: Installer SSL avec Let's Encrypt
```bash
# Installer Certbot
apt install -y certbot python3-certbot-nginx

# Obtenir les certificats SSL (APRÈS avoir configuré le DNS)
certbot --nginx -d video-studio.iafactory.ch -d api.iafactory.ch

# Suivre les instructions interactives
# Choisir: Redirect HTTP to HTTPS (option 2)

# Vérifier l'auto-renewal
certbot renew --dry-run
```

**Nginx va être automatiquement mis à jour pour HTTPS!**

---

## 🔑 ÉTAPES CRITIQUES AVANT DE DÉPLOYER

### 1. Obtenir les Clés API (1-2h)

#### Fal.ai (Génération Vidéo)
```bash
# 1. Créer compte: https://fal.ai/dashboard
# 2. Aller dans Settings > API Keys
# 3. Créer une nouvelle clé
# 4. Budget recommandé: $50 pour commencer
# Copier: FAL_KEY=fal_xxxxxx
```

#### Replicate (Génération Image/Vidéo)
```bash
# 1. Créer compte: https://replicate.com/account
# 2. Aller dans Account > API Tokens
# 3. Créer un token
# 4. Budget recommandé: $50
# Copier: REPLICATE_API_TOKEN=r8_xxxxxx
```

#### ElevenLabs (Voix Darija)
```bash
# 1. Créer compte: https://elevenlabs.io
# 2. Souscrire au plan Creator ($22/mois)
# 3. Aller dans Profile > API Key
# 4. Copier la clé
# Copier: ELEVENLABS_API_KEY=sk_xxxxxx
```

#### Stripe (Paiements)
```bash
# 1. Créer compte: https://dashboard.stripe.com
# 2. Activer le mode production
# 3. Aller dans Developers > API Keys
# 4. Copier les clés publishable et secret
# 5. Créer un webhook endpoint: https://api.iafactory.ch/webhooks/stripe
# Copier: STRIPE_PUBLISHABLE_KEY=pk_live_xxxxx
#         STRIPE_SECRET_KEY=sk_live_xxxxx
#         STRIPE_WEBHOOK_SECRET=whsec_xxxxx
```

#### Cloudflare R2 (Stockage Vidéos)
```bash
# 1. Créer compte Cloudflare
# 2. Aller dans R2 Object Storage
# 3. Créer un bucket: iafactory-videos
# 4. Générer des access keys
# 5. Configurer CORS:
#    AllowedOrigins: ["https://video-studio.iafactory.ch"]
#    AllowedMethods: ["GET", "PUT", "POST", "DELETE"]
# Copier: S3_ACCESS_KEY=xxxxx
#         S3_SECRET_KEY=xxxxx
#         S3_ENDPOINT=https://xxxxx.r2.cloudflarestorage.com
```

---

### 2. Créer la Base de Données (30min)

```bash
# Se connecter au container PostgreSQL
docker exec -it video-studio-db-1 psql -U postgres

# Dans psql, créer les tables (à adapter selon vos modèles)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    credits INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'draft',
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE videos (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    url TEXT,
    duration INTEGER,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    amount INTEGER NOT NULL,
    type VARCHAR(50),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

# Quitter psql
\q
```

**OU utiliser Alembic (recommandé):**
```bash
# Dans le container backend
docker exec -it video-studio-backend-1 bash

# Créer la première migration
alembic revision --autogenerate -m "Initial schema"

# Appliquer les migrations
alembic upgrade head

# Sortir du container
exit
```

---

## 🧪 TESTS POST-DÉPLOIEMENT

### Test 1: API Health Check
```bash
curl https://api.iafactory.ch/health
# Doit retourner: {"status":"healthy",...}
```

### Test 2: Documentation API
```bash
# Ouvrir dans le navigateur:
https://api.iafactory.ch/docs
# Doit afficher Swagger UI
```

### Test 3: Frontend
```bash
# Ouvrir dans le navigateur:
https://video-studio.iafactory.ch
# Doit afficher la page d'accueil Next.js
```

### Test 4: Base de données
```bash
docker exec -it video-studio-db-1 psql -U postgres -d iafactory_video -c "SELECT COUNT(*) FROM users;"
# Doit retourner: count: 0 (ou plus si des users existent)
```

### Test 5: Redis
```bash
docker exec -it video-studio-redis-1 redis-cli PING
# Doit retourner: PONG
```

---

## 🔧 COMMANDES UTILES

### Gestion des containers
```bash
# Voir les logs en temps réel
docker-compose logs -f

# Redémarrer un service
docker-compose restart backend

# Arrêter tout
docker-compose down

# Supprimer tout (ATTENTION: efface la DB)
docker-compose down -v

# Reconstruire après modification
docker-compose up -d --build
```

### Accéder aux containers
```bash
# Backend Python
docker exec -it video-studio-backend-1 bash

# Frontend Node
docker exec -it video-studio-frontend-1 sh

# PostgreSQL
docker exec -it video-studio-db-1 psql -U postgres

# Redis
docker exec -it video-studio-redis-1 redis-cli
```

### Monitoring
```bash
# Utilisation ressources
docker stats

# Espace disque
df -h

# Logs Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

## 🚨 TROUBLESHOOTING

### Problème: "Connection refused" sur le frontend
```bash
# Vérifier que le backend tourne
docker-compose ps

# Voir les logs du backend
docker-compose logs backend

# Redémarrer le backend
docker-compose restart backend
```

### Problème: "Database connection failed"
```bash
# Vérifier que PostgreSQL tourne
docker exec -it video-studio-db-1 pg_isready

# Voir les logs
docker-compose logs db

# Se connecter manuellement
docker exec -it video-studio-db-1 psql -U postgres
```

### Problème: "Out of memory"
```bash
# Vérifier la mémoire
free -h

# Augmenter la swap
dd if=/dev/zero of=/swapfile bs=1G count=4
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### Problème: Certificat SSL expiré
```bash
# Renouveler manuellement
certbot renew

# Recharger Nginx
systemctl reload nginx
```

---

## 📊 MONITORING PRODUCTION

### Installer Prometheus + Grafana (Optionnel)
```bash
# Ajouter dans docker-compose.yml
prometheus:
  image: prom/prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml

grafana:
  image: grafana/grafana
  ports:
    - "3001:3000"
  depends_on:
    - prometheus
```

### Logs centralisés avec Loki (Optionnel)
```bash
docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions
```

---

## 💰 COÛTS MENSUELS ESTIMÉS

| Service | Coût |
|---------|------|
| VPS Hetzner (déjà payé) | 15-40€ |
| ElevenLabs (Creator) | 22€ |
| Fal.ai (100 vidéos) | ~50€ |
| Replicate (100 vidéos) | ~50€ |
| Cloudflare R2 (50GB) | 0€ (gratuit jusqu'à 10GB) |
| **TOTAL** | **~137-162€/mois** |

---

## ✅ CHECKLIST FINALE

Avant de dire "C'est en prod":

- [ ] VPS accessible via SSH
- [ ] Docker + Docker Compose installés
- [ ] FFmpeg installé
- [ ] Repository cloné dans /opt/iafactory
- [ ] .env configuré avec toutes les clés API
- [ ] `docker-compose up -d` lancé avec succès
- [ ] Base de données créée et migrée
- [ ] Nginx installé et configuré
- [ ] DNS configuré (A records)
- [ ] SSL installé (Let's Encrypt)
- [ ] Tests API fonctionnent (curl health check)
- [ ] Frontend accessible via HTTPS
- [ ] Logs vérifiés (pas d'erreurs critiques)
- [ ] Backup automatique configuré

---

## 📞 SUPPORT

**En cas de problème:**
1. Voir les logs: `docker-compose logs -f`
2. Vérifier la checklist ci-dessus
3. Tester les endpoints un par un
4. Me contacter avec les logs d'erreur
