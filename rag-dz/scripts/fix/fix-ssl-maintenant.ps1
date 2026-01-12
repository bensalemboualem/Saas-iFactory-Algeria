################################################################################
# 🔧 FIX SSL MAINTENANT - iafactoryalgeria.com
# Corrige ERR_CERT_COMMON_NAME_INVALID en un clic
################################################################################

$VPS_IP = "46.224.3.125"
$VPS_USER = "root"

Write-Host "================================" -ForegroundColor Red
Write-Host "🔧 FIX SSL URGENT" -ForegroundColor Red
Write-Host "================================" -ForegroundColor Red
Write-Host ""
Write-Host "Problème détecté:" -ForegroundColor Yellow
Write-Host "  ❌ ERR_CERT_COMMON_NAME_INVALID" -ForegroundColor Red
Write-Host "  ❌ Certificat SSL manquant pour iafactoryalgeria.com" -ForegroundColor Red
Write-Host ""

# Demander le mot de passe VPS
$VPS_PASSWORD = Read-Host "🔐 Mot de passe root VPS (46.224.3.125)" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($VPS_PASSWORD)
$VPS_PASSWORD_PLAIN = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host ""
Write-Host "🔥 Correction en cours..." -ForegroundColor Green
Write-Host ""

# Script de correction
$fixScript = @'
#!/bin/bash
set -e

echo "🔧 FIX SSL URGENT - iafactoryalgeria.com"
echo "========================================"
echo ""

# Arrêter Nginx
echo "1. Arrêt de Nginx..."
systemctl stop nginx

# Supprimer l'ancien certificat
echo "2. Nettoyage des anciens certificats..."
certbot delete --cert-name iafactoryalgeria.com --non-interactive 2>/dev/null || true

# Générer un nouveau certificat
echo "3. Génération du certificat SSL..."
certbot certonly \
    --standalone \
    --non-interactive \
    --agree-tos \
    --email support@iafactoryalgeria.com \
    -d iafactoryalgeria.com \
    --preferred-challenges http

# Vérifier le certificat
if [ -f /etc/letsencrypt/live/iafactoryalgeria.com/fullchain.pem ]; then
    echo "✅ Certificat créé avec succès!"

    # Créer la config Nginx
    cat > /etc/nginx/sites-available/iafactoryalgeria.com << 'EOFNGINX'
server {
    listen 80;
    server_name iafactoryalgeria.com www.iafactoryalgeria.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name iafactoryalgeria.com www.iafactoryalgeria.com;

    ssl_certificate /etc/letsencrypt/live/iafactoryalgeria.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/iafactoryalgeria.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header Access-Control-Allow-Origin "https://iafactoryalgeria.com" always;
    add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
    add_header Access-Control-Allow-Credentials "true" always;

    client_max_body_size 50M;

    location / {
        proxy_pass http://localhost:3002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Tenant-Profile "education";
        proxy_set_header X-Country "DZ";
    }

    location /api/ {
        proxy_pass http://localhost:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Tenant-Profile "education";
        proxy_set_header X-Country "DZ";
    }

    access_log /var/log/nginx/iafactoryalgeria.com-access.log;
    error_log /var/log/nginx/iafactoryalgeria.com-error.log;
}
EOFNGINX

    # Activer le site
    ln -sf /etc/nginx/sites-available/iafactoryalgeria.com /etc/nginx/sites-enabled/

    # Tester la config
    echo "4. Test de la configuration Nginx..."
    nginx -t

    # Démarrer Nginx
    echo "5. Redémarrage de Nginx..."
    systemctl start nginx

    echo ""
    echo "================================"
    echo "✅ SSL CORRIGÉ!"
    echo "================================"
    echo ""
    echo "🌐 Testez: https://iafactoryalgeria.com"
    echo ""

    # Test
    curl -I https://iafactoryalgeria.com 2>&1 | head -5

else
    echo "❌ Échec de création du certificat!"
    echo ""
    echo "Vérifiez que:"
    echo "  1. DNS pointe vers 46.224.3.125"
    echo "  2. Port 80 est ouvert"

    # Redémarrer Nginx quand même
    systemctl start nginx
    exit 1
fi
'@

# Sauvegarder le script
$tempScript = "$env:TEMP\fix-ssl-urgent.sh"
$fixScript | Out-File -FilePath $tempScript -Encoding UTF8 -NoNewline

# Vérifier Plink
$plinkPath = Get-Command plink -ErrorAction SilentlyContinue

if ($plinkPath) {
    Write-Host "📤 Copie du script sur le VPS..." -ForegroundColor Cyan

    # Accepter l'empreinte
    echo y | & plink -batch -pw $VPS_PASSWORD_PLAIN "${VPS_USER}@${VPS_IP}" "exit" 2>$null

    # Copier le script
    & pscp -batch -pw $VPS_PASSWORD_PLAIN $tempScript "${VPS_USER}@${VPS_IP}:/tmp/fix-ssl.sh"

    Write-Host "✅ Script copié" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Exécution du fix sur le VPS..." -ForegroundColor Cyan
    Write-Host ""

    # Exécuter
    & plink -batch -pw $VPS_PASSWORD_PLAIN "${VPS_USER}@${VPS_IP}" "bash /tmp/fix-ssl.sh"

    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "✅ FIX SSL TERMINÉ!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Testez maintenant:" -ForegroundColor Cyan
    Write-Host "   https://iafactoryalgeria.com" -ForegroundColor Green
    Write-Host ""
    Write-Host "💡 Rechargez avec Ctrl+Shift+R (hard refresh)" -ForegroundColor Yellow

} else {
    Write-Host "⚠️  PuTTY (plink) non trouvé" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📖 OPTION 1: Installer PuTTY" -ForegroundColor Cyan
    Write-Host "   https://www.putty.org/" -ForegroundColor White
    Write-Host ""
    Write-Host "📖 OPTION 2: Exécuter manuellement" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Connectez-vous:" -ForegroundColor Yellow
    Write-Host "   ssh root@46.224.3.125" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Puis collez:" -ForegroundColor Yellow
    Write-Host $fixScript -ForegroundColor Gray
}

# Nettoyer
Remove-Item $tempScript -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
