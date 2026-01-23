# 🚀 Guide de Déploiement VPS - CAN 2025

## 📋 Prérequis

- VPS Linux (Ubuntu 20.04+ recommandé)
- Node.js 18+ installé
- Nginx installé
- PM2 installé globalement
- Domaine pointant vers le VPS (optionnel)
- Certificat SSL (Let's Encrypt recommandé)

---

## 1️⃣ Préparation du VPS

### Connexion SSH

```bash
ssh root@votre-ip-vps
```

### Installation des dépendances

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install PM2
sudo npm install -g pm2

# Install Nginx
sudo apt install -y nginx

# Install Certbot (pour SSL)
sudo apt install -y certbot python3-certbot-nginx
```

---

## 2️⃣ Transfert du Code

### Option A: Git Clone (Recommandé)

```bash
# Créer répertoire
mkdir -p /var/www
cd /var/www

# Cloner repo (remplacer par votre URL)
git clone https://github.com/votre-username/rag-dz.git
cd rag-dz/apps/can2025

# Installer dependencies
npm install

# Build production
npm run build
```

### Option B: SCP/SFTP

```bash
# Depuis votre machine locale
scp -r D:\IAFactory\rag-dz\apps\can2025 root@votre-ip:/var/www/

# Sur le VPS
cd /var/www/can2025
npm install
npm run build
```

---

## 3️⃣ Configuration PM2

### Créer fichier ecosystem

```bash
cd /var/www/rag-dz/apps/can2025

# Créer ecosystem.config.js
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'can2025',
    script: 'npm',
    args: 'start',
    cwd: '/var/www/rag-dz/apps/can2025',
    instances: 1,
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 3002
    },
    error_file: '/var/log/pm2/can2025-error.log',
    out_file: '/var/log/pm2/can2025-out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    autorestart: true,
    max_restarts: 10,
    min_uptime: '10s'
  }]
};
EOF
```

### Lancer l'app avec PM2

```bash
# Démarrer
pm2 start ecosystem.config.js

# Vérifier status
pm2 status

# Voir logs
pm2 logs can2025

# Sauvegarder config PM2
pm2 save

# Auto-start au boot
pm2 startup
# Copier-coller la commande affichée
```

---

## 4️⃣ Configuration Nginx

### Créer config Nginx

```bash
sudo nano /etc/nginx/sites-available/can2025
```

### Config sans SSL (temporaire)

```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    location / {
        proxy_pass http://localhost:3002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Cache static files
    location /_next/static {
        proxy_pass http://localhost:3002;
        proxy_cache_valid 200 1y;
        add_header Cache-Control "public, immutable";
    }

    # Service Worker
    location /sw.js {
        proxy_pass http://localhost:3002;
        add_header Cache-Control "no-cache";
    }

    # Manifest
    location /manifest.json {
        proxy_pass http://localhost:3002;
        add_header Cache-Control "public, max-age=604800";
    }
}
```

### Activer site

```bash
# Symlink
sudo ln -s /etc/nginx/sites-available/can2025 /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

---

## 5️⃣ SSL avec Let's Encrypt

### Obtenir certificat

```bash
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com
```

### Auto-renouvellement

```bash
# Test renouvellement
sudo certbot renew --dry-run

# Cron job (déjà configuré par certbot)
sudo crontab -l
```

### Config Nginx finale (avec SSL)

Certbot modifie automatiquement la config. Vérifier:

```bash
sudo nano /etc/nginx/sites-available/can2025
```

Devrait contenir:

```nginx
server {
    listen 443 ssl http2;
    server_name votre-domaine.com www.votre-domaine.com;

    ssl_certificate /etc/letsencrypt/live/votre-domaine.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/votre-domaine.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # ... reste de la config
}

server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;
    return 301 https://$server_name$request_uri;
}
```

---

## 6️⃣ Firewall

### Configurer UFW

```bash
# Activer UFW
sudo ufw enable

# Allow SSH
sudo ufw allow OpenSSH

# Allow HTTP & HTTPS
sudo ufw allow 'Nginx Full'

# Vérifier
sudo ufw status
```

---

## 7️⃣ Monitoring

