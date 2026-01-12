# ============================================================
# AUDIT COMPLET IA FACTORY ALGERIA - ZÉRO TOLÉRANCE
# Script de vérification exhaustif avant production
# PowerShell Version pour Windows
# ============================================================

$ErrorActionPreference = "Continue"

# Couleurs
$Green = "Green"
$Red = "Red"
$Yellow = "Yellow"
$Blue = "Cyan"

# Compteurs
$script:PASS = 0
$script:FAIL = 0
$script:WARN = 0

function Log-Pass { param($msg) Write-Host "  PASS: $msg" -ForegroundColor $Green; $script:PASS++ }
function Log-Fail { param($msg) Write-Host "  FAIL: $msg" -ForegroundColor $Red; $script:FAIL++ }
function Log-Warn { param($msg) Write-Host "  WARN: $msg" -ForegroundColor $Yellow; $script:WARN++ }
function Log-Info { param($msg) Write-Host "  INFO: $msg" -ForegroundColor $Blue }
function Log-Section {
    param($title)
    Write-Host ""
    Write-Host ("=" * 65) -ForegroundColor $Blue
    Write-Host "  $title" -ForegroundColor $Blue
    Write-Host ("=" * 65) -ForegroundColor $Blue
    Write-Host ""
}

$PROJECT_ROOT = "d:\IAFactory\rag-dz"
Set-Location $PROJECT_ROOT

Write-Host ""
Write-Host "+" + ("=" * 66) + "+" -ForegroundColor $Blue
Write-Host "|     AUDIT COMPLET IA FACTORY ALGERIA - ZERO TOLERANCE          |" -ForegroundColor $Blue
Write-Host "|                    $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')                           |" -ForegroundColor $Blue
Write-Host "+" + ("=" * 66) + "+" -ForegroundColor $Blue
Write-Host ""

# ============================================================
# SECTION 1: SÉCURITÉ CRITIQUE
# ============================================================
Log-Section "1. SECURITE CRITIQUE"

# 1.1 Clés API hardcodées dans le frontend
Log-Info "Verification des cles API hardcodees..."
$hardcodedKeys = Get-ChildItem -Path "frontend" -Recurse -Include "*.tsx","*.ts","*.js" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike "*node_modules*" -and $_.FullName -notlike "*.next*" } |
    Select-String -Pattern "test-api-key-123|test-api-key|api-key-123" -ErrorAction SilentlyContinue

if ($null -eq $hardcodedKeys -or $hardcodedKeys.Count -eq 0) {
    Log-Pass "Aucune cle API hardcodee dans le frontend"
} else {
    Log-Fail "Cles API hardcodees trouvees: $($hardcodedKeys.Count) occurrences"
    $hardcodedKeys | ForEach-Object { Write-Host "    - $($_.Path):$($_.LineNumber)" -ForegroundColor $Red }
}

# 1.2 Tenant IDs hardcodés
Log-Info "Verification des Tenant IDs hardcodes..."
$hardcodedTenants = Get-ChildItem -Path "frontend" -Recurse -Include "*.tsx","*.ts" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike "*node_modules*" } |
    Select-String -Pattern "00000000-0000-0000-0000-000000000001" -ErrorAction SilentlyContinue

if ($null -eq $hardcodedTenants -or $hardcodedTenants.Count -eq 0) {
    Log-Pass "Aucun Tenant ID de test hardcode"
} else {
    Log-Fail "Tenant IDs hardcodes trouves"
}

# 1.3 Fichiers .env
Log-Info "Verification du fichier .env..."
$envFile = "services\api\.env"
if (Test-Path $envFile) {
    $envContent = Get-Content $envFile -Raw
    if ($envContent -match "test-api-key-123|password123|secret123") {
        Log-Fail ".env contient des secrets de test faibles"
    } else {
        Log-Pass ".env ne contient pas de secrets de test evidents"
    }
} else {
    Log-Warn "Fichier .env non trouve"
}

# 1.4 Vérifier .gitignore
if (Test-Path ".gitignore") {
    $gitignore = Get-Content ".gitignore" -Raw
    if ($gitignore -match "\.env") {
        Log-Pass ".gitignore exclut les fichiers .env"
    } else {
        Log-Warn ".gitignore ne mentionne pas .env"
    }
}

