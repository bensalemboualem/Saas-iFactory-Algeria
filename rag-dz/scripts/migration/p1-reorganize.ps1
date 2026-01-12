# ============================================================================
# MIGRATION P1 - Reorganisation Structure
# ============================================================================
# Executer depuis la racine du projet: .\scripts\migration\p1-reorganize.ps1
# ============================================================================

$ErrorActionPreference = "Continue"
$ROOT = "D:\IAFactory\rag-dz"
Set-Location $ROOT

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[P1] MIGRATION P1 - REORGANISATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# 1. CREATION DOSSIER ARCHIVE APPS
# ============================================================================
Write-Host "[1/4] Creation apps/_archived/..." -ForegroundColor Yellow

$archivedPath = "apps\_archived"
if (-not (Test-Path $archivedPath)) {
    New-Item -Path $archivedPath -ItemType Directory | Out-Null
    Write-Host "   [OK] Dossier cree" -ForegroundColor Green
} else {
    Write-Host "   [SKIP] Existe deja" -ForegroundColor Gray
}

# Creer README pour le dossier archive
$archiveReadme = @"
# Apps Archivees

Ce dossier contient les applications inactives ou en pause.

## Pourquoi archiver ?
- Apps sans code fonctionnel (HTML-only shells)
- Apps en attente de developpement
- Apps remplacees par d'autres solutions

## Comment desarchiver ?
1. Deplacer le dossier vers `apps/`
2. Verifier les dependances
3. Mettre a jour les references dans la documentation

## Liste des apps archivees
$(Get-Date -Format "yyyy-MM-dd")
"@
$archiveReadme | Out-File -FilePath "$archivedPath\README.md" -Encoding utf8

# ============================================================================
# 2. DEPLACEMENT APPS VIDES VERS ARCHIVE
# ============================================================================
Write-Host ""
Write-Host "[2/4] Archivage des apps vides..." -ForegroundColor Yellow

$emptyApps = @(
    "agriculture-dz",
    "business-dz", 
    "commerce-dz",
    "council",
    "creative-studio",
    "dashboard-central",
    "data-dz-dashboard",
    "douanes-dz",
    "dzirvideo-ai",
    "education-dz",
    "finance-dz",
    "industrie-dz",
    "islam-dz",
    "pme-dz",
    "sante-dz",
    "seo-dz-boost",
    "transport-dz",
    "api-packages",
    "pipeline-creator"
)

$movedCount = 0
$skippedApps = @()

