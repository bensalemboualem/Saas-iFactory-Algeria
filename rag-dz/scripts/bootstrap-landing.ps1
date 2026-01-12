param(
    [switch]$ForceBackup
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$repoRoot = Split-Path -Parent $scriptDir
$sourceFile = Join-Path $repoRoot 'landing-complete-responsive.html'
$backupFile = Join-Path $repoRoot 'landing-complete-responsive.base.html'

if (-not (Test-Path $sourceFile)) {
    Write-Error "La page responsive ($sourceFile) est introuvable."
    exit 1
}

if ($ForceBackup -or -not (Test-Path $backupFile)) {
    Copy-Item $sourceFile $backupFile -Force
    Write-Host "Copie de sauvegarde créée → $backupFile"
} else {
    Write-Host "Sauvegarde existante détectée ($backupFile). Utilise -ForceBackup pour écraser."
}

$launcher = Join-Path $scriptDir 'start-landing-servers.ps1'
Write-Host "Démarrage des landing pages via $launcher"
& $launcher
