#!/bin/bash

# Setup VPS IP - Helper Script (Bash version)
# IA Factory - Deployment Configuration

echo ""
echo "================================================"
echo "  IA FACTORY - CONFIGURATION VPS IP"
echo "================================================"
echo ""

# Vérifier si deploy-all-apps.sh existe
if [ ! -f "deploy-all-apps.sh" ]; then
    echo "❌ Erreur: deploy-all-apps.sh non trouvé!"
    echo "   Assurez-vous d'être dans le dossier rag-dz"
    exit 1
fi

echo "📋 Instructions pour obtenir l'IP VPS:"
echo ""
echo "1. Ouvrir un terminal SSH:"
echo "   ssh user@votre-vps"
echo ""
echo "2. Exécuter:"
echo "   curl ifconfig.me"
echo ""
echo "3. Copier l'IP affichée (ex: 123.45.67.89)"
echo ""
echo "================================================"
echo ""

# Demander l'IP VPS
read -p "Entrez l'IP de votre VPS: " vpsIP

# Valider format IP (basique)
if [[ $vpsIP =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
    echo ""
    echo "✅ IP valide: $vpsIP"
    echo ""

    # Backup du script original
    cp deploy-all-apps.sh deploy-all-apps.sh.backup
    echo "📁 Backup créé: deploy-all-apps.sh.backup"

    # Remplacer l'IP dans le script
    sed -i "s/VPS_HOST=\"your-vps-ip\"/VPS_HOST=\"$vpsIP\"/" deploy-all-apps.sh

    echo "✅ Script mis à jour avec IP: $vpsIP"
    echo ""
    echo "================================================"
    echo "  PRÊT POUR DÉPLOIEMENT!"
    echo "================================================"
    echo ""
    echo "Prochaine étape:"
    echo ""
    echo "  ./deploy-all-apps.sh"
    echo ""
    echo "Durée estimée: 15-20 minutes"
    echo ""

else
    echo ""
    echo "❌ Format IP invalide!"
    echo "   Format attendu: 123.45.67.89"
    echo ""
    exit 1
fi
