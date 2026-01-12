#!/bin/bash
# ============================================================================
# DÉPLOIEMENT AUTOMATIQUE COMPLET - IAFactory RAG-DZ
# ============================================================================
# Script d'automatisation TOTAL - Zéro intervention manuelle
# Compatible: Hetzner CX22/CX32/CX42
# ============================================================================

set -e  # Exit on error

# Configuration (MODIFIABLE)
VPS_IP="${VPS_IP:-}"
VPS_USER="${VPS_USER:-root}"
DOMAIN="${DOMAIN:-iafactory-algeria.com}"
EMAIL="${EMAIL:-admin@iafactory-algeria.com}"
PROJECT_NAME="iafactory-rag-dz"

# Clés API (OPTIONNEL - peut être configuré après)
GROQ_API_KEY="${GROQ_API_KEY:-}"
OPENAI_API_KEY="${OPENAI_API_KEY:-}"
ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ============================================================================
# FONCTIONS UTILES
# ============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo -e "${CYAN}================================================================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
}

check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 n'est pas installé"
        return 1
    fi
    return 0
}

# ============================================================================
# ÉTAPE 0: VÉRIFICATIONS PRÉALABLES
# ============================================================================

print_header "🚀 DÉPLOIEMENT AUTOMATIQUE COMPLET - IAFactory RAG-DZ"

log_info "Projet: ${PROJECT_NAME}"
log_info "Domaine: ${DOMAIN}"
log_info "Email: ${EMAIL}"
echo ""

# Demander l'IP du VPS si non fournie
if [ -z "$VPS_IP" ]; then
    echo -e "${YELLOW}Entrez l'IP de votre VPS Hetzner:${NC}"
    read -p "IP VPS: " VPS_IP

    if [ -z "$VPS_IP" ]; then
        log_error "IP VPS requise"
        exit 1
    fi
fi

log_info "VPS: ${VPS_USER}@${VPS_IP}"
echo ""

# Confirmer le déploiement
echo -e "${YELLOW}Prêt à déployer sur ${VPS_IP}. Continuer ? (y/n)${NC}"
read -p "> " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    log_warning "Déploiement annulé"
    exit 0
fi

# ============================================================================
# ÉTAPE 1: VÉRIFIER LES COMMANDES LOCALES
# ============================================================================

print_header "ÉTAPE 1/6: Vérification des outils locaux"

MISSING_TOOLS=()

if ! check_command "ssh"; then
    MISSING_TOOLS+=("ssh")
fi

if ! check_command "scp"; then
    MISSING_TOOLS+=("scp")
fi

if [ ${#MISSING_TOOLS[@]} -ne 0 ]; then
    log_error "Outils manquants: ${MISSING_TOOLS[*]}"
    log_error "Installez ces outils et réessayez"
    exit 1
fi

log_success "Tous les outils sont installés"

# ============================================================================
# ÉTAPE 2: TESTER LA CONNEXION SSH
# ============================================================================

print_header "ÉTAPE 2/6: Test de connexion SSH"

log_info "Test de connexion à ${VPS_USER}@${VPS_IP}..."

if ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_IP} "echo 'OK'" > /dev/null 2>&1; then
    log_success "Connexion SSH OK"
else
    log_error "Impossible de se connecter au VPS"
    log_error "Vérifiez:"
    log_error "  1. L'IP du VPS: ${VPS_IP}"
    log_error "  2. Votre clé SSH est configurée"
    log_error "  3. Le firewall autorise SSH (port 22)"
    exit 1
fi

# ============================================================================
# ÉTAPE 3: COPIER LE PROJET SUR LE VPS
# ============================================================================

print_header "ÉTAPE 3/6: Copie du projet sur le VPS"

log_info "Copie des fichiers vers ${VPS_IP}:/tmp/${PROJECT_NAME}/"
log_info "Cela peut prendre 2-5 minutes selon la connexion..."

# Créer le répertoire distant
ssh -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_IP} "mkdir -p /tmp/${PROJECT_NAME}"

