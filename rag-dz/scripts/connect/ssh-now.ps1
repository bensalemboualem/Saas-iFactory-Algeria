# Connexion IMMEDIATE au VPS
$VPS_IP = "46.224.3.125"
$VPS_PASSWORD = "Ainsefra+0819692025"

Write-Host "`n=== CONNEXION VPS ===" -ForegroundColor Cyan

# Plink
$plink = "$env:TEMP\plink.exe"
if (!(Test-Path $plink)) {
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink -UseBasicParsing
}

# Commandes
$cmd = "echo '=== VPS CONNECTE ===' && uname -a && echo '' && docker ps 2>/dev/null && echo '' && systemctl is-active nginx 2>/dev/null"

Write-Host "root@$VPS_IP`n" -ForegroundColor Yellow

# Essayer avec -no-antispoof (version récente de plink)
& $plink -no-antispoof -pw $VPS_PASSWORD root@$VPS_IP $cmd

Write-Host "`n=== FIN ===" -ForegroundColor Green
