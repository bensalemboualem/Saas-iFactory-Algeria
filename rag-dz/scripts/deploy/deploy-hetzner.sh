#!/bin/bash
set -euo pipefail

###############################################################################
# Script de Déploiement Automatique - IAFactory RAG-DZ sur Hetzner Cloud
# Version: 1.0.0
# Date: 2025-11-24
###############################################################################

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
HETZNER_API_TOKEN="${HETZNER_API_TOKEN:-}"
SERVER_NAME="iafactory-prod-01"
SERVER_TYPE="cx41"  # 4 vCPU, 16GB RAM
SERVER_LOCATION="nbg1"  # Nuremberg
SERVER_IMAGE="ubuntu-22.04"
DOMAIN="${DOMAIN:-}"
EMAIL="${EMAIL:-}"

# Fonctions utilitaires
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

check_requirements() {
    log_info "Vérification des prérequis..."

    # Vérifier hcloud CLI
    if ! command -v hcloud &> /dev/null; then
        log_error "hcloud CLI n'est pas installé"
        echo ""
        echo "Installation:"
        echo "  macOS:   brew install hcloud"
        echo "  Linux:   wget -O hcloud.tar.gz https://github.com/hetznercloud/cli/releases/latest/download/hcloud-linux-amd64.tar.gz && tar -xvf hcloud.tar.gz && sudo mv hcloud /usr/local/bin/"
        echo "  Windows: scoop install hcloud"
        exit 1
    fi

    # Vérifier le token
    if [ -z "$HETZNER_API_TOKEN" ]; then
        log_error "HETZNER_API_TOKEN n'est pas défini"
        echo ""
        echo "Obtenez votre token API sur: https://console.hetzner.com/projects"
        echo "Puis exportez-le:"
        echo "  export HETZNER_API_TOKEN='your_token_here'"
        exit 1
    fi

    # Vérifier le domaine
    if [ -z "$DOMAIN" ]; then
        log_warning "DOMAIN n'est pas défini - SSL automatique sera désactivé"
        echo "Pour activer SSL, exportez votre domaine:"
        echo "  export DOMAIN='iafactory.example.com'"
    fi

    # Vérifier l'email
    if [ -z "$EMAIL" ]; then
        log_warning "EMAIL n'est pas défini - requis pour Let's Encrypt"
        echo "  export EMAIL='admin@example.com'"
    fi

    log_success "Prérequis OK"
}

create_ssh_key() {
    log_info "Création de la clé SSH..."

    if ! hcloud ssh-key list | grep -q "iafactory-deploy"; then
        if [ ! -f ~/.ssh/iafactory_deploy ]; then
            ssh-keygen -t ed25519 -f ~/.ssh/iafactory_deploy -N "" -C "iafactory-deploy"
        fi
        hcloud ssh-key create --name iafactory-deploy --public-key-from-file ~/.ssh/iafactory_deploy.pub
        log_success "Clé SSH créée"
    else
        log_success "Clé SSH existe déjà"
    fi
}

create_server() {
    log_info "Création du serveur Hetzner..."

    # Vérifier si le serveur existe déjà
    if hcloud server list | grep -q "$SERVER_NAME"; then
        log_warning "Le serveur $SERVER_NAME existe déjà"
        read -p "Voulez-vous le supprimer et recréer? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log_info "Suppression du serveur existant..."
            hcloud server delete "$SERVER_NAME"
            sleep 5
        else
            log_info "Utilisation du serveur existant"
            SERVER_IP=$(hcloud server ip "$SERVER_NAME")
            return 0
        fi
    fi

    # Créer le serveur
    log_info "Création d'un nouveau serveur $SERVER_TYPE à $SERVER_LOCATION..."
    hcloud server create \
        --name "$SERVER_NAME" \
        --type "$SERVER_TYPE" \
        --location "$SERVER_LOCATION" \
        --image "$SERVER_IMAGE" \
        --ssh-key iafactory-deploy

    # Récupérer l'IP
    SERVER_IP=$(hcloud server ip "$SERVER_NAME")
    log_success "Serveur créé avec l'IP: $SERVER_IP"

    # Attendre que le serveur soit prêt
    log_info "Attente du démarrage du serveur (30s)..."
    sleep 30
}