# ============================================================
# SECTION 2: BASE DE DONNÉES
# ============================================================
Log-Section "2. BASE DE DONNEES"

# 2.1 Connexion PostgreSQL
Log-Info "Test de connexion PostgreSQL..."
$pgReady = docker exec iaf-dz-postgres-local pg_isready -U postgres -d iafactory_dz 2>$null
if ($LASTEXITCODE -eq 0) {
    Log-Pass "PostgreSQL repond"
} else {
    Log-Fail "PostgreSQL ne repond pas"
}

# 2.2 Tables requises
Log-Info "Verification des tables..."
$requiredTables = @("tenants", "user_credits", "billing_tenants", "subscription_plans", "service_pricing", "credit_transactions", "api_keys", "app_catalog", "agent_catalog")

foreach ($table in $requiredTables) {
    $result = docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT 1 FROM pg_tables WHERE tablename='$table'" 2>$null
    if ($result -match "1") {
        Log-Pass "Table '$table' existe"
    } else {
        Log-Fail "Table '$table' MANQUANTE"
    }
}

# 2.3 Données seed
Log-Info "Verification des donnees seed..."
$tenantCount = docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT COUNT(*) FROM tenants" 2>$null
$tenantCount = [int]($tenantCount -replace '\s','')
if ($tenantCount -gt 0) {
    Log-Pass "Table tenants: $tenantCount enregistrement(s)"
} else {
    Log-Fail "Table tenants VIDE"
}

$creditsCount = docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT COUNT(*) FROM user_credits" 2>$null
$creditsCount = [int]($creditsCount -replace '\s','')
if ($creditsCount -gt 0) {
    Log-Pass "Table user_credits: $creditsCount enregistrement(s)"
} else {
    Log-Fail "Table user_credits VIDE"
}

$billingCount = docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT COUNT(*) FROM billing_tenants" 2>$null
$billingCount = [int]($billingCount -replace '\s','')
if ($billingCount -gt 0) {
    Log-Pass "Table billing_tenants: $billingCount enregistrement(s)"
} else {
    Log-Fail "Table billing_tenants VIDE"
}

# 2.4 Plans de subscription
$plansCount = docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT COUNT(*) FROM subscription_plans" 2>$null
$plansCount = [int]($plansCount -replace '\s','')
if ($plansCount -ge 4) {
    Log-Pass "subscription_plans: $plansCount plans configures"
} else {
    Log-Warn "subscription_plans: seulement $plansCount plans (attendu: 4+)"
}

# 2.5 Catalog apps
$appsCount = docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT COUNT(*) FROM app_catalog WHERE is_published=true" 2>$null
$appsCount = [int]($appsCount -replace '\s','')
if ($appsCount -gt 0) {
    Log-Pass "app_catalog: $appsCount apps publiees"
} else {
    Log-Warn "app_catalog: aucune app publiee"
}

# ============================================================
# SECTION 3: CONFIGURATION
# ============================================================
Log-Section "3. CONFIGURATION"

# 3.1 DATABASE_URL unique
Log-Info "Verification DATABASE_URL..."
if (Test-Path $envFile) {
    $dbUrlCount = (Get-Content $envFile | Select-String -Pattern "^DATABASE_URL=" | Measure-Object).Count
    if ($dbUrlCount -eq 1) {
        Log-Pass "Un seul DATABASE_URL dans .env"
    } else {
        Log-Fail "DATABASE_URL duplique ou manquant ($dbUrlCount occurrences)"
    }
}

# 3.2 Port cohérent
Log-Info "Verification coherence des ports..."
$port8002 = Get-ChildItem -Path "frontend\ia-factory-ui" -Recurse -Include "*.ts","*.tsx","*.js" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike "*node_modules*" } |
    Select-String -Pattern "localhost:8002|:8002" -ErrorAction SilentlyContinue

if ($null -eq $port8002 -or $port8002.Count -eq 0) {
    Log-Pass "Pas de reference au port 8002 (obsolete)"
} else {
    Log-Warn "$($port8002.Count) references au port 8002 trouvees"
}

