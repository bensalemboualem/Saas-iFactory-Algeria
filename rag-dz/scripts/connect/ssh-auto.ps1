# Connexion SSH au VPS avec acceptation automatique de la clé
$VPS_IP = "46.224.3.125"
$VPS_PASSWORD = "Ainsefra+0819692025"

Write-Host "`n=== CONNEXION VPS IAFACTORY ===" -ForegroundColor Cyan
Write-Host "Serveur: root@$VPS_IP`n" -ForegroundColor Yellow

# Télécharger plink si nécessaire
$plink = "$env:TEMP\plink.exe"
if (!(Test-Path $plink)) {
    Write-Host "Telechargement plink..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink -UseBasicParsing
    Write-Host "OK`n" -ForegroundColor Green
}

# Commandes à exécuter
$cmd = @"
echo '=== VPS STATUS ==='
echo ''
echo 'Systeme:'
uname -a
echo ''
echo 'Uptime:'
uptime
echo ''
echo 'Docker:'
docker ps --format 'table {{.Names}}\t{{.Status}}' 2>/dev/null || echo 'Docker non disponible'
echo ''
echo 'Nginx:'
systemctl is-active nginx 2>/dev/null || echo 'Nginx non actif'
"@

# Créer un fichier temporaire avec "y" pour accepter la clé
$yesFile = "$env:TEMP\yes.txt"
"y" | Out-File -FilePath $yesFile -Encoding ASCII -NoNewline

# Connexion avec input pour accepter la clé
Write-Host "Connexion..." -ForegroundColor Yellow
Get-Content $yesFile | & $plink -pw $VPS_PASSWORD root@$VPS_IP $cmd

Remove-Item $yesFile -ErrorAction SilentlyContinue

Write-Host "`n=== CONNEXION TERMINEE ===" -ForegroundColor Green