configure_server() {
    log_info "Configuration du serveur..."

    # Copier les scripts de configuration
    scp -i ~/.ssh/iafactory_deploy -o StrictHostKeyChecking=no \
        ./scripts/setup-server.sh \
        root@$SERVER_IP:/root/

    # Exécuter la configuration
    ssh -i ~/.ssh/iafactory_deploy -o StrictHostKeyChecking=no \
        root@$SERVER_IP 'bash /root/setup-server.sh'

    log_success "Serveur configuré"
}

deploy_application() {
    log_info "Déploiement de l'application..."

    # Créer le répertoire de déploiement
    ssh -i ~/.ssh/iafactory_deploy root@$SERVER_IP 'mkdir -p /opt/iafactory'

    # Copier les fichiers
    log_info "Transfert des fichiers..."
    rsync -avz -e "ssh -i ~/.ssh/iafactory_deploy" \
        --exclude='node_modules' \
        --exclude='.git' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='.env*' \
        --exclude='data' \
        ./ root@$SERVER_IP:/opt/iafactory/

    # Copier la configuration production
    scp -i ~/.ssh/iafactory_deploy \
        docker-compose.prod.yml root@$SERVER_IP:/opt/iafactory/docker-compose.yml

    # Créer le fichier .env
    log_info "Configuration des variables d'environnement..."
    ssh -i ~/.ssh/iafactory_deploy root@$SERVER_IP << 'EOF'
cd /opt/iafactory
cat > .env << 'ENVEOF'
# Database
POSTGRES_USER=iafactory_admin
POSTGRES_PASSWORD=$(openssl rand -base64 32)
POSTGRES_DB=iafactory_prod

# Redis
REDIS_PASSWORD=$(openssl rand -base64 32)

# API Keys
RAG_API_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)

# URLs
BACKEND_URL=http://iafactory-backend:8180
FRONTEND_URL=https://${DOMAIN:-localhost}

# AI Providers (à compléter)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GROQ_API_KEY=
ABACUS_API_KEY=

# Email (optionnel)
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM=

# Twilio (optionnel)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
ENVEOF
EOF

    # Démarrer les services
    log_info "Démarrage des services Docker..."
    ssh -i ~/.ssh/iafactory_deploy root@$SERVER_IP << 'EOF'
cd /opt/iafactory
docker-compose pull
docker-compose up -d
EOF

    log_success "Application déployée"
}

configure_nginx() {
    log_info "Configuration Nginx et SSL..."

    if [ -n "$DOMAIN" ] && [ -n "$EMAIL" ]; then
        ssh -i ~/.ssh/iafactory_deploy root@$SERVER_IP << EOF
# Installer Certbot
apt-get install -y certbot python3-certbot-nginx

# Créer la configuration Nginx
cat > /etc/nginx/sites-available/iafactory << 'NGINXEOF'
server {
    listen 80;
    server_name $DOMAIN;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://\\\$server_name\\\$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN;

    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;

    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Hub UI
    location / {
        proxy_pass http://localhost:8182;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \\\$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \\\$host;
        proxy_cache_bypass \\\$http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8180;
        proxy_http_version 1.1;
        proxy_set_header X-Real-IP \\\$remote_addr;
        proxy_set_header X-Forwarded-For \\\$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \\\$scheme;
    }

    # RAG Docs
    location /docs {
        proxy_pass http://localhost:8183;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \\\$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \\\$host;
        proxy_cache_bypass \\\$http_upgrade;
    }

    # Bolt Studio
    location /studio {
        proxy_pass http://localhost:8184;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \\\$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \\\$host;
        proxy_cache_bypass \\\$http_upgrade;
    }

    # n8n Automation
    location /automation {
        proxy_pass http://localhost:8185;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \\\$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \\\$host;
        proxy_cache_bypass \\\$http_upgrade;
    }
}
NGINXEOF

# Activer le site
ln -sf /etc/nginx/sites-available/iafactory /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Tester la configuration
nginx -t

# Obtenir le certificat SSL
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email $EMAIL

# Recharger Nginx
systemctl reload nginx
EOF
        log_success "Nginx et SSL configurés pour $DOMAIN"
    else
        log_warning "Configuration Nginx/SSL ignorée (DOMAIN ou EMAIL manquant)"
    fi
}