# 3.3 Variables d'environnement requises
Log-Info "Verification variables d'environnement..."
if (Test-Path $envFile) {
    $envContent = Get-Content $envFile
    $requiredVars = @("DATABASE_URL", "JWT_SECRET_KEY", "GROQ_API_KEY", "CHARGILY_API_KEY")
    foreach ($var in $requiredVars) {
        if ($envContent -match "^$var=") {
            Log-Pass "Variable $var definie"
        } else {
            Log-Fail "Variable $var MANQUANTE"
        }
    }
}

# ============================================================
# SECTION 4: FICHIERS CRITIQUES
# ============================================================
Log-Section "4. FICHIERS CRITIQUES"

# 4.1 Fichiers backend
$criticalFiles = @(
    "services\api\app\main.py",
    "services\api\app\routers\credits.py",
    "services\api\app\routers\payment.py",
    "services\api\app\routers\catalog.py",
    "apps\video-studio\backend\services\credits_proxy.py"
)
foreach ($file in $criticalFiles) {
    if (Test-Path $file) {
        Log-Pass "Fichier $file existe"
    } else {
        Log-Fail "Fichier $file MANQUANT"
    }
}

# 4.2 Fichiers frontend
$frontendFiles = @(
    "frontend\ia-factory-ui\app\pricing\page.tsx",
    "frontend\ia-factory-ui\app\apps\page.tsx",
    "frontend\ia-factory-ui\app\checkout\page.tsx",
    "frontend\ia-factory-ui\components\CreditBalance.tsx"
)
foreach ($file in $frontendFiles) {
    if (Test-Path $file) {
        Log-Pass "Fichier $file existe"
    } else {
        Log-Fail "Fichier $file MANQUANT"
    }
}

# ============================================================
# SECTION 5: IMPORTS ET DÉPENDANCES
# ============================================================
Log-Section "5. IMPORTS ET DEPENDANCES"

# 5.1 Vérifier les imports dans main.py
Log-Info "Verification imports API..."
$mainPy = Get-Content "services\api\app\main.py" -Raw -ErrorAction SilentlyContinue
if ($mainPy -match "catalog") {
    Log-Pass "Router catalog importe dans main.py"
} else {
    Log-Fail "Router catalog NON importe dans main.py"
}

if ($mainPy -match "credits") {
    Log-Pass "Router credits importe dans main.py"
} else {
    Log-Fail "Router credits NON importe dans main.py"
}

# 5.2 Vérifier __init__.py
$initPy = Get-Content "services\api\app\routers\__init__.py" -Raw -ErrorAction SilentlyContinue
if ($initPy -match "catalog") {
    Log-Pass "catalog dans __init__.py des routers"
} else {
    Log-Fail "catalog ABSENT de __init__.py"
}

# ============================================================
# SECTION 6: WEBHOOK CHARGILY
# ============================================================
Log-Section "6. WEBHOOK CHARGILY"

Log-Info "Verification webhook payment.py..."
$paymentPy = Get-Content "services\api\app\routers\payment.py" -Raw -ErrorAction SilentlyContinue

if ($paymentPy -match "billing_tenants") {
    if ($paymentPy -match "ON CONFLICT \(tenant_id\)") {
        Log-Pass "Webhook utilise UPSERT pour billing_tenants"
    } else {
        Log-Warn "Webhook reference billing_tenants mais sans UPSERT"
    }
} else {
    Log-Fail "Webhook ne met pas a jour billing_tenants"
}

if ($paymentPy -match "user_credits") {
    Log-Pass "Webhook met a jour user_credits"
} else {
    Log-Fail "Webhook ne met pas a jour user_credits"
}

# ============================================================
# SECTION 7: DOCKER ET SERVICES
# ============================================================
Log-Section "7. DOCKER ET SERVICES"

Log-Info "Verification conteneurs Docker..."
$postgresRunning = docker ps --filter "name=postgres" --filter "status=running" -q 2>$null
if ($postgresRunning) {
    Log-Pass "PostgreSQL en cours d'execution"
} else {
    Log-Fail "PostgreSQL NON en cours d'execution"
}

$redisRunning = docker ps --filter "name=redis" --filter "status=running" -q 2>$null
if ($redisRunning) {
    Log-Pass "Redis en cours d'execution"
} else {
    Log-Warn "Redis non detecte (optionnel)"
}

