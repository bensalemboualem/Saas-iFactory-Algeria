################################################################################
# 🔥 CORRECTION AUTOMATIQUE VPS - SANS INTERVENTION
################################################################################

$VPS_IP = "46.224.3.125"
$VPS_USER = "root"

Write-Host "================================" -ForegroundColor Red
Write-Host "🔥 CORRECTION VPS AUTOMATIQUE" -ForegroundColor Red
Write-Host "================================" -ForegroundColor Red
Write-Host ""

# Demander le mot de passe UNE SEULE FOIS
$VPS_PASSWORD = Read-Host "Mot de passe VPS" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($VPS_PASSWORD)
$VPS_PWD = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host ""
Write-Host "🚀 Connexion et correction en cours..." -ForegroundColor Green
Write-Host ""

# Script de correction complet
$fixScript = @'
systemctl stop nginx
certbot delete --cert-name iafactory.ch --non-interactive 2>/dev/null || true
certbot delete --cert-name iafactoryalgeria.com --non-interactive 2>/dev/null || true
rm -rf /etc/letsencrypt/live/iafactory.ch* /etc/letsencrypt/live/iafactoryalgeria.com*
rm -rf /etc/letsencrypt/archive/iafactory.ch* /etc/letsencrypt/archive/iafactoryalgeria.com*
rm -rf /etc/letsencrypt/renewal/*.conf
certbot certonly --standalone --non-interactive --agree-tos --register-unsafely-without-email -d iafactory.ch -d www.iafactory.ch
certbot certonly --standalone --non-interactive --agree-tos --register-unsafely-without-email -d iafactoryalgeria.com -d www.iafactoryalgeria.com
cat > /etc/nginx/sites-available/iafactory.ch << 'EOFCH'
server {
    listen 80;
    server_name iafactory.ch www.iafactory.ch;
    return 301 https://$host$request_uri;
}
server {
    listen 443 ssl http2;
    server_name iafactory.ch www.iafactory.ch;
    ssl_certificate /etc/letsencrypt/live/iafactory.ch/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/iafactory.ch/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    location / {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Tenant-ID "814c132a-1cdd-4db6-bc1f-21abd21ec37d";
    }
    location /api/ {
        proxy_pass http://localhost:8002;
        proxy_set_header X-Tenant-ID "814c132a-1cdd-4db6-bc1f-21abd21ec37d";
    }
}
EOFCH
cat > /etc/nginx/sites-available/iafactoryalgeria.com << 'EOFDZ'
server {
    listen 80;
    server_name iafactoryalgeria.com www.iafactoryalgeria.com;
    return 301 https://$host$request_uri;
}
server {
    listen 443 ssl http2;
    server_name iafactoryalgeria.com www.iafactoryalgeria.com;
    ssl_certificate /etc/letsencrypt/live/iafactoryalgeria.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/iafactoryalgeria.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    location / {
        proxy_pass http://localhost:3002;
        proxy_set_header Host $host;
        proxy_set_header X-Tenant-ID "922d243b-2dee-5ec7-cd2g-32bce32fd48e";
    }
    location /api/ {
        proxy_pass http://localhost:8002;
        proxy_set_header X-Tenant-ID "922d243b-2dee-5ec7-cd2g-32bce32fd48e";
    }
}
EOFDZ
ln -sf /etc/nginx/sites-available/iafactory.ch /etc/nginx/sites-enabled/
ln -sf /etc/nginx/sites-available/iafactoryalgeria.com /etc/nginx/sites-enabled/
nginx -t && systemctl start nginx
certbot certificates
curl -I https://iafactory.ch | head -3
curl -I https://iafactoryalgeria.com | head -3
'@

$tempScript = "$env:TEMP\fix-vps.sh"
$fixScript | Out-File -FilePath $tempScript -Encoding ASCII -NoNewline

# Essayer avec plink d'abord
$plink = Get-Command plink -ErrorAction SilentlyContinue

if ($plink) {
    Write-Host "✅ PuTTY trouvé, connexion..." -ForegroundColor Green

    # Accepter la clé
    echo y | & plink -batch -pw $VPS_PWD "$VPS_USER@$VPS_IP" "exit" 2>$null

    # Copier le script
    & pscp -batch -pw $VPS_PWD $tempScript "$VPS_USER@${VPS_IP}:/tmp/fix.sh"

    # Exécuter
    & plink -batch -pw $VPS_PWD "$VPS_USER@$VPS_IP" "bash /tmp/fix.sh"

    Write-Host ""
    Write-Host "✅ CORRIGÉ!" -ForegroundColor Green

} else {
    Write-Host "⚠️ PuTTY non trouvé, installation requise..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Téléchargement de PuTTY..." -ForegroundColor Cyan

    # Télécharger plink
    $plinkUrl = "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe"
    $plinkPath = "$env:TEMP\plink.exe"

    Invoke-WebRequest -Uri $plinkUrl -OutFile $plinkPath

    Write-Host "✅ PuTTY téléchargé" -ForegroundColor Green
    Write-Host "🚀 Connexion..." -ForegroundColor Cyan

    # Accepter la clé
    echo y | & $plinkPath -batch -pw $VPS_PWD "$VPS_USER@$VPS_IP" "exit" 2>$null

    # Exécuter directement
    & $plinkPath -batch -pw $VPS_PWD "$VPS_USER@$VPS_IP" $fixScript

    Write-Host ""
    Write-Host "✅ CORRIGÉ!" -ForegroundColor Green
}

Remove-Item $tempScript -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🌐 Testez (Ctrl+Shift+R):" -ForegroundColor Cyan
Write-Host "   https://iafactory.ch" -ForegroundColor Green
Write-Host "   https://iafactoryalgeria.com" -ForegroundColor Green
Write-Host ""

Read-Host "Appuyez sur Entrée"
