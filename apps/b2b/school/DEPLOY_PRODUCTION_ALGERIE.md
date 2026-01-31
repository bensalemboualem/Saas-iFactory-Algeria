# 🇩🇿 Guide de Déploiement Production - IAFactory School Algeria

## Architecture Recommandée

```
┌─────────────────────────────────────────────────────────────────────┐
│                         LOAD BALANCER                                │
│                    (Cloudflare / Nginx)                              │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   Web Server  │    │   Web Server  │    │   Web Server  │
│   (Laravel)   │    │   (Laravel)   │    │   (Laravel)   │
│   PHP 8.2     │    │   PHP 8.2     │    │   PHP 8.2     │
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│    MySQL      │    │    Redis      │    │   S3/Minio    │
│   Primary     │    │   Cluster     │    │   Storage     │
└───────────────┘    └───────────────┘    └───────────────┘
```

---

## 1. Prérequis VPS

### Configuration Minimale (1 école, < 500 élèves)
- **CPU:** 2 vCPU
- **RAM:** 4 GB
- **Storage:** 50 GB SSD
- **OS:** Ubuntu 22.04 LTS
- **Prix estimé:** 15-20€/mois (Hetzner, OVH)

### Configuration Recommandée (Multi-tenant, 5+ écoles)
- **CPU:** 4 vCPU
- **RAM:** 8 GB
- **Storage:** 100 GB SSD
- **OS:** Ubuntu 22.04 LTS
- **Prix estimé:** 30-40€/mois

### Configuration Enterprise (50+ écoles)
- **CPU:** 8 vCPU
- **RAM:** 16 GB
- **Storage:** 500 GB SSD + S3
- **Database:** Managed MySQL (séparé)
- **Prix estimé:** 80-150€/mois

---

## 2. Installation Serveur

### 2.1 Mise à jour système

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y software-properties-common curl wget git unzip
```

### 2.2 Installation PHP 8.2

```bash
sudo add-apt-repository ppa:ondrej/php -y
sudo apt update
sudo apt install -y php8.2 php8.2-fpm php8.2-mysql php8.2-mbstring \
    php8.2-xml php8.2-bcmath php8.2-zip php8.2-gd php8.2-curl \
    php8.2-redis php8.2-intl
```

### 2.3 Installation MySQL 8.0

```bash
sudo apt install -y mysql-server
sudo mysql_secure_installation

# Créer base de données et utilisateur
sudo mysql -e "CREATE DATABASE iafactory_school CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER 'school_user'@'localhost' IDENTIFIED BY 'VOTRE_MOT_DE_PASSE_SECURISE';"
sudo mysql -e "GRANT ALL PRIVILEGES ON iafactory_school.* TO 'school_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
```

### 2.4 Installation Redis

```bash
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

### 2.5 Installation Nginx

```bash
sudo apt install -y nginx
sudo systemctl enable nginx
```

### 2.6 Installation Composer

```bash
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
```

### 2.7 Installation Node.js (pour assets)

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

---

## 3. Déploiement Application

### 3.1 Cloner le projet

```bash
cd /var/www
sudo git clone https://votre-repo.git school
sudo chown -R www-data:www-data school
cd school
```

### 3.2 Configuration environnement

```bash
cp .env.example .env
nano .env
```

### 3.3 Variables .env Production

```env
# Application
APP_NAME="École [NOM]"
APP_ENV=production
APP_DEBUG=false
APP_URL=https://ecole.votredomaine.dz
APP_HTTPS=true

# Database
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=iafactory_school
DB_USERNAME=school_user
DB_PASSWORD=VOTRE_MOT_DE_PASSE_SECURISE

# Cache & Session
CACHE_DRIVER=redis
SESSION_DRIVER=redis
QUEUE_CONNECTION=redis
REDIS_HOST=127.0.0.1

# Multi-tenant SaaS
APP_SAAS=true

# AI Assistant
AI_PROVIDER=openai
AI_API_KEY=sk-votre-cle-openai
AI_MODEL=gpt-4o-mini
AI_ASSISTANT_ENABLED=true

# Paiement SATIM (CIB/EDAHABIA)
SATIM_MODE=production
SATIM_MERCHANT_ID=votre_merchant_id
SATIM_SECRET_KEY=votre_secret_key
SATIM_CIB_ENABLED=true
SATIM_EDAHABIA_ENABLED=true

# SMS (Twilio)
TWILIO_ACCOUNT_SID=votre_sid
TWILIO_AUTH_TOKEN=votre_token
TWILIO_FROM=+213xxxxxxxx

# Email
MAIL_MAILER=smtp
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=ecole@gmail.com
MAIL_PASSWORD=app_password
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=noreply@votredomaine.dz
MAIL_FROM_NAME="${APP_NAME}"

# Firebase (Push Notifications)
FIREBASE_CREDENTIALS=/var/www/school/storage/app/firebase-credentials.json
```

### 3.4 Installation dépendances

```bash
composer install --no-dev --optimize-autoloader
npm install
npm run build
```

### 3.5 Configuration Laravel

