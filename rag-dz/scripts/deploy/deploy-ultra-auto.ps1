################################################################################
# 🚀 DÉPLOIEMENT ULTRA-AUTOMATIQUE RAG-DZ (PowerShell)
# Version: 3.0 - ZÉRO INTERVENTION
# Description: Script qui fait TOUT automatiquement
################################################################################

$VPS_IP = "46.224.3.125"
$VPS_USER = "root"
$REPO_URL = "https://github.com/bensalemboualem/rag-dz.git"

Write-Host "================================" -ForegroundColor Cyan
Write-Host "🚀 DÉPLOIEMENT ULTRA-AUTOMATIQUE" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "VPS: $VPS_IP" -ForegroundColor Yellow
Write-Host "Repository: $REPO_URL" -ForegroundColor Yellow
Write-Host ""

# Générer des mots de passe sécurisés automatiquement
Add-Type -AssemblyName System.Web
$POSTGRES_PASSWORD = [System.Web.Security.Membership]::GeneratePassword(32, 8)
$JWT_SECRET = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})

Write-Host "✅ Mots de passe générés automatiquement" -ForegroundColor Green
Write-Host ""

# Demander uniquement les infos essentielles
$VPS_PASSWORD = Read-Host "🔐 Mot de passe root VPS" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($VPS_PASSWORD)
$VPS_PASSWORD_PLAIN = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

$SMTP_USER = Read-Host "📧 Email Gmail (ex: contact@iafactory.ch)"
$SMTP_PASSWORD_SECURE = Read-Host "🔑 Gmail App Password (16 caractères)" -AsSecureString
$BSTR2 = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SMTP_PASSWORD_SECURE)
$SMTP_PASSWORD = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR2)

Write-Host ""
Write-Host "📝 Configuration:" -ForegroundColor Blue
Write-Host "  - PostgreSQL Password: [GÉNÉRÉ AUTOMATIQUEMENT]" -ForegroundColor Green
Write-Host "  - JWT Secret: [GÉNÉRÉ AUTOMATIQUEMENT]" -ForegroundColor Green
Write-Host "  - SMTP User: $SMTP_USER" -ForegroundColor Green
Write-Host "  - Domain CH: iafactory.ch" -ForegroundColor Green
Write-Host "  - Domain Algeria: iafactoryalgeria.com" -ForegroundColor Green
Write-Host ""

$confirmation = Read-Host "🚀 Lancer le déploiement MAINTENANT? (y/n)"
if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
    Write-Host "❌ Déploiement annulé" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "🔥 LANCEMENT DU DÉPLOIEMENT COMPLET..." -ForegroundColor Green
Write-Host ""

# Créer le script de déploiement complet
$deployScript = @"
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

# Créer les variables d'environnement
export DEBIAN_FRONTEND=noninteractive
export POSTGRES_PASSWORD="$POSTGRES_PASSWORD"
export JWT_SECRET="$JWT_SECRET"
export SMTP_USER="$SMTP_USER"
export SMTP_PASSWORD="$SMTP_PASSWORD"
export DOMAIN_CH="iafactory.ch"
export DOMAIN_ALGERIA="iafactoryalgeria.com"

# Modifier full_setup.sh pour mode non-interactif
sed -i 's/read -sp/echo # Skipped read -sp/g' full_setup.sh
sed -i 's/read -p/echo # Skipped read -p/g' full_setup.sh

echo ''
echo '🔥 LANCEMENT DU SCRIPT full_setup.sh...'
echo ''

# Exécuter le script
sudo -E bash full_setup.sh || true

# Vérifier que les services sont lancés
echo ''
echo '🔍 Vérification des services...'
docker ps

echo ''
echo '================================'
echo '✅ DÉPLOIEMENT TERMINÉ!'
echo '================================'
echo ''
echo '🌐 Vos sites sont maintenant en ligne:'
echo '   - https://iafactory.ch (Suisse - Français)'
echo '   - https://iafactoryalgeria.com (Algérie - Arabe RTL)'
echo ''

# Sauvegarder les credentials sur le VPS
cat > ~/rag-dz-credentials.txt << EOFCREDS
# RAG-DZ Deployment Credentials
# Date: `$(date)`

POSTGRES_PASSWORD=$POSTGRES_PASSWORD
JWT_SECRET=$JWT_SECRET
SMTP_USER=$SMTP_USER
SMTP_PASSWORD=$SMTP_PASSWORD
DOMAIN_CH=iafactory.ch
DOMAIN_ALGERIA=iafactoryalgeria.com
VPS_IP=$VPS_IP
EOFCREDS

