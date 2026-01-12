# Connexion SSH au VPS - Version Simple
$VPS_IP = "46.224.3.125"
$VPS_PASSWORD = "Ainsefra+0819692025"

Write-Host "`n=== CONNEXION VPS IAFACTORY ===" -ForegroundColor Cyan
Write-Host "Serveur: root@$VPS_IP`n" -ForegroundColor Yellow

# Télécharger plink
$plink = "$env:TEMP\plink.exe"
if (!(Test-Path $plink)) {
    Write-Host "Telechargement plink..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink -UseBasicParsing
}

# Commande simple
$cmd = 'echo "=== VPS STATUS ===" && uname -a && echo "" && docker ps 2>/dev/null'

# Connexion avec -hostkey pour accepter automatiquement
# La clé SSH du serveur est: ssh-ed25519 255 SHA256:nbUSYoWSzfdX2kRJCRbR9ljbpT8LpPlwxmTQLR9EBn8
& $plink -hostkey "ed25519:255:nbUSYoWSzfdX2kRJCRbR9ljbpT8LpPlwxmTQLR9EBn8" -batch -pw $VPS_PASSWORD root@$VPS_IP $cmd

Write-Host "`n=== CONNEXION OK ===" -ForegroundColor Green
