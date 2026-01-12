$file = "D:\IAFactory\iafactory-academy\docker-compose.yml"
$content = Get-Content $file -Raw
$content = $content -replace '"8000:8200"', '"8200:8000"'
$content = $content -replace '"3000:3100"', '"3100:3000"'
Set-Content -Path $file -Value $content -NoNewline
Write-Host "Ports docker-compose corriges" -ForegroundColor Green
