#!/bin/bash
################################################################################
# 🔧 FIX SSL URGENT - iafactoryalgeria.com
# Corrige l'erreur ERR_CERT_COMMON_NAME_INVALID
################################################################################

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}================================${NC}"
echo -e "${CYAN}🔧 FIX SSL URGENT${NC}"
echo -e "${CYAN}================================${NC}"
echo ""

# Vérifier si nous sommes sur le VPS
if [ ! -f /etc/nginx/nginx.conf ]; then
    echo -e "${RED}❌ Ce script doit être exécuté sur le VPS!${NC}"
    echo ""
    echo -e "${YELLOW}Connectez-vous d'abord:${NC}"
    echo -e "${CYAN}ssh root@46.224.3.125${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Diagnostic du problème SSL...${NC}"
echo ""

# Vérifier les certificats existants
echo -e "${CYAN}1. Vérification des certificats SSL existants...${NC}"
certbot certificates

echo ""
echo -e "${CYAN}2. Vérification de la configuration Nginx...${NC}"
nginx -t

echo ""
echo -e "${CYAN}3. Vérification des domaines DNS...${NC}"
nslookup iafactory.ch || true
nslookup iafactoryalgeria.com || true

echo ""
echo -e "${YELLOW}🔧 Correction du problème...${NC}"
echo ""

# Stopper Nginx temporairement
echo -e "${CYAN}4. Arrêt temporaire de Nginx...${NC}"
systemctl stop nginx

# Supprimer les anciens certificats si problématiques
echo -e "${CYAN}5. Nettoyage des anciens certificats...${NC}"
certbot delete --cert-name iafactoryalgeria.com --non-interactive || true

# Regénérer le certificat pour iafactoryalgeria.com
echo -e "${CYAN}6. Génération d'un nouveau certificat SSL...${NC}"
certbot certonly \
    --standalone \
    --non-interactive \
    --agree-tos \
    --email support@iafactoryalgeria.com \
    -d iafactoryalgeria.com \
    -d www.iafactoryalgeria.com \
    --preferred-challenges http

# Vérifier si le certificat a été créé
if [ -f /etc/letsencrypt/live/iafactoryalgeria.com/fullchain.pem ]; then
    echo -e "${GREEN}✅ Certificat SSL créé avec succès!${NC}"
else
    echo -e "${RED}❌ Échec de création du certificat!${NC}"
    echo ""
    echo -e "${YELLOW}Vérifiez que:${NC}"
    echo "  1. Le DNS pointe vers ce serveur (46.224.3.125)"
    echo "  2. Le port 80 est ouvert"
    echo "  3. Aucun autre service n'utilise le port 80"
    exit 1
fi

# Mettre à jour la configuration Nginx pour iafactoryalgeria.com
echo -e "${CYAN}7. Mise à jour de la configuration Nginx...${NC}"

cat > /etc/nginx/sites-available/iafactoryalgeria.com << 'EOFNGINX'
# Algeria Frontend (iafactoryalgeria.com) - Port 3002
server {
    listen 80;
    server_name iafactoryalgeria.com www.iafactoryalgeria.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name iafactoryalgeria.com www.iafactoryalgeria.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/iafactoryalgeria.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/iafactoryalgeria.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # CORS Headers
    add_header Access-Control-Allow-Origin "https://iafactoryalgeria.com" always;
    add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, PATCH, OPTIONS" always;
    add_header Access-Control-Allow-Headers "Authorization, Content-Type, X-Tenant-ID, X-Requested-With, Accept" always;
    add_header Access-Control-Allow-Credentials "true" always;

    # CSP Header (updated for CDNs)
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://unpkg.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: https: blob:; connect-src 'self' https://iafactoryalgeria.com wss://iafactoryalgeria.com;" always;

    # Client body size
    client_max_body_size 50M;

    # Timeouts (extended for voice transcription)
    proxy_connect_timeout 600s;
    proxy_send_timeout 600s;
    proxy_read_timeout 600s;
    send_timeout 600s;

    # Root location
    location / {
        proxy_pass http://localhost:3002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Multi-Tenant Headers
        proxy_set_header X-Tenant-Profile "education";
        proxy_set_header X-Country "DZ";
        proxy_set_header X-Tenant-ID "922d243b-2dee-5ec7-cd2g-32bce32fd48e";
    }

    # API Backend routing
    location /api/ {
        proxy_pass http://localhost:8002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Multi-Tenant Headers
        proxy_set_header X-Tenant-Profile "education";
        proxy_set_header X-Country "DZ";
        proxy_set_header X-Tenant-ID "922d243b-2dee-5ec7-cd2g-32bce32fd48e";

        # CORS for API
        if ($request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Origin "https://iafactoryalgeria.com" always;
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, PATCH, OPTIONS" always;
            add_header Access-Control-Allow-Headers "Authorization, Content-Type, X-Tenant-ID, X-Requested-With, Accept" always;
            add_header Access-Control-Allow-Credentials "true" always;
            add_header Content-Length 0;
            add_header Content-Type text/plain;
            return 204;
        }
    }

    # Health check
    location /health {
        access_log off;
        return 200 "Algeria Frontend Healthy\n";
        add_header Content-Type text/plain;
    }

    # Logs
    access_log /var/log/nginx/iafactoryalgeria.com-access.log;
    error_log /var/log/nginx/iafactoryalgeria.com-error.log;
}
EOFNGINX

# Créer le lien symbolique
ln -sf /etc/nginx/sites-available/iafactoryalgeria.com /etc/nginx/sites-enabled/

echo -e "${CYAN}8. Test de la configuration Nginx...${NC}"
nginx -t

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Configuration Nginx valide!${NC}"
else
    echo -e "${RED}❌ Erreur dans la configuration Nginx!${NC}"
    exit 1
fi

# Redémarrer Nginx
echo -e "${CYAN}9. Redémarrage de Nginx...${NC}"
systemctl start nginx
systemctl status nginx --no-pager

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✅ FIX SSL TERMINÉ!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

echo -e "${CYAN}🌐 Testez maintenant:${NC}"
echo -e "   ${GREEN}https://iafactoryalgeria.com${NC}"
echo ""

echo -e "${YELLOW}📋 Certificats SSL actifs:${NC}"
certbot certificates

echo ""
echo -e "${CYAN}🔍 Test SSL en ligne de commande:${NC}"
echo -e "${YELLOW}curl -I https://iafactoryalgeria.com${NC}"
curl -I https://iafactoryalgeria.com || true

echo ""
echo -e "${GREEN}✅ C'est corrigé! Rechargez votre navigateur avec Ctrl+Shift+R${NC}"
