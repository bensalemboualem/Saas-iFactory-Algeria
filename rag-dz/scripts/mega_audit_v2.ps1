# ============================================================
# MEGA-AUDIT CRITIQUE IA FACTORY ALGERIA V2
# ZERO COMPLAISANCE - ZERO RISQUE - VERIFICATION TOTALE
# PowerShell Version
# ============================================================

$ErrorActionPreference = "Continue"
$PROJECT_ROOT = "d:\IAFactory\rag-dz"
Set-Location $PROJECT_ROOT

# Compteurs
$script:MISSING_COUNT = 0
$script:SECURITY_ISSUES = 0
$script:DB_ISSUES = 0
$script:CODE_ISSUES = 0
$script:FRONTEND_ISSUES = 0
$script:API_ISSUES = 0
$script:DEP_ISSUES = 0
$script:INT_ISSUES = 0

function Write-Header { param($text) Write-Host "`n$("=" * 65)" -ForegroundColor Cyan; Write-Host "  $text" -ForegroundColor Cyan; Write-Host "$("=" * 65)`n" -ForegroundColor Cyan }
function Write-Pass { param($text) Write-Host "  PASS: $text" -ForegroundColor Green }
function Write-Fail { param($text) Write-Host "  FAIL: $text" -ForegroundColor Red }
function Write-Warn { param($text) Write-Host "  WARN: $text" -ForegroundColor Yellow }
function Write-Info { param($text) Write-Host "  INFO: $text" -ForegroundColor Cyan }

Write-Host "`n" + ("+" + "=" * 66 + "+") -ForegroundColor Blue
Write-Host "|  MEGA-AUDIT CRITIQUE IA FACTORY ALGERIA V2                    |" -ForegroundColor Blue
Write-Host "|  ZERO COMPLAISANCE - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')                    |" -ForegroundColor Blue
Write-Host ("+" + "=" * 66 + "+") -ForegroundColor Blue

# ============================================
# PHASE 1 : EXISTENCE DES FICHIERS
# ============================================
Write-Header "PHASE 1 : VERIFICATION EXISTENCE FICHIERS"

$FICHIERS_CRITIQUES = @(
    # Backend - Core
    "services/api/app/main.py",
    "services/api/app/core/credit_service.py",
    # Backend - Routers
    "services/api/app/routers/__init__.py",
    "services/api/app/routers/auth.py",
    "services/api/app/routers/credits.py",
    "services/api/app/routers/catalog.py",
    "services/api/app/routers/payment.py",
    # Video Studio
    "apps/video-studio/backend/main.py",
    "apps/video-studio/backend/services/credits_proxy.py",
    # Frontend - Pages
    "frontend/ia-factory-ui/app/layout.tsx",
    "frontend/ia-factory-ui/app/pricing/page.tsx",
    "frontend/ia-factory-ui/app/apps/page.tsx",
    "frontend/ia-factory-ui/app/checkout/page.tsx",
    # Frontend - Components
    "frontend/ia-factory-ui/components/CreditBalance.tsx",
    "frontend/ia-factory-ui/components/layout/Header.tsx",
    # Frontend - i18n
    "frontend/ia-factory-ui/messages/fr.json",
    "frontend/ia-factory-ui/messages/ar.json",
    "frontend/ia-factory-ui/messages/en.json",
    # Config
    "frontend/ia-factory-ui/next.config.js",
    "frontend/ia-factory-ui/package.json",
    # Env
    "services/api/.env"
)

foreach ($fichier in $FICHIERS_CRITIQUES) {
    if (Test-Path $fichier) {
        Write-Pass $fichier
    } else {
        Write-Fail "MANQUANT: $fichier"
        $script:MISSING_COUNT++
    }
}

Write-Host "`nRESULTAT PHASE 1: $script:MISSING_COUNT fichiers manquants sur $($FICHIERS_CRITIQUES.Count)" -ForegroundColor $(if($script:MISSING_COUNT -eq 0){"Green"}else{"Red"})

# ============================================
# PHASE 2 : SÉCURITÉ - CLÉS EXPOSÉES
# ============================================
Write-Header "PHASE 2 : AUDIT SECURITE - CLES EXPOSEES"

Write-Info "Recherche de cles API hardcodees dans le frontend..."

$patterns = @(
    "test-api-key",
    "00000000-0000-0000-0000-000000000001"
)

foreach ($pattern in $patterns) {
    $results = Get-ChildItem -Path "frontend" -Recurse -Include "*.tsx","*.ts","*.js" -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notlike "*node_modules*" -and $_.FullName -notlike "*.next*" } |
        Select-String -Pattern $pattern -ErrorAction SilentlyContinue

    if ($null -eq $results -or $results.Count -eq 0) {
        Write-Pass "Pattern '$pattern' non trouve"
    } else {
        Write-Fail "Pattern '$pattern' TROUVE ($($results.Count) occurrences)"
        $results | ForEach-Object { Write-Host "    - $($_.Path):$($_.LineNumber)" -ForegroundColor Red }
        $script:SECURITY_ISSUES++
    }
}

