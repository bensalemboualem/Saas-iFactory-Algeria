#!/bin/bash
set -euo pipefail

###############################################################################
# Déploiement IAFactory RAG-DZ sur Serveur Hetzner Existant
# Serveur: iafactorysuisse (46.224.3.125)
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
SERVER_IP="46.224.3.125"
SERVER_USER="root"
DOMAIN="www.iafactoryalgeria.com"
EMAIL="admin@iafactoryalgeria.com"

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  IAFactory RAG-DZ - Déploiement sur Serveur Existant         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
log_info "Serveur: $SERVER_IP (iafactorysuisse)"
log_info "Domaine: $DOMAIN"
echo ""

# Étape 1: Tester la connexion SSH
log_info "Test de connexion SSH..."
if ssh -o ConnectTimeout=10 -o BatchMode=yes $SERVER_USER@$SERVER_IP "echo OK" &>/dev/null; then
    log_success "Connexion SSH OK"
else
    log_error "Impossible de se connecter via SSH"
    echo ""
    echo "Vérifiez que:"
    echo "1. Votre clé SSH est configurée sur Hetzner"
    echo "2. Vous pouvez vous connecter manuellement: ssh root@$SERVER_IP"
    echo ""
    exit 1
fi

# Étape 2: Créer l'archive du projet
log_info "Création de l'archive du projet..."
tar czf /tmp/iafactory-deploy.tar.gz \
    --exclude='node_modules' \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='data' \
    --exclude='*.tar.gz' \
    -C "$(pwd)" \
    backend/ \
    frontend/ \
    bolt-diy/ \
    scripts/ \
    docker-compose.prod.yml \
    .env.prod.example

log_success "Archive créée: /tmp/iafactory-deploy.tar.gz"

# Étape 3: Copier l'archive sur le serveur
log_info "Copie de l'archive sur le serveur..."
scp -q /tmp/iafactory-deploy.tar.gz $SERVER_USER@$SERVER_IP:/tmp/
log_success "Archive copiée"

# Étape 4: Extraction et installation sur le serveur
log_info "Installation sur le serveur..."

ssh $SERVER_USER@$SERVER_IP << 'ENDSSH'
set -e

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Installation sur le Serveur"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Extraire l'archive
cd /tmp
mkdir -p iafactory-temp
tar xzf iafactory-deploy.tar.gz -C iafactory-temp

# Créer le répertoire de destination
mkdir -p /opt/iafactory

# Copier les fichiers
cp -r iafactory-temp/* /opt/iafactory/
rm -rf iafactory-temp iafactory-deploy.tar.gz

cd /opt/iafactory

# Rendre les scripts exécutables
chmod +x scripts/*.sh

echo "✓ Fichiers copiés dans /opt/iafactory"

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo ""
    echo "📦 Installation de Docker..."

    # Mettre à jour le système
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -y -qq ca-certificates curl gnupg lsb-release

    # Ajouter le repository Docker
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

    apt-get update -qq
    apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    systemctl enable docker
    systemctl start docker

    echo "✓ Docker installé"
else
    echo "✓ Docker déjà installé"
fi

# Créer le fichier .env s'il n'existe pas
if [ ! -f .env ]; then
    echo ""
    echo "📝 Création du fichier .env..."
    cp .env.prod.example .env

    # Générer des mots de passe sécurisés
    POSTGRES_PASSWORD=$(openssl rand -base64 32)
    REDIS_PASSWORD=$(openssl rand -base64 32)
    JWT_SECRET=$(openssl rand -hex 32)
    RAG_API_KEY=$(openssl rand -hex 32)
    API_SECRET=$(openssl rand -hex 32)

    # Remplacer dans .env
    sed -i "s|POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=$POSTGRES_PASSWORD|" .env
    sed -i "s|REDIS_PASSWORD=.*|REDIS_PASSWORD=$REDIS_PASSWORD|" .env
    sed -i "s|JWT_SECRET_KEY=.*|JWT_SECRET_KEY=$JWT_SECRET|" .env
    sed -i "s|RAG_API_KEY=.*|RAG_API_KEY=$RAG_API_KEY|" .env
    sed -i "s|API_SECRET_KEY=.*|API_SECRET_KEY=$API_SECRET|" .env
    sed -i "s|DOMAIN=.*|DOMAIN=www.iafactoryalgeria.com|" .env
    sed -i "s|EMAIL=.*|EMAIL=admin@iafactoryalgeria.com|" .env

    echo "✓ Fichier .env créé avec mots de passe sécurisés"
    echo ""
    echo "⚠️  IMPORTANT: Ajoutez vos API keys dans /opt/iafactory/.env"
    echo "   nano /opt/iafactory/.env"
    echo ""
    echo "   Minimum requis (gratuit):"
    echo "   GROQ_API_KEY=gsk_...    # https://console.groq.com/keys"
fi

# Démarrer les services Docker
echo ""
echo "🐳 Démarrage des services Docker..."
docker-compose -f docker-compose.prod.yml pull -q
docker-compose -f docker-compose.prod.yml up -d

echo ""
echo "⏳ Attente du démarrage des services (30s)..."
sleep 30

# Vérifier l'état
echo ""
echo "📊 État des services:"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  ✓ Installation Terminée"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "🌐 Services accessibles:"
echo "   Hub:     http://46.224.3.125:8182"
echo "   API:     http://46.224.3.125:8180"
echo "   Docs:    http://46.224.3.125:8183"
echo "   Studio:  http://46.224.3.125:8184"
echo "   n8n:     http://46.224.3.125:8185"
echo ""
echo "🔑 Prochaines étapes:"
echo "   1. Configurer les API keys:"
echo "      nano /opt/iafactory/.env"
echo ""
echo "   2. Redémarrer après modification:"
echo "      docker-compose -f /opt/iafactory/docker-compose.prod.yml restart"
echo ""
echo "   3. Configurer Nginx + SSL (optionnel):"
echo "      cd /opt/iafactory"
echo "      export DOMAIN=www.iafactoryalgeria.com"
echo "      export EMAIL=admin@iafactoryalgeria.com"
echo "      bash scripts/configure-nginx.sh"
echo ""
echo "═══════════════════════════════════════════════════════════════"

ENDSSH

log_success "Installation terminée!"

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  Déploiement Réussi!                                          ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 URLs d'accès:"
echo "   Hub:     http://46.224.3.125:8182"
echo "   API:     http://46.224.3.125:8180"
echo "   Docs:    http://46.224.3.125:8183"
echo "   Studio:  http://46.224.3.125:8184"
echo "   n8n:     http://46.224.3.125:8185"
echo ""
echo "🔐 Connexion SSH:"
echo "   ssh root@46.224.3.125"
echo ""
echo "📝 Configuration:"
echo "   1. Connectez-vous au serveur:"
echo "      ssh root@46.224.3.125"
echo ""
echo "   2. Éditez /opt/iafactory/.env et ajoutez votre clé Groq:"
echo "      nano /opt/iafactory/.env"
echo "      # Ajoutez: GROQ_API_KEY=gsk_..."
echo ""
echo "   3. Redémarrez les services:"
echo "      cd /opt/iafactory"
echo "      docker-compose -f docker-compose.prod.yml restart"
echo ""
echo "   4. (Optionnel) Configurez Nginx + SSL pour www.iafactoryalgeria.com:"
echo "      cd /opt/iafactory"
echo "      export DOMAIN=www.iafactoryalgeria.com"
echo "      export EMAIL=admin@iafactoryalgeria.com"
echo "      bash scripts/configure-nginx.sh"
echo ""
echo "═══════════════════════════════════════════════════════════════"
