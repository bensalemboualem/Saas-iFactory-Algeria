# Fix VPS - Acceptation automatique de la clé SSH
$VPS_PASSWORD = "Ainsefra+0819692025"
$VPS_IP = "46.224.3.125"

Write-Host "Téléchargement plink..." -ForegroundColor Yellow
$plink = "$env:TEMP\plink.exe"
if (!(Test-Path $plink)) {
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink
}

Write-Host "Connexion au VPS (acceptation automatique clé SSH)..." -ForegroundColor Green
Write-Host ""

# Script complet
$fixScript = @'
echo "=== FIX SSL MAINTENANT ===" &&
systemctl stop nginx 2>/dev/null &&
certbot delete --cert-name iafactory.ch --non-interactive 2>/dev/null; true &&
certbot delete --cert-name iafactoryalgeria.com --non-interactive 2>/dev/null; true &&
rm -rf /etc/letsencrypt/live/iafactory* /etc/letsencrypt/archive/iafactory* 2>/dev/null; true &&
certbot certonly --standalone --non-interactive --agree-tos --register-unsafely-without-email -d iafactory.ch -d www.iafactory.ch &&
certbot certonly --standalone --non-interactive --agree-tos --register-unsafely-without-email -d iafactoryalgeria.com -d www.iafactoryalgeria.com &&
cat > /etc/nginx/sites-available/iafactory.ch << 'EOFCH'
server {listen 80;server_name iafactory.ch www.iafactory.ch;return 301 https://$host$request_uri;}
server {listen 443 ssl http2;server_name iafactory.ch www.iafactory.ch;ssl_certificate /etc/letsencrypt/live/iafactory.ch/fullchain.pem;ssl_certificate_key /etc/letsencrypt/live/iafactory.ch/privkey.pem;ssl_protocols TLSv1.2 TLSv1.3;location / {proxy_pass http://localhost:3001;proxy_set_header Host $host;}location /api/ {proxy_pass http://localhost:8002;}}
EOFCH
cat > /etc/nginx/sites-available/iafactoryalgeria.com << 'EOFDZ'
server {listen 80;server_name iafactoryalgeria.com www.iafactoryalgeria.com;return 301 https://$host$request_uri;}
server {listen 443 ssl http2;server_name iafactoryalgeria.com www.iafactoryalgeria.com;ssl_certificate /etc/letsencrypt/live/iafactoryalgeria.com/fullchain.pem;ssl_certificate_key /etc/letsencrypt/live/iafactoryalgeria.com/privkey.pem;ssl_protocols TLSv1.2 TLSv1.3;location / {proxy_pass http://localhost:3002;proxy_set_header Host $host;}location /api/ {proxy_pass http://localhost:8002;}}
EOFDZ
ln -sf /etc/nginx/sites-available/iafactory.ch /etc/nginx/sites-enabled/ &&
ln -sf /etc/nginx/sites-available/iafactoryalgeria.com /etc/nginx/sites-enabled/ &&
nginx -t && systemctl start nginx &&
certbot certificates &&
echo "" &&
echo "✅ CORRIGÉ!"
'@

# Utiliser echo pour envoyer "y" automatiquement
$process = Start-Process -FilePath $plink -ArgumentList "-batch","-pw",$VPS_PASSWORD,"root@$VPS_IP",$fixScript -NoNewWindow -Wait -PassThru -RedirectStandardInput "$env:TEMP\yes.txt"

# Créer un fichier avec "y"
"y" | Out-File -FilePath "$env:TEMP\yes.txt" -Encoding ASCII

# Réessayer avec -hostkey acceptall (version récente de plink)
& $plink -no-antispoof -pw $VPS_PASSWORD root@$VPS_IP $fixScript

Write-Host ""
Write-Host "✅ FAIT!" -ForegroundColor Green
