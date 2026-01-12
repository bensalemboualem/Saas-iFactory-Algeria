#!/bin/bash
################################################################################
# 🔍 DIAGNOSTIC COMPLET + FIX SSL
################################################################################

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${RED}================================${NC}"
echo -e "${RED}🔍 DIAGNOSTIC SSL COMPLET${NC}"
echo -e "${RED}================================${NC}"
echo ""

# === 1. VÉRIFIER DNS ===
echo -e "${CYAN}=== 1. DNS ====${NC}"
echo -n "iafactory.ch → "
dig +short iafactory.ch A || nslookup iafactory.ch | grep Address | tail -1
echo -n "iafactoryalgeria.com → "
dig +short iafactoryalgeria.com A || nslookup iafactoryalgeria.com | grep Address | tail -1
echo -n "IP du VPS → "
curl -s ifconfig.me
echo ""

# === 2. VÉRIFIER PORTS ===
echo -e "${CYAN}=== 2. PORTS ====${NC}"
netstat -tuln | grep -E ':(80|443) ' || ss -tuln | grep -E ':(80|443) '
echo ""

# === 3. VÉRIFIER NGINX ===
echo -e "${CYAN}=== 3. NGINX ====${NC}"
systemctl status nginx --no-pager | head -5
echo ""
echo "Sites actifs:"
ls -la /etc/nginx/sites-enabled/
echo ""

# === 4. VÉRIFIER CERTIFICATS ===
echo -e "${CYAN}=== 4. CERTIFICATS SSL ====${NC}"
certbot certificates 2>&1 || echo "Certbot pas installé ou aucun certificat"
echo ""

# === 5. VÉRIFIER CONTAINERS ===
echo -e "${CYAN}=== 5. CONTAINERS DOCKER ====${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""

# === 6. TEST LOCAL ===
echo -e "${CYAN}=== 6. TEST LOCAL ====${NC}"
curl -s -o /dev/null -w "Frontend CH (3001): %{http_code}\n" http://localhost:3001
curl -s -o /dev/null -w "Frontend DZ (3002): %{http_code}\n" http://localhost:3002
curl -s -o /dev/null -w "Backend (8002): %{http_code}\n" http://localhost:8002/health
echo ""

echo -e "${RED}================================${NC}"
echo -e "${RED}🔧 FIX AUTOMATIQUE${NC}"
echo -e "${RED}================================${NC}"
echo ""

# === ARRÊTER NGINX ===
echo -e "${YELLOW}→ Arrêt de Nginx...${NC}"
systemctl stop nginx
sleep 2

# === NETTOYER ANCIENS CERTIFICATS ===
echo -e "${YELLOW}→ Nettoyage des anciens certificats...${NC}"
certbot delete --cert-name iafactory.ch --non-interactive 2>/dev/null || true
certbot delete --cert-name iafactoryalgeria.com --non-interactive 2>/dev/null || true
rm -rf /etc/letsencrypt/live/iafactory.ch /etc/letsencrypt/live/iafactoryalgeria.com
rm -rf /etc/letsencrypt/archive/iafactory.ch /etc/letsencrypt/archive/iafactoryalgeria.com
rm -rf /etc/letsencrypt/renewal/iafactory.ch.conf /etc/letsencrypt/renewal/iafactoryalgeria.com.conf

# === GÉNÉRER CERTIFICAT CH ===
echo -e "${YELLOW}→ Génération certificat iafactory.ch...${NC}"
certbot certonly \
    --standalone \
    --non-interactive \
    --agree-tos \
    --register-unsafely-without-email \
    -d iafactory.ch \
    -d www.iafactory.ch \
    --preferred-challenges http

if [ -f /etc/letsencrypt/live/iafactory.ch/fullchain.pem ]; then
    echo -e "${GREEN}✅ Certificat iafactory.ch créé${NC}"
else
    echo -e "${RED}❌ ÉCHEC iafactory.ch${NC}"
fi

# === GÉNÉRER CERTIFICAT DZ ===
echo -e "${YELLOW}→ Génération certificat iafactoryalgeria.com...${NC}"
certbot certonly \
    --standalone \
    --non-interactive \
    --agree-tos \
    --register-unsafely-without-email \
    -d iafactoryalgeria.com \
    -d www.iafactoryalgeria.com \
    --preferred-challenges http

