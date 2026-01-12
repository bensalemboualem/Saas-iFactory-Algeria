#!/bin/bash
# Script de déploiement complet
set -e

echo "=== VERIFICATION CODE ==="
if [ -d ~/rag-dz ]; then
    echo "Code existe! Mise à jour..."
    cd ~/rag-dz && git pull
else
    echo "Code n'existe pas. Entrez l'URL du repo:"
    read REPO_URL
    cd ~ && git clone $REPO_URL rag-dz
fi

echo ""
echo "=== LANCEMENT CONTAINERS ==="
cd ~/rag-dz
docker compose up -d

echo ""
echo "=== ATTENTE DEMARRAGE ==="
sleep 10

echo ""
echo "=== GENERATION SSL ==="
systemctl stop nginx
certbot certonly --standalone --non-interactive --agree-tos --register-unsafely-without-email -d iafactory.ch -d www.iafactory.ch
certbot certonly --standalone --non-interactive --agree-tos --register-unsafely-without-email -d iafactoryalgeria.com -d www.iafactoryalgeria.com

echo ""
echo "=== CONFIGURATION NGINX ==="
cat > /etc/nginx/sites-available/iafactory.ch << 'EOF'
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
    location / {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
    }
    location /api/ {
        proxy_pass http://localhost:8002;
    }
}
EOF

cat > /etc/nginx/sites-available/iafactoryalgeria.com << 'EOF'
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
    location / {
        proxy_pass http://localhost:3002;
        proxy_set_header Host $host;
    }
    location /api/ {
        proxy_pass http://localhost:8002;
    }
}
EOF

ln -sf /etc/nginx/sites-available/iafactory.ch /etc/nginx/sites-enabled/
ln -sf /etc/nginx/sites-available/iafactoryalgeria.com /etc/nginx/sites-enabled/
nginx -t && systemctl start nginx

echo ""
echo "=== STATUS FINAL ==="
docker ps
echo ""
certbot certificates
echo ""
echo "✅ TERMINE!"
echo "Testez: https://iafactory.ch et https://iafactoryalgeria.com"
