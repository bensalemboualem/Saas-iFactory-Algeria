@echo off
REM Quick Start - SaaS Zero Risque Tests
REM Lance tous les services necessaires pour tester

setlocal enabledelayedexpansion

echo ========================================
echo   QUICK START - TESTS SAAS ZERO RISQUE
echo ========================================
echo.

REM Verifier qu'on est dans le bon dossier
if not exist "app\main.py" (
    echo [91mERREUR: Executez ce script depuis services\api\[0m
    pause
    exit /b 1
)

REM Etape 1: Verifier .env.local existe
echo [93m[1/5] Verification .env.local...[0m
if not exist ".env.local" (
    echo [93m.env.local n'existe pas, creation du template...[0m
    (
        echo # Configuration TEST - IA Factory Algeria
        echo POSTGRES_URL=postgresql://postgres:password@localhost:5432/iafactory_dz
        echo REDIS_URL=redis://localhost:6379/0
        echo GROQ_API_KEY=votre_cle_groq
        echo OPENROUTER_API_KEY=votre_cle_openrouter
        echo CHARGILY_SECRET_KEY=sk_test_fake
        echo CHARGILY_PUBLIC_KEY=pk_test_fake
        echo CHARGILY_MODE=test
        echo JWT_SECRET_KEY=test_secret_key_dev_only
        echo MAX_DAILY_BUDGET_USD=50.0
        echo ENVIRONMENT=development
    ) > .env.local
    echo [92mV Template .env.local cree[0m
    echo [93mEditez .env.local et ajoutez vos vraies cles API[0m
    pause
)
echo [92mV .env.local existe[0m
echo.

REM Etape 2: Verifier PostgreSQL
echo [93m[2/5] Test connexion PostgreSQL...[0m
psql -U postgres -c "SELECT 1" >nul 2>&1
if errorlevel 1 (
    echo [91mX PostgreSQL non accessible[0m
    echo Verifiez que PostgreSQL tourne et que les credentials sont corrects
    pause
    exit /b 1
)
echo [92mV PostgreSQL accessible[0m
echo.

REM Etape 3: Creer DB si n'existe pas
echo [93m[3/5] Creation base de donnees...[0m
psql -U postgres -lqt | findstr iafactory_dz >nul
if errorlevel 1 (
    echo Creation de la base iafactory_dz...
    psql -U postgres -c "CREATE DATABASE iafactory_dz;"
    echo [92mV Base de donnees creee[0m
) else (
    echo [92mV Base de donnees existe deja[0m
)
echo.

REM Etape 4: Appliquer migration
echo [93m[4/5] Application migration SQL...[0m
if exist "migrations\005_billing_tiers.sql" (
    psql -U postgres -d iafactory_dz -f migrations\005_billing_tiers.sql
    if errorlevel 1 (
        echo [91mX Erreur lors de la migration[0m
        echo Si les tables existent deja, c'est normal
    ) else (
        echo [92mV Migration appliquee avec succes[0m
    )
) else (
    echo [93mWarning: Fichier migration introuvable[0m
)
echo.

REM Etape 5: Verifier Redis
echo [93m[5/5] Test connexion Redis...[0m
redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo [93mWarning: Redis non accessible[0m
    echo L'API peut demarrer mais le rate limiting ne fonctionnera pas
    echo Demarrez Redis avec: redis-server
    pause
) else (
    echo [92mV Redis accessible[0m
)
echo.

echo ========================================
echo   PRET A DEMARRER L'API
echo ========================================
echo.
echo Execution: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo Appuyez sur une touche pour demarrer l'API...
pause >nul

REM Demarrer l'API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