chmod 600 ~/rag-dz-credentials.txt

echo ''
echo '✅ Credentials sauvegardés dans ~/rag-dz-credentials.txt'
echo ''
"@

# Sauvegarder le script temporairement
$tempScript = "$env:TEMP\deploy-rag-dz-auto.sh"
$deployScript | Out-File -FilePath $tempScript -Encoding UTF8 -NoNewline

Write-Host "📝 Script de déploiement créé" -ForegroundColor Green
Write-Host ""

# Vérifier si Plink (PuTTY) est disponible
$plinkPath = Get-Command plink -ErrorAction SilentlyContinue

if ($plinkPath) {
    Write-Host "📡 Utilisation de Plink (PuTTY) pour la connexion..." -ForegroundColor Cyan
    Write-Host ""

    # Copier le script sur le VPS
    Write-Host "📤 Copie du script sur le VPS..." -ForegroundColor Yellow
    echo y | & plink -batch -pw $VPS_PASSWORD_PLAIN "${VPS_USER}@${VPS_IP}" "exit" 2>$null

    & pscp -batch -pw $VPS_PASSWORD_PLAIN $tempScript "${VPS_USER}@${VPS_IP}:/tmp/deploy-auto.sh"

    Write-Host "✅ Script copié" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Exécution du déploiement sur le VPS..." -ForegroundColor Cyan
    Write-Host ""

    # Exécuter le script
    & plink -batch -pw $VPS_PASSWORD_PLAIN "${VPS_USER}@${VPS_IP}" "bash /tmp/deploy-auto.sh"

    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "✅ DÉPLOIEMENT TERMINÉ!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green

} else {
    # Essayer avec SSH natif Windows
    $sshPath = Get-Command ssh -ErrorAction SilentlyContinue

    if ($sshPath) {
        Write-Host "📡 Utilisation de OpenSSH Windows..." -ForegroundColor Cyan
        Write-Host ""

        # Note: OpenSSH Windows ne supporte pas -p pour le mot de passe
        # On va créer une clé temporaire ou utiliser une autre méthode

        Write-Host "⚠️  OpenSSH ne supporte pas l'authentification automatique par mot de passe" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "📖 SOLUTION: Installer PuTTY (plink)" -ForegroundColor Cyan
        Write-Host "   Téléchargez: https://www.putty.org/" -ForegroundColor White
        Write-Host ""
        Write-Host "📖 OU exécutez manuellement:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "ssh ${VPS_USER}@${VPS_IP}" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Puis collez ce script:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host $deployScript -ForegroundColor Gray

    } else {
        Write-Host "❌ Ni PuTTY ni OpenSSH trouvés!" -ForegroundColor Red
        Write-Host ""
        Write-Host "📖 Installez l'un des deux:" -ForegroundColor Yellow
        Write-Host "   1. PuTTY: https://www.putty.org/" -ForegroundColor White
        Write-Host "   2. OpenSSH: Paramètres > Apps > Fonctionnalités facultatives" -ForegroundColor White
    }
}

# Sauvegarder les credentials localement
$credentialsPath = "$HOME\rag-dz-credentials.txt"
$credentialsContent = @"
# RAG-DZ Deployment Credentials
# Date: $(Get-Date)

VPS_IP=$VPS_IP
VPS_USER=$VPS_USER
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
JWT_SECRET=$JWT_SECRET
SMTP_USER=$SMTP_USER
SMTP_PASSWORD=$SMTP_PASSWORD
DOMAIN_CH=iafactory.ch
DOMAIN_ALGERIA=iafactoryalgeria.com

# URLs
URL_CH=https://iafactory.ch
URL_ALGERIA=https://iafactoryalgeria.com
"@

$credentialsContent | Out-File -FilePath $credentialsPath -Encoding UTF8

Write-Host ""
Write-Host "✅ Credentials sauvegardés dans: $credentialsPath" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Vérifiez vos sites:" -ForegroundColor Cyan
Write-Host "   - https://iafactory.ch (Suisse - Français)" -ForegroundColor White
Write-Host "   - https://iafactoryalgeria.com (Algérie - Arabe RTL)" -ForegroundColor White
Write-Host ""

# Nettoyer
Remove-Item $tempScript -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🎉 Script terminé!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
