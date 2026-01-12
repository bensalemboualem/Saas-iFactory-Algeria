#!/bin/bash

# DÉPLOIEMENT COMPLET - 4 APPS VPS
# IA Factory - 16 Décembre 2025

set -e  # Exit on error

echo "🚀 DÉPLOIEMENT VPS - 5 APPS IA FACTORY"
echo "======================================="

# Configuration
VPS_USER="root"
VPS_HOST="your-vps-ip"  # À REMPLACER!
VPS_PATH="/var/www/rag-dz"

echo ""
echo "📦 ÉTAPE 1: Upload du code"
echo "============================"

# Sync chaque app (exclure node_modules et .next)
echo "→ Upload AI Agents..."
rsync -avz --exclude 'node_modules' --exclude '.next' \
  ./apps/agents-ia/ ${VPS_USER}@${VPS_HOST}:${VPS_PATH}/apps/agents-ia/

echo "→ Upload CAN 2025..."
rsync -avz --exclude 'node_modules' --exclude '.next' \
  ./apps/can2025/ ${VPS_USER}@${VPS_HOST}:${VPS_PATH}/apps/can2025/

echo "→ Upload News DZ..."
rsync -avz --exclude 'node_modules' --exclude '.next' \
  ./apps/news-dz/ ${VPS_USER}@${VPS_HOST}:${VPS_PATH}/apps/news-dz/

echo "→ Upload Sport Magazine..."
rsync -avz --exclude 'node_modules' --exclude '.next' \
  ./apps/sport-magazine/ ${VPS_USER}@${VPS_HOST}:${VPS_PATH}/apps/sport-magazine/

echo "→ Upload Landing Page (SaaS)..."
rsync -avz ./apps/landing/ ${VPS_USER}@${VPS_HOST}:${VPS_PATH}/apps/landing/

echo "→ Upload ecosystem.config.js..."
rsync -avz ./ecosystem.config.js ${VPS_USER}@${VPS_HOST}:${VPS_PATH}/

echo ""
echo "🔧 ÉTAPE 2: Build sur VPS"
echo "=========================="

ssh ${VPS_USER}@${VPS_HOST} << 'ENDSSH'
cd /var/www/rag-dz

echo "→ Build AI Agents..."
cd apps/agents-ia
npm install
npm run build

echo "→ Build CAN 2025..."
cd ../can2025
npm install
npm run build

echo "→ Build News DZ..."
cd ../news-dz
npm install
npm run build

echo "→ Build Sport Magazine..."
cd ../sport-magazine
npm install
npm run build

cd /var/www/rag-dz
echo "✅ Tous les builds terminés!"
ENDSSH

echo ""
echo "🌐 ÉTAPE 3: Configuration Nginx"
echo "================================"

ssh ${VPS_USER}@${VPS_HOST} << 'ENDSSH'
# Créer les vhosts Nginx
cat > /etc/nginx/sites-available/agents.iafactoryalgeria.com << 'EOF'
server {
    listen 80;
    server_name agents.iafactoryalgeria.com;

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
    }
}
EOF

cat > /etc/nginx/sites-available/can2025.iafactoryalgeria.com << 'EOF'
server {
    listen 80;
    server_name can2025.iafactoryalgeria.com;

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
    }
}
EOF

cat > /etc/nginx/sites-available/news.iafactoryalgeria.com << 'EOF'
server {
    listen 80;
    server_name news.iafactoryalgeria.com;

    location / {
        proxy_pass http://localhost:3003;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

cat > /etc/nginx/sites-available/sport.iafactoryalgeria.com << 'EOF'
server {
    listen 80;
    server_name sport.iafactoryalgeria.com;

    location / {
        proxy_pass http://localhost:3004;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

cat > /etc/nginx/sites-available/iafactoryalgeria.com << 'EOF'
server {
    listen 80;
    server_name iafactoryalgeria.com www.iafactoryalgeria.com;

    root /var/www/rag-dz/apps/landing;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip compression
    gzip on;
    gzip_types text/css application/javascript image/svg+xml;
    gzip_min_length 256;
}
EOF

# Activer les sites
ln -sf /etc/nginx/sites-available/agents.iafactoryalgeria.com /etc/nginx/sites-enabled/
ln -sf /etc/nginx/sites-available/can2025.iafactoryalgeria.com /etc/nginx/sites-enabled/
ln -sf /etc/nginx/sites-available/news.iafactoryalgeria.com /etc/nginx/sites-enabled/
ln -sf /etc/nginx/sites-available/sport.iafactoryalgeria.com /etc/nginx/sites-enabled/
ln -sf /etc/nginx/sites-available/iafactoryalgeria.com /etc/nginx/sites-enabled/

# Tester la config
nginx -t

# Recharger Nginx
systemctl reload nginx

echo "✅ Nginx configuré et rechargé!"
ENDSSH

echo ""
echo "🔒 ÉTAPE 4: SSL Certificates"
echo "============================="

ssh ${VPS_USER}@${VPS_HOST} << 'ENDSSH'
certbot --nginx -d agents.iafactoryalgeria.com --non-interactive --agree-tos -m admin@iafactoryalgeria.com
certbot --nginx -d can2025.iafactoryalgeria.com --non-interactive --agree-tos -m admin@iafactoryalgeria.com
certbot --nginx -d news.iafactoryalgeria.com --non-interactive --agree-tos -m admin@iafactoryalgeria.com
certbot --nginx -d sport.iafactoryalgeria.com --non-interactive --agree-tos -m admin@iafactoryalgeria.com
certbot --nginx -d iafactoryalgeria.com -d www.iafactoryalgeria.com --non-interactive --agree-tos -m admin@iafactoryalgeria.com

echo "✅ SSL certificates installés (5 domains)!"
ENDSSH

echo ""
echo "🚀 ÉTAPE 5: Lancement PM2"
echo "========================="

ssh ${VPS_USER}@${VPS_HOST} << 'ENDSSH'
cd /var/www/rag-dz

# Stopper les apps existantes si elles existent
pm2 delete all || true

# Démarrer toutes les apps
pm2 start ecosystem.config.js

# Sauvegarder la config PM2
pm2 save

# Auto-restart au démarrage
pm2 startup

echo "✅ PM2 démarré et configuré!"
ENDSSH

echo ""
echo "✅ DÉPLOIEMENT TERMINÉ!"
echo "======================="
echo ""
echo "🌐 URLs Disponibles:"
echo "  • https://iafactoryalgeria.com (Landing SaaS)"
echo "  • https://agents.iafactoryalgeria.com"
echo "  • https://can2025.iafactoryalgeria.com"
echo "  • https://news.iafactoryalgeria.com"
echo "  • https://sport.iafactoryalgeria.com"
echo ""
echo "📊 Monitoring:"
echo "  • pm2 status"
echo "  • pm2 logs [app-name]"
echo "  • pm2 monit"
echo ""
echo "🎉 Tout est en ligne! 🚀"
