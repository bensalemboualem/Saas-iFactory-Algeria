# Test IAFactory Gateway Chat API

$baseUrl = "http://localhost:3001"

Write-Host "🧪 Test IAFactory Gateway Chat API" -ForegroundColor Cyan
Write-Host "=" * 60

# Test 1: iaf-fast-llama (Groq)
Write-Host "`n1️⃣ Test iaf-fast-llama (Groq - Ultra Fast)..." -ForegroundColor Yellow

$body = @{
    model = "iaf-fast-llama"
    messages = @(
        @{
            role = "user"
            content = "Dis bonjour en français en une phrase courte"
        }
    )
    temperature = 0.7
    max_tokens = 100
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/v1/chat/completions" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✅ Réponse:" -ForegroundColor Green
    Write-Host $response.choices[0].message.content -ForegroundColor White
    Write-Host "Tokens: $($response.usage.total_tokens)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Erreur: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host $_.Exception.Response.StatusCode -ForegroundColor Red
}

# Test 2: iaf-cheap-deepseek
Write-Host "`n2️⃣ Test iaf-cheap-deepseek (DeepSeek - Économique)..." -ForegroundColor Yellow

$body = @{
    model = "iaf-cheap-deepseek"
    messages = @(
        @{
            role = "user"
            content = "Write a Python function to add two numbers"
        }
    )
    temperature = 0.7
    max_tokens = 150
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/v1/chat/completions" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✅ Réponse:" -ForegroundColor Green
    Write-Host $response.choices[0].message.content -ForegroundColor White
    Write-Host "Tokens: $($response.usage.total_tokens)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Erreur: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Streaming (iaf-fast-llama)
Write-Host "`n3️⃣ Test Streaming (iaf-fast-llama)..." -ForegroundColor Yellow
Write-Host "⚠️ Streaming SSE nécessite un client spécial (curl, EventSource)" -ForegroundColor Gray

Write-Host "`n✅ Tests terminés!" -ForegroundColor Green
Write-Host "`n📝 Pour tester streaming, utilise:" -ForegroundColor Cyan
Write-Host @"
curl http://localhost:3001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "iaf-fast-llama",
    "messages": [{"role": "user", "content": "Count to 5"}],
    "stream": true
  }'
"@ -ForegroundColor Gray
