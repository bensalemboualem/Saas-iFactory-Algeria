# Démarrage IAFactory

Write-Host " Démarrage IAFactory..." -ForegroundColor Cyan

# Gateway
cd D:\IAFactory\iafactory-gateway-python
docker-compose up -d
Start-Sleep -Seconds 10

# Test
curl http://localhost:3001/health -UseBasicParsing

Write-Host "`n Gateway démarré sur http://localhost:3001`n" -ForegroundColor Green
