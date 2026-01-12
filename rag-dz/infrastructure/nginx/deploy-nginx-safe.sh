#!/bin/bash
# Script de déploiement Nginx SÉCURISÉ avec rollback automatique
# Date: 2025-12-12
# Usage: ./deploy-nginx-safe.sh

set -e  # Arrête sur erreur

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Déploiement Nginx V2 (Astro Marketing) ===${NC}"

# ============================================
# ÉTAPE 1 : Vérifications pré-deploy
# ============================================
echo -e "\n${YELLOW}[1/6] Vérifications pré-deploy...${NC}"

# Vérifier que le fichier de config existe
if [ ! -f "/etc/nginx/sites-available/iafactoryalgeria" ]; then
    echo -e "${RED}Erreur: /etc/nginx/sites-available/iafactoryalgeria introuvable${NC}"
    exit 1
fi

# Vérifier que le nouveau dossier marketing existe
if [ ! -d "/opt/rag-dz-v2/marketing-dist" ]; then
    echo -e "${RED}Erreur: /opt/rag-dz-v2/marketing-dist introuvable${NC}"
    echo -e "${YELLOW}Exécutez d'abord: mkdir -p /opt/rag-dz-v2/marketing-dist${NC}"
    exit 1
fi

# Vérifier que le dossier contient index.html
if [ ! -f "/opt/rag-dz-v2/marketing-dist/index.html" ]; then
    echo -e "${RED}Erreur: /opt/rag-dz-v2/marketing-dist/index.html introuvable${NC}"
    echo -e "${YELLOW}Exécutez d'abord le rsync du build Astro${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Vérifications OK${NC}"

# ============================================
# ÉTAPE 2 : Backup config actuelle
# ============================================
BACKUP_FILE="/etc/nginx/sites-available/iafactoryalgeria.backup-$(date +%Y%m%d-%H%M%S)"
echo -e "\n${YELLOW}[2/6] Backup config actuelle...${NC}"
cp /etc/nginx/sites-available/iafactoryalgeria "$BACKUP_FILE"
echo -e "${GREEN}✓ Backup créé: $BACKUP_FILE${NC}"

# ============================================
# ÉTAPE 3 : Modifier config Nginx
# ============================================
echo -e "\n${YELLOW}[3/6] Modification config Nginx...${NC}"

# Créer fichier temporaire avec nouvelle config
cat > /tmp/nginx-iafactoryalgeria-new.conf << 'NGINX_CONF'
# Map for WebSocket upgrade
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

