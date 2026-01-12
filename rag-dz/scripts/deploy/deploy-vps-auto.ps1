# Déploiement automatique sur VPS
$plink = "$env:TEMP\plink.exe"
$pscp = "$env:TEMP\pscp.exe"

# Télécharger plink et pscp
if (!(Test-Path $plink)) {
    Write-Host "Téléchargement plink..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink
}

if (!(Test-Path $pscp)) {
    Write-Host "Téléchargement pscp..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/pscp.exe" -OutFile $pscp
}

$VPS_PW = "Ainsefra+0819692025"
$VPS_IP = "46.224.3.125"

Write-Host "=== DEPLOIEMENT AUTOMATIQUE ===" -ForegroundColor Cyan
Write-Host ""

# Accepter la clé SSH
Write-Host "Acceptation clé SSH..." -ForegroundColor Yellow
echo y | & $plink -pw $VPS_PW root@$VPS_IP "echo 'Connecte'" 2>&1 | Out-Null

# Transférer le script
Write-Host "Transfert du script..." -ForegroundColor Yellow
& $pscp -batch -pw $VPS_PW "setup-vps.sh" root@${VPS_IP}:/root/setup-vps.sh

# Rendre exécutable et lancer
Write-Host "Exécution du script..." -ForegroundColor Green
Write-Host ""

& $plink -batch -pw $VPS_PW root@$VPS_IP "chmod +x /root/setup-vps.sh && /root/setup-vps.sh"

Write-Host ""
Write-Host "=== TERMINE ===" -ForegroundColor Green
