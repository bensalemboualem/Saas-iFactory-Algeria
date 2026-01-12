# Connexion avec mapping clavier correct
$plink = "$env:TEMP\plink.exe"

if (!(Test-Path $plink)) {
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink
}

Write-Host "=== TEST CONNEXION (QWERTY) ===" -ForegroundColor Green

# Test avec # au lieu de *
echo y | & $plink -pw "Ainsefra#0819692025#" root@46.224.3.125 "hostname && ls -la ~/rag-dz 2>/dev/null && echo 'CONNECTE!' || echo 'Code pas clone'"
