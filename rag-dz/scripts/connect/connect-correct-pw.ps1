# Connexion VPS avec le bon mot de passe
$plink = "$env:TEMP\plink.exe"

# Télécharger plink si nécessaire
if (!(Test-Path $plink)) {
    Write-Host "Téléchargement plink..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink
}

Write-Host "=== CONNEXION VPS ===" -ForegroundColor Green

# Commande simple de diagnostic
$cmd = "docker --version 2>&1 || echo 'Docker NON installe'"

# Connexion avec le bon mot de passe
$response = echo y | & $plink -pw "Ainsefra*0819692025*" root@46.224.3.125 $cmd 2>&1

Write-Host $response
Write-Host ""
Write-Host "=== TERMINE ===" -ForegroundColor Green