# Vérifier .gitignore
if (Test-Path ".gitignore") {
    $gitignore = Get-Content ".gitignore" -Raw
    if ($gitignore -match "\.env") {
        Write-Pass ".gitignore protege .env"
    } else {
        Write-Fail ".env NON PROTEGE dans .gitignore"
        $script:SECURITY_ISSUES++
    }
}

Write-Host "`nRESULTAT PHASE 2: $script:SECURITY_ISSUES problemes de securite" -ForegroundColor $(if($script:SECURITY_ISSUES -eq 0){"Green"}else{"Red"})

# ============================================
# PHASE 3 : BASE DE DONNÉES
# ============================================
Write-Header "PHASE 3 : AUDIT BASE DE DONNEES"

Write-Info "Connexion PostgreSQL..."
$pgReady = docker exec iaf-dz-postgres-local pg_isready -U postgres -d iafactory_dz 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Pass "PostgreSQL accessible"
} else {
    Write-Fail "PostgreSQL NON accessible"
    $script:DB_ISSUES++
}

Write-Info "Verification des tables..."
$REQUIRED_TABLES = @("tenants", "user_credits", "credit_transactions", "service_pricing", "subscription_plans", "billing_tenants", "app_catalog", "agent_catalog")

foreach ($table in $REQUIRED_TABLES) {
    $result = docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT 1 FROM pg_tables WHERE tablename='$table'" 2>$null
    if ($result -match "1") {
        $count = docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT COUNT(*) FROM $table" 2>$null
        $count = [int]($count -replace '\s','')
        Write-Pass "Table '$table' ($count enregistrements)"
    } else {
        Write-Fail "TABLE MANQUANTE: $table"
        $script:DB_ISSUES++
    }
}

# Vérifier données critiques
Write-Info "Verification donnees critiques..."

$plans_count = docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT COUNT(*) FROM subscription_plans" 2>$null
$plans_count = [int]($plans_count -replace '\s','')
if ($plans_count -ge 4) {
    Write-Pass "subscription_plans: $plans_count plans"
} else {
    Write-Fail "subscription_plans: Seulement $plans_count plans (besoin de 4)"
    $script:DB_ISSUES++
}

$apps_count = docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT COUNT(*) FROM app_catalog WHERE is_published=true" 2>$null
$apps_count = [int]($apps_count -replace '\s','')
if ($apps_count -ge 8) {
    Write-Pass "app_catalog: $apps_count apps publiees"
} else {
    Write-Warn "app_catalog: Seulement $apps_count apps"
}

$agents_count = docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT COUNT(*) FROM agent_catalog WHERE is_published=true" 2>$null
$agents_count = [int]($agents_count -replace '\s','')
if ($agents_count -ge 4) {
    Write-Pass "agent_catalog: $agents_count agents publies"
} else {
    Write-Warn "agent_catalog: Seulement $agents_count agents"
}

# Tenant dev
$dev_tenant = docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT COUNT(*) FROM tenants WHERE id = '550e8400-e29b-41d4-a716-446655440000'" 2>$null
$dev_tenant = [int]($dev_tenant -replace '\s','')
if ($dev_tenant -ge 1) {
    Write-Pass "Tenant de developpement existe"
} else {
    Write-Fail "Tenant de developpement MANQUANT"
    $script:DB_ISSUES++
}

# Crédits
$dev_credits = docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT total_credits FROM user_credits WHERE tenant_id = '550e8400-e29b-41d4-a716-446655440000'" 2>$null
$dev_credits = [int]($dev_credits -replace '\s','')
if ($dev_credits -ge 1000) {
    Write-Pass "Credits tenant dev: $dev_credits"
} else {
    Write-Fail "Credits tenant dev: $dev_credits (insuffisant)"
    $script:DB_ISSUES++
}

Write-Host "`nRESULTAT PHASE 3: $script:DB_ISSUES problemes de base de donnees" -ForegroundColor $(if($script:DB_ISSUES -eq 0){"Green"}else{"Red"})

# ============================================
# PHASE 4 : COHÉRENCE CODE
# ============================================
Write-Header "PHASE 4 : COHERENCE DU CODE"

Write-Info "Verification ports API..."
$port_8002 = Get-ChildItem -Path "frontend/ia-factory-ui" -Recurse -Include "*.tsx","*.ts","*.js" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike "*node_modules*" } |
    Select-String -Pattern "8002" -ErrorAction SilentlyContinue

