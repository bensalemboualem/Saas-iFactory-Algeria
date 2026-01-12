#!/bin/bash
################################################################################
# 🚀 DÉPLOIEMENT ULTRA-AUTOMATIQUE RAG-DZ
# Version: 3.0 - ZÉRO INTERVENTION
# Description: Script qui fait TOUT automatiquement
################################################################################

set -e

VPS_IP="46.224.3.125"
VPS_USER="root"
REPO_URL="https://github.com/bensalemboualem/rag-dz.git"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}================================${NC}"
echo -e "${CYAN}🚀 DÉPLOIEMENT ULTRA-AUTOMATIQUE${NC}"
echo -e "${CYAN}================================${NC}"
echo ""
echo -e "${YELLOW}VPS:${NC} $VPS_IP"
echo -e "${YELLOW}Repository:${NC} $REPO_URL"
echo ""

# Générer un mot de passe sécurisé pour PostgreSQL
POSTGRES_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
JWT_SECRET=$(openssl rand -hex 32)

echo -e "${GREEN}✅ Mots de passe générés automatiquement${NC}"
echo ""

# Demander uniquement le mot de passe VPS et les credentials SMTP
read -sp "🔐 Mot de passe root VPS: " VPS_PASSWORD
echo ""
read -p "📧 Email Gmail (ex: contact@iafactory.ch): " SMTP_USER
echo ""
read -sp "🔑 Gmail App Password (16 caractères): " SMTP_PASSWORD
echo ""
echo ""

echo -e "${BLUE}📝 Configuration:${NC}"
echo -e "  - PostgreSQL Password: ${GREEN}[GÉNÉRÉ AUTOMATIQUEMENT]${NC}"
echo -e "  - JWT Secret: ${GREEN}[GÉNÉRÉ AUTOMATIQUEMENT]${NC}"
echo -e "  - SMTP User: ${GREEN}$SMTP_USER${NC}"
echo -e "  - Domain CH: ${GREEN}iafactory.ch${NC}"
echo -e "  - Domain Algeria: ${GREEN}iafactoryalgeria.com${NC}"
echo ""

read -p "🚀 Lancer le déploiement MAINTENANT? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}❌ Déploiement annulé${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🔥 LANCEMENT DU DÉPLOIEMENT COMPLET...${NC}"
echo ""

# Créer le script de déploiement complet avec toutes les réponses automatiques
cat > /tmp/deploy-vps-complete.sh << 'EOFSCRIPT'
#!/bin/bash
set -e

echo '================================'
echo '🚀 DÉPLOIEMENT RAG-DZ EN COURS'
echo '================================'
echo ''

# Aller dans le répertoire home
cd ~

# Supprimer l'ancien clone si existe
if [ -d "rag-dz" ]; then
    echo '🗑️  Suppression de l'\''ancien clone...'
    rm -rf rag-dz
fi

# Cloner le repository
echo '📥 Clonage du repository...'
git clone https://github.com/bensalemboualem/rag-dz.git

# Entrer dans le répertoire
cd rag-dz

# Rendre le script exécutable
chmod +x full_setup.sh

echo ''
echo '✅ Repository cloné avec succès!'
echo ''

# Créer un fichier de configuration automatique
cat > /tmp/deploy-answers.txt << EOFANSWERS
POSTGRES_PASSWORD_AUTO
JWT_SECRET_AUTO
SMTP_USER_AUTO
SMTP_PASSWORD_AUTO
iafactory.ch
iafactoryalgeria.com
EOFANSWERS

# Modifier full_setup.sh pour utiliser les réponses automatiques
echo ''
echo '🔧 Configuration automatique des réponses...'
echo ''

# Lancer le déploiement en mode non-interactif
export DEBIAN_FRONTEND=noninteractive
export POSTGRES_PASSWORD="POSTGRES_PASSWORD_AUTO"
export JWT_SECRET="JWT_SECRET_AUTO"
export SMTP_USER="SMTP_USER_AUTO"
export SMTP_PASSWORD="SMTP_PASSWORD_AUTO"
export DOMAIN_CH="iafactory.ch"
export DOMAIN_ALGERIA="iafactoryalgeria.com"

