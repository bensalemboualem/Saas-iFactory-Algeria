#!/bin/bash
# ==============================================
# DÉPLOIEMENT VPS MASTER - IAFactory RAG-DZ
# ==============================================
# Déploiement automatique complet sur Hetzner VPS
# Compatible: CX22 (40 GB), CX32 (80 GB), CX42 (160 GB)
# ==============================================

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="iafactory-rag-dz"
DEPLOY_DIR="/opt/${PROJECT_NAME}"
DOMAIN="${DOMAIN:-iafactory-algeria.com}"
EMAIL="${EMAIL:-admin@iafactory-algeria.com}"

echo "================================================================================"
echo "🚀 DÉPLOIEMENT VPS MASTER - IAFactory RAG-DZ"
echo "================================================================================"
echo "📍 Serveur: $(hostname)"
echo "📍 Domaine: ${DOMAIN}"
echo "📍 Région: Algérie (DZ)"
echo "================================================================================"
echo ""

# ==============================================
# ÉTAPE 1: Vérifications préalables
# ==============================================
echo -e "${BLUE}[1/8]${NC} Vérifications préalables..."

# Vérifier si root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}❌ Ce script doit être exécuté en tant que root${NC}"
   exit 1
fi

# Vérifier l'espace disque
AVAILABLE_SPACE=$(df / | tail -1 | awk '{print $4}')
REQUIRED_SPACE=$((15 * 1024 * 1024))  # 15 GB minimum

if [ $AVAILABLE_SPACE -lt $REQUIRED_SPACE ]; then
    echo -e "${RED}❌ Espace disque insuffisant${NC}"
    echo "Disponible: $(($AVAILABLE_SPACE / 1024 / 1024)) GB"
    echo "Requis: 15 GB minimum"
    exit 1
fi

echo -e "${GREEN}✅ Espace disque suffisant: $(($AVAILABLE_SPACE / 1024 / 1024)) GB disponibles${NC}"

# ==============================================
# ÉTAPE 2: Installation des dépendances
# ==============================================
echo ""
echo -e "${BLUE}[2/8]${NC} Installation des dépendances..."

# Update system
apt-get update -qq

# Install required packages
apt-get install -y -qq \
    curl \
    git \
    docker.io \
    docker-compose \
    nginx \
    certbot \
    python3-certbot-nginx \
    ufw \
    htop \
    net-tools

# Enable and start Docker
systemctl enable docker
systemctl start docker

echo -e "${GREEN}✅ Dépendances installées${NC}"

# ==============================================
# ÉTAPE 3: Configuration du firewall
# ==============================================
echo ""
echo -e "${BLUE}[3/8]${NC} Configuration du firewall..."

# Configure UFW
ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp

echo -e "${GREEN}✅ Firewall configuré${NC}"

# ==============================================
# ÉTAPE 4: Clonage/Mise à jour du code
# ==============================================
echo ""
echo -e "${BLUE}[4/8]${NC} Préparation du code..."

# Create deploy directory
mkdir -p ${DEPLOY_DIR}
cd ${DEPLOY_DIR}

# If git repo exists, pull, otherwise copy files
if [ -d ".git" ]; then
    echo "📥 Mise à jour du repository..."
    git pull origin main
