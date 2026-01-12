#!/usr/bin/env bash
# ==============================================
# 🚀 IAFactory RAG-DZ - Déploiement VPS Complet
# ==============================================
# Script d'installation automatique sur VPS
# Testé sur: Ubuntu 22.04, Debian 11, AlmaLinux 9
# ==============================================

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
DOMAIN="${DOMAIN:-www.iafactoryalgeria.com}"
EMAIL="${EMAIL:-admin@iafactoryalgeria.com}"
INSTALL_DIR="${INSTALL_DIR:-/opt/iafactory}"
GIT_REPO="${GIT_REPO:-https://github.com/votre-org/rag-dz.git}"
GIT_BRANCH="${GIT_BRANCH:-main}"
ENABLE_SSL="${ENABLE_SSL:-true}"
ENABLE_MONITORING="${ENABLE_MONITORING:-true}"
ENABLE_BACKUP="${ENABLE_BACKUP:-true}"

echo -e "${BLUE}==============================================\${NC}"
echo -e "${CYAN}🚀 IAFactory RAG-DZ - Déploiement VPS${NC}"
echo -e "${BLUE}==============================================\${NC}"
echo -e "${CYAN}Domaine: ${DOMAIN}${NC}"
echo -e "${CYAN}Email: ${EMAIL}${NC}"
echo -e "${CYAN}Répertoire: ${INSTALL_DIR}${NC}"
echo -e "${BLUE}==============================================\${NC}"

# Vérifier si root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Ce script doit être exécuté en tant que root${NC}"
    echo -e "${YELLOW}Utilisez: sudo ./deploy-vps-complete.sh${NC}"
    exit 1
fi

# Fonction: Détection du système
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
        VER=$VERSION_ID
    else
        echo -e "${RED}❌ Impossible de détecter le système d'exploitation${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ Système détecté: $OS $VER${NC}"
}

# Fonction: Installation des prérequis
install_prerequisites() {
    echo -e "${YELLOW}📦 Installation des prérequis...${NC}"

    if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]]; then
        apt-get update
        apt-get install -y \
            curl \
            wget \
            git \
            ufw \
            fail2ban \
            htop \
            nano \
            vim \
            jq \
            certbot \
            python3-certbot-nginx \
            ca-certificates \
            gnupg \
            lsb-release
    elif [[ "$OS" == "almalinux" ]] || [[ "$OS" == "rhel" ]] || [[ "$OS" == "centos" ]]; then
        yum install -y epel-release
        yum install -y \
            curl \
            wget \
            git \
            firewalld \
            fail2ban \
            htop \
            nano \
            vim \
            jq \
            certbot \
            python3-certbot-nginx \
            ca-certificates
    fi

    echo -e "${GREEN}✅ Prérequis installés${NC}"
}

# Fonction: Installation de Docker
install_docker() {
    echo -e "${YELLOW}🐳 Installation de Docker...${NC}"

    if command -v docker &> /dev/null; then
        echo -e "${GREEN}✅ Docker déjà installé ($(docker --version))${NC}"
        return
    fi

    # Installation Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh

    # Démarrer Docker
    systemctl start docker
    systemctl enable docker

    # Ajouter utilisateur au groupe docker (optionnel)
    # usermod -aG docker $SUDO_USER

    echo -e "${GREEN}✅ Docker installé: $(docker --version)${NC}"
}

# Fonction: Installation de Docker Compose
install_docker_compose() {
    echo -e "${YELLOW}🐳 Installation de Docker Compose...${NC}"

    if command -v docker-compose &> /dev/null; then
        echo -e "${GREEN}✅ Docker Compose déjà installé ($(docker-compose --version))${NC}"
        return
    fi

    # Installation Docker Compose v2
    DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | jq -r .tag_name)
    curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

    echo -e "${GREEN}✅ Docker Compose installé: $(docker-compose --version)${NC}"
}

# Fonction: Configuration du firewall
configure_firewall() {
    echo -e "${YELLOW}🔥 Configuration du firewall...${NC}"

    if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]]; then
        # UFW
        ufw --force enable
        ufw default deny incoming
        ufw default allow outgoing
        ufw allow ssh
        ufw allow 80/tcp
        ufw allow 443/tcp
        ufw --force reload
        echo -e "${GREEN}✅ Firewall configuré (UFW)${NC}"
    elif [[ "$OS" == "almalinux" ]] || [[ "$OS" == "rhel" ]] || [[ "$OS" == "centos" ]]; then
        # FirewallD
        systemctl start firewalld
        systemctl enable firewalld
        firewall-cmd --permanent --add-service=ssh
        firewall-cmd --permanent --add-service=http
        firewall-cmd --permanent --add-service=https
        firewall-cmd --reload
        echo -e "${GREEN}✅ Firewall configuré (FirewallD)${NC}"
    fi
}

