#!/bin/bash
# ==============================================
# DEPLOIEMENT SERVICES EXTRAS
# ==============================================
# Flowise + Firecrawl + Voice Bridge
# ==============================================

set -e

echo "=========================================="
echo "  DEPLOIEMENT SERVICES EXTRAS"
echo "  Flowise + Firecrawl + Voice Bridge"
echo "=========================================="

# Variables
DEPLOY_DIR="/root/rag-dz"
cd $DEPLOY_DIR

# 1. Creer le reseau Docker s'il n'existe pas
echo ""
echo "[1/6] Verification reseau Docker..."
docker network create rag-dz_iafactory-net 2>/dev/null || echo "Reseau deja existant"

# 2. Creer le volume Flowise
echo ""
echo "[2/6] Creation volumes..."
docker volume create iaf-flowise-data 2>/dev/null || echo "Volume flowise deja existant"

# 3. Creer la base de donnees Flowise dans PostgreSQL
echo ""
echo "[3/6] Creation base Flowise dans PostgreSQL..."
docker exec iaf-dz-postgres psql -U postgres -c "CREATE DATABASE flowise;" 2>/dev/null || echo "Base flowise deja existante"

# 4. Deployer les services extras
echo ""
echo "[4/6] Deploiement des services..."
docker-compose -f docker-compose.extras.yml up -d --build

# 5. Configurer Nginx
echo ""
echo "[5/6] Configuration Nginx..."

# Flowise
cat > /etc/nginx/sites-available/flowise.iafactoryalgeria.com << 'EOF'
server {
    listen 80;
    server_name flowise.iafactoryalgeria.com;

    location / {
        proxy_pass http://127.0.0.1:8220;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        proxy_read_timeout 300;
        client_max_body_size 50M;
    }
}
EOF

# Voice Bridge
cat > /etc/nginx/sites-available/voice-bridge.iafactoryalgeria.com << 'EOF'
server {
    listen 80;
    server_name voice-bridge.iafactoryalgeria.com;

    location / {
        proxy_pass http://127.0.0.1:8223;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF

# Activer les sites
ln -sf /etc/nginx/sites-available/flowise.iafactoryalgeria.com /etc/nginx/sites-enabled/
ln -sf /etc/nginx/sites-available/voice-bridge.iafactoryalgeria.com /etc/nginx/sites-enabled/

# Tester et recharger Nginx
nginx -t && systemctl reload nginx

# 6. Certificats SSL
echo ""
echo "[6/6] Generation certificats SSL..."
certbot --nginx -d flowise.iafactoryalgeria.com --non-interactive --agree-tos || echo "SSL flowise en attente DNS"

echo ""
echo "=========================================="
echo "  DEPLOIEMENT TERMINE"
echo "=========================================="
echo ""
echo "SERVICES DISPONIBLES:"
echo "  - Flowise:      http://localhost:8220"
echo "  - Firecrawl:    http://localhost:8221"
echo "  - Playwright:   http://localhost:8222"
echo "  - Voice Bridge: http://localhost:8223"
echo ""
echo "URLS PUBLIQUES (apres DNS):"
echo "  - https://flowise.iafactoryalgeria.com"
echo "  - https://voice-bridge.iafactoryalgeria.com"
echo ""
echo "CREDENTIALS FLOWISE:"
echo "  - Username: admin"
echo "  - Password: IAFactory2025!"
echo ""
