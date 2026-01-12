# Setup VPS IP - Helper Script
# IA Factory - Deployment Configuration

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  IA FACTORY - CONFIGURATION VPS IP" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si deploy-all-apps.sh existe
if (-not (Test-Path "deploy-all-apps.sh")) {
    Write-Host "❌ Erreur: deploy-all-apps.sh non trouvé!" -ForegroundColor Red
    Write-Host "   Assurez-vous d'être dans le dossier D:\IAFactory\rag-dz" -ForegroundColor Yellow
    exit 1
}

Write-Host "📋 Instructions pour obtenir l'IP VPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Ouvrir un terminal SSH:" -ForegroundColor White
Write-Host "   ssh user@votre-vps" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Exécuter:" -ForegroundColor White
Write-Host "   curl ifconfig.me" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Copier l'IP affichée (ex: 123.45.67.89)" -ForegroundColor White
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Demander l'IP VPS
$vpsIP = Read-Host "Entrez l'IP de votre VPS"

# Valider format IP (basique)
if ($vpsIP -match '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$') {
    Write-Host ""
    Write-Host "✅ IP valide: $vpsIP" -ForegroundColor Green
    Write-Host ""

    # Backup du script original
    Copy-Item "deploy-all-apps.sh" "deploy-all-apps.sh.backup"
    Write-Host "📁 Backup créé: deploy-all-apps.sh.backup" -ForegroundColor Gray

    # Remplacer l'IP dans le script
    (Get-Content "deploy-all-apps.sh") -replace 'VPS_HOST="your-vps-ip"', "VPS_HOST=`"$vpsIP`"" | Set-Content "deploy-all-apps.sh"

    Write-Host "✅ Script mis à jour avec IP: $vpsIP" -ForegroundColor Green
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "  PRÊT POUR DÉPLOIEMENT!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Prochaine étape:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Ouvrir Git Bash ou WSL" -ForegroundColor White
    Write-Host "2. Naviguer vers le dossier:" -ForegroundColor White
    Write-Host "   cd /d/IAFactory/rag-dz" -ForegroundColor Gray
    Write-Host "3. Lancer le déploiement:" -ForegroundColor White
    Write-Host "   ./deploy-all-apps.sh" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Durée estimée: 15-20 minutes" -ForegroundColor Gray
    Write-Host ""

} else {
    Write-Host ""
    Write-Host "❌ Format IP invalide!" -ForegroundColor Red
    Write-Host "   Format attendu: 123.45.67.89" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