# Fonction: Configuration de Fail2Ban
configure_fail2ban() {
    echo -e "${YELLOW}🛡️  Configuration de Fail2Ban...${NC}"

    # Configuration SSH
    cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
EOF

    systemctl restart fail2ban
    systemctl enable fail2ban

    echo -e "${GREEN}✅ Fail2Ban configuré${NC}"
}

# Fonction: Clone du repository
clone_repository() {
    echo -e "${YELLOW}📥 Clonage du repository...${NC}"

    # Créer le répertoire d'installation
    mkdir -p $INSTALL_DIR
    cd $INSTALL_DIR

    # Si déjà cloné, pull les dernières modifications
    if [ -d ".git" ]; then
        echo -e "${YELLOW}⬆️  Mise à jour du repository...${NC}"
        git pull origin $GIT_BRANCH
    else
        # Sinon, cloner le repository
        if [ -n "$GIT_REPO" ] && [ "$GIT_REPO" != "https://github.com/votre-org/rag-dz.git" ]; then
            git clone -b $GIT_BRANCH $GIT_REPO .
        else
            echo -e "${YELLOW}⚠️  Repository Git non configuré, utilisation des fichiers locaux${NC}"
        fi
    fi

    echo -e "${GREEN}✅ Repository prêt${NC}"
}

# Fonction: Configuration de l'environnement
setup_environment() {
    echo -e "${YELLOW}⚙️  Configuration de l'environnement...${NC}"

    cd $INSTALL_DIR

    # Copier le template .env si pas existant
    if [ ! -f ".env.production" ]; then
        if [ -f ".env.production.template" ]; then
            cp .env.production.template .env.production
            echo -e "${YELLOW}⚠️  Fichier .env.production créé depuis le template${NC}"
            echo -e "${YELLOW}⚠️  IMPORTANT: Éditez .env.production et configurez vos clés API !${NC}"
            echo -e "${YELLOW}    nano .env.production${NC}"
        else
            echo -e "${RED}❌ Template .env.production.template non trouvé${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✅ Fichier .env.production existe déjà${NC}"
    fi

    # Sécuriser les permissions
    chmod 600 .env.production

    # Substituer les variables dans .env.production
    sed -i "s|DOMAIN=.*|DOMAIN=$DOMAIN|g" .env.production
    sed -i "s|ADMIN_EMAIL=.*|ADMIN_EMAIL=$EMAIL|g" .env.production

    echo -e "${GREEN}✅ Environnement configuré${NC}"
}

# Fonction: Configuration Nginx
setup_nginx() {
    echo -e "${YELLOW}🌐 Configuration de Nginx...${NC}"

    cd $INSTALL_DIR

    # Copier la configuration Nginx
    if [ -f "nginx/nginx.conf" ]; then
        mkdir -p /etc/nginx/sites-available
        mkdir -p /etc/nginx/sites-enabled
        mkdir -p /var/www/html
        mkdir -p /var/www/certbot

        # Copier les landing pages
        if [ -f "landing-complete-responsive.html" ]; then
            cp landing-complete-responsive.html /var/www/html/
            cp -r docs /var/www/html/ 2>/dev/null || true
            cp -r apps /var/www/html/ 2>/dev/null || true
        fi

        # Installer Nginx si nécessaire
        if ! command -v nginx &> /dev/null; then
            if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]]; then
                apt-get install -y nginx
            elif [[ "$OS" == "almalinux" ]] || [[ "$OS" == "rhel" ]]; then
                yum install -y nginx
            fi
        fi

        # Copier la configuration
        cp nginx/nginx.conf /etc/nginx/nginx.conf

        # Tester la configuration
        nginx -t

        # Redémarrer Nginx
        systemctl restart nginx
        systemctl enable nginx

        echo -e "${GREEN}✅ Nginx configuré${NC}"
    else
        echo -e "${YELLOW}⚠️  Fichier nginx/nginx.conf non trouvé${NC}"
    fi
}

# Fonction: Configuration SSL
setup_ssl() {
    if [ "$ENABLE_SSL" != "true" ]; then
        echo -e "${YELLOW}⏭️  SSL désactivé${NC}"
        return
    fi

    echo -e "${YELLOW}🔒 Configuration SSL/HTTPS...${NC}"

    cd $INSTALL_DIR

    if [ -f "nginx/setup-ssl.sh" ]; then
        chmod +x nginx/setup-ssl.sh
        DOMAIN=$DOMAIN EMAIL=$EMAIL nginx/setup-ssl.sh
        echo -e "${GREEN}✅ SSL configuré${NC}"
    else
        echo -e "${YELLOW}⚠️  Script nginx/setup-ssl.sh non trouvé${NC}"
        echo -e "${YELLOW}Configuration SSL manuelle requise${NC}"
    fi
}

# Fonction: Démarrage des services Docker
start_services() {
    echo -e "${YELLOW}🚀 Démarrage des services Docker...${NC}"

    cd $INSTALL_DIR

    # Arrêter les services existants
    docker-compose down 2>/dev/null || true

    # Build et démarrage
    echo -e "${YELLOW}🔨 Build des images Docker...${NC}"
    docker-compose build --parallel

    echo -e "${YELLOW}⬆️  Démarrage des containers...${NC}"
    docker-compose up -d

    # Attendre que les services soient prêts
    echo -e "${YELLOW}⏳ Attente du démarrage des services...${NC}"
    sleep 30

    # Vérifier les services
    docker-compose ps

    echo -e "${GREEN}✅ Services démarrés${NC}"
}