```bash
php artisan key:generate
php artisan migrate --force
php artisan db:seed --class=AlgeriaEducationSeeder
php artisan storage:link
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

### 3.6 Permissions

```bash
sudo chown -R www-data:www-data storage bootstrap/cache
sudo chmod -R 775 storage bootstrap/cache
```

---

## 4. Configuration Nginx

### 4.1 Créer le fichier de configuration

```bash
sudo nano /etc/nginx/sites-available/school
```

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name ecole.votredomaine.dz *.votredomaine.dz;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name ecole.votredomaine.dz *.votredomaine.dz;
    root /var/www/school/public;

    index index.php;

    # SSL (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/votredomaine.dz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/votredomaine.dz/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # Upload limits
    client_max_body_size 50M;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
        fastcgi_read_timeout 300;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }

    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### 4.2 Activer le site

```bash
sudo ln -s /etc/nginx/sites-available/school /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 5. SSL avec Let's Encrypt

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d ecole.votredomaine.dz -d *.votredomaine.dz
```

---

## 6. Configuration Queue Workers

### 6.1 Créer le service Supervisor

```bash
sudo apt install -y supervisor
sudo nano /etc/supervisor/conf.d/school-worker.conf
```

```ini
[program:school-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /var/www/school/artisan queue:work redis --sleep=3 --tries=3 --max-time=3600
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
user=www-data
numprocs=2
redirect_stderr=true
stdout_logfile=/var/www/school/storage/logs/worker.log
stopwaitsecs=3600
```

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start school-worker:*
```

---

## 7. Cron Jobs

```bash
sudo crontab -e -u www-data
```

```cron
* * * * * cd /var/www/school && php artisan schedule:run >> /dev/null 2>&1
```

---

## 8. Backup Automatique

### 8.1 Script de backup

```bash
sudo nano /opt/backup-school.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/school"
DB_NAME="iafactory_school"
DB_USER="school_user"
DB_PASS="VOTRE_MOT_DE_PASSE"

mkdir -p $BACKUP_DIR

# Backup database
mysqldump -u$DB_USER -p$DB_PASS $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup storage
tar -czf $BACKUP_DIR/storage_$DATE.tar.gz /var/www/school/storage/app

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
sudo chmod +x /opt/backup-school.sh
sudo crontab -e
```

```cron
0 2 * * * /opt/backup-school.sh >> /var/log/backup-school.log 2>&1
```

---

## 9. Monitoring

### 9.1 Installation de monitoring simple

```bash
# Installer htop pour monitoring système
sudo apt install -y htop

# Logs Laravel
tail -f /var/www/school/storage/logs/laravel.log

# Logs Nginx
tail -f /var/log/nginx/error.log
```

### 9.2 Healthcheck endpoint

Ajouter dans `routes/api.php`:
```php
Route::get('/health', function () {
    return response()->json([
        'status' => 'ok',
        'timestamp' => now()->toIso8601String(),
        'db' => DB::connection()->getPdo() ? 'connected' : 'error',
        'cache' => Cache::store('redis')->put('health', 'ok', 1) ? 'connected' : 'error',
    ]);
});
```

---

## 10. Multi-Tenant Setup (SaaS)

### 10.1 Créer une nouvelle école (tenant)

```bash
php artisan tinker
```

```php
$tenant = App\Models\Tenant::create([
    'id' => 'ecole-alger',
    'name' => 'École El Feth Alger',
    'sub_domain_key' => 'elfeth',
    'address' => 'Rue Didouche Mourad, Alger',
    'phone' => '+213 21 XX XX XX',
    'email' => 'contact@elfeth.dz',
]);

$tenant->domains()->create(['domain' => 'elfeth.votredomaine.dz']);
$tenant->run(function () {
    Artisan::call('migrate', ['--path' => 'database/migrations/tenant', '--force' => true]);
});
```

### 10.2 Accès

- École 1: `https://elfeth.votredomaine.dz`
- École 2: `https://iqra.votredomaine.dz`
- Admin Central: `https://admin.votredomaine.dz`

---

## 11. Tarification Recommandée (DZD)

| Plan | Élèves | Prix/mois | Prix/an |
|------|--------|-----------|---------|
| **Starter** | < 200 | 15,000 DA | 150,000 DA |
| **Pro** | < 500 | 30,000 DA | 300,000 DA |
| **Enterprise** | < 2000 | 50,000 DA | 500,000 DA |
| **Unlimited** | Illimité | 80,000 DA | 800,000 DA |

### Options supplémentaires
- Module IA/Chatbot: +10,000 DA/mois
- SMS illimités: +5,000 DA/mois
- Support prioritaire: +10,000 DA/mois
- Formation sur site: 50,000 DA (one-time)

---

## 12. Checklist Pré-Production

- [ ] SSL configuré et valide
- [ ] APP_DEBUG=false
- [ ] APP_ENV=production
- [ ] Backup automatique configuré
- [ ] Queue workers actifs
- [ ] Logs rotatifs configurés
- [ ] Firewall (UFW) configuré
- [ ] Fail2ban installé
- [ ] Monitoring actif
- [ ] Tests de charge effectués
- [ ] DNS configuré (A records + wildcard)

---

## 13. Support

- **Email:** support@iafactory.dz
- **WhatsApp:** +213 XX XX XX XX
- **Documentation:** https://docs.iafactory.dz/school

---

*Document généré le 25/01/2026 - IAFactory Algeria*
