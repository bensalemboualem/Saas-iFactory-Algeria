################################################################################
# 🔥 EXÉCUTER FIX MAINTENANT - AUTOMATIQUE
################################################################################

$VPS_IP = "46.224.3.125"
$VPS_USER = "root"

Write-Host "================================" -ForegroundColor Red
Write-Host "🔥 FIX AUTOMATIQUE EN COURS" -ForegroundColor Red
Write-Host "================================" -ForegroundColor Red
Write-Host ""

# Demander le mot de passe UNE SEULE FOIS
$VPS_PASSWORD = Read-Host "🔐 Mot de passe VPS (46.224.3.125)" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($VPS_PASSWORD)
$VPS_PASSWORD_PLAIN = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host ""
Write-Host "🚀 Connexion et correction en cours..." -ForegroundColor Green
Write-Host ""

# Script de fix complet
$fixScript = Get-Content "D:\IAFactory\rag-dz\fix-tout-maintenant.sh" -Raw

# Sauvegarder temporairement
$tempScript = "$env:TEMP\fix-vps-now.sh"
$fixScript | Out-File -FilePath $tempScript -Encoding UTF8 -NoNewline

# Vérifier plink
$plinkPath = Get-Command plink -ErrorAction SilentlyContinue

if ($plinkPath) {
    Write-Host "📤 Copie du script..." -ForegroundColor Cyan

    # Accepter l'empreinte
    echo y | & plink -batch -pw $VPS_PASSWORD_PLAIN "${VPS_USER}@${VPS_IP}" "exit" 2>$null

    # Copier
    & pscp -batch -pw $VPS_PASSWORD_PLAIN $tempScript "${VPS_USER}@${VPS_IP}:/tmp/fix-now.sh"

    Write-Host "✅ Script copié" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔥 EXÉCUTION DES CORRECTIONS..." -ForegroundColor Red
    Write-Host ""

    # Exécuter
    & plink -batch -pw $VPS_PASSWORD_PLAIN "${VPS_USER}@${VPS_IP}" "bash /tmp/fix-now.sh"

    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "✅ CORRECTIONS TERMINÉES!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Testez maintenant (Ctrl+Shift+R):" -ForegroundColor Cyan
    Write-Host "   https://iafactory.ch" -ForegroundColor Green
    Write-Host "   https://iafactoryalgeria.com" -ForegroundColor Green

} else {
    Write-Host "⚠️  PuTTY non trouvé, tentative avec SSH natif..." -ForegroundColor Yellow

    $sshPath = Get-Command ssh -ErrorAction SilentlyContinue
    if ($sshPath) {
        Write-Host "📡 Utilisation de OpenSSH..." -ForegroundColor Cyan
        Write-Host ""
        Write-Host "⚠️  Vous devrez entrer le mot de passe manuellement" -ForegroundColor Yellow
        Write-Host ""

        # Créer un script qui copie et exécute
        $sshCommand = @"
bash -c '$(Get-Content $tempScript -Raw | ForEach-Object { $_ -replace "'", "'\''"})'
"@

        ssh "${VPS_USER}@${VPS_IP}" $sshCommand

    } else {
        Write-Host "❌ Ni PuTTY ni SSH trouvés!" -ForegroundColor Red
        Write-Host ""
        Write-Host "📖 Copiez ce script et exécutez sur le VPS:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host $fixScript -ForegroundColor Gray
    }
}

# Nettoyer
Remove-Item $tempScript -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Appuyez sur une touche..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
