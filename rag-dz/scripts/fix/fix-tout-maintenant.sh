#!/bin/bash
################################################################################
# 🔥 FIX TOUT MAINTENANT - ULTRA RAPIDE
################################################################################

set -e

echo "================================"
echo "🔥 FIX AUTOMATIQUE EN COURS"
echo "================================"
echo ""

# === DIAGNOSTIC ===
echo "=== 1. DIAGNOSTIC ==="
docker ps || docker-compose up -d
sleep 2
curl -s -o /dev/null -w "Frontend CH: %{http_code}\n" http://localhost:3001 || echo "❌ CH pas prêt"
curl -s -o /dev/null -w "Frontend DZ: %{http_code}\n" http://localhost:3002 || echo "❌ DZ pas prêt"
curl -s -o /dev/null -w "Backend: %{http_code}\n" http://localhost:8002/health || echo "❌ Backend pas prêt"

# === FIX NGINX CH ===
echo ""
echo "=== 2. FIX NGINX iafactory.ch ==="
cat > /etc/nginx/sites-available/iafactory.ch << 'EOFCH'
server {
    listen 80;
    server_name iafactory.ch www.iafactory.ch;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name iafactory.ch www.iafactory.ch;

    ssl_certificate /etc/letsencrypt/live/iafactory.ch/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/iafactory.ch/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    add_header Strict-Transport-Security "max-age=31536000" always;

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Tenant-ID "814c132a-1cdd-4db6-bc1f-21abd21ec37d";
        proxy_set_header X-Tenant-Profile "psychologist";
        proxy_set_header X-Country "CH";
    }

    location /api/ {
        proxy_pass http://localhost:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Tenant-ID "814c132a-1cdd-4db6-bc1f-21abd21ec37d";
    }
}
EOFCH

# === FIX NGINX DZ ===
echo "=== 3. FIX NGINX iafactoryalgeria.com ==="
cat > /etc/nginx/sites-available/iafactoryalgeria.com << 'EOFDZ'
server {
    listen 80;
    server_name iafactoryalgeria.com www.iafactoryalgeria.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name iafactoryalgeria.com www.iafactoryalgeria.com;

    ssl_certificate /etc/letsencrypt/live/iafactoryalgeria.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/iafactoryalgeria.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    add_header Strict-Transport-Security "max-age=31536000" always;

    location / {
        proxy_pass http://localhost:3002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Tenant-ID "922d243b-2dee-5ec7-cd2g-32bce32fd48e";
        proxy_set_header X-Tenant-Profile "education";
        proxy_set_header X-Country "DZ";
    }

    location /api/ {
        proxy_pass http://localhost:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Tenant-ID "922d243b-2dee-5ec7-cd2g-32bce32fd48e";
    }
}
EOFDZ

# === ACTIVER ===
echo "=== 4. ACTIVATION ==="
ln -sf /etc/nginx/sites-available/iafactory.ch /etc/nginx/sites-enabled/
ln -sf /etc/nginx/sites-available/iafactoryalgeria.com /etc/nginx/sites-enabled/

# === FIX SSL ===
echo ""
echo "=== 5. FIX SSL ==="
systemctl stop nginx

echo "Suppression anciens certificats..."
certbot delete --cert-name iafactory.ch --non-interactive 2>/dev/null || true
certbot delete --cert-name iafactoryalgeria.com --non-interactive 2>/dev/null || true

echo "Génération iafactory.ch..."
certbot certonly --standalone --non-interactive --agree-tos \
    --email support@iafactory.ch \
    -d iafactory.ch -d www.iafactory.ch \
    --preferred-challenges http || true

echo "Génération iafactoryalgeria.com..."
certbot certonly --standalone --non-interactive --agree-tos \
    --email support@iafactoryalgeria.com \
    -d iafactoryalgeria.com -d www.iafactoryalgeria.com \
    --preferred-challenges http || true

# === REDÉMARRAGE ===
echo ""
echo "=== 6. REDÉMARRAGE ==="
nginx -t
systemctl start nginx
systemctl reload nginx

# === VÉRIFICATION ===
echo ""
echo "=== 7. VÉRIFICATION ==="
sleep 3
curl -I https://iafactory.ch 2>&1 | head -5
echo ""
curl -I https://iafactoryalgeria.com 2>&1 | head -5

echo ""
echo "================================"
echo "✅ FIX TERMINÉ!"
echo "================================"
echo ""
certbot certificates
echo ""
echo "🌐 Testez:"
echo "   https://iafactory.ch"
echo "   https://iafactoryalgeria.com"
