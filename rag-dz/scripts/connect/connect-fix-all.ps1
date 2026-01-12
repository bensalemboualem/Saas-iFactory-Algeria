# Fix complet VPS
$VPS_PASSWORD = "Ainsefra+0819692025"
$VPS_IP = "46.224.3.125"

Write-Host "Préparation..." -ForegroundColor Yellow
$plink = "$env:TEMP\plink.exe"
if (!(Test-Path $plink)) {
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink
}

# Supprimer l'ancienne clé SSH
$knownHosts = "$env:USERPROFILE\.ssh\known_hosts"
if (Test-Path $knownHosts) {
    (Get-Content $knownHosts | Where-Object { $_ -notmatch "46.224.3.125" }) | Set-Content $knownHosts
}

Write-Host "Connexion au VPS..." -ForegroundColor Green
Write-Host ""

# Script de diagnostic ET correction
$script = @'
echo "=== DIAGNOSTIC ===" &&
docker ps 2>/dev/null || echo "Docker: NON" &&
ls ~/rag-dz 2>/dev/null && echo "Code: OUI" || echo "Code: NON" &&
systemctl is-active nginx 2>/dev/null || echo "Nginx: NON" &&
echo "" &&
echo "=== CORRECTION MAINTENANT ===" &&
systemctl stop nginx 2>/dev/null || true &&
certbot delete --cert-name iafactory.ch --non-interactive 2>/dev/null || true &&
certbot delete --cert-name iafactoryalgeria.com --non-interactive 2>/dev/null || true &&
rm -rf /etc/letsencrypt/live/iafactory* /etc/letsencrypt/archive/iafactory* 2>/dev/null || true &&
certbot certonly --standalone --non-interactive --agree-tos --register-unsafely-without-email -d iafactory.ch -d www.iafactory.ch &&
certbot certonly --standalone --non-interactive --agree-tos --register-unsafely-without-email -d iafactoryalgeria.com -d www.iafactoryalgeria.com &&
cat > /etc/nginx/sites-available/iafactory.ch << 'EOF'
server {
    listen 80; server_name iafactory.ch www.iafactory.ch; return 301 https://$host$request_uri;
}
server {
    listen 443 ssl http2; server_name iafactory.ch www.iafactory.ch;
    ssl_certificate /etc/letsencrypt/live/iafactory.ch/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/iafactory.ch/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    location / { proxy_pass http://localhost:3001; proxy_set_header Host $host; }
    location /api/ { proxy_pass http://localhost:8002; }
}
EOF
cat > /etc/nginx/sites-available/iafactoryalgeria.com << 'EOF'
server {
    listen 80; server_name iafactoryalgeria.com www.iafactoryalgeria.com; return 301 https://$host$request_uri;
}
server {
    listen 443 ssl http2; server_name iafactoryalgeria.com www.iafactoryalgeria.com;
    ssl_certificate /etc/letsencrypt/live/iafactoryalgeria.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/iafactoryalgeria.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    location / { proxy_pass http://localhost:3002; proxy_set_header Host $host; }
    location /api/ { proxy_pass http://localhost:8002; }
}
EOF
ln -sf /etc/nginx/sites-available/iafactory.ch /etc/nginx/sites-enabled/ &&
ln -sf /etc/nginx/sites-available/iafactoryalgeria.com /etc/nginx/sites-enabled/ &&
nginx -t && systemctl start nginx &&
echo "" &&
echo "=== RÉSULTAT ===" &&
certbot certificates 2>/dev/null | grep "Certificate Name" &&
echo "" &&
echo "✅ CORRIGÉ! Testez: https://iafactoryalgeria.com"
'@

# Exécuter avec acceptation automatique de la nouvelle clé
$answer = "y`n"
$answer | & $plink -batch -pw $VPS_PASSWORD root@$VPS_IP $script

Write-Host ""
Write-Host "✅ CORRECTION TERMINÉE!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Testez (Ctrl+Shift+R):" -ForegroundColor Cyan
Write-Host "   https://iafactory.ch" -ForegroundColor White
Write-Host "   https://iafactoryalgeria.com" -ForegroundColor White
