################################################################################
# 🚀 Déploiement Automatique RAG-DZ sur VPS Hetzner
# Version: 2.0
# Description: Script PowerShell qui se connecte au VPS et fait tout automatiquement
################################################################################

# Configuration
$VPS_IP = "46.224.3.125"
$VPS_USER = "root"
$REPO_URL = "https://github.com/bensalemboualem/rag-dz.git"

Write-Host "================================" -ForegroundColor Cyan
Write-Host "🚀 DÉPLOIEMENT AUTOMATIQUE RAG-DZ" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "VPS: $VPS_IP" -ForegroundColor Yellow
Write-Host "Repository: $REPO_URL" -ForegroundColor Yellow
Write-Host ""

# Demander le mot de passe root
$password = Read-Host "Entrez le mot de passe root du VPS" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host ""
Write-Host "📡 Connexion au VPS..." -ForegroundColor Green

# Créer le script de déploiement qui sera exécuté sur le VPS
$remoteScript = @"
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
git clone $REPO_URL

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
if [[ \$REPLY =~ ^[Yy]$ ]]; then
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
"@

# Sauvegarder le script temporairement
$tempScript = "$env:TEMP\deploy-rag-dz.sh"
$remoteScript | Out-File -FilePath $tempScript -Encoding ASCII -NoNewline

Write-Host "📝 Script de déploiement créé" -ForegroundColor Green
Write-Host ""

# Utiliser SSH pour se connecter (nécessite OpenSSH installé sur Windows)
Write-Host "🔐 Connexion SSH et transfert du script..." -ForegroundColor Green
Write-Host ""

# Vérifier si ssh est disponible
$sshPath = Get-Command ssh -ErrorAction SilentlyContinue
if (-not $sshPath) {
    Write-Host "❌ ERREUR: SSH n'est pas installé sur votre système Windows!" -ForegroundColor Red
    Write-Host ""
    Write-Host "📖 SOLUTION 1: Installer OpenSSH pour Windows" -ForegroundColor Yellow
    Write-Host "   1. Paramètres > Applications > Fonctionnalités facultatives" -ForegroundColor White
    Write-Host "   2. Ajouter une fonctionnalité > OpenSSH Client" -ForegroundColor White
    Write-Host ""
    Write-Host "📖 SOLUTION 2: Utiliser PuTTY" -ForegroundColor Yellow
    Write-Host "   Téléchargez PuTTY depuis: https://www.putty.org/" -ForegroundColor White
    Write-Host ""
    Write-Host "📖 SOLUTION 3: Connexion manuelle" -ForegroundColor Yellow
    Write-Host "   Copiez ces commandes et exécutez-les manuellement sur le VPS:" -ForegroundColor White
    Write-Host ""
    Write-Host $remoteScript -ForegroundColor Gray
    exit 1
}

# Créer une commande SSH qui copie et exécute le script
Write-Host "Connexion à ${VPS_USER}@${VPS_IP}..." -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  Note: Vous devrez peut-être accepter l'empreinte du serveur (tapez 'yes')" -ForegroundColor Yellow
Write-Host ""

# Utiliser plink si disponible (PuTTY), sinon ssh natif
try {
    # Méthode 1: SSH natif Windows (recommandé)
    $sshCommand = "bash -c `"$(Get-Content $tempScript -Raw)`""

    Write-Host "Exécution de la commande SSH..." -ForegroundColor Green
    Write-Host ""

    # Utiliser sshpass si disponible, sinon demander mot de passe interactivement
    ssh -o StrictHostKeyChecking=no "${VPS_USER}@${VPS_IP}" $sshCommand

    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "✅ DÉPLOIEMENT TERMINÉ!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Vérifiez vos sites:" -ForegroundColor Cyan
    Write-Host "   - https://iafactory.ch (Suisse - Français)" -ForegroundColor White
    Write-Host "   - https://iafactoryalgeria.com (Algérie - Arabe RTL)" -ForegroundColor White
    Write-Host ""

} catch {
    Write-Host "❌ ERREUR lors de la connexion SSH: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "📖 SOLUTION ALTERNATIVE: Connexion Manuelle" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1️⃣ Ouvrez PuTTY ou un terminal SSH" -ForegroundColor Cyan
    Write-Host "2️⃣ Connectez-vous: ssh root@46.224.3.125" -ForegroundColor Cyan
    Write-Host "3️⃣ Exécutez ces commandes:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "cd ~" -ForegroundColor Gray
    Write-Host "git clone https://github.com/bensalemboualem/rag-dz.git" -ForegroundColor Gray
    Write-Host "cd rag-dz" -ForegroundColor Gray
    Write-Host "chmod +x full_setup.sh" -ForegroundColor Gray
    Write-Host "sudo ./full_setup.sh" -ForegroundColor Gray
    Write-Host ""
}

# Nettoyer le fichier temporaire
Remove-Item $tempScript -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
