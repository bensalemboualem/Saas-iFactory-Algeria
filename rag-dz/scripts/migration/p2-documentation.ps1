# ============================================================================
# MIGRATION P2 - Documentation & README Generator
# ============================================================================
# Executer depuis la racine du projet: .\scripts\migration\p2-documentation.ps1
# ============================================================================

$ErrorActionPreference = "Continue"
$ROOT = "D:\IAFactory\rag-dz"
Set-Location $ROOT

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[P2] MIGRATION P2 - DOCUMENTATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# FONCTION: Detecter le stack d'une app
# ============================================================================
function Get-AppStack {
    param([string]$appPath)
    
    $stack = @{
        Type = "static"
        Framework = "HTML/CSS/JS"
        InstallCmd = "# No dependencies"
        DevCmd = "# Open index.html in browser"
        BuildCmd = "# No build required"
        HasBackend = $false
        HasFrontend = $false
    }
    
    # Next.js
    if (Test-Path "$appPath\next.config.*" -ErrorAction SilentlyContinue) {
        $stack.Type = "nextjs"
        $stack.Framework = "Next.js 14"
        $stack.InstallCmd = "npm install"
        $stack.DevCmd = "npm run dev"
        $stack.BuildCmd = "npm run build"
        $stack.HasFrontend = $true
    }
    # Vite/React
    elseif (Test-Path "$appPath\vite.config.*" -ErrorAction SilentlyContinue) {
        $stack.Type = "vite"
        $stack.Framework = "React + Vite"
        $stack.InstallCmd = "npm install"
        $stack.DevCmd = "npm run dev"
        $stack.BuildCmd = "npm run build"
        $stack.HasFrontend = $true
    }
    # Node.js
    elseif (Test-Path "$appPath\package.json" -ErrorAction SilentlyContinue) {
        $stack.Type = "nodejs"
        $stack.Framework = "Node.js"
        $stack.InstallCmd = "npm install"
        $stack.DevCmd = "npm start"
        $stack.BuildCmd = "npm run build"
        $stack.HasFrontend = $true
    }
    
    # Check for backend
    if (Test-Path "$appPath\backend" -ErrorAction SilentlyContinue) {
        $stack.HasBackend = $true
        if (Test-Path "$appPath\backend\requirements.txt" -ErrorAction SilentlyContinue) {
            $stack.Framework += " + FastAPI"
        }
    }
    elseif (Test-Path "$appPath\requirements.txt" -ErrorAction SilentlyContinue) {
        $stack.Type = "python"
        $stack.Framework = "Python/FastAPI"
        $stack.InstallCmd = "pip install -r requirements.txt"
        $stack.DevCmd = "uvicorn app.main:app --reload"
        $stack.BuildCmd = "# No build (Python)"
        $stack.HasBackend = $true
    }
    
    return $stack
}

