# Connexion FORCÉE au VPS - Accepte automatiquement la clé
$VPS_IP = "46.224.3.125"
$VPS_PASSWORD = "Ainsefra+0819692025"

Write-Host "=== CONNEXION VPS FORCEE ===" -ForegroundColor Green

# Télécharger plink
$plink = "$env:TEMP\plink.exe"
if (!(Test-Path $plink)) {
    Write-Host "Telechargement plink..."
    Invoke-WebRequest -Uri "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe" -OutFile $plink -UseBasicParsing
}

# Commandes
$cmd = @"
echo '=== CONNECTE AU VPS ==='
echo ''
echo 'Systeme:'
uname -a
echo ''
echo 'Uptime:'
uptime
echo ''
echo 'Espace disque:'
df -h / | tail -1
echo ''
echo 'Memoire:'
free -h | grep Mem
echo ''
echo 'Docker containers:'
docker ps --format 'table {{.Names}}\t{{.Status}}' 2>/dev/null || echo 'Docker non disponible'
echo ''
echo 'Nginx:'
systemctl is-active nginx 2>/dev/null || echo 'Nginx non actif'
echo ''
echo 'SSL Certificats:'
certbot certificates 2>/dev/null | grep -E 'Certificate Name|Domains|Expiry' | head -10 || echo 'Aucun certificat'
"@

Write-Host "Connexion a root@$VPS_IP..." -ForegroundColor Cyan
Write-Host ""

# Utiliser Start-Process pour gérer l'interaction
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $plink
$psi.Arguments = "-pw `"$VPS_PASSWORD`" root@$VPS_IP `"$cmd`""
$psi.RedirectStandardInput = $true
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.UseShellExecute = $false

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $psi
$process.Start() | Out-Null

# Envoyer "y" pour accepter la clé
$process.StandardInput.WriteLine("y")
$process.StandardInput.Close()

# Lire la sortie
$output = $process.StandardOutput.ReadToEnd()
$errors = $process.StandardError.ReadToEnd()

$process.WaitForExit()

Write-Host $output
if ($errors) { Write-Host $errors -ForegroundColor Yellow }

Write-Host ""
Write-Host "=== FIN CONNEXION ===" -ForegroundColor Green