### PM2 Monitoring

```bash
# Status
pm2 status

# Logs temps réel
pm2 logs can2025 --lines 100

# Monitoring CPU/RAM
pm2 monit

# Logs dashboard web (optionnel)
pm2 install pm2-logrotate
```

### Nginx Logs

```bash
# Access log
sudo tail -f /var/log/nginx/access.log

# Error log
sudo tail -f /var/log/nginx/error.log
```

---

## 8️⃣ Mises à Jour

### Update app

```bash
cd /var/www/rag-dz/apps/can2025

# Pull latest
git pull origin main

# Install deps
npm install

# Build
npm run build

# Restart PM2
pm2 restart can2025

# Vérifier
pm2 logs can2025 --lines 50
```

---

## 9️⃣ Troubleshooting

### App ne démarre pas

```bash
# Vérifier logs PM2
pm2 logs can2025 --err --lines 100

# Vérifier port 3002 libre
sudo netstat -tulpn | grep 3002

# Restart manuel
cd /var/www/rag-dz/apps/can2025
npm run build
pm2 restart can2025
```

### Nginx errors

```bash
# Test config
sudo nginx -t

# Vérifier logs
sudo tail -f /var/log/nginx/error.log

# Restart Nginx
sudo systemctl restart nginx
```

### SSL errors

```bash
# Renouveler certificat
sudo certbot renew

# Vérifier expiration
sudo certbot certificates
```

---

## 🔟 Optimisations Production

### 1. Compression Brotli (optionnel)

```bash
sudo apt install -y nginx-module-brotli

# Ajouter dans nginx.conf
sudo nano /etc/nginx/nginx.conf

# Ajouter:
# brotli on;
# brotli_types text/plain text/css application/json application/javascript text/xml application/xml;
```

### 2. Cache Nginx

Ajouter dans `/etc/nginx/nginx.conf`:

```nginx
http {
    # ...
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=can2025_cache:10m max_size=100m inactive=60m use_temp_path=off;
}
```

Dans `/etc/nginx/sites-available/can2025`:

```nginx
location / {
    # ...
    proxy_cache can2025_cache;
    proxy_cache_valid 200 10m;
    add_header X-Cache-Status $upstream_cache_status;
}
```

### 3. Rate Limiting

```nginx
http {
    limit_req_zone $binary_remote_addr zone=can2025_limit:10m rate=10r/s;
}

server {
    location / {
        limit_req zone=can2025_limit burst=20 nodelay;
        # ...
    }
}
```

---

## ✅ Checklist Déploiement

**Avant déploiement**:
- [ ] Code testé localement
- [ ] Build production OK (`npm run build`)
- [ ] .env configuré si nécessaire
- [ ] Domaine configuré (DNS A record)

**Déploiement**:
- [ ] Code transféré sur VPS
- [ ] Dependencies installées
- [ ] Build production créé
- [ ] PM2 configuré et running
- [ ] Nginx configuré
- [ ] SSL activé
- [ ] Firewall configuré

**Post-déploiement**:
- [ ] App accessible via domaine
- [ ] HTTPS fonctionne
- [ ] PWA installable
- [ ] Service Worker actif
- [ ] Logs PM2 OK
- [ ] Monitoring configuré

---

## 📞 Support

En cas de problème:

1. Vérifier logs PM2: `pm2 logs can2025`
2. Vérifier logs Nginx: `sudo tail -f /var/log/nginx/error.log`
3. Vérifier status: `pm2 status` et `sudo systemctl status nginx`
4. Restart: `pm2 restart can2025` et `sudo systemctl restart nginx`

---

## 🎯 Commandes Rapides

```bash
# Status global
pm2 status && sudo systemctl status nginx

# Logs live
pm2 logs can2025 --lines 100

# Restart tout
pm2 restart can2025 && sudo systemctl reload nginx

# Update app
cd /var/www/rag-dz/apps/can2025 && git pull && npm install && npm run build && pm2 restart can2025

# Monitoring
pm2 monit
```

---

**Déploiement réussi! 🎉**

L'app CAN 2025 est maintenant accessible en production! 🏆🇩🇿
