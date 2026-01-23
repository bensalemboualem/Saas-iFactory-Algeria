# Guide d'Installation Détaillé - OneStSchooled

**Version:** 2.0.0
**Dernière mise à jour:** Décembre 2024

---

## Prérequis Système

### Serveur Web

| Composant | Minimum | Recommandé |
|-----------|---------|------------|
| OS | Ubuntu 20.04 / Windows 10 | Ubuntu 22.04 LTS |
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Stockage | 20 GB SSD | 50+ GB SSD |

### Logiciels Requis

- **PHP** >= 7.4 (8.0+ recommandé)
- **Composer** >= 2.0
- **MySQL** >= 8.0 ou **PostgreSQL** >= 14
- **Node.js** >= 16.x
- **npm** >= 8.x
- **Git**

### Extensions PHP Requises

```bash
# Extensions obligatoires
php-bcmath
php-ctype
php-fileinfo
php-json
php-mbstring
php-openssl
php-pdo
php-pdo-mysql  # ou php-pdo-pgsql
php-tokenizer
php-xml
php-curl
php-gd
php-zip

# Installation Ubuntu/Debian
sudo apt update
sudo apt install php8.1-bcmath php8.1-ctype php8.1-fileinfo \
    php8.1-json php8.1-mbstring php8.1-openssl php8.1-pdo \
    php8.1-mysql php8.1-tokenizer php8.1-xml php8.1-curl \
    php8.1-gd php8.1-zip
```

---

## Installation Pas à Pas

### 1. Cloner le Repository

```bash
cd /var/www
git clone https://github.com/iafactory/onestschooled.git
cd onestschooled
```

### 2. Configurer les Permissions

```bash
# Linux/Mac
sudo chown -R www-data:www-data storage bootstrap/cache
sudo chmod -R 775 storage bootstrap/cache

# Créer le lien symbolique pour le stockage
php artisan storage:link
```

### 3. Installer les Dépendances PHP

```bash
composer install --optimize-autoloader --no-dev

# En développement
composer install
```

### 4. Installer les Dépendances JavaScript

```bash
npm install
npm run dev

# En production
npm run production
```

### 5. Configurer l'Environnement

```bash
cp .env.example .env
php artisan key:generate
```

### 6. Éditer le Fichier .env

```bash
# ============================================
# APPLICATION
# ============================================
APP_NAME="OneStSchooled"
APP_ENV=production
APP_KEY=base64:GENERATED_KEY
APP_DEBUG=false
APP_URL=https://school.example.dz

# Mode SaaS ou Single School
APP_SAAS=false

# ============================================
# BASE DE DONNÉES
# ============================================
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=onestschooled
DB_USERNAME=school_user
DB_PASSWORD=secure_password

# ============================================
# CACHE & SESSION
# ============================================
CACHE_DRIVER=redis
SESSION_DRIVER=redis
QUEUE_CONNECTION=redis

# En mode single school sans Redis:
# CACHE_DRIVER=array
# SESSION_DRIVER=file
# QUEUE_CONNECTION=sync

# ============================================
# REDIS
# ============================================
REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379

# ============================================
# MAIL
# ============================================
MAIL_MAILER=smtp
MAIL_HOST=smtp.mailgun.org
MAIL_PORT=587
MAIL_USERNAME=postmaster@school.example.dz
MAIL_PASSWORD=your_mail_password
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=no-reply@school.example.dz
MAIL_FROM_NAME="${APP_NAME}"

# ============================================
# PAIEMENTS (Chargily)
# ============================================
CHARGILY_APP_KEY=your_chargily_key
CHARGILY_APP_SECRET=your_chargily_secret
CHARGILY_MODE=live

# ============================================
# SMS (Optionnel)
# ============================================
SMS_PROVIDER=twilio
TWILIO_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_FROM=+213xxxxxxxxx

# ============================================
# NOTIFICATIONS
# ============================================
NOTIFICATION_JOB=sync
# Utiliser queue pour les notifications asynchrones:
# NOTIFICATION_JOB=queue

# ============================================
# LANGUE
# ============================================
APP_LOCALE=fr
APP_FALLBACK_LOCALE=en
APP_TIMEZONE=Africa/Algiers
```

### 7. Créer la Base de Données

```bash
# MySQL
mysql -u root -p
CREATE DATABASE onestschooled CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'school_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON onestschooled.* TO 'school_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# PostgreSQL
sudo -u postgres psql
CREATE DATABASE onestschooled;
CREATE USER school_user WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE onestschooled TO school_user;
\q
```

### 8. Exécuter les Migrations

#### Mode Single School (Une école)

```bash
# Migrations pour une seule école
php artisan migrate:fresh --seed --path=database/migrations/tenant
```

#### Mode SaaS (Multi-écoles)

```bash
# Migrations pour le mode SaaS
php artisan migrate:fresh --path=modules/MainApp/database/migrations
php artisan module:seed MainApp
```

### 9. Configurer le Serveur Web

#### Apache