# ============================================================
# SECTION 8: API ENDPOINTS
# ============================================================
Log-Section "8. API ENDPOINTS (si API demarree)"

Log-Info "Test endpoint /health..."
try {
    $health = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($health.StatusCode -eq 200) {
        Log-Pass "API /health repond 200"
    }
} catch {
    Log-Warn "API /health non accessible"
}

Log-Info "Test endpoint /api/credits/pricing..."
try {
    $pricing = Invoke-WebRequest -Uri "http://localhost:8000/api/credits/pricing" -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($pricing.StatusCode -eq 200) {
        Log-Pass "API /api/credits/pricing repond 200"
    }
} catch {
    Log-Warn "API /api/credits/pricing non accessible"
}

# ============================================================
# SECTION 9: i18n ET DARK MODE
# ============================================================
Log-Section "9. i18n ET DARK MODE"

Log-Info "Verification fichiers i18n..."
$i18nFiles = @("fr.json", "ar.json", "en.json")
foreach ($file in $i18nFiles) {
    if (Test-Path "frontend\ia-factory-ui\messages\$file") {
        Log-Pass "Traduction $file existe"
    } else {
        Log-Warn "Traduction $file MANQUANTE"
    }
}

Log-Info "Verification classes dark mode..."
$darkClasses = Get-ChildItem -Path "frontend\ia-factory-ui" -Recurse -Include "*.tsx" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike "*node_modules*" } |
    Select-String -Pattern "dark:" -ErrorAction SilentlyContinue

$darkCount = if ($darkClasses) { $darkClasses.Count } else { 0 }
if ($darkCount -gt 50) {
    Log-Pass "Dark mode: $darkCount classes dark: trouvees"
} elseif ($darkCount -gt 0) {
    Log-Warn "Dark mode partiel: seulement $darkCount classes"
} else {
    Log-Fail "Dark mode: AUCUNE classe dark: trouvee"
}

if (Test-Path "frontend\ia-factory-ui\components\ThemeProvider.tsx") {
    Log-Pass "ThemeProvider.tsx existe"
} else {
    Log-Warn "ThemeProvider.tsx MANQUANT"
}

# ============================================================
# RAPPORT FINAL
# ============================================================
Write-Host ""
Write-Host "+" + ("=" * 66) + "+" -ForegroundColor $Blue
Write-Host "|                      RAPPORT FINAL                              |" -ForegroundColor $Blue
Write-Host "+" + ("=" * 66) + "+" -ForegroundColor $Blue
Write-Host ""

$TOTAL = $script:PASS + $script:FAIL + $script:WARN
if ($TOTAL -gt 0) {
    $SCORE = [math]::Round(($script:PASS * 100 / $TOTAL), 0)
} else {
    $SCORE = 0
}

Write-Host "  PASS: $($script:PASS)" -ForegroundColor $Green
Write-Host "  FAIL: $($script:FAIL)" -ForegroundColor $Red
Write-Host "  WARN: $($script:WARN)" -ForegroundColor $Yellow
Write-Host ""
Write-Host "SCORE: $SCORE% ($($script:PASS)/$TOTAL)" -ForegroundColor $Blue
Write-Host ""

if ($script:FAIL -eq 0) {
    Write-Host ("=" * 65) -ForegroundColor $Green
    Write-Host "  PROJET PRET POUR STAGING - AUCUNE ERREUR CRITIQUE" -ForegroundColor $Green
    Write-Host ("=" * 65) -ForegroundColor $Green
    exit 0
} elseif ($script:FAIL -le 2) {
    Write-Host ("=" * 65) -ForegroundColor $Yellow
    Write-Host "  PROJET PARTIELLEMENT PRET - $($script:FAIL) ERREUR(S) A CORRIGER" -ForegroundColor $Yellow
    Write-Host ("=" * 65) -ForegroundColor $Yellow
    exit 1
} else {
    Write-Host ("=" * 65) -ForegroundColor $Red
    Write-Host "  PROJET NON PRET - $($script:FAIL) ERREURS CRITIQUES" -ForegroundColor $Red
    Write-Host ("=" * 65) -ForegroundColor $Red
    exit 2
}
