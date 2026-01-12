# Connexion simple au VPS
$plink = "$env:TEMP\plink.exe"

if (!(Test-Path $plink)) {
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink
}

Write-Host "Connexion au VPS..." -ForegroundColor Green

# Juste se connecter et afficher hostname
echo y | & $plink -pw "Ainsefra*0819692025*" root@46.224.3.125 "hostname && pwd && whoami"
