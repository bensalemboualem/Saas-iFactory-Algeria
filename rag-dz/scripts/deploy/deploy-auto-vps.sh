#!/bin/bash
################################################################################
# 🚀 Déploiement Automatique RAG-DZ sur VPS Hetzner
# Version: 2.0 (Bash)
# Description: Script Bash pour Git Bash / WSL / Linux
################################################################################

VPS_IP="46.224.3.125"
VPS_USER="root"
REPO_URL="https://github.com/bensalemboualem/rag-dz.git"

echo "================================"
echo "🚀 DÉPLOIEMENT AUTOMATIQUE RAG-DZ"
echo "================================"
echo ""
echo "VPS: $VPS_IP"
echo "Repository: $REPO_URL"
echo ""

# Script qui sera exécuté sur le VPS
read -r -d '' REMOTE_SCRIPT << 'EOFREMOTE'
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
    echo '🗑️  Suppression de l\'ancien clone...'
    rm -rf rag-dz
fi

# Cloner le repository
echo '📥 Clonage du repository...'
git clone https://github.com/bensalemboualem/rag-dz.git

# Entrer dans le répertoire
cd rag-dz

# Rendre le script exécutable
chmod +x full_setup.sh

# Afficher le contenu pour vérification
echo ''
echo '✅ Repository cloné avec succès!'
echo ''
echo '📋 Fichiers importants détectés:'
ls -lh full_setup.sh FINAL_QA_VERIFICATION.md 2>/dev/null || echo '⚠️  Certains fichiers manquent'
echo ''

# Demander confirmation avant de lancer
read -p "🚀 Lancer le déploiement complet maintenant? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ''
    echo '🔥 LANCEMENT DU DÉPLOIEMENT COMPLET...'
    echo ''
    sudo ./full_setup.sh
else
    echo ''
    echo '⏸️  Déploiement en pause. Pour lancer manuellement plus tard:'
    echo '   cd ~/rag-dz'
    echo '   sudo ./full_setup.sh'
fi
EOFREMOTE

echo "🔐 Connexion SSH au VPS..."
echo ""
echo "⚠️  Note: Vous devrez peut-être accepter l'empreinte du serveur (tapez 'yes')"
echo ""

# Se connecter et exécuter le script
ssh -o StrictHostKeyChecking=no "${VPS_USER}@${VPS_IP}" "$REMOTE_SCRIPT"

echo ""
echo "================================"
echo "✅ DÉPLOIEMENT TERMINÉ!"
echo "================================"
echo ""
echo "🌐 Vérifiez vos sites:"
echo "   - https://iafactory.ch (Suisse - Français)"
echo "   - https://iafactoryalgeria.com (Algérie - Arabe RTL)"
echo ""
