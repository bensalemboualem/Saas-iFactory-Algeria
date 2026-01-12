# Exécution complète sur VPS
$plink = "$env:TEMP\plink.exe"

if (!(Test-Path $plink)) {
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink
}

Write-Host "=== CONNEXION ET EXECUTION ===" -ForegroundColor Green

# Vérifier si le code existe
$checkCmd = "ls -la ~/rag-dz 2>/dev/null && echo 'CODE_EXISTE' || echo 'CODE_NEXISTE_PAS'"

Write-Host "Vérification du code..." -ForegroundColor Yellow
$result = echo y | & $plink -pw "Ainsefra*0819692025*" root@46.224.3.125 $checkCmd 2>&1

Write-Host $result
Write-Host ""

if ($result -match "CODE_NEXISTE_PAS") {
    Write-Host "Le code n'existe pas. Besoin de l'URL du repo GitHub." -ForegroundColor Red
} else {
    Write-Host "Le code existe! Lancement des containers..." -ForegroundColor Green

    # Lancer les containers
    $launchCmd = "cd ~/rag-dz && git pull && docker compose up -d && sleep 5 && docker ps"

    $launchResult = & $plink -batch -pw "Ainsefra*0819692025*" root@46.224.3.125 $launchCmd 2>&1

    Write-Host $launchResult
}

Write-Host ""
Write-Host "=== TERMINE ===" -ForegroundColor Green
