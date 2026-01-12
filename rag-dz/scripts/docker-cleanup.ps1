# =============================================================================
# DOCKER CLEANUP SCRIPT - IAFactory RAG-DZ
# Mis a jour le 2025-12-27 apres audit complet
# ATTENTION: Executer scripts\backup-before-cleanup.ps1 AVANT ce script!
# =============================================================================

param(
    [switch]$Force,
    [switch]$DryRun
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DOCKER CLEANUP - IAFactory RAG-DZ" -ForegroundColor Cyan
Write-Host "  Audit: AUDIT_DOCKER_COMPLET.md" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verification du backup
$BackupDir = "D:\IAFactory\BACKUPS\$(Get-Date -Format 'yyyy-MM-dd')"
if (-not (Test-Path $BackupDir) -and -not $Force) {
    Write-Host "ERREUR: Backup non trouve!" -ForegroundColor Red
    Write-Host "Executez d'abord: .\scripts\backup-before-cleanup.ps1" -ForegroundColor Yellow
    Write-Host "Ou utilisez -Force pour ignorer (DANGER!)" -ForegroundColor Yellow
    exit 1
}

if ($DryRun) {
    Write-Host "MODE DRY-RUN: Aucune suppression reelle" -ForegroundColor Magenta
    Write-Host ""
}

# Etape 1: Afficher l'espace actuel
Write-Host "[1/7] Espace disque Docker actuel:" -ForegroundColor Yellow
docker system df

Write-Host ""
Write-Host "[2/7] Suppression containers OBSOLETES (Created/Exited)..." -ForegroundColor Yellow

# Containers a supprimer (selon audit)
$containersToDelete = @(
    "private-gpt-private-gpt-ollama-1",
    "private-gpt-ollama-cpu-1",
    "private-gpt-ollama-1",
    "iaf-ollama",
    "postgres-iafactory",
    "ia-factory-postgres",
    "bolt-diy-fresh-app-dev-1",
    "dziria-app-dev-1"
)
foreach ($c in $containersToDelete) {
    if ($DryRun) {
        Write-Host "  [DRY-RUN] Supprimerait: $c" -ForegroundColor Gray
    } else {
        Write-Host "  Suppression: $c" -ForegroundColor Gray
        docker rm -f $c 2>$null
    }
}

Write-Host ""
Write-Host "[3/7] Containers RECONSTRUCTIBLES (garder code, supprimer container)..." -ForegroundColor Yellow
$rebuildableContainers = @(
    "ia-factory-automation",
    "ia-factory-celery",
    "ia-factory-beat",
    "dzirvideo",
    "iaf-dz-backend-local",
    "iaf-dz-docs-local"
)
foreach ($c in $rebuildableContainers) {
    if ($DryRun) {
        Write-Host "  [DRY-RUN] Supprimerait: $c (reconstructible)" -ForegroundColor Gray
    } else {
        Write-Host "  Suppression: $c (Dockerfile existe)" -ForegroundColor Gray
        docker rm $c 2>$null
    }
}

Write-Host ""
Write-Host "[4/7] Suppression des images dangling (<none>)..." -ForegroundColor Yellow
if (-not $DryRun) {
    docker image prune -f
}

Write-Host ""
Write-Host "[5/7] Suppression des images ENORMES (code existe)..." -ForegroundColor Yellow
# NE PAS supprimer bolt-ai:production - le sauvegarder d'abord!
$obsoleteImages = @(
    "rag-dz-iafactory-backend:latest",     # 17.8 GB - Dockerfile existe
    "rag-dz-backend-local:latest",          # 11 GB - Dockerfile existe
    "video-operator-video-operator:latest", # 13.3 GB - Dockerfile existe
    "bolt-ai:development",                   # 4.34 GB - version dev
    "dzirvideo-dzirvideo:latest",           # 4.87 GB - Dockerfile existe
    "zylonai/private-gpt:0.6.2-ollama",     # Non utilise
    "ghcr.io/stackblitz-labs/bolt.diy:latest", # Remplace par bolt-ai
    "mcr.microsoft.com/devcontainers/javascript-node:1-18-bookworm", # Dev container
    "rediscommander/redis-commander:latest", # Non utilise
    "dpage/pgadmin4:latest",                 # Non utilise
    "traefik:v2.10"                          # Non utilise
)
foreach ($img in $obsoleteImages) {
    if ($DryRun) {
        Write-Host "  [DRY-RUN] Supprimerait: $img" -ForegroundColor Gray
    } else {
        Write-Host "  Suppression: $img" -ForegroundColor Gray
        docker rmi $img 2>$null
    }
}

Write-Host ""
Write-Host "[6/7] Suppression des volumes orphelins..." -ForegroundColor Yellow
docker volume prune -f

Write-Host ""
Write-Host "[7/7] Nettoyage du build cache..." -ForegroundColor Yellow
docker builder prune -f --all

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  NETTOYAGE TERMINÉ!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Afficher l'espace libéré
Write-Host "Espace disque Docker après nettoyage:" -ForegroundColor Yellow
docker system df

Write-Host ""
Write-Host "Containers restants:" -ForegroundColor Yellow
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