# ============================================================================
# FONCTION: Generer README pour une app
# ============================================================================
function Generate-AppReadme {
    param(
        [string]$appName,
        [string]$appPath,
        [hashtable]$stack
    )
    
    # Determiner le status
    $status = "En developpement"
    $statusIcon = "[DEV]"
    if ($appName -in @("video-studio", "marketing", "can2025", "news", "sport")) {
        $status = "Production"
        $statusIcon = "[PROD]"
    }
    
    # Lister les fichiers principaux
    $mainFiles = Get-ChildItem -Path $appPath -File -ErrorAction SilentlyContinue | 
                 Where-Object { $_.Extension -in @(".ts", ".tsx", ".py", ".js", ".jsx") } |
                 Select-Object -First 5 -ExpandProperty Name
    
    # Lister les dossiers
    $folders = Get-ChildItem -Path $appPath -Directory -ErrorAction SilentlyContinue |
               Where-Object { $_.Name -notin @("node_modules", "__pycache__", ".next", "dist", ".git") } |
               Select-Object -First 6 -ExpandProperty Name
    
    $structureText = ""
    foreach ($folder in $folders) {
        $structureText += "    $folder/`n"
    }
    if ($mainFiles) {
        $structureText += "    $($mainFiles -join ', ')"
    }

    $readme = @"
# $appName

> Application $appName - IAFactory SaaS Platform

## Status

| Aspect | Valeur |
|--------|--------|
| **Production** | $statusIcon $status |
| **Stack** | $($stack.Framework) |
| **Tests** | A implementer |
| **Documentation** | Ce fichier |

## Description

Application $appName faisant partie de la plateforme IAFactory.
$( if ($stack.HasBackend -and $stack.HasFrontend) { "Architecture full-stack avec frontend et backend separes." } 
   elseif ($stack.HasBackend) { "Service backend/API." }
   else { "Application frontend." } )

## Quick Start

### Installation

``````bash
$($stack.InstallCmd)
$( if ($stack.HasBackend) { "
# Backend (si applicable)
cd backend
pip install -r requirements.txt" } )
``````

### Developpement

``````bash
$($stack.DevCmd)
$( if ($stack.HasBackend) { "
# Backend
cd backend
uvicorn app.main:app --reload --port 8000" } )
``````

### Build

``````bash
$($stack.BuildCmd)
``````

## Structure

``````
$appName/
$structureText
``````

## Configuration

Copier ``.env.example`` vers ``.env`` et configurer les variables:

``````env
# API
API_URL=http://localhost:8000

# Voir .env.example pour la liste complete
``````

## API Endpoints

$( if ($stack.HasBackend) { "
| Methode | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/v1/health | Health check |
| ... | ... | A documenter |
" } else { "Non applicable (frontend only)" } )

## TODO

- [ ] Completer la documentation
- [ ] Ajouter tests unitaires
- [ ] Ajouter tests integration
- [ ] Configurer CI/CD

## Liens

- [Documentation principale](../../docs/README.md)
- [Architecture](../../docs/ARCHITECTURE.md)
- [Audit](../../docs/AUDIT.md)

---

*IAFactory SaaS Platform - Generated $(Get-Date -Format "yyyy-MM-dd")*
"@

    return $readme
}

# ============================================================================
# 1. SCAN APPS SANS README
# ============================================================================
Write-Host "[1/3] Scan des apps sans README..." -ForegroundColor Yellow

$appsPath = "apps"
$apps = Get-ChildItem -Path $appsPath -Directory | Where-Object { $_.Name -ne "_archived" }

$appsWithoutReadme = @()
$appsWithReadme = @()

foreach ($app in $apps) {
    $readmePath = Join-Path $app.FullName "README.md"
    if (-not (Test-Path $readmePath)) {
        $appsWithoutReadme += $app
    } else {
        $appsWithReadme += $app
    }
}

Write-Host "   [INFO] $($appsWithReadme.Count) apps avec README" -ForegroundColor Gray
Write-Host "   [INFO] $($appsWithoutReadme.Count) apps sans README" -ForegroundColor Yellow

# ============================================================================
# 2. GENERATION README POUR CHAQUE APP SANS README
# ============================================================================
Write-Host ""
Write-Host "[2/3] Generation des README..." -ForegroundColor Yellow

$generatedCount = 0

foreach ($app in $appsWithoutReadme) {
    $appName = $app.Name
    $appPath = $app.FullName
    
    # Detecter le stack
    $stack = Get-AppStack -appPath $appPath
    
    # Generer README
    $readme = Generate-AppReadme -appName $appName -appPath $appPath -stack $stack
    
    # Ecrire le fichier
    $readmePath = Join-Path $appPath "README.md"
    $readme | Out-File -FilePath $readmePath -Encoding utf8
    
    Write-Host "   [NEW] $appName/README.md ($($stack.Framework))" -ForegroundColor Gray
    $generatedCount++
}

Write-Host "   [OK] $generatedCount README generes" -ForegroundColor Green

# ============================================================================
# 3. GENERATION .env.example POUR APPS CONFIGURABLES
# ============================================================================
Write-Host ""
Write-Host "[3/3] Generation des .env.example..." -ForegroundColor Yellow

$envTemplate = @"
# ============================================================================
# Configuration {APP_NAME}
# ============================================================================
# Copier ce fichier vers .env et remplir les valeurs

# === API ===
API_URL=http://localhost:8000
API_KEY=your_api_key_here

# === Database (si applicable) ===
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# === LLM Providers (si applicable) ===
OPENAI_API_KEY=sk-your_openai_key
ANTHROPIC_API_KEY=sk-ant-your_anthropic_key
GROQ_API_KEY=gsk_your_groq_key

# === Environment ===
NODE_ENV=development
DEBUG=true
"@

$envCreatedCount = 0

foreach ($app in $apps) {
    $appPath = $app.FullName
    $envExamplePath = Join-Path $appPath ".env.example"
    
    # Ne creer que si pas d'exemple existant ET si app configurable
    $hasPackageJson = Test-Path (Join-Path $appPath "package.json")
    $hasRequirements = Test-Path (Join-Path $appPath "requirements.txt")
    $hasBackend = Test-Path (Join-Path $appPath "backend")
    
    if ((-not (Test-Path $envExamplePath)) -and ($hasPackageJson -or $hasRequirements -or $hasBackend)) {
        $envContent = $envTemplate -replace "{APP_NAME}", $app.Name
        $envContent | Out-File -FilePath $envExamplePath -Encoding utf8
        Write-Host "   [NEW] $($app.Name)/.env.example" -ForegroundColor Gray
        $envCreatedCount++
    }
}

Write-Host "   [OK] $envCreatedCount .env.example generes" -ForegroundColor Green

# ============================================================================
# RESUME
# ============================================================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[OK] MIGRATION P2 TERMINEE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "Actions effectuees:" -ForegroundColor White
Write-Host "   - $generatedCount README.md generes" -ForegroundColor Gray
Write-Host "   - $envCreatedCount .env.example generes" -ForegroundColor Gray
Write-Host "   - $($appsWithReadme.Count) apps avaient deja un README" -ForegroundColor Gray

Write-Host ""
Write-Host "[!] ACTIONS MANUELLES:" -ForegroundColor Yellow
Write-Host "   1. Commit: git add -A && git commit -m 'docs(P2): generate README and .env.example for all apps'" -ForegroundColor White
Write-Host "   2. Personnaliser chaque README avec descriptions specifiques" -ForegroundColor White
Write-Host "   3. Verifier/adapter les .env.example" -ForegroundColor White

Write-Host ""
Write-Host "[OK] MIGRATION P0-P1-P2 COMPLETE!" -ForegroundColor Green
Write-Host "     Voir docs/AUDIT.md et docs/MIGRATION_CHECKLIST.md" -ForegroundColor Cyan
