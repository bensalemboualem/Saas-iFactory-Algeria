# ============================================
# BACKUP AVANT NETTOYAGE DOCKER - IAFACTORY
# Date: 2025-12-27
# ============================================

$ErrorActionPreference = "Continue"
$BackupDir = "D:\IAFactory\BACKUPS\$(Get-Date -Format 'yyyy-MM-dd')"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  BACKUP IAFACTORY AVANT NETTOYAGE DOCKER" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Creer le dossier de backup
Write-Host "[1/5] Creation du dossier de backup..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
New-Item -ItemType Directory -Force -Path "$BackupDir\volumes" | Out-Null
New-Item -ItemType Directory -Force -Path "$BackupDir\configs" | Out-Null
New-Item -ItemType Directory -Force -Path "$BackupDir\images" | Out-Null
Write-Host "  -> $BackupDir" -ForegroundColor Green

# ============================================
# BACKUP VOLUMES CRITIQUES
# ============================================
Write-Host ""
Write-Host "[2/5] Backup des volumes critiques..." -ForegroundColor Yellow

$CriticalVolumes = @(
    @{Name="iafactory-openwebui-data"; Desc="OpenWebUI configs"},
    @{Name="iaf-dz-qdrant-data"; Desc="Embeddings production"},
    @{Name="iaf-dz-backend-cache"; Desc="Cache backend RAG"},
    @{Name="iafactory-video-studio-pro_postgres_data"; Desc="DB Video Studio"},
    @{Name="ragdz-qdrant-data"; Desc="Embeddings RAG DZ"},
    @{Name="ia-factory-automation_qdrant-data"; Desc="Embeddings automation"},
    @{Name="iafactory-video-studio-pro_n8n_data"; Desc="Workflows n8n"},
    @{Name="iaf-grafana-data"; Desc="Dashboards Grafana"},
    @{Name="iaf-dz-postgres-data-local"; Desc="DB locale"}
)

foreach ($vol in $CriticalVolumes) {
    Write-Host "  Backup: $($vol.Name) ($($vol.Desc))..." -ForegroundColor Gray
    $tarFile = "$BackupDir\volumes\$($vol.Name).tar.gz"

    # Verifier si le volume existe
    $volExists = docker volume ls -q | Where-Object { $_ -eq $vol.Name }
    if ($volExists) {
        docker run --rm -v "$($vol.Name):/data" -v "${BackupDir}\volumes:/backup" alpine tar czf "/backup/$($vol.Name).tar.gz" /data 2>$null
        if (Test-Path $tarFile) {
            $size = (Get-Item $tarFile).Length / 1MB
            Write-Host "    -> OK ($([math]::Round($size, 2)) MB)" -ForegroundColor Green
        } else {
            Write-Host "    -> Vide ou erreur" -ForegroundColor Yellow
        }
    } else {
        Write-Host "    -> Volume non trouve" -ForegroundColor Red
    }
}

# ============================================
# BACKUP CONFIGURATIONS (.env files)
# ============================================
Write-Host ""
Write-Host "[3/5] Backup des fichiers de configuration..." -ForegroundColor Yellow

$ConfigPaths = @(
    @{Src="D:\IAFactory\rag-dz\.env*"; Dst="rag-dz"},
    @{Src="D:\IAFactory\rag-dz\infrastructure\docker\.env*"; Dst="docker"},
    @{Src="D:\IAFactory\iafactory-video-studio\.env*"; Dst="video-studio"},
    @{Src="D:\IAFactory\iafactory-video-studio-pro\.env*"; Dst="video-studio-pro"},
    @{Src="D:\IAFactory\iafactory-video-studio-pro\infrastructure\.env*"; Dst="video-studio-pro-infra"},
    @{Src="D:\iafactoryrag\docker\.env*"; Dst="iafactoryrag"}
)

foreach ($cfg in $ConfigPaths) {
    $destDir = "$BackupDir\configs\$($cfg.Dst)"
    New-Item -ItemType Directory -Force -Path $destDir | Out-Null

    $files = Get-ChildItem -Path $cfg.Src -ErrorAction SilentlyContinue
    if ($files) {
        Copy-Item -Path $cfg.Src -Destination $destDir -Force -ErrorAction SilentlyContinue
        Write-Host "  -> $($cfg.Dst): $($files.Count) fichier(s)" -ForegroundColor Green
    } else {
        Write-Host "  -> $($cfg.Dst): aucun fichier" -ForegroundColor Gray
    }
}

# ============================================
# EXPORT IMAGES IMPORTANTES
# ============================================
Write-Host ""
Write-Host "[4/5] Export des images Docker importantes..." -ForegroundColor Yellow

$ImagesToSave = @(
    "bolt-ai:production"
)

foreach ($img in $ImagesToSave) {
    Write-Host "  Export: $img..." -ForegroundColor Gray
    $imgFile = $img -replace ":", "-"
    docker save $img -o "$BackupDir\images\$imgFile.tar" 2>$null
    if (Test-Path "$BackupDir\images\$imgFile.tar") {
        $size = (Get-Item "$BackupDir\images\$imgFile.tar").Length / 1GB
        Write-Host "    -> OK ($([math]::Round($size, 2)) GB)" -ForegroundColor Green
    } else {
        Write-Host "    -> Image non trouvee ou erreur" -ForegroundColor Yellow
    }
}

# ============================================
# INVENTAIRE AVANT NETTOYAGE
# ============================================
Write-Host ""
Write-Host "[5/5] Generation de l'inventaire..." -ForegroundColor Yellow

$inventoryFile = "$BackupDir\INVENTAIRE_AVANT_NETTOYAGE.txt"

"============================================" | Out-File $inventoryFile
"INVENTAIRE DOCKER - $(Get-Date)" | Out-File $inventoryFile -Append
"============================================" | Out-File $inventoryFile -Append
"" | Out-File $inventoryFile -Append

"=== CONTAINERS ===" | Out-File $inventoryFile -Append
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}" | Out-File $inventoryFile -Append
"" | Out-File $inventoryFile -Append

"=== VOLUMES ===" | Out-File $inventoryFile -Append
docker volume ls | Out-File $inventoryFile -Append
"" | Out-File $inventoryFile -Append

"=== IMAGES ===" | Out-File $inventoryFile -Append
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | Out-File $inventoryFile -Append
"" | Out-File $inventoryFile -Append

"=== ESPACE DISQUE ===" | Out-File $inventoryFile -Append
docker system df | Out-File $inventoryFile -Append

Write-Host "  -> Inventaire sauvegarde" -ForegroundColor Green

# ============================================
# RESUME
# ============================================
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  BACKUP TERMINE" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$totalSize = (Get-ChildItem -Path $BackupDir -Recurse | Measure-Object -Property Length -Sum).Sum / 1GB
Write-Host "Dossier: $BackupDir" -ForegroundColor White
Write-Host "Taille totale: $([math]::Round($totalSize, 2)) GB" -ForegroundColor White
Write-Host ""
Write-Host "Contenu:" -ForegroundColor Yellow
Get-ChildItem -Path $BackupDir | ForEach-Object {
    $subSize = (Get-ChildItem -Path $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "  $($_.Name): $([math]::Round($subSize, 2)) MB" -ForegroundColor Gray
}

Write-Host ""
Write-Host "PROCHAINE ETAPE: Verifier le backup puis executer le nettoyage" -ForegroundColor Yellow
Write-Host "Script de nettoyage: scripts\docker-cleanup.ps1" -ForegroundColor Yellow
