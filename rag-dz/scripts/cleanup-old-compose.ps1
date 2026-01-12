# =============================================================================
# SCRIPT: cleanup-old-compose.ps1
# Description: Archive les anciens fichiers docker-compose fragmentés
# Usage: .\scripts\cleanup-old-compose.ps1
# =============================================================================

param(
    [switch]$DryRun = $false,
    [switch]$Force = $false
)

$ErrorActionPreference = "Stop"

# Couleurs
function Write-Success { param($msg) Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Info { param($msg) Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Warn { param($msg) Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red }

# Configuration
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if (-not $ProjectRoot) { $ProjectRoot = Get-Location }

$ArchiveDir = Join-Path $ProjectRoot "infrastructure\docker\_archive_compose"
$FilesToArchive = @(
    "infrastructure\docker\docker-compose.essential.yml",
    "infrastructure\docker\docker-compose.simple.yml",
    "infrastructure\docker\docker-compose.prod.yml",
    "infrastructure\docker\docker-compose.production.yml",
    "infrastructure\docker\docker-compose.frontend.yml",
    "infrastructure\docker\docker-compose.apps.yml",
    "infrastructure\docker\docker-compose.extras.yml",
    "infrastructure\docker\docker-compose-local.yml",
    "infrastructure\docker\docker-compose-ai-agents.yml",
    "infrastructure\docker\docker-compose-ai-agents-phase2.yml",
    "infrastructure\docker\docker-compose-ai-agents-phase3.yml",
    "infrastructure\docker\docker-compose-ai-agents-phase4.yml"
)

# Fichiers à conserver (ne pas archiver)
$FilesToKeep = @(
    "docker-compose.yml",
    "docker-compose.minimal.yml",
    "infrastructure\docker\docker-compose.yml",
    "infrastructure\docker\docker-compose.minimal.yml"
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Magenta
Write-Host "  CLEANUP OLD DOCKER-COMPOSE FILES" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host ""

Write-Info "Project root: $ProjectRoot"
Write-Info "Archive dir: $ArchiveDir"

if ($DryRun) {
    Write-Warn "Mode DRY-RUN: aucune modification ne sera effectuée"
}

# Créer le dossier d'archive
if (-not $DryRun) {
    if (-not (Test-Path $ArchiveDir)) {
        New-Item -ItemType Directory -Path $ArchiveDir -Force | Out-Null
        Write-Success "Dossier d'archive créé: $ArchiveDir"
    }
}

# Compter les fichiers
$FilesFound = 0
$FilesMoved = 0
$FilesNotFound = 0

Write-Host ""
Write-Info "Fichiers à archiver:"
Write-Host ""

foreach ($RelativePath in $FilesToArchive) {
    $FullPath = Join-Path $ProjectRoot $RelativePath
    $FileName = Split-Path -Leaf $RelativePath

    if (Test-Path $FullPath) {
        $FilesFound++
        Write-Host "  [X] $RelativePath" -ForegroundColor Yellow

        if (-not $DryRun) {
            $DestPath = Join-Path $ArchiveDir $FileName

            # Gérer les doublons
            if (Test-Path $DestPath) {
                $Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
                $DestPath = Join-Path $ArchiveDir "$($FileName.Replace('.yml', ''))-$Timestamp.yml"
            }

            Move-Item -Path $FullPath -Destination $DestPath -Force
            $FilesMoved++
        }
    } else {
        $FilesNotFound++
        Write-Host "  [ ] $RelativePath (non trouvé)" -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RÉSUMÉ" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Fichiers trouvés:   $FilesFound" -ForegroundColor White
Write-Host "  Fichiers archivés:  $FilesMoved" -ForegroundColor Green
Write-Host "  Non trouvés:        $FilesNotFound" -ForegroundColor DarkGray
Write-Host ""

# Fichiers conservés
Write-Info "Fichiers Docker Compose actifs (conservés):"
Write-Host ""
foreach ($KeepFile in $FilesToKeep) {
    $FullPath = Join-Path $ProjectRoot $KeepFile
    if (Test-Path $FullPath) {
        Write-Host "  [*] $KeepFile" -ForegroundColor Green
    }
}

Write-Host ""

if ($DryRun) {
    Write-Warn "Mode DRY-RUN terminé. Relancer sans -DryRun pour effectuer les modifications."
} elseif ($FilesMoved -gt 0) {
    Write-Success "Cleanup terminé! $FilesMoved fichiers archivés dans:"
    Write-Host "  $ArchiveDir" -ForegroundColor Cyan

    # Créer un fichier README dans l'archive
    $ReadmePath = Join-Path $ArchiveDir "README.md"
    @"
# Archive Docker-Compose

Ces fichiers ont été archivés le $(Get-Date -Format "yyyy-MM-dd HH:mm:ss").

Ils ont été remplacés par les fichiers consolidés à la racine du projet:
- `docker-compose.yml` - Stack complète
- `docker-compose.minimal.yml` - Stack RAG minimale

Pour restaurer un fichier, déplacez-le vers son emplacement original.
"@ | Set-Content -Path $ReadmePath -Encoding UTF8

} else {
    Write-Info "Aucun fichier à archiver."
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Magenta
Write-Host "  PROCHAINES ÉTAPES" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "  1. Copier .env.docker.example vers .env" -ForegroundColor White
Write-Host "     cp .env.docker.example .env" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  2. Configurer les clés API dans .env" -ForegroundColor White
Write-Host ""
Write-Host "  3. Démarrer la stack minimale:" -ForegroundColor White
Write-Host "     docker compose -f docker-compose.minimal.yml up -d" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  4. Ou démarrer la stack complète:" -ForegroundColor White
Write-Host "     docker compose up -d" -ForegroundColor DarkGray
Write-Host ""