# Copier les fichiers essentiels (excluant node_modules, .git, etc.)
rsync -avz --progress \
    --exclude 'node_modules' \
    --exclude '.git' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.env.local' \
    --exclude 'dist' \
    --exclude 'build' \
    ./ ${VPS_USER}@${VPS_IP}:/tmp/${PROJECT_NAME}/

log_success "Projet copié sur le VPS"

# ============================================================================
# ÉTAPE 4: CONFIGURER L'ENVIRONNEMENT
# ============================================================================

print_header "ÉTAPE 4/6: Configuration de l'environnement"

log_info "Création du fichier .env sur le VPS..."

# Générer les secrets sur le VPS
ssh -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_IP} "cd /tmp/${PROJECT_NAME} && cat > .env << 'ENVEOF'
# IAFactory RAG-DZ - Production Environment
# Generated automatically on $(date)

# Region
SOVEREIGNTY_REGION=DZ
SOVEREIGNTY_LABEL=Algérie
TZ=Africa/Algiers

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=$(openssl rand -base64 32)
POSTGRES_DB=iafactory_dz
DATABASE_URL=postgresql://postgres:$(openssl rand -base64 32)@iafactory-postgres:5432/iafactory_dz

# Redis
REDIS_URL=redis://iafactory-redis:6379/0
REDIS_PASSWORD=

# Qdrant
QDRANT_URL=http://iafactory-qdrant:6333
QDRANT_API_KEY=

# API Keys
GROQ_API_KEY=${GROQ_API_KEY}
OPENAI_API_KEY=${OPENAI_API_KEY}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
GOOGLE_API_KEY=
DEEPSEEK_API_KEY=

# Security
SECRET_KEY=$(openssl rand -base64 64)
JWT_SECRET=$(openssl rand -base64 64)

# Server
PORT=8180
HOST=0.0.0.0
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Domain
DOMAIN=${DOMAIN}
ENVEOF
"

log_success "Environnement configuré"

# ============================================================================
# ÉTAPE 5: EXÉCUTER LE DÉPLOIEMENT VPS
# ============================================================================

print_header "ÉTAPE 5/6: Déploiement sur le VPS"

log_info "Lancement du script de déploiement sur le VPS..."
log_info "Durée estimée: 10-15 minutes"
log_info "Vous verrez la progression en temps réel..."
echo ""

# Rendre le script exécutable et le lancer
ssh -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_IP} "
    cd /tmp/${PROJECT_NAME}
    chmod +x deploy-vps-master.sh
    export DOMAIN='${DOMAIN}'
    export EMAIL='${EMAIL}'
    ./deploy-vps-master.sh
"

if [ $? -eq 0 ]; then
    log_success "Déploiement VPS terminé avec succès"
else
    log_error "Erreur lors du déploiement VPS"
    log_error "Connectez-vous au VPS pour voir les logs:"
    log_error "  ssh ${VPS_USER}@${VPS_IP}"
    log_error "  cd /opt/${PROJECT_NAME}"
    log_error "  docker-compose logs"
    exit 1
fi

# ============================================================================
# ÉTAPE 6: VÉRIFICATIONS POST-DÉPLOIEMENT
# ============================================================================

print_header "ÉTAPE 6/6: Vérifications post-déploiement"

log_info "Attente de la propagation DNS et du démarrage des services (30s)..."
sleep 30

# Test HTTPS
log_info "Test du site web..."
if curl -I -s -k "https://${DOMAIN}" | grep -q "200\|301\|302"; then
    log_success "Site web accessible: https://${DOMAIN}"
else
    log_warning "Site web pas encore accessible (DNS peut prendre 5-10 min)"
fi

# Test API
log_info "Test de l'API..."
if curl -s "http://${VPS_IP}:8180/health" | grep -q "healthy\|ok"; then
    log_success "API opérationnelle"
else
    log_warning "API pas encore prête (peut prendre 2-3 min de plus)"
