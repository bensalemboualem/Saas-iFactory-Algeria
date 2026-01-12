#!/bin/bash
# ============================================================================
# LANCEMENT IMMÉDIAT - IAFactory RAG-DZ
# ============================================================================
# VPS: iafactorysuisse (Hetzner)
# IP: 46.224.3.125
# Domaine: www.iafactoryalgeria.com
# ============================================================================

set -e

# Configuration
VPS_IP="46.224.3.125"
VPS_USER="root"
DOMAIN="www.iafactoryalgeria.com"
EMAIL="admin@iafactoryalgeria.com"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}=============================================================================="
echo "DEPLOIEMENT AUTOMATIQUE - IAFactory RAG-DZ"
echo "==============================================================================${NC}"
echo ""
echo -e "${GREEN}Serveur:${NC} iafactorysuisse"
echo -e "${GREEN}IP:${NC} $VPS_IP"
echo -e "${GREEN}Domaine:${NC} $DOMAIN"
echo -e "${GREEN}Email:${NC} $EMAIL"
echo ""
echo -e "${CYAN}==============================================================================${NC}"
echo ""

# Test connexion SSH
echo -e "${YELLOW}[TEST]${NC} Connexion SSH au VPS..."
if ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_IP} "echo 'OK'" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Connexion SSH OK${NC}"
else
    echo -e "${RED}❌ Impossible de se connecter au VPS${NC}"
    echo ""
    echo -e "${YELLOW}Configuration SSH nécessaire:${NC}"
    echo ""
    echo "Option 1: Utiliser le mot de passe root (reçu par email Hetzner)"
    echo "  ssh root@${VPS_IP}"
    echo ""
    echo "Option 2: Configurer une clé SSH"
    echo "  1. Générer une clé (si pas déjà fait):"
    echo "     ssh-keygen -t rsa -b 4096"
    echo "  2. Copier la clé publique:"
    echo "     cat ~/.ssh/id_rsa.pub"
    echo "  3. L'ajouter dans Hetzner Cloud Console → SSH Keys"
    echo ""
    exit 1
fi

echo ""
echo -e "${YELLOW}Prêt à déployer sur ${VPS_IP}. Continuer? (y/n)${NC}"
read -p "> " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo -e "${RED}Déploiement annulé${NC}"
    exit 0
fi

# Export variables pour le script principal
export VPS_IP="${VPS_IP}"
export VPS_USER="${VPS_USER}"
export DOMAIN="${DOMAIN}"
export EMAIL="${EMAIL}"

# Lancer le déploiement automatique
echo ""
echo -e "${GREEN}[DEPLOIEMENT]${NC} Lancement du script automatique..."
echo ""

./deploy-auto-complete.sh
