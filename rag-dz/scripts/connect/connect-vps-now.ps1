# Connexion VPS immédiate
$plink = "$env:TEMP\plink.exe"
if (!(Test-Path $plink)) {
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink
}

Write-Host "Connexion..." -ForegroundColor Green

# Diagnostic
& $plink -no-antispoof -pw "Ainsefra+0819692025" root@46.224.3.125 "docker ps 2>/dev/null || echo 'Docker: NON' && ls ~/rag-dz 2>/dev/null && echo 'Code: OUI' || echo 'Code: NON'"

Write-Host ""
Write-Host "Voulez-vous installer Docker maintenant? (o/n)" -ForegroundColor Yellow
$reponse = Read-Host

if ($reponse -eq "o") {
    Write-Host "Installation Docker en cours..." -ForegroundColor Cyan

    $installScript = "apt-get update && apt-get install -y ca-certificates curl gnupg git nginx certbot python3-certbot-nginx && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && echo 'deb [arch=`$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu `$(lsb_release -cs) stable' | tee /etc/apt/sources.list.d/docker.list && apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin && docker --version"

    & $plink -no-antispoof -pw "Ainsefra+0819692025" root@46.224.3.125 $installScript

    Write-Host ""
    Write-Host "Docker installé!" -ForegroundColor Green
}
