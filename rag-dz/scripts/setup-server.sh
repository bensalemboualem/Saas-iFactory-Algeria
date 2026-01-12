#!/bin/bash
set -euo pipefail

###############################################################################
# Script de Configuration Serveur Ubuntu 22.04 pour IAFactory RAG-DZ
# Ce script configure un serveur Ubuntu fresh pour héberger l'application
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

main() {
    log_info "Début de la configuration du serveur..."

    # Mise à jour du système
    log_info "Mise à jour du système..."
    export DEBIAN_FRONTEND=noninteractive
    apt-get update
    apt-get upgrade -y
    log_success "Système à jour"

    # Installation des dépendances de base
    log_info "Installation des paquets de base..."
    apt-get install -y \
        curl \
        wget \
        git \
        vim \
        htop \
        net-tools \
        ufw \
        fail2ban \
        jq \
        openssl \
        ca-certificates \
        gnupg \
        lsb-release
    log_success "Paquets de base installés"

    # Installation de Docker
    log_info "Installation de Docker..."
    if ! command -v docker &> /dev/null; then
        # Ajouter le repository Docker
        mkdir -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

        echo \
          "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
          $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

        apt-get update
        apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

        # Démarrer Docker
        systemctl enable docker
        systemctl start docker

        log_success "Docker installé"
    else
        log_success "Docker déjà installé"
    fi

    # Installation de Docker Compose standalone
    log_info "Installation de Docker Compose..."
    if ! command -v docker-compose &> /dev/null; then
        curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        log_success "Docker Compose installé"
    else
        log_success "Docker Compose déjà installé"
    fi

    # Configuration du firewall
    log_info "Configuration du firewall UFW..."
    ufw --force enable
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow ssh
    ufw allow http
    ufw allow https
    ufw allow 8180/tcp  # Backend API
    ufw allow 8182/tcp  # Hub UI
    ufw allow 8183/tcp  # Docs UI
    ufw allow 8184/tcp  # Bolt Studio
    ufw allow 8185/tcp  # n8n
    log_success "Firewall configuré"

    # Configuration de Fail2Ban
    log_info "Configuration de Fail2Ban..."
    systemctl enable fail2ban
    systemctl start fail2ban

    cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
EOF

    systemctl restart fail2ban
    log_success "Fail2Ban configuré"

    # Installation de Nginx
    log_info "Installation de Nginx..."
    apt-get install -y nginx
    systemctl enable nginx
    systemctl start nginx
    log_success "Nginx installé"

    # Configuration de logrotate pour Docker
    log_info "Configuration de logrotate..."
    cat > /etc/logrotate.d/docker << 'EOF'
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    missingok
    delaycompress
    copytruncate
}
EOF
    log_success "Logrotate configuré"

    # Optimisation système pour Docker
    log_info "Optimisation système..."

    # Augmenter les limites de fichiers
    cat >> /etc/security/limits.conf << 'EOF'
* soft nofile 65536
* hard nofile 65536
root soft nofile 65536
root hard nofile 65536
EOF

    # Optimisation réseau
    cat >> /etc/sysctl.conf << 'EOF'
# Optimisations réseau
net.core.somaxconn = 4096
net.ipv4.tcp_max_syn_backlog = 4096
net.ipv4.ip_local_port_range = 10000 65535
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 15
net.core.netdev_max_backlog = 4096
EOF

    sysctl -p
    log_success "Optimisations appliquées"

    # Créer les répertoires nécessaires
    log_info "Création des répertoires..."
    mkdir -p /opt/iafactory
    mkdir -p /backup/iafactory
    mkdir -p /var/log/iafactory
    log_success "Répertoires créés"

    # Configuration de swap si nécessaire
    if [ ! -f /swapfile ]; then
        log_info "Création d'un fichier swap de 4GB..."
        fallocate -l 4G /swapfile
        chmod 600 /swapfile
        mkswap /swapfile
        swapon /swapfile
        echo '/swapfile none swap sw 0 0' | tee -a /etc/fstab
        log_success "Swap configuré"
    else
        log_success "Swap déjà configuré"
    fi

    # Installer des outils de monitoring
    log_info "Installation des outils de monitoring..."
    apt-get install -y \
        iotop \
        iftop \
        ncdu \
        sysstat
    log_success "Outils de monitoring installés"

    # Configuration de la timezone
    log_info "Configuration de la timezone..."
    timedatectl set-timezone Europe/Paris
    log_success "Timezone configurée (Europe/Paris)"

    # Nettoyage
    log_info "Nettoyage..."
    apt-get autoremove -y
    apt-get autoclean
    log_success "Nettoyage terminé"

    # Afficher le résumé
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    log_success "Configuration du serveur terminée!"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "📦 Logiciels installés:"
    echo "   Docker version: $(docker --version)"
    echo "   Docker Compose: $(docker-compose --version)"
    echo "   Nginx version: $(nginx -v 2>&1)"
    echo ""
    echo "🔥 Firewall UFW:"
    ufw status numbered | grep -E "ALLOW|Status"
    echo ""
    echo "💾 Espace disque:"
    df -h / | tail -1
    echo ""
    echo "🧠 Mémoire:"
    free -h | grep -E "Mem|Swap"
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
}

# Exécution
main "$@"