if ($null -eq $port_8002 -or $port_8002.Count -eq 0) {
    Write-Pass "Pas de reference au port 8002 (obsolete)"
} else {
    Write-Warn "$($port_8002.Count) references au port 8002 trouvees"
    $script:CODE_ISSUES++
}

Write-Info "Verification CHF supprime..."
$chf_count = Get-ChildItem -Path "frontend/ia-factory-ui/app" -Recurse -Include "*.tsx" -ErrorAction SilentlyContinue |
    Select-String -Pattern "CHF|franc|suisse" -ErrorAction SilentlyContinue

if ($null -eq $chf_count -or $chf_count.Count -eq 0) {
    Write-Pass "CHF supprime, DZD uniquement"
} else {
    Write-Fail "CHF/Suisse encore present ($($chf_count.Count) occurrences)"
    $script:CODE_ISSUES++
}

Write-Host "`nRESULTAT PHASE 4: $script:CODE_ISSUES problemes de coherence" -ForegroundColor $(if($script:CODE_ISSUES -eq 0){"Green"}else{"Yellow"})

# ============================================
# PHASE 5 : FRONTEND - i18n ET DARK MODE
# ============================================
Write-Header "PHASE 5 : FRONTEND - i18n & DARK MODE"

Write-Info "Fichiers de traduction..."
$i18n_files = @("fr.json", "ar.json", "en.json")
foreach ($file in $i18n_files) {
    if (Test-Path "frontend/ia-factory-ui/messages/$file") {
        Write-Pass "Traduction $file existe"
    } else {
        Write-Fail "Traduction $file MANQUANTE"
        $script:FRONTEND_ISSUES++
    }
}

Write-Info "ThemeProvider..."
if (Test-Path "frontend/ia-factory-ui/components/ThemeProvider.tsx") {
    Write-Pass "ThemeProvider.tsx existe"
} else {
    Write-Warn "ThemeProvider.tsx MANQUANT"
    $script:FRONTEND_ISSUES++
}

Write-Info "Classes dark mode..."
$dark_classes = Get-ChildItem -Path "frontend/ia-factory-ui" -Recurse -Include "*.tsx" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike "*node_modules*" } |
    Select-String -Pattern "dark:" -ErrorAction SilentlyContinue

$dark_count = if ($dark_classes) { $dark_classes.Count } else { 0 }
if ($dark_count -gt 50) {
    Write-Pass "Dark mode: $dark_count classes dark: trouvees"
} elseif ($dark_count -gt 10) {
    Write-Warn "Dark mode partiel: $dark_count classes"
} else {
    Write-Fail "Dark mode INSUFFISANT: $dark_count classes"
    $script:FRONTEND_ISSUES++
}

Write-Info "Support RTL..."
$layout = Get-Content "frontend/ia-factory-ui/app/layout.tsx" -Raw -ErrorAction SilentlyContinue
if ($layout -match "dir=|rtl") {
    Write-Pass "Support RTL configure"
} else {
    Write-Warn "Support RTL non trouve"
    $script:FRONTEND_ISSUES++
}

Write-Host "`nRESULTAT PHASE 5: $script:FRONTEND_ISSUES problemes frontend" -ForegroundColor $(if($script:FRONTEND_ISSUES -eq 0){"Green"}else{"Yellow"})

# ============================================
# PHASE 6 : INTÉGRATIONS
# ============================================
Write-Header "PHASE 6 : INTEGRATIONS"

Write-Info "Video Studio -> Credits..."
$credits_proxy = Get-Content "apps/video-studio/backend/services/credits_proxy.py" -Raw -ErrorAction SilentlyContinue
if ($credits_proxy -match "deduct.*credits|IAFACTORY_API") {
    Write-Pass "credits_proxy.py integre le systeme de credits"
} else {
    Write-Fail "credits_proxy.py n'appelle pas l'API de credits"
    $script:INT_ISSUES++
}

Write-Info "Payment -> Credits..."
$payment = Get-Content "services/api/app/routers/payment.py" -Raw -ErrorAction SilentlyContinue
if ($payment -match "user_credits.*billing_tenants|ON CONFLICT") {
    Write-Pass "payment.py met a jour les credits avec UPSERT"
} else {
    Write-Fail "payment.py ne gere pas correctement les credits"
    $script:INT_ISSUES++
}

Write-Info "Main.py inclut tous les routers..."
$mainPy = Get-Content "services/api/app/main.py" -Raw -ErrorAction SilentlyContinue
$routers = @("catalog", "credits", "payment")
foreach ($router in $routers) {
    if ($mainPy -match $router) {
        Write-Pass "Router $router inclus"
    } else {
        Write-Fail "Router $router NON inclus"
        $script:INT_ISSUES++
    }
}