else
    echo "📥 Initialisation du projet..."
    # Si on exécute depuis le repo local, copier les fichiers
    if [ -f "$(dirname $0)/docker-compose.yml" ]; then
        cp -r $(dirname $0)/* ${DEPLOY_DIR}/
    else
        echo -e "${YELLOW}⚠️  Veuillez copier les fichiers du projet dans ${DEPLOY_DIR}${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Code préparé${NC}"

# ==============================================
# ÉTAPE 5: Configuration de l'environnement
# ==============================================
echo ""
echo -e "${BLUE}[5/8]${NC} Configuration de l'environnement..."

# Create .env if not exists
if [ ! -f ".env" ]; then
    cat > .env <<EOF
# IAFactory RAG-DZ - Production Environment
# Generated: $(date)

# Region
SOVEREIGNTY_REGION=DZ
SOVEREIGNTY_LABEL=Algérie
TZ=Africa/Algiers

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=$(openssl rand -base64 32)
POSTGRES_DB=iafactory_dz
DATABASE_URL=postgresql://postgres:$(openssl rand -base64 32)@iafactory-postgres:5432/iafactory_dz

# Redis
REDIS_URL=redis://iafactory-redis:6379/0
REDIS_PASSWORD=

# Qdrant
QDRANT_URL=http://iafactory-qdrant:6333
QDRANT_API_KEY=

# API Keys (À CONFIGURER)
# Groq
GROQ_API_KEY=

# OpenAI
OPENAI_API_KEY=

# Anthropic
ANTHROPIC_API_KEY=

# Google
GOOGLE_API_KEY=

# DeepSeek
DEEPSEEK_API_KEY=

# Security
SECRET_KEY=$(openssl rand -base64 64)
JWT_SECRET=$(openssl rand -base64 64)

# Server
PORT=8180
HOST=0.0.0.0
ENVIRONMENT=production
DEBUG=false

# Domain
DOMAIN=${DOMAIN}
EOF

    echo -e "${GREEN}✅ Fichier .env créé${NC}"
    echo -e "${YELLOW}⚠️  IMPORTANT: Configurez vos clés API dans ${DEPLOY_DIR}/.env${NC}"
else
    echo -e "${GREEN}✅ Fichier .env existant${NC}"
fi

# ==============================================
# ÉTAPE 6: Configuration Nginx
# ==============================================
echo ""
echo -e "${BLUE}[6/8]${NC} Configuration Nginx..."

# Create Nginx config
cat > /etc/nginx/sites-available/${PROJECT_NAME} <<'NGINXEOF'
# IAFactory RAG-DZ - Nginx Configuration
# Generated automatically

upstream backend_api {
    least_conn;
    server localhost:8180 max_fails=3 fail_timeout=30s;
}

# HTTP → HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name DOMAIN_PLACEHOLDER;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name DOMAIN_PLACEHOLDER;

    # SSL (will be configured by certbot)
    ssl_certificate /etc/letsencrypt/live/DOMAIN_PLACEHOLDER/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/DOMAIN_PLACEHOLDER/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json application/javascript;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;

    # Landing page (root)
    location / {
        alias /opt/iafactory-rag-dz/apps/landing/;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Applications
    location /apps/ {
        alias /opt/iafactory-rag-dz/apps/;
        index index.html;
        try_files $uri $uri/ $uri/index.html =404;
    }

    # Directory IA
    location /docs/ {
        alias /opt/iafactory-rag-dz/docs/;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend_api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check
    location /health {
        proxy_pass http://backend_api/health;
        access_log off;
    }

    # Static files caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
NGINXEOF

# Replace domain placeholder
sed -i "s/DOMAIN_PLACEHOLDER/${DOMAIN}/g" /etc/nginx/sites-available/${PROJECT_NAME}

# Enable site
ln -sf /etc/nginx/sites-available/${PROJECT_NAME} /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test nginx config
nginx -t

echo -e "${GREEN}✅ Nginx configuré${NC}"

# ==============================================
# ÉTAPE 7: Démarrage Docker Compose
# ==============================================
echo ""
echo -e "${BLUE}[7/8]${NC} Démarrage des services Docker..."

# Pull images
docker-compose pull

# Build custom images
docker-compose build --no-cache

# Start services
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Attente du démarrage des services..."
sleep 10

# Check services status
docker-compose ps

echo -e "${GREEN}✅ Services Docker démarrés${NC}"

# ==============================================
# ÉTAPE 8: Configuration SSL avec Let's Encrypt
# ==============================================
echo ""
echo -e "${BLUE}[8/8]${NC} Configuration SSL (Let's Encrypt)..."

# Reload Nginx first
systemctl reload nginx

# Request SSL certificate
certbot --nginx \
    --non-interactive \
    --agree-tos \
    --email ${EMAIL} \
    --domains ${DOMAIN} \
    --redirect

# Setup auto-renewal
systemctl enable certbot.timer
systemctl start certbot.timer

echo -e "${GREEN}✅ SSL configuré${NC}"

# ==============================================
# RÉSUMÉ FINAL
# ==============================================
echo ""
echo "================================================================================"
echo -e "${GREEN}✅ DÉPLOIEMENT TERMINÉ AVEC SUCCÈS !${NC}"
echo "================================================================================"
echo ""
echo "📊 SERVICES DÉPLOYÉS:"
echo "  • 47 Applications web"
echo "  • Backend FastAPI (RAG Souverain)"
echo "  • PostgreSQL + PGVector"
echo "  • Redis Cache"
echo "  • Qdrant Vector Database"
echo "  • Nginx + SSL/HTTPS"
echo ""
echo "🌐 URLS:"
echo "  • Landing page: https://${DOMAIN}"
echo "  • Applications: https://${DOMAIN}/apps/"
echo "  • Directory IA: https://${DOMAIN}/docs/directory/"
echo "  • API Backend: https://${DOMAIN}/api/"
echo "  • Health check: https://${DOMAIN}/health"
echo ""
echo "📁 FICHIERS IMPORTANTS:"
echo "  • Config: ${DEPLOY_DIR}/.env"
echo "  • Logs: docker-compose logs -f"
echo "  • Nginx: /etc/nginx/sites-available/${PROJECT_NAME}"
echo ""
echo "⚙️  COMMANDES UTILES:"
echo "  • Logs backend: docker-compose logs -f iafactory-backend"
echo "  • Redémarrer: docker-compose restart"
echo "  • Arrêter: docker-compose down"
echo "  • Status: docker-compose ps"
echo ""
echo "⚠️  IMPORTANT:"
echo "  1. Configurez vos clés API dans: ${DEPLOY_DIR}/.env"
echo "  2. Redémarrez après config: cd ${DEPLOY_DIR} && docker-compose restart"
echo ""
echo "================================================================================"
echo -e "${GREEN}🎉 IAFactory RAG-DZ est maintenant en ligne !${NC}"
echo "================================================================================"
