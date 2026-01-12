# Test complet IAFactory
cd D:\IAFactory\iafactory-gateway-python
docker-compose up -d
Start-Sleep -Seconds 10

Write-Host "Tests providers..." -ForegroundColor Cyan
$body = @{model="gpt-3.5-turbo";messages=@(@{role="user";content="Test"});max_tokens=5} | ConvertTo-Json -Depth 10
curl http://localhost:3001/api/llm/chat/completions -Method POST -Body $body -ContentType "application/json" -UseBasicParsing | Select-Object StatusCode

curl http://localhost:3001/api/credits/test-user -UseBasicParsing | Select-Object Content

Write-Host "`nGateway OK" -ForegroundColor Green