Write-Host "`nRESULTAT PHASE 6: $script:INT_ISSUES problemes d'integration" -ForegroundColor $(if($script:INT_ISSUES -eq 0){"Green"}else{"Yellow"})

# ============================================
# RAPPORT FINAL
# ============================================
Write-Host "`n" + ("+" + "=" * 66 + "+") -ForegroundColor Blue
Write-Host "|                       RAPPORT FINAL                             |" -ForegroundColor Blue
Write-Host ("+" + "=" * 66 + "+") -ForegroundColor Blue

$TOTAL_ISSUES = $script:MISSING_COUNT + $script:SECURITY_ISSUES + $script:DB_ISSUES + $script:CODE_ISSUES + $script:FRONTEND_ISSUES + $script:INT_ISSUES

Write-Host ""
Write-Host "  CATEGORIE                  PROBLEMES   STATUS" -ForegroundColor White
Write-Host "  --------------------------------------------------------"
Write-Host "  Fichiers manquants         $script:MISSING_COUNT           $(if($script:MISSING_COUNT -eq 0){'OK'}else{'CRITIQUE'})" -ForegroundColor $(if($script:MISSING_COUNT -eq 0){"Green"}else{"Red"})
Write-Host "  Securite                   $script:SECURITY_ISSUES           $(if($script:SECURITY_ISSUES -eq 0){'OK'}else{'CRITIQUE'})" -ForegroundColor $(if($script:SECURITY_ISSUES -eq 0){"Green"}else{"Red"})
Write-Host "  Base de donnees            $script:DB_ISSUES           $(if($script:DB_ISSUES -eq 0){'OK'}else{'A CORRIGER'})" -ForegroundColor $(if($script:DB_ISSUES -eq 0){"Green"}else{"Yellow"})
Write-Host "  Coherence code             $script:CODE_ISSUES           $(if($script:CODE_ISSUES -eq 0){'OK'}else{'A CORRIGER'})" -ForegroundColor $(if($script:CODE_ISSUES -eq 0){"Green"}else{"Yellow"})
Write-Host "  Frontend (i18n/dark)       $script:FRONTEND_ISSUES           $(if($script:FRONTEND_ISSUES -eq 0){'OK'}else{'A CORRIGER'})" -ForegroundColor $(if($script:FRONTEND_ISSUES -eq 0){"Green"}else{"Yellow"})
Write-Host "  Integrations               $script:INT_ISSUES           $(if($script:INT_ISSUES -eq 0){'OK'}else{'A CORRIGER'})" -ForegroundColor $(if($script:INT_ISSUES -eq 0){"Green"}else{"Yellow"})
Write-Host "  --------------------------------------------------------"
Write-Host "  TOTAL                      $TOTAL_ISSUES" -ForegroundColor White
Write-Host ""

# Score
$MAX_CHECKS = 50
$PASSED = $MAX_CHECKS - $TOTAL_ISSUES
$SCORE = [math]::Round(($PASSED / $MAX_CHECKS) * 100, 0)

Write-Host ("=" * 65) -ForegroundColor Blue
if ($TOTAL_ISSUES -eq 0) {
    Write-Host "  SCORE: 100% - PRET POUR PRODUCTION" -ForegroundColor Green
} elseif ($TOTAL_ISSUES -le 3) {
    Write-Host "  SCORE: $SCORE% - PRET POUR STAGING" -ForegroundColor Green
} elseif ($TOTAL_ISSUES -le 8) {
    Write-Host "  SCORE: $SCORE% - CORRECTIONS NECESSAIRES" -ForegroundColor Yellow
} else {
    Write-Host "  SCORE: $SCORE% - PROBLEMES MAJEURS" -ForegroundColor Red
}
Write-Host ("=" * 65) -ForegroundColor Blue
Write-Host ""

# Actions requises
if ($TOTAL_ISSUES -gt 0) {
    Write-Host "ACTIONS REQUISES:" -ForegroundColor Yellow
    if ($script:MISSING_COUNT -gt 0) { Write-Host "  1. Creer les $script:MISSING_COUNT fichiers manquants" }
    if ($script:SECURITY_ISSUES -gt 0) { Write-Host "  2. URGENT: Corriger les $script:SECURITY_ISSUES problemes de securite" -ForegroundColor Red }
    if ($script:DB_ISSUES -gt 0) { Write-Host "  3. Corriger les $script:DB_ISSUES problemes de base de donnees" }
    if ($script:FRONTEND_ISSUES -gt 0) { Write-Host "  4. Implementer dark mode complet ($script:FRONTEND_ISSUES fichiers)" }
    Write-Host ""
}

exit $TOTAL_ISSUES