setup_monitoring() {
    log_info "Configuration du monitoring..."

    ssh -i ~/.ssh/iafactory_deploy root@$SERVER_IP << 'EOF'
cd /opt/iafactory

# Créer un script de monitoring
cat > /usr/local/bin/iafactory-health.sh << 'HEALTHEOF'
#!/bin/bash
cd /opt/iafactory
docker-compose ps --format json | jq -r '.[] | "\(.Service): \(.State)"'
HEALTHEOF

chmod +x /usr/local/bin/iafactory-health.sh

# Créer un script de backup quotidien
cat > /usr/local/bin/iafactory-backup.sh << 'BACKUPEOF'
#!/bin/bash
BACKUP_DIR="/backup/iafactory"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker exec iaf-dz-postgres pg_dump -U iafactory_admin iafactory_prod | gzip > $BACKUP_DIR/postgres_$DATE.sql.gz

# Backup Qdrant
docker exec iaf-dz-qdrant tar czf - /qdrant/storage > $BACKUP_DIR/qdrant_$DATE.tar.gz

# Garder seulement les 7 derniers backups
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
BACKUPEOF

chmod +x /usr/local/bin/iafactory-backup.sh

# Ajouter au crontab
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/iafactory-backup.sh >> /var/log/iafactory-backup.log 2>&1") | crontab -

echo "Monitoring configuré"
EOF

    log_success "Monitoring configuré"
}

display_summary() {
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    log_success "Déploiement Terminé!"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "📡 IP du Serveur: $SERVER_IP"
    echo "🖥️  Type: $SERVER_TYPE ($SERVER_LOCATION)"
    echo ""

    if [ -n "$DOMAIN" ]; then
        echo "🌐 URLs d'Accès:"
        echo "   Hub:        https://$DOMAIN"
        echo "   API:        https://$DOMAIN/api"
        echo "   Docs:       https://$DOMAIN/docs"
        echo "   Studio:     https://$DOMAIN/studio"
        echo "   Automation: https://$DOMAIN/automation"
    else
        echo "🌐 URLs d'Accès (HTTP):"
        echo "   Hub:        http://$SERVER_IP:8182"
        echo "   API:        http://$SERVER_IP:8180"
        echo "   Docs:       http://$SERVER_IP:8183"
        echo "   Studio:     http://$SERVER_IP:8184"
        echo "   Automation: http://$SERVER_IP:8185"
    fi

    echo ""
    echo "🔐 Connexion SSH:"
    echo "   ssh -i ~/.ssh/iafactory_deploy root@$SERVER_IP"
    echo ""
    echo "📊 Vérifier l'état:"
    echo "   ssh -i ~/.ssh/iafactory_deploy root@$SERVER_IP '/usr/local/bin/iafactory-health.sh'"
    echo ""
    echo "⚙️  Configuration:"
    echo "   Éditez /opt/iafactory/.env sur le serveur pour configurer les API keys"
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
}

main() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║  IAFactory RAG-DZ - Déploiement Automatique Hetzner Cloud    ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""

    check_requirements

    # Configurer hcloud
    hcloud context create iafactory || true
    hcloud context use iafactory

    create_ssh_key
    create_server
    configure_server
    deploy_application
    configure_nginx
    setup_monitoring
    display_summary
}

# Exécuter
main "$@"