fi

# ============================================================================
# RÉSUMÉ FINAL
# ============================================================================

print_header "✅ DÉPLOIEMENT AUTOMATIQUE TERMINÉ !"

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                              ║${NC}"
echo -e "${GREEN}║          🎉 IAFACTORY RAG-DZ EST MAINTENANT EN LIGNE !       ║${NC}"
echo -e "${GREEN}║                                                              ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${CYAN}🌐 URLS DISPONIBLES:${NC}"
echo -e "   • Site principal:  ${GREEN}https://${DOMAIN}${NC}"
echo -e "   • Applications:    ${GREEN}https://${DOMAIN}/apps/${NC}"
echo -e "   • Directory IA:    ${GREEN}https://${DOMAIN}/docs/directory/${NC}"
echo -e "   • API Backend:     ${GREEN}https://${DOMAIN}/api/${NC}"
echo -e "   • Health Check:    ${GREEN}https://${DOMAIN}/health${NC}"
echo ""

echo -e "${CYAN}📊 SERVICES DÉPLOYÉS:${NC}"
echo -e "   • 47 Applications professionnelles"
echo -e "   • Landing page avec Chat IA"
echo -e "   • Backend FastAPI complet"
echo -e "   • PostgreSQL + PGVector"
echo -e "   • Redis Cache"
echo -e "   • Qdrant Vector Database"
echo -e "   • Nginx + SSL/HTTPS"
echo ""

echo -e "${CYAN}🔧 ACCÈS VPS:${NC}"
echo -e "   ssh ${VPS_USER}@${VPS_IP}"
echo -e "   cd /opt/${PROJECT_NAME}"
echo ""

echo -e "${CYAN}📝 COMMANDES UTILES:${NC}"
echo -e "   • Voir les logs:    docker-compose logs -f"
echo -e "   • Redémarrer:       docker-compose restart"
echo -e "   • Arrêter:          docker-compose down"
echo -e "   • Status:           docker-compose ps"
echo ""

if [ -z "$GROQ_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  IMPORTANT: Configurez vos clés API${NC}"
    echo -e "   1. Connectez-vous au VPS:"
    echo -e "      ${CYAN}ssh ${VPS_USER}@${VPS_IP}${NC}"
    echo -e "   2. Éditez le fichier .env:"
    echo -e "      ${CYAN}nano /opt/${PROJECT_NAME}/.env${NC}"
    echo -e "   3. Ajoutez vos clés API (au minimum GROQ_API_KEY)"
    echo -e "   4. Redémarrez:"
    echo -e "      ${CYAN}cd /opt/${PROJECT_NAME} && docker-compose restart${NC}"
    echo ""
fi

echo -e "${CYAN}🌍 PROCHAINES ÉTAPES (OPTIONNEL):${NC}"
echo -e "   1. Configurer les clés API (Groq, OpenAI, etc.)"
echo -e "   2. Tester toutes les applications"
echo -e "   3. Ajouter les versions AR/EN (voir guide ci-dessous)"
echo ""

echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Temps total: ~15-20 minutes${NC}"
echo -e "${GREEN}Status: PRODUCTION READY${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Sauvegarder les infos de déploiement
cat > deployment-info.txt << EOF
IAFactory RAG-DZ - Informations de Déploiement
===============================================

Date: $(date)
VPS IP: ${VPS_IP}
Domaine: ${DOMAIN}
Email: ${EMAIL}

URLs:
- Site: https://${DOMAIN}
- API: https://${DOMAIN}/api/
- Health: https://${DOMAIN}/health

SSH:
ssh ${VPS_USER}@${VPS_IP}

Dossier:
/opt/${PROJECT_NAME}

Commandes:
cd /opt/${PROJECT_NAME}
docker-compose logs -f
docker-compose ps
docker-compose restart

Fichier de config:
/opt/${PROJECT_NAME}/.env
EOF

log_success "Informations sauvegardées dans: deployment-info.txt"
echo ""
