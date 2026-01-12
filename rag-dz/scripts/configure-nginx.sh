#!/bin/bash
set -euo pipefail

###############################################################################
# Script de Configuration Nginx avec SSL pour IAFactory RAG-DZ
# Domaine: www.iafactoryalgeria.com
###############################################################################

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }

# Configuration
DOMAIN="${DOMAIN:-www.iafactoryalgeria.com}"
EMAIL="${EMAIL:-admin@iafactoryalgeria.com}"
NGINX_SITE_CONFIG="/etc/nginx/sites-available/iafactory"
NGINX_ENABLED="/etc/nginx/sites-enabled/iafactory"

main() {
    log_info "Configuration de Nginx pour $DOMAIN..."

    # Vérifier que Nginx est installé
    if ! command -v nginx &> /dev/null; then
        log_error "Nginx n'est pas installé"
        exit 1
    fi

    # Créer la configuration Nginx
    log_info "Création de la configuration Nginx..."
    cat > $NGINX_SITE_CONFIG << 'EOF'
# =============================================================================
# IAFactory RAG-DZ - Configuration Nginx
# Domaine: www.iafactoryalgeria.com
# =============================================================================

# Redirection HTTP vers HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name www.iafactoryalgeria.com iafactoryalgeria.com;

    # Let's Encrypt ACME challenge
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    # Redirect all other traffic to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# Configuration HTTPS
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name www.iafactoryalgeria.com iafactoryalgeria.com;

    # SSL Certificates (will be configured by Certbot)
    ssl_certificate /etc/letsencrypt/live/www.iafactoryalgeria.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/www.iafactoryalgeria.com/privkey.pem;

    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_stapling on;
    ssl_stapling_verify on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Logs
    access_log /var/log/nginx/iafactory-access.log;
    error_log /var/log/nginx/iafactory-error.log;

    # Max body size for file uploads
    client_max_body_size 50M;

    # =================================================================
    # FRONTEND - Archon Hub (Dashboard Principal)
    # =================================================================
    location / {
        proxy_pass http://localhost:8182;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # =================================================================
    # BACKEND API
    # =================================================================
    location /api {
        proxy_pass http://localhost:8180;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;

        # CORS headers for API
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization,X-API-Key' always;

        # Handle preflight
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization,X-API-Key';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }
    }

    # =================================================================
    # RAG DOCS UI (Upload & Documents)
    # =================================================================
    location /docs {
        proxy_pass http://localhost:8183;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
    }

    # =================================================================
    # BOLT STUDIO (Génération de code)
    # =================================================================
    location /studio {
        proxy_pass http://localhost:8184;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
    }

    # =================================================================
    # N8N AUTOMATION
    # =================================================================
    location /automation {
        proxy_pass http://localhost:8185;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
    }

    # =================================================================
    # HEALTH CHECK
    # =================================================================
    location /health {
        proxy_pass http://localhost:8180/health;
        access_log off;
    }

    # =================================================================
    # STATIC FILES CACHING
    # =================================================================
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        proxy_pass http://localhost:8182;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

    log_success "Configuration Nginx créée"

    # Activer le site
    log_info "Activation du site..."
    rm -f /etc/nginx/sites-enabled/default
    ln -sf $NGINX_SITE_CONFIG $NGINX_ENABLED
    log_success "Site activé"

    # Tester la configuration
    log_info "Test de la configuration Nginx..."
    if nginx -t; then
        log_success "Configuration Nginx valide"
    else
        log_error "Configuration Nginx invalide"
        exit 1
    fi

    # Installer Certbot si nécessaire
    if ! command -v certbot &> /dev/null; then
        log_info "Installation de Certbot..."
        apt-get install -y certbot python3-certbot-nginx
        log_success "Certbot installé"
    fi

    # Obtenir le certificat SSL
    log_info "Obtention du certificat SSL pour $DOMAIN..."
    log_warning "Assurez-vous que le domaine $DOMAIN pointe vers ce serveur!"
    read -p "Appuyez sur Entrée pour continuer ou Ctrl+C pour annuler..."

    certbot --nginx \
        -d $DOMAIN \
        -d iafactoryalgeria.com \
        --non-interactive \
        --agree-tos \
        --email $EMAIL \
        --redirect

    if [ $? -eq 0 ]; then
        log_success "Certificat SSL obtenu avec succès"
    else
        log_error "Échec de l'obtention du certificat SSL"
        log_warning "Vérifiez que:"
        log_warning "  1. Le domaine pointe vers ce serveur"
        log_warning "  2. Les ports 80 et 443 sont ouverts"
        log_warning "  3. Le firewall autorise le trafic HTTP/HTTPS"
        exit 1
    fi

    # Recharger Nginx
    log_info "Rechargement de Nginx..."
    systemctl reload nginx
    log_success "Nginx rechargé"

    # Configurer le renouvellement automatique
    log_info "Configuration du renouvellement automatique..."
    (crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet --post-hook 'systemctl reload nginx'") | crontab -
    log_success "Renouvellement automatique configuré"

    # Afficher le résumé
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    log_success "Configuration Nginx Terminée!"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "🌐 URLs d'Accès:"
    echo "   Hub:        https://$DOMAIN"
    echo "   API:        https://$DOMAIN/api"
    echo "   Docs:       https://$DOMAIN/docs"
    echo "   Studio:     https://$DOMAIN/studio"
    echo "   Automation: https://$DOMAIN/automation"
    echo ""
    echo "🔒 SSL:"
    echo "   Certificat: Installé et valide"
    echo "   Renouvellement: Automatique (tous les jours à 3h)"
    echo ""
    echo "📊 Logs:"
    echo "   Access: /var/log/nginx/iafactory-access.log"
    echo "   Error:  /var/log/nginx/iafactory-error.log"
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
}

# Exécution
main "$@"
