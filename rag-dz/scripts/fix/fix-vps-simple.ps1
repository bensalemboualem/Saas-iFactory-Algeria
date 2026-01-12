$plink = "$env:TEMP\plink.exe"
if (!(Test-Path $plink)) {
    Write-Host "Téléchargement plink..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink
}

Write-Host "Connexion au VPS (avec acceptation de clé)..." -ForegroundColor Green
Write-Host ""

# Première connexion pour accepter la clé
$null = echo y | & $plink -pw "Ainsefra+0819692025" root@46.224.3.125 "exit" 2>&1

# Maintenant la vraie commande
$command = "echo '=== DIAGNOSTIC VPS ===' && docker ps 2>/dev/null || echo 'Docker pas installé' && echo '' && ls -la ~/rag-dz 2>/dev/null || echo 'Code pas cloné'"

& $plink -batch -pw "Ainsefra+0819692025" root@46.224.3.125 $command

Write-Host ""
Write-Host "Terminé!" -ForegroundColor Green