if [ -f /etc/letsencrypt/live/iafactoryalgeria.com/fullchain.pem ]; then
    echo -e "${GREEN}✅ Certificat iafactoryalgeria.com créé${NC}"
else
    echo -e "${RED}❌ ÉCHEC iafactoryalgeria.com${NC}"
    echo ""
    echo -e "${YELLOW}Causes possibles:${NC}"
    echo "  1. DNS ne pointe pas vers ce serveur"
    echo "  2. Port 80 bloqué par firewall"
    echo "  3. Autre service utilise le port 80"
    echo ""
    echo -e "${CYAN}Vérification:${NC}"
    echo "  - IP VPS: $(curl -s ifconfig.me)"
    echo "  - DNS DZ: $(dig +short iafactoryalgeria.com A)"
fi

# === CRÉER CONFIG NGINX CH ===
echo -e "${YELLOW}→ Configuration Nginx iafactory.ch...${NC}"
cat > /etc/nginx/sites-available/iafactory.ch << 'EOFCH'
server {
    listen 80;
    server_name iafactory.ch www.iafactory.ch;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name iafactory.ch www.iafactory.ch;

    ssl_certificate /etc/letsencrypt/live/iafactory.ch/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/iafactory.ch/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    add_header Strict-Transport-Security "max-age=31536000" always;

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Tenant-ID "814c132a-1cdd-4db6-bc1f-21abd21ec37d";
        proxy_set_header X-Tenant-Profile "psychologist";
        proxy_set_header X-Country "CH";
    }

    location /api/ {
        proxy_pass http://localhost:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Tenant-ID "814c132a-1cdd-4db6-bc1f-21abd21ec37d";
    }
}
EOFCH

# === CRÉER CONFIG NGINX DZ ===
echo -e "${YELLOW}→ Configuration Nginx iafactoryalgeria.com...${NC}"
cat > /etc/nginx/sites-available/iafactoryalgeria.com << 'EOFDZ'
server {
    listen 80;
    server_name iafactoryalgeria.com www.iafactoryalgeria.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name iafactoryalgeria.com www.iafactoryalgeria.com;

    ssl_certificate /etc/letsencrypt/live/iafactoryalgeria.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/iafactoryalgeria.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    add_header Strict-Transport-Security "max-age=31536000" always;

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
        proxy_set_header X-Tenant-ID "922d243b-2dee-5ec7-cd2g-32bce32fd48e";
        proxy_set_header X-Tenant-Profile "education";
        proxy_set_header X-Country "DZ";
    }

    location /api/ {
        proxy_pass http://localhost:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Tenant-ID "922d243b-2dee-5ec7-cd2g-32bce32fd48e";
    }
}
EOFDZ

# === ACTIVER SITES ===
ln -sf /etc/nginx/sites-available/iafactory.ch /etc/nginx/sites-enabled/
ln -sf /etc/nginx/sites-available/iafactoryalgeria.com /etc/nginx/sites-enabled/

# === TEST NGINX ===
echo -e "${YELLOW}→ Test configuration Nginx...${NC}"
nginx -t

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Configuration Nginx valide${NC}"
else
    echo -e "${RED}❌ Configuration Nginx invalide${NC}"
    exit 1
fi

# === DÉMARRER NGINX ===
echo -e "${YELLOW}→ Démarrage Nginx...${NC}"
systemctl start nginx
systemctl reload nginx

# === VÉRIFICATION FINALE ===
echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✅ FIX TERMINÉ${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

echo -e "${CYAN}Certificats installés:${NC}"
certbot certificates

echo ""
echo -e "${CYAN}Test HTTPS:${NC}"
sleep 3
curl -I https://iafactory.ch 2>&1 | head -10
echo ""
curl -I https://iafactoryalgeria.com 2>&1 | head -10

echo ""
echo -e "${GREEN}🌐 Testez dans votre navigateur:${NC}"
echo "   https://iafactory.ch"
echo "   https://iafactoryalgeria.com"
echo ""
echo -e "${YELLOW}💡 Utilisez Ctrl+Shift+R pour forcer le rafraîchissement${NC}"
