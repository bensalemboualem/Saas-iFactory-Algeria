@echo off
REM Deploy Zero Risque Architecture - IA Factory Algeria
REM IMPORTANT: Run this AFTER rotating the 18 exposed API keys

setlocal enabledelayedexpansion

echo ========================================
echo   DEPLOY ZERO RISQUE - IA FACTORY DZ
echo ========================================
echo.

REM Step 1: Check environment variables
echo [1/6] Verification des variables d'environnement...

set "missing_vars="

if "%POSTGRES_URL%"=="" set "missing_vars=!missing_vars! POSTGRES_URL"
if "%REDIS_URL%"=="" set "missing_vars=!missing_vars! REDIS_URL"
if "%GROQ_API_KEY%"=="" set "missing_vars=!missing_vars! GROQ_API_KEY"
if "%OPENROUTER_API_KEY%"=="" set "missing_vars=!missing_vars! OPENROUTER_API_KEY"
if "%GOOGLE_API_KEY%"=="" set "missing_vars=!missing_vars! GOOGLE_API_KEY"
if "%CHARGILY_SECRET_KEY%"=="" set "missing_vars=!missing_vars! CHARGILY_SECRET_KEY"
if "%CHARGILY_PUBLIC_KEY%"=="" set "missing_vars=!missing_vars! CHARGILY_PUBLIC_KEY"

if not "%missing_vars%"=="" (
    echo [91mX Variables manquantes:%missing_vars%[0m
    echo Veuillez configurer ces variables dans .env
    pause
    exit /b 1
)

echo [92mV Toutes les variables requises sont presentes[0m
echo.

REM Step 2: Test database connection
echo [2/6] Test de connexion PostgreSQL...
psql "%POSTGRES_URL%" -c "SELECT 1" >nul 2>&1
if errorlevel 1 (
    echo [91mX Impossible de se connecter a PostgreSQL[0m
    pause
    exit /b 1
)
echo [92mV PostgreSQL accessible[0m
echo.

REM Step 3: Test Redis connection
echo [3/6] Test de connexion Redis...
redis-cli -u "%REDIS_URL%" PING >nul 2>&1
if errorlevel 1 (
    echo [91mX Impossible de se connecter a Redis[0m
    pause
    exit /b 1
)
echo [92mV Redis accessible[0m
echo.

REM Step 4: Apply SQL migrations
echo [4/6] Application des migrations SQL...
set "MIGRATION_FILE=migrations\005_billing_tiers.sql"

if not exist "%MIGRATION_FILE%" (
    echo [91mX Fichier de migration introuvable: %MIGRATION_FILE%[0m
    pause
    exit /b 1
)

echo Executing migration: %MIGRATION_FILE%
psql "%POSTGRES_URL%" -f "%MIGRATION_FILE%"

if errorlevel 1 (
    echo [91mX Erreur lors de l'application de la migration[0m
    pause
    exit /b 1
)
echo [92mV Migration appliquee avec succes[0m
echo.

REM Step 5: Verify tables created
echo [5/6] Verification des tables creees...

psql "%POSTGRES_URL%" -c "\d user_tiers" >nul 2>&1
if errorlevel 1 (
    echo [91m  X Table user_tiers manquante[0m
    pause
    exit /b 1
)
echo [92m  V Table user_tiers creee[0m

psql "%POSTGRES_URL%" -c "\d llm_usage_logs" >nul 2>&1
if errorlevel 1 (
    echo [91m  X Table llm_usage_logs manquante[0m
    pause
    exit /b 1
)
echo [92m  V Table llm_usage_logs creee[0m

psql "%POSTGRES_URL%" -c "\d payment_transactions" >nul 2>&1
if errorlevel 1 (
    echo [91m  X Table payment_transactions manquante[0m
    pause
    exit /b 1
)
echo [92m  V Table payment_transactions creee[0m
echo.

REM Step 6: Instructions for starting server
echo [6/6] Demarrage/Reload du serveur FastAPI...
echo Si vous utilisez Docker, executez:
echo   docker-compose restart iafactory-api
echo.
echo Si vous lancez en local, executez:
echo   cd services\api
echo   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo [92m========================================[0m
echo [92m  DEPLOIEMENT TERMINE AVEC SUCCES V[0m
echo [92m========================================[0m
echo.
echo Prochaines etapes:
echo 1. Tester les endpoints avec le script de test:
echo    python services\api\test_zero_risque.py
echo.
echo 2. Acceder au dashboard admin:
echo    http://localhost:8000/api/admin/dashboard
echo.
echo 3. Tester le chat avec routing:
echo    curl -X POST http://localhost:8000/api/v2/chat ^
echo      -H "Authorization: Bearer YOUR_TOKEN" ^
echo      -H "Content-Type: application/json" ^
echo      -d "{\"messages\": [{\"role\": \"user\", \"content\": \"Test\"}]}"
echo.

pause
