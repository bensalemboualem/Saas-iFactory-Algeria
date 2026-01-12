# Connexion VPS avec le BON mot de passe
$VPS_IP = "46.224.3.125"
$VPS_PASSWORD = "aINSRFRA#0819692025#"

Write-Host "`n=== CONNEXION VPS IAFACTORY ===" -ForegroundColor Green
Write-Host "Serveur: root@$VPS_IP`n" -ForegroundColor Cyan

# Télécharger plink
$plink = "$env:TEMP\plink.exe"
if (!(Test-Path $plink)) {
    Write-Host "Telechargement plink..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink -UseBasicParsing
    Write-Host "OK`n" -ForegroundColor Green
}

# Commandes à exécuter
$cmd = @"
echo '================================'
echo '     VPS CONNECTE - SUCCESS!'
echo '================================'
echo ''
echo '📊 SYSTEME:'
uname -a
echo ''
echo '⏱️ UPTIME:'
uptime
echo ''
echo '💾 DISQUE:'
df -h / | tail -1
echo ''
echo '🧠 MEMOIRE:'
free -h | grep Mem
echo ''
echo '================================'
echo '🐳 DOCKER CONTAINERS'
echo '================================'
docker ps --format 'table {{.Names}}\t{{.Status}}' 2>/dev/null || echo 'Docker non disponible'
echo ''
echo '================================'
echo '🌐 NGINX STATUS'
echo '================================'
systemctl is-active nginx 2>/dev/null && echo 'Nginx: ACTIF ✅' || echo 'Nginx: INACTIF ❌'
echo ''
echo '================================'
echo '🔐 SSL CERTIFICATS'
echo '================================'
certbot certificates 2>/dev/null | grep -E 'Certificate Name|Domains|Expiry Date' | head -10 || echo 'Aucun certificat'
echo ''
echo '================================'
"@

Write-Host "Connexion en cours..." -ForegroundColor Yellow

# Accepter la clé automatiquement avec echo y
echo y | & $plink -pw $VPS_PASSWORD root@$VPS_IP $cmd

Write-Host "`n=== CONNEXION TERMINEE ===" -ForegroundColor Green
Write-Host "`nPour session interactive:" -ForegroundColor Yellow
Write-Host "  $plink -pw `"$VPS_PASSWORD`" root@$VPS_IP`n" -ForegroundColor Gray