# Fonction: Configuration du monitoring
setup_monitoring() {
    if [ "$ENABLE_MONITORING" != "true" ]; then
        echo -e "${YELLOW}⏭️  Monitoring désactivé${NC}"
        return
    fi

    echo -e "${YELLOW}📊 Configuration du monitoring...${NC}"

    cd $INSTALL_DIR

    # Démarrer les services de monitoring
    docker-compose --profile monitoring up -d

    echo -e "${GREEN}✅ Monitoring configuré${NC}"
    echo -e "${CYAN}Grafana: https://monitoring.$DOMAIN${NC}"
    echo -e "${CYAN}Prometheus: http://localhost:8187${NC}"
}

# Fonction: Configuration des backups
setup_backup() {
    if [ "$ENABLE_BACKUP" != "true" ]; then
        echo -e "${YELLOW}⏭️  Backup désactivé${NC}"
        return
    fi

    echo -e "${YELLOW}💾 Configuration des backups automatiques...${NC}"

    cd $INSTALL_DIR

    if [ -f "scripts/backup.sh" ]; then
        chmod +x scripts/backup.sh

        # Créer un cron job pour les backups quotidiens
        (crontab -l 2>/dev/null; echo "0 2 * * * $INSTALL_DIR/scripts/backup.sh >> /var/log/iafactory-backup.log 2>&1") | crontab -

        echo -e "${GREEN}✅ Backups automatiques configurés (2h du matin)${NC}"
    else
        echo -e "${YELLOW}⚠️  Script scripts/backup.sh non trouvé${NC}"
    fi
}

# Fonction: Affichage du résumé
show_summary() {
    echo -e "${BLUE}==============================================\${NC}"
    echo -e "${GREEN}✅ Déploiement terminé avec succès !${NC}"
    echo -e "${BLUE}==============================================\${NC}"

    echo -e "\n${CYAN}📝 URLs d'accès:${NC}"
    echo -e "${GREEN}  • Site principal:     https://$DOMAIN${NC}"
    echo -e "${GREEN}  • API Backend:        https://api.$DOMAIN/docs${NC}"
    echo -e "${GREEN}  • Hub Dashboard:      https://hub.$DOMAIN${NC}"
    echo -e "${GREEN}  • Bolt Studio:        https://studio.$DOMAIN${NC}"

    if [ "$ENABLE_MONITORING" == "true" ]; then
        echo -e "${GREEN}  • Monitoring:         https://monitoring.$DOMAIN${NC}"
    fi

    echo -e "\n${CYAN}📋 Gestion des services:${NC}"
    echo -e "  • Voir les logs:      ${YELLOW}docker-compose logs -f${NC}"
    echo -e "  • Redémarrer:         ${YELLOW}docker-compose restart${NC}"
    echo -e "  • Arrêter:            ${YELLOW}docker-compose down${NC}"
    echo -e "  • Status:             ${YELLOW}docker-compose ps${NC}"

    echo -e "\n${CYAN}🔧 Prochaines étapes:${NC}"
    echo -e "  1. Éditez .env.production et configurez vos clés API"
    echo -e "     ${YELLOW}nano $INSTALL_DIR/.env.production${NC}"
    echo -e "  2. Redémarrez les services:"
    echo -e "     ${YELLOW}cd $INSTALL_DIR && docker-compose restart${NC}"
    echo -e "  3. Vérifiez les logs:"
    echo -e "     ${YELLOW}docker-compose logs -f iafactory-backend${NC}"
    echo -e "  4. Testez l'API:"
    echo -e "     ${YELLOW}curl https://api.$DOMAIN/health${NC}"

    echo -e "\n${CYAN}📚 Documentation:${NC}"
    echo -e "  • README:             $INSTALL_DIR/README.md"
    echo -e "  • Inventaire:         $INSTALL_DIR/INVENTAIRE_COMPLET_RAG-DZ.md"

    echo -e "\n${GREEN}🎉 IAFactory RAG-DZ est maintenant en ligne !${NC}"
    echo -e "${BLUE}==============================================\${NC}"
}

# ==============================================
# EXÉCUTION PRINCIPALE
# ==============================================

main() {
    echo -e "${PURPLE}Début de l'installation...${NC}\n"

    detect_os
    install_prerequisites
    install_docker
    install_docker_compose
    configure_firewall
    configure_fail2ban
    clone_repository
    setup_environment
    setup_nginx
    setup_ssl
    start_services
    setup_monitoring
    setup_backup
    show_summary
}

# Lancer l'installation
main

# Log de fin
echo "[$(date)] Déploiement IAFactory RAG-DZ terminé" >> /var/log/iafactory-install.log