```apache
<VirtualHost *:80>
    ServerName school.example.dz
    DocumentRoot /var/www/onestschooled/public

    <Directory /var/www/onestschooled/public>
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/school_error.log
    CustomLog ${APACHE_LOG_DIR}/school_access.log combined
</VirtualHost>
```

```bash
sudo a2ensite onestschooled.conf
sudo a2enmod rewrite
sudo systemctl restart apache2
```

#### Nginx

```nginx
server {
    listen 80;
    server_name school.example.dz;
    root /var/www/onestschooled/public;

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";

    index index.php;

    charset utf-8;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    error_page 404 /index.php;

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/onestschooled /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 10. SSL avec Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d school.example.dz
```

---

## Installation Docker

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: onestschooled-app
    restart: unless-stopped
    working_dir: /var/www
    volumes:
      - .:/var/www
      - ./docker/php/local.ini:/usr/local/etc/php/conf.d/local.ini
    networks:
      - school-network
    depends_on:
      - db
      - redis

  nginx:
    image: nginx:alpine
    container_name: onestschooled-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - .:/var/www
      - ./docker/nginx/conf.d:/etc/nginx/conf.d
      - ./docker/nginx/ssl:/etc/nginx/ssl
    networks:
      - school-network
    depends_on:
      - app

  db:
    image: mysql:8.0
    container_name: onestschooled-db
    restart: unless-stopped
    environment:
      MYSQL_DATABASE: ${DB_DATABASE}
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_USER: ${DB_USERNAME}
    volumes:
      - dbdata:/var/lib/mysql
    networks:
      - school-network
    ports:
      - "3307:3306"

  redis:
    image: redis:alpine
    container_name: onestschooled-redis
    restart: unless-stopped
    networks:
      - school-network

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: onestschooled-phpmyadmin
    restart: unless-stopped
    environment:
      PMA_HOST: db
      PMA_PORT: 3306
    ports:
      - "8080:80"
    networks:
      - school-network
    depends_on:
      - db

networks:
  school-network:
    driver: bridge

volumes:
  dbdata:
```

### Dockerfile

```dockerfile
FROM php:8.1-fpm

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpng-dev \
    libjpeg62-turbo-dev \
    libfreetype6-dev \
    locales \
    zip \
    jpegoptim optipng pngquant gifsicle \
    vim \
    unzip \
    git \
    curl \
    libzip-dev \
    libonig-dev

# Clear cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install extensions
RUN docker-php-ext-install pdo_mysql mbstring zip exif pcntl
RUN docker-php-ext-configure gd --with-freetype --with-jpeg
RUN docker-php-ext-install gd

# Install composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Set working directory
WORKDIR /var/www

# Copy existing application
COPY . .

# Install dependencies
RUN composer install --optimize-autoloader --no-dev

# Set permissions
RUN chown -R www-data:www-data /var/www/storage /var/www/bootstrap/cache

EXPOSE 9000
CMD ["php-fpm"]
```

### Lancement Docker

```bash
# Construire et démarrer
docker-compose up -d --build

# Migrations
docker-compose exec app php artisan migrate --seed

# Logs
docker-compose logs -f
```

---

## Vérification de l'Installation

### 1. Vérifier l'État de l'Application

```bash
# Vérifier les migrations
php artisan migrate:status

# Vérifier les routes
php artisan route:list

# Vérifier la configuration
php artisan config:cache
```

### 2. Créer le Premier Administrateur

```bash
php artisan tinker
>>> \App\Models\User::create([
...     'name' => 'Admin',
...     'email' => 'admin@school.dz',
...     'password' => bcrypt('password'),
...     'role_id' => 1
... ]);
```

### 3. Accéder à l'Application

- **URL:** https://school.example.dz
- **Email:** admin@school.dz
- **Mot de passe:** password

---

## Post-Installation

### Configurer les Tâches Planifiées

```bash
# Ajouter au crontab
crontab -e

# Ajouter cette ligne
* * * * * cd /var/www/onestschooled && php artisan schedule:run >> /dev/null 2>&1
```

### Configurer le Worker de Queue

```bash
# Avec Supervisor
sudo apt install supervisor

# Créer /etc/supervisor/conf.d/laravel-worker.conf
[program:laravel-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /var/www/onestschooled/artisan queue:work redis --sleep=3 --tries=3
autostart=true
autorestart=true
user=www-data
numprocs=2
redirect_stderr=true
stdout_logfile=/var/www/onestschooled/storage/logs/worker.log

# Démarrer
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start laravel-worker:*
```

---

## Troubleshooting Installation

| Problème | Solution |
|----------|----------|
| Permission denied | `sudo chown -R www-data:www-data storage bootstrap/cache` |
| 500 Error | Vérifier `storage/logs/laravel.log` |
| Class not found | `composer dump-autoload` |
| Migration failed | Vérifier les credentials DB dans `.env` |
| Assets manquants | `npm run dev` ou `npm run production` |
| Session issues | `php artisan config:clear && php artisan cache:clear` |