echo ''
echo '🔥 LANCEMENT DU SCRIPT full_setup.sh...'
echo ''

# Exécuter le script avec les variables d'environnement
sudo -E bash full_setup.sh

echo ''
echo '================================'
echo '✅ DÉPLOIEMENT TERMINÉ!'
echo '================================'
echo ''
echo '🌐 Vos sites sont maintenant en ligne:'
echo '   - https://iafactory.ch (Suisse - Français)'
echo '   - https://iafactoryalgeria.com (Algérie - Arabe RTL)'
echo ''
EOFSCRIPT

# Remplacer les placeholders dans le script
sed -i "s/POSTGRES_PASSWORD_AUTO/$POSTGRES_PASSWORD/g" /tmp/deploy-vps-complete.sh
sed -i "s/JWT_SECRET_AUTO/$JWT_SECRET/g" /tmp/deploy-vps-complete.sh
sed -i "s/SMTP_USER_AUTO/$SMTP_USER/g" /tmp/deploy-vps-complete.sh
sed -i "s/SMTP_PASSWORD_AUTO/$SMTP_PASSWORD/g" /tmp/deploy-vps-complete.sh

echo -e "${BLUE}📡 Connexion au VPS...${NC}"
echo ""

# Utiliser sshpass si disponible, sinon demander d'installer
if command -v sshpass &> /dev/null; then
    # Copier le script sur le VPS et l'exécuter
    sshpass -p "$VPS_PASSWORD" scp -o StrictHostKeyChecking=no /tmp/deploy-vps-complete.sh ${VPS_USER}@${VPS_IP}:/tmp/

    echo -e "${GREEN}✅ Script copié sur le VPS${NC}"
    echo ""
    echo -e "${BLUE}🚀 Exécution du déploiement sur le VPS...${NC}"
    echo ""

    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_IP} 'bash /tmp/deploy-vps-complete.sh'

    echo ""
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}✅ DÉPLOIEMENT TERMINÉ!${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
    echo -e "${CYAN}🌐 Vérifiez vos sites:${NC}"
    echo -e "   - ${GREEN}https://iafactory.ch${NC} (Suisse - Français)"
    echo -e "   - ${GREEN}https://iafactoryalgeria.com${NC} (Algérie - Arabe RTL)"
    echo ""
    echo -e "${YELLOW}📋 Credentials sauvegardés dans:${NC} ~/rag-dz-credentials.txt"

    # Sauvegarder les credentials localement
    cat > ~/rag-dz-credentials.txt << EOFCREDS
# RAG-DZ Deployment Credentials
# Date: $(date)

POSTGRES_PASSWORD=$POSTGRES_PASSWORD
JWT_SECRET=$JWT_SECRET
SMTP_USER=$SMTP_USER
SMTP_PASSWORD=$SMTP_PASSWORD
DOMAIN_CH=iafactory.ch
DOMAIN_ALGERIA=iafactoryalgeria.com
EOFCREDS

    chmod 600 ~/rag-dz-credentials.txt
    echo -e "${GREEN}✅ Credentials sauvegardés dans ~/rag-dz-credentials.txt${NC}"

else
    # sshpass n'est pas installé, utiliser expect ou méthode manuelle
    echo -e "${YELLOW}⚠️  sshpass n'est pas installé${NC}"
    echo ""
    echo -e "${CYAN}📖 SOLUTION 1: Installer sshpass${NC}"
    echo -e "   ${BLUE}sudo apt-get install -y sshpass${NC}  # Ubuntu/Debian"
    echo -e "   ${BLUE}brew install hudochenkov/sshpass/sshpass${NC}  # macOS"
    echo ""
    echo -e "${CYAN}📖 SOLUTION 2: Connexion manuelle${NC}"
    echo ""
    echo -e "${YELLOW}Exécutez ces commandes sur le VPS:${NC}"
    echo ""
    echo -e "${BLUE}ssh root@46.224.3.125${NC}"
    echo ""
    cat /tmp/deploy-vps-complete.sh
    echo ""
fi

# Nettoyer
rm -f /tmp/deploy-vps-complete.sh

echo ""
echo -e "${CYAN}🎉 Déploiement terminé avec succès!${NC}"
