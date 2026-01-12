# Connexion et diagnostic VPS
$plink = "$env:TEMP\plink.exe"

if (!(Test-Path $plink)) {
    Write-Host "Téléchargement plink..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink
    Write-Host "Plink téléchargé!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Connexion au VPS 46.224.3.125..." -ForegroundColor Cyan
Write-Host ""

# Accepter la clé SSH automatiquement
$acceptKey = "y`n"
$acceptKey | & $plink -pw "Ainsefra+0819692025" root@46.224.3.125 "exit" 2>&1 | Out-Null

# Diagnostic
Write-Host "=== DIAGNOSTIC VPS ===" -ForegroundColor Yellow
Write-Host ""

& $plink -batch -pw "Ainsefra+0819692025" root@46.224.3.125 "docker ps 2>/dev/null || echo 'Docker: NON' && echo '' && ls -la ~/rag-dz 2>/dev/null && echo 'Code: OUI' || echo 'Code: NON'"

Write-Host ""
Write-Host "=== TERMINÉ ===" -ForegroundColor Green
