# Installation Docker sur VPS
$plink = "$env:TEMP\plink.exe"

if (!(Test-Path $plink)) {
    Write-Host "Téléchargement plink..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink
}

Write-Host "=== INSTALLATION DOCKER SUR VPS ===" -ForegroundColor Cyan
Write-Host ""

# Commande d'installation complète
$installCmd = @"
apt-get update && apt-get install -y ca-certificates curl gnupg git nginx certbot python3-certbot-nginx && install -m 0755 -d /etc/apt/keyrings && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && chmod a+r /etc/apt/keyrings/docker.gpg && echo 'deb [arch=`$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu `$(lsb_release -cs) stable' | tee /etc/apt/sources.list.d/docker.list > /dev/null && apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin && systemctl start docker && systemctl enable docker && docker --version && echo 'DOCKER INSTALLE!'
"@

Write-Host "Connexion et installation (cela prendra 3-5 minutes)..." -ForegroundColor Green
Write-Host ""

# Exécution
echo y | & $plink -pw "Ainsefra*0819692025*" root@46.224.3.125 $installCmd

Write-Host ""
Write-Host "=== TERMINE ===" -ForegroundColor Green