# HTTP → HTTPS redirect
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name www.iafactoryalgeria.com iafactoryalgeria.com _;

    location ^~ /ollama/ {
        proxy_pass http://127.0.0.1:11434/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    location / {
        return 301 https://www.iafactoryalgeria.com$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name www.iafactoryalgeria.com iafactoryalgeria.com;

    ssl_certificate /etc/letsencrypt/live/www.iafactoryalgeria.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/www.iafactoryalgeria.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # NOUVEAU ROOT (Astro Marketing)
    root /opt/rag-dz-v2/marketing-dist;
    index index.html;

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Ollama API
    location ^~ /ollama/ {
        proxy_pass http://127.0.0.1:11434/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Archon UI
    location /archon/ {
        alias /opt/iafactory-rag-dz/frontend/archon-ui/dist/;
        try_files $uri $uri/ /archon/index.html;
    }

    # RAG UI
    location /rag-ui/ {
        alias /opt/iafactory-rag-dz/frontend/rag-ui/dist/;
        try_files $uri $uri/ /rag-ui/index.html;
    }

    # Hub
    location /hub/ {
        alias /opt/iafactory-rag-dz/frontend/archon-ui/dist/;
        try_files $uri $uri/ /hub/index.html;
    }

    # API Backend
    location /api/ {
        proxy_pass http://127.0.0.1:8180/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # WebSocket
    location /ws {
        proxy_pass http://127.0.0.1:8180/ws;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Marketing Astro SSG (MUST BE LAST)
    location / {
        try_files $uri $uri/ $uri/index.html =404;

        location ~* ^/_astro/.+\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        location ~* \.html$ {
            expires -1;
            add_header Cache-Control "no-store, no-cache, must-revalidate";
        }
    }

    error_page 404 /404.html;
}
NGINX_CONF

# Copier nouvelle config
cp /tmp/nginx-iafactoryalgeria-new.conf /etc/nginx/sites-available/iafactoryalgeria
echo -e "${GREEN}✓ Config modifiée${NC}"

# ============================================
# ÉTAPE 4 : Test syntaxe Nginx
# ============================================
echo -e "\n${YELLOW}[4/6] Test syntaxe Nginx...${NC}"
if nginx -t 2>&1 | tee /tmp/nginx-test.log; then
    echo -e "${GREEN}✓ Syntaxe Nginx OK${NC}"
else
    echo -e "${RED}✗ Erreur syntaxe Nginx !${NC}"
    echo -e "${YELLOW}Rollback automatique...${NC}"
    cp "$BACKUP_FILE" /etc/nginx/sites-available/iafactoryalgeria
    echo -e "${GREEN}✓ Config restaurée depuis backup${NC}"
    exit 1
fi

# ============================================
# ÉTAPE 5 : Reload Nginx
# ============================================
echo -e "\n${YELLOW}[5/6] Reload Nginx...${NC}"
if systemctl reload nginx; then
    echo -e "${GREEN}✓ Nginx rechargé avec succès${NC}"
else
    echo -e "${RED}✗ Erreur reload Nginx !${NC}"
    echo -e "${YELLOW}Rollback automatique...${NC}"
    cp "$BACKUP_FILE" /etc/nginx/sites-available/iafactoryalgeria
    systemctl reload nginx
    echo -e "${GREEN}✓ Config restaurée et Nginx rechargé${NC}"
    exit 1
fi

# ============================================
# ÉTAPE 6 : Test HTTP
# ============================================
echo -e "\n${YELLOW}[6/6] Test HTTP...${NC}"

# Test page d'accueil (local)
if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "200\|301"; then
    echo -e "${GREEN}✓ Page d'accueil accessible (HTTP)${NC}"
else
    echo -e "${YELLOW}⚠ Avertissement: page d'accueil HTTP retourne code inattendu${NC}"
fi

# Test HTTPS (local)
if curl -s -k -o /dev/null -w "%{http_code}" https://localhost | grep -q "200"; then
    echo -e "${GREEN}✓ Page d'accueil accessible (HTTPS)${NC}"
else
    echo -e "${YELLOW}⚠ Avertissement: page d'accueil HTTPS retourne code inattendu${NC}"
fi

# Test routes proxy
echo -e "\n${YELLOW}Test routes existantes...${NC}"
for route in "/api/health" "/archon/" "/rag-ui/" "/hub/"; do
    if curl -s -k -o /dev/null -w "%{http_code}" "https://localhost$route" | grep -q "200\|301\|302\|404"; then
        echo -e "${GREEN}✓ $route accessible${NC}"
    else
        echo -e "${YELLOW}⚠ $route retourne code inattendu${NC}"
    fi
done

# ============================================
# RÉSUMÉ
# ============================================
echo -e "\n${GREEN}=== Déploiement terminé avec succès ===${NC}"
echo -e "${YELLOW}Backup sauvegardé:${NC} $BACKUP_FILE"
echo -e "${YELLOW}Pour restaurer (si problème):${NC}"
echo -e "  cp $BACKUP_FILE /etc/nginx/sites-available/iafactoryalgeria"
echo -e "  systemctl reload nginx"
echo -e "\n${YELLOW}Test final recommandé:${NC}"
echo -e "  curl -I https://www.iafactoryalgeria.com/"
echo -e "  curl -I https://www.iafactoryalgeria.com/hub/"
echo -e "  curl -I https://www.iafactoryalgeria.com/api/health"
