# Connexion SSH simple au VPS
$VPS_IP = "46.224.3.125"
$VPS_PASSWORD = "Ainsefra+0819692025"

Write-Host "🔌 Connexion SSH au VPS IAFactory" -ForegroundColor Cyan
Write-Host "📍 Serveur: root@$VPS_IP" -ForegroundColor Yellow
Write-Host ""

# Télécharger plink si nécessaire
$plink = "$env:TEMP\plink.exe"
if (!(Test-Path $plink)) {
    Write-Host "📥 Téléchargement de plink.exe..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink -UseBasicParsing
        Write-Host "✅ plink.exe téléchargé" -ForegroundColor Green
    } catch {
        Write-Host "❌ Erreur de téléchargement" -ForegroundColor Red
        exit 1
    }
}

Write-Host "🔍 Vérification du serveur..." -ForegroundColor Cyan
Write-Host ""

# Commandes à exécuter
$commands = @'
echo "✅ Connexion SSH réussie!"
echo ""
echo "═══════════════════════════════════════════"
echo "📊 INFORMATIONS SYSTÈME"
echo "═══════════════════════════════════════════"
echo ""
echo "🖥️  Système:"
uname -a
echo ""
echo "⏱️  Uptime:"
uptime
echo ""
echo "💾 Espace disque:"
df -h / | tail -1
echo ""
echo "🧠 Mémoire:"
free -h | grep Mem
echo ""
echo "═══════════════════════════════════════════"
echo "🐳 DOCKER CONTAINERS"
echo "═══════════════════════════════════════════"
docker ps --format 'table {{.Names}}\t{{.Status}}' 2>/dev/null || echo "Docker non disponible"
echo ""
echo "═══════════════════════════════════════════"
echo "🌐 NGINX STATUS"
echo "═══════════════════════════════════════════"
systemctl is-active nginx 2>/dev/null && echo "Nginx: ✅ Actif" || echo "Nginx: ❌ Inactif"
echo ""
echo "═══════════════════════════════════════════"
echo "🔐 CERTIFICATS SSL"
echo "═══════════════════════════════════════════"
certbot certificates 2>/dev/null | grep -E "(Certificate Name|Domains|Expiry Date)" || echo "Aucun certificat trouvé"
'@

# Exécution avec acceptation automatique de la clé
try {
    $answer = "y"
    $answer | & $plink -batch -pw $VPS_PASSWORD root@$VPS_IP $commands

    Write-Host ""
    Write-Host "════════════════════════════════════════" -ForegroundColor Green
    Write-Host "✅ Connexion terminée avec succès!" -ForegroundColor Green
    Write-Host "════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    Write-Host "💡 Pour une session interactive:" -ForegroundColor Yellow
    Write-Host "   $plink -pw `"$VPS_PASSWORD`" root@$VPS_IP" -ForegroundColor Gray

} catch {
    Write-Host ""
    Write-Host "❌ Erreur de connexion: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
