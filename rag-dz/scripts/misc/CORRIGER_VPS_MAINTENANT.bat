@echo off
setlocal enabledelayedexpansion
color 0C
cls

echo ================================
echo CORRECTION VPS AUTOMATIQUE
echo ================================
echo.

set /p VPS_PASSWORD="Mot de passe VPS: "
echo.
echo Connexion...
echo.

REM Télécharger plink si nécessaire
if not exist "%TEMP%\plink.exe" (
    echo Telechargement de PuTTY...
    powershell -Command "Invoke-WebRequest -Uri 'https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe' -OutFile '%TEMP%\plink.exe'"
)

REM Script de correction
set SCRIPT=^
systemctl stop nginx^&^&^
certbot delete --cert-name iafactory.ch --non-interactive 2^>^/dev/null ^|^| true^&^&^
certbot delete --cert-name iafactoryalgeria.com --non-interactive 2^>^/dev/null ^|^| true^&^&^
rm -rf /etc/letsencrypt/live/iafactory.ch* /etc/letsencrypt/live/iafactoryalgeria.com*^&^&^
certbot certonly --standalone --non-interactive --agree-tos --register-unsafely-without-email -d iafactory.ch -d www.iafactory.ch^&^&^
certbot certonly --standalone --non-interactive --agree-tos --register-unsafely-without-email -d iafactoryalgeria.com -d www.iafactoryalgeria.com^&^&^
cat ^> /etc/nginx/sites-available/iafactory.ch ^<^< 'EOF'^
server {^
    listen 80;^
    server_name iafactory.ch www.iafactory.ch;^
    return 301 https://$host$request_uri;^
}^
server {^
    listen 443 ssl http2;^
    server_name iafactory.ch www.iafactory.ch;^
    ssl_certificate /etc/letsencrypt/live/iafactory.ch/fullchain.pem;^
    ssl_certificate_key /etc/letsencrypt/live/iafactory.ch/privkey.pem;^
    ssl_protocols TLSv1.2 TLSv1.3;^
    location / { proxy_pass http://localhost:3001; proxy_set_header Host $host; }^
    location /api/ { proxy_pass http://localhost:8002; }^
}^
EOF^
cat ^> /etc/nginx/sites-available/iafactoryalgeria.com ^<^< 'EOF'^
server {^
    listen 80;^
    server_name iafactoryalgeria.com www.iafactoryalgeria.com;^
    return 301 https://$host$request_uri;^
}^
server {^
    listen 443 ssl http2;^
    server_name iafactoryalgeria.com www.iafactoryalgeria.com;^
    ssl_certificate /etc/letsencrypt/live/iafactoryalgeria.com/fullchain.pem;^
    ssl_certificate_key /etc/letsencrypt/live/iafactoryalgeria.com/privkey.pem;^
    ssl_protocols TLSv1.2 TLSv1.3;^
    location / { proxy_pass http://localhost:3002; proxy_set_header Host $host; }^
    location /api/ { proxy_pass http://localhost:8002; }^
}^
EOF^
ln -sf /etc/nginx/sites-available/iafactory.ch /etc/nginx/sites-enabled/^&^&^
ln -sf /etc/nginx/sites-available/iafactoryalgeria.com /etc/nginx/sites-enabled/^&^&^
nginx -t ^&^& systemctl start nginx^&^&^
certbot certificates

echo y | "%TEMP%\plink.exe" -batch -pw %VPS_PASSWORD% root@46.224.3.125 "exit" 2>nul
"%TEMP%\plink.exe" -batch -pw %VPS_PASSWORD% root@46.224.3.125 "%SCRIPT%"

echo.
echo ================================
echo CORRIGE!
echo ================================
echo.
echo Testez (Ctrl+Shift+R):
echo    https://iafactory.ch
echo    https://iafactoryalgeria.com
echo.
pause
