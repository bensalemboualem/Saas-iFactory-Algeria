# ============================================================================
# MIGRATION P0 - Actions Critiques (Securite & Nettoyage)
# ============================================================================
# Executer depuis la racine du projet: .\scripts\migration\p0-critical.ps1
# ============================================================================

$ErrorActionPreference = "Stop"
$ROOT = "D:\IAFactory\rag-dz"
Set-Location $ROOT

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[P0] MIGRATION P0 - ACTIONS CRITIQUES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# 1. SUPPRESSION rag-compat (98% duplication avec api/)
# ============================================================================
Write-Host "[1/5] Suppression services/backend/rag-compat/..." -ForegroundColor Yellow

$ragCompatPath = "services\backend\rag-compat"
if (Test-Path $ragCompatPath) {
    $fileCount = (Get-ChildItem -Path $ragCompatPath -Recurse -File -ErrorAction SilentlyContinue).Count
    Write-Host "   [INFO] $fileCount fichiers trouves" -ForegroundColor Gray
    
    # Supprimer du tracking git
    & git rm -r --cached $ragCompatPath 2>$null
    
    # Supprimer physiquement
    Remove-Item -Path $ragCompatPath -Recurse -Force -ErrorAction SilentlyContinue
    
    Write-Host "   [OK] rag-compat supprime ($fileCount fichiers)" -ForegroundColor Green
} else {
    Write-Host "   [SKIP] Deja supprime" -ForegroundColor Gray
}

# ============================================================================
# 2. SUPPRESSION node_modules commite
# ============================================================================
Write-Host ""
Write-Host "[2/5] Suppression node_modules commites..." -ForegroundColor Yellow

$nodeModulesPaths = @(
    "apps\video-studio\frontend\node_modules"
)

foreach ($nmPath in $nodeModulesPaths) {
    if (Test-Path $nmPath) {
        $sizeBytes = (Get-ChildItem -Path $nmPath -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        $sizeMB = [math]::Round($sizeBytes / 1MB, 2)
        Write-Host "   [INFO] $nmPath ($sizeMB MB)" -ForegroundColor Gray
        
        & git rm -r --cached $nmPath 2>$null
        Remove-Item -Path $nmPath -Recurse -Force -ErrorAction SilentlyContinue
        
        Write-Host "   [OK] Supprime" -ForegroundColor Green
    } else {
        Write-Host "   [SKIP] $nmPath - Deja supprime" -ForegroundColor Gray
    }
}

# ============================================================================
# 3. SUPPRESSION .env/.env.local exposes
# ============================================================================
Write-Host ""
Write-Host "[3/5] Suppression fichiers .env exposes..." -ForegroundColor Yellow

$envFiles = @(
    "apps\interview\.env.local",
    "apps\interview\.env"
)

foreach ($envFile in $envFiles) {
    if (Test-Path $envFile) {
        Write-Host "   [SEC] $envFile" -ForegroundColor Gray
        
        # Creer .env.example si n existe pas
        $exampleFile = $envFile -replace "\.env.*", ".env.example"
        if (-not (Test-Path $exampleFile)) {
            $content = Get-Content $envFile -ErrorAction SilentlyContinue | ForEach-Object {
                if ($_ -match "^([^=]+)=") {
                    "$($matches[1])=your_value_here"
                } else {
                    $_
                }
            }
            if ($content) {
                $content | Out-File -FilePath $exampleFile -Encoding utf8
                Write-Host "   [NEW] Cree $exampleFile" -ForegroundColor Gray
            }
        }
        
        & git rm --cached $envFile 2>$null
        Remove-Item $envFile -Force -ErrorAction SilentlyContinue
        
        Write-Host "   [OK] Supprime (secrets proteges)" -ForegroundColor Green
    } else {
        Write-Host "   [SKIP] $envFile - Deja supprime" -ForegroundColor Gray
    }
}

# ============================================================================
# 4. MISE A JOUR .gitignore GLOBAL
# ============================================================================
Write-Host ""
Write-Host "[4/5] Mise a jour .gitignore..." -ForegroundColor Yellow

$gitignorePath = ".gitignore"
$newEntries = @"

# === P0 Migration Additions (Dec 2024) ===
# Node modules (NEVER commit)
**/node_modules/

# Environment files with secrets
**/.env
**/.env.local
**/.env.*.local

# Python cache
**/__pycache__/
**/*.pyc
**/.venv/

# IDE
.idea/
.vscode/settings.json

# Build outputs
**/dist/
**/build/
**/.next/

# Logs
*.log
npm-debug.log*
"@

$currentContent = ""
if (Test-Path $gitignorePath) {
    $currentContent = Get-Content $gitignorePath -Raw -ErrorAction SilentlyContinue
}

if ($currentContent -notmatch "P0 Migration Additions") {
    Add-Content -Path $gitignorePath -Value $newEntries
    Write-Host "   [OK] Entrees ajoutees" -ForegroundColor Green
} else {
    Write-Host "   [SKIP] .gitignore deja mis a jour" -ForegroundColor Gray
}

# ============================================================================
# 5. RECHERCHE TODO SECURITE
# ============================================================================
Write-Host ""
Write-Host "[5/5] Scan TODO securite critiques..." -ForegroundColor Yellow

$findings = @()
$securityPatterns = @("TODO.*security", "TODO.*signature", "FIXME.*security", "hardcoded.*key")

foreach ($pattern in $securityPatterns) {
    $results = & git grep -n -i $pattern -- "*.py" "*.ts" "*.js" 2>$null
    if ($results) {
        $findings += $results
    }
}

if ($findings.Count -gt 0) {
    Write-Host "   [WARN] $($findings.Count) problemes de securite trouves:" -ForegroundColor Red
    $findings | Select-Object -First 10 | ForEach-Object {
        Write-Host "      $_" -ForegroundColor Gray
    }
    Write-Host ""
    Write-Host "   [INFO] Voir rapport complet: docs/AUDIT.md" -ForegroundColor Yellow
} else {
    Write-Host "   [OK] Aucun TODO securite critique trouve" -ForegroundColor Green
}

# ============================================================================
# RESUME
# ============================================================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[OK] MIGRATION P0 TERMINEE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "Actions effectuees:" -ForegroundColor White
Write-Host "   - rag-compat supprime" -ForegroundColor Gray
Write-Host "   - node_modules supprimes du repo" -ForegroundColor Gray
Write-Host "   - Fichiers .env secrets supprimes" -ForegroundColor Gray
Write-Host "   - .gitignore mis a jour" -ForegroundColor Gray

Write-Host ""
Write-Host "[!] ACTIONS MANUELLES REQUISES:" -ForegroundColor Yellow
Write-Host "   1. Commit: git add -A && git commit -m 'chore: P0 migration - cleanup'" -ForegroundColor White
Write-Host "   2. Verifier/corriger les TODO securite" -ForegroundColor White
Write-Host "   3. Regenerer node_modules: cd apps/video-studio/frontend && npm install" -ForegroundColor White

Write-Host ""
Write-Host "[>] Prochaine etape: .\scripts\migration\p1-reorganize.ps1" -ForegroundColor Cyan
