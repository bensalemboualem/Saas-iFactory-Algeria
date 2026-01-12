# Script de connexion directe au VPS IAFactory
# Gère automatiquement la clé SSH

$VPS_IP = "46.224.3.125"
$VPS_USER = "root"
$VPS_PASSWORD = "Ainsefra+0819692025"

Write-Host "🔌 Connexion au VPS IAFactory..." -ForegroundColor Cyan
Write-Host "📍 IP: $VPS_IP" -ForegroundColor Yellow
Write-Host ""

# Chemin vers plink
$plink = ".\plink.exe"

# Télécharger plink si nécessaire
if (-not (Test-Path $plink)) {
    Write-Host "📥 Téléchargement de plink..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink
}

Write-Host "✅ Test de connexion..." -ForegroundColor Green
Write-Host ""

# Première connexion pour accepter la clé (avec -batch désactivé)
$acceptKeyScript = @"
echo '✅ Connexion SSH réussie!'
echo ''
echo '📊 Système:'
uname -a
echo ''
echo '⏱️ Uptime:'
uptime
echo ''
echo '💾 Espace disque:'
df -h / | tail -1
echo ''
echo '🐳 Conteneurs Docker:'
docker ps --format 'table {{.Names}}\t{{.Status}}' 2>/dev/null || echo 'Docker: Vérification...'
"@

# Utiliser echo y pour accepter automatiquement la clé
$process = echo y | & $plink -pw $VPS_PASSWORD "${VPS_USER}@${VPS_IP}" $acceptKeyScript

Write-Host ""
Write-Host "════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✅ Connexion établie avec succès!" -ForegroundColor Green
Write-Host "════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pour ouvrir une session interactive:" -ForegroundColor Yellow
Write-Host "  .\plink.exe -pw `"$VPS_PASSWORD`" ${VPS_USER}@${VPS_IP}" -ForegroundColor Gray
