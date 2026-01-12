# Connexion et diagnostic VPS
$VPS_PASSWORD = "Ainsefra+0819692025"
$VPS_IP = "46.224.3.125"

Write-Host "Téléchargement plink si nécessaire..." -ForegroundColor Yellow
$plink = "$env:TEMP\plink.exe"
if (!(Test-Path $plink)) {
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink
    Write-Host "✅ Plink téléchargé" -ForegroundColor Green
}

Write-Host "Connexion au VPS $VPS_IP..." -ForegroundColor Cyan
Write-Host ""

# Accepter la clé SSH
echo y | & $plink -batch -pw $VPS_PASSWORD root@$VPS_IP "exit" 2>$null

# Diagnostic complet
$diagnosticScript = @'
echo "================================"
echo "🔍 DIAGNOSTIC VPS"
echo "================================"
echo ""
echo "=== DOCKER ==="
docker ps 2>/dev/null || echo "❌ Docker pas installé"
echo ""
echo "=== CODE ==="
ls -la ~/rag-dz 2>/dev/null || echo "❌ Code pas cloné"
echo ""
echo "=== NGINX ==="
systemctl status nginx --no-pager | head -3 2>/dev/null || echo "❌ Nginx pas actif"
echo ""
echo "=== SSL ==="
certbot certificates 2>/dev/null | grep "Certificate Name" || echo "❌ Pas de certificats"
echo ""
echo "=== PORTS ==="
curl -s -o /dev/null -w "CH (3001): %{http_code}\n" http://localhost:3001 || echo "❌ 3001 down"
curl -s -o /dev/null -w "DZ (3002): %{http_code}\n" http://localhost:3002 || echo "❌ 3002 down"
curl -s -o /dev/null -w "API (8002): %{http_code}\n" http://localhost:8002/health || echo "❌ 8002 down"
'@

& $plink -batch -pw $VPS_PASSWORD root@$VPS_IP $diagnosticScript

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "Diagnostic terminé!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