foreach ($app in $emptyApps) {
    $sourcePath = "apps\$app"
    $destPath = "$archivedPath\$app"
    
    if (Test-Path $sourcePath) {
        # Verifier si c'est vraiment une app "vide" (pas de Python/TS complexe)
        $pyFiles = Get-ChildItem -Path $sourcePath -Filter "*.py" -Recurse -ErrorAction SilentlyContinue
        $tsxFiles = Get-ChildItem -Path $sourcePath -Filter "*.tsx" -Recurse -ErrorAction SilentlyContinue
        
        # Si pas de fichiers Python ou TSX substantiels, archiver
        if ($pyFiles.Count -eq 0 -and $tsxFiles.Count -eq 0) {
            Move-Item -Path $sourcePath -Destination $destPath -Force -ErrorAction SilentlyContinue
            Write-Host "   [MOVED] $app -> _archived/" -ForegroundColor Gray
            $movedCount++
        } else {
            $skippedApps += $app
            Write-Host "   [SKIP] $app (contient du code actif)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   [SKIP] $app (n'existe pas)" -ForegroundColor Gray
    }
}

Write-Host "   [OK] $movedCount apps archivees" -ForegroundColor Green
if ($skippedApps.Count -gt 0) {
    Write-Host "   [INFO] Apps avec code actif (non archivees): $($skippedApps -join ', ')" -ForegroundColor Yellow
}

# ============================================================================
# 3. CONSOLIDATION DES DOSSIERS SHARED
# ============================================================================
Write-Host ""
Write-Host "[3/4] Consolidation shared/ -> packages/shared/..." -ForegroundColor Yellow

$packagesPath = "packages"
$sharedTargetPath = "$packagesPath\shared"

# Creer structure packages/
if (-not (Test-Path $packagesPath)) {
    New-Item -Path $packagesPath -ItemType Directory | Out-Null
    Write-Host "   [NEW] packages/ cree" -ForegroundColor Gray
}

if (-not (Test-Path $sharedTargetPath)) {
    New-Item -Path $sharedTargetPath -ItemType Directory | Out-Null
    Write-Host "   [NEW] packages/shared/ cree" -ForegroundColor Gray
}

$sharedSources = @(
    @{Path="apps\shared"; Name="apps_shared"},
    @{Path="services\shared"; Name="services_shared"},
    @{Path="shared"; Name="root_shared"}
)

foreach ($source in $sharedSources) {
    if (Test-Path $source.Path) {
        $files = Get-ChildItem -Path $source.Path -Recurse -File -ErrorAction SilentlyContinue
        Write-Host "   [FOUND] $($source.Path) ($($files.Count) fichiers)" -ForegroundColor Gray
        
        $targetSubPath = "$sharedTargetPath\$($source.Name)"
        if (-not (Test-Path $targetSubPath)) {
            Copy-Item -Path $source.Path -Destination $targetSubPath -Recurse -ErrorAction SilentlyContinue
            Write-Host "   [COPY] -> packages/shared/$($source.Name)/" -ForegroundColor Gray
        }
    }
}

# Creer README pour packages/shared
$sharedReadme = @"
# Shared Packages

Code partage entre les differentes applications et services.

## Structure
- `apps_shared/` - Code partage entre les apps frontend
- `services_shared/` - Code partage entre les services backend  
- `root_shared/` - Utilitaires globaux

## Usage
Importer depuis ce dossier centralise plutot que depuis les anciens emplacements.

## Migration
Les anciens dossiers shared sont conserves temporairement pour compatibilite.
Une fois tous les imports mis a jour, ils seront supprimes.

Generated: $(Get-Date -Format "yyyy-MM-dd")
"@
$sharedReadme | Out-File -FilePath "$sharedTargetPath\README.md" -Encoding utf8
Write-Host "   [OK] Shared consolide" -ForegroundColor Green

# ============================================================================
# 4. ANALYSE DOCKER-COMPOSE
# ============================================================================
Write-Host ""
Write-Host "[4/4] Analyse docker-compose files..." -ForegroundColor Yellow

$dockerPath = "infrastructure\docker"
$composeFiles = Get-ChildItem -Path $dockerPath -Filter "docker-compose*.yml" -ErrorAction SilentlyContinue

if ($composeFiles) {
    Write-Host "   [INFO] $($composeFiles.Count) fichiers docker-compose trouves:" -ForegroundColor Gray
    
    $composeFiles | ForEach-Object {
        $size = [math]::Round($_.Length / 1KB, 1)
        Write-Host "      - $($_.Name) ($size KB)" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "   [RECO] Consolider en 3 fichiers:" -ForegroundColor Yellow
    Write-Host "      - docker-compose.dev.yml (developpement local)" -ForegroundColor White
    Write-Host "      - docker-compose.staging.yml (pre-production)" -ForegroundColor White  
    Write-Host "      - docker-compose.prod.yml (production VPS)" -ForegroundColor White
} else {
    Write-Host "   [SKIP] Aucun docker-compose trouve dans $dockerPath" -ForegroundColor Gray
}

# ============================================================================
# RESUME
# ============================================================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[OK] MIGRATION P1 TERMINEE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "Actions effectuees:" -ForegroundColor White
Write-Host "   - apps/_archived/ cree avec README" -ForegroundColor Gray
Write-Host "   - $movedCount apps vides archivees" -ForegroundColor Gray
Write-Host "   - packages/shared/ cree et consolide" -ForegroundColor Gray
Write-Host "   - Analyse docker-compose effectuee" -ForegroundColor Gray

Write-Host ""
Write-Host "[!] ACTIONS MANUELLES:" -ForegroundColor Yellow
Write-Host "   1. Commit: git add -A && git commit -m 'chore(P1): reorganize - archive empty apps, consolidate shared'" -ForegroundColor White
Write-Host "   2. Mettre a jour imports vers packages/shared/" -ForegroundColor White
Write-Host "   3. Consolider docker-compose manuellement" -ForegroundColor White

Write-Host ""
Write-Host "[>] Prochaine etape: .\scripts\migration\p2-documentation.ps1" -ForegroundColor Cyan
