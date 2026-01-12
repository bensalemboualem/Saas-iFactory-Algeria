@echo off
REM Script automatique de rotation des clés API exposées
REM STEP 1: Suppression et protection du fichier exposé

setlocal enabledelayedexpansion

echo ========================================
echo   ROTATION CLES API - STEP 1/5
echo   Suppression fichier expose
echo ========================================
echo.

REM Vérifier qu'on est à la racine du projet
if not exist "apps\video-studio\.env.ready" (
    echo [91mERREUR: Fichier apps\video-studio\.env.ready introuvable[0m
    echo Assurez-vous d'etre a la racine du projet rag-dz
    pause
    exit /b 1
)

echo [93m[STEP 1.1] Backup du fichier expose...[0m
copy "apps\video-studio\.env.ready" "apps\video-studio\.env.ready.EXPOSED.backup" >nul
if errorlevel 1 (
    echo [91mERREUR: Impossible de creer le backup[0m
    pause
    exit /b 1
)
echo # WARNING: CLES EXPOSEES - NE JAMAIS UTILISER > "apps\video-studio\.env.ready.EXPOSED.backup.txt"
echo # Date d'exposition: 2024-12-23 >> "apps\video-studio\.env.ready.EXPOSED.backup.txt"
echo # Ces cles DOIVENT etre regenerees >> "apps\video-studio\.env.ready.EXPOSED.backup.txt"
echo. >> "apps\video-studio\.env.ready.EXPOSED.backup.txt"
type "apps\video-studio\.env.ready" >> "apps\video-studio\.env.ready.EXPOSED.backup.txt"
echo [92mV Backup cree: .env.ready.EXPOSED.backup.txt[0m
echo.

echo [93m[STEP 1.2] Suppression du tracking Git...[0m
git rm --cached apps\video-studio\.env.ready
if errorlevel 1 (
    echo [93mWarning: Fichier deja supprime du tracking ou git non disponible[0m
) else (
    echo [92mV Fichier supprime du tracking Git[0m
)
echo.

echo [93m[STEP 1.3] Mise a jour .gitignore...[0m
findstr /C:"**/.env.ready" .gitignore >nul 2>&1
if errorlevel 1 (
    echo **/.env.ready >> .gitignore
    echo **/.env.local >> .gitignore
    echo **/.env.*.backup* >> .gitignore
    echo [92mV .gitignore mis a jour[0m
) else (
    echo [92mV .gitignore deja configure[0m
)
echo.

echo [93m[STEP 1.4] Creation template .env.local...[0m
(
echo # ============================================
echo # IA Factory Algeria - Production Keys
echo # GENERE: %date% %time%
echo # WARNING: NE JAMAIS COMMIT CE FICHIER
echo # ============================================
echo.
echo # === PRIORITE 1: LLM PROVIDERS ===
echo # Obtenir ici: https://openrouter.ai/keys
echo OPENROUTER_API_KEY=sk-or-v1-VOTRE_NOUVELLE_CLE_ICI
echo.
echo # Obtenir ici: https://console.groq.com/keys
echo GROQ_API_KEY=gsk_VOTRE_NOUVELLE_CLE_ICI
echo.
echo # Obtenir ici: https://console.anthropic.com/settings/keys
echo ANTHROPIC_API_KEY=sk-ant-VOTRE_NOUVELLE_CLE_ICI
echo.
echo # Obtenir ici: https://platform.openai.com/api-keys
echo OPENAI_API_KEY=sk-proj-VOTRE_NOUVELLE_CLE_ICI
echo.
echo # Obtenir ici: https://makersuite.google.com/app/apikey
echo GOOGLE_API_KEY=AIzaSy_VOTRE_NOUVELLE_CLE_ICI
echo.
echo # === PRIORITE 2: AUTRES PROVIDERS ^(optionnel^) ===
echo MISTRAL_API_KEY=
echo DEEPSEEK_API_KEY=
echo COHERE_API_KEY=
echo TOGETHER_API_KEY=
echo.
echo # === VIDEO GENERATION ^(optionnel^) ===
echo LUMA_API_KEY=
echo RUNWAY_API_KEY=
echo KLING_API_KEY=
echo MINIMAX_API_KEY=
echo PIKA_API_KEY=
echo REPLICATE_API_TOKEN=
echo STABILITY_API_KEY=
echo QWEN_API_KEY=
echo.
echo # === DATABASE ===
echo DATABASE_URL=postgresql://postgres:password@localhost:5432/iafactory_dz
echo POSTGRES_URL=postgresql://postgres:password@localhost:5432/iafactory_dz
echo REDIS_URL=redis://localhost:6379/0
echo.
echo # === PAYMENT CHARGILY ===
echo # Obtenir ici: https://chargily.com/dashboard/settings/api
echo CHARGILY_SECRET_KEY=sk_test_VOTRE_CLE_TEST_ICI
echo CHARGILY_PUBLIC_KEY=pk_test_VOTRE_CLE_TEST_ICI
echo CHARGILY_WEBHOOK_SECRET=whsec_VOTRE_SECRET_ICI
echo CHARGILY_MODE=test
echo.
echo # === APP CONFIG ===
echo JWT_SECRET_KEY=GENERER_AVEC_OPENSSL_RAND_HEX_32
echo FRONTEND_URL=http://localhost:3000
echo API_URL=http://localhost:8000
echo ENVIRONMENT=development
echo.
echo # === ZERO RISQUE BUDGET ===
echo MAX_DAILY_BUDGET_USD=50.0
echo MONTHLY_BUDGET_USD=1500.0
echo.
echo # === ADMIN ===
echo ADMIN_EMAIL=admin@iafactory.dz
echo ADMIN_PASSWORD=ChangeMeInProduction123!
) > "services\api\.env.local"

echo [92mV Template .env.local cree dans services\api\[0m
echo.

echo ========================================
echo   STEP 1 TERMINE
echo ========================================
echo.
echo [92mFichier expose supprime du tracking Git[0m
echo [92mBackup cree: apps\video-studio\.env.ready.EXPOSED.backup.txt[0m
echo [92mTemplate cree: services\api\.env.local[0m
echo.
echo [93mPROCHAINES ETAPES:[0m
echo.
echo 1. Ouvrir services\api\.env.local dans votre editeur
echo 2. Regenerer les 5 cles PRIORITE 1:
echo    - OpenRouter: https://openrouter.ai/keys
echo    - Groq: https://console.groq.com/keys
echo    - Anthropic: https://console.anthropic.com/settings/keys
echo    - OpenAI: https://platform.openai.com/api-keys
echo    - Google: https://makersuite.google.com/app/apikey
echo.
echo 3. Remplacer VOTRE_NOUVELLE_CLE_ICI par les vraies cles
echo.
echo 4. Generer JWT_SECRET_KEY:
echo    - Windows PowerShell:
echo      [System.Convert]::ToBase64String^([byte[]]^(1..32 ^| ForEach-Object { Get-Random -Maximum 256 }^)^)
echo    - OU utiliser: https://generate-secret.vercel.app/32
echo.
echo 5. Executer: git add .gitignore
echo 6. Executer: git commit -m "security: remove exposed API keys from tracking"
echo.
echo [93mTemps estime pour completer: 20-30 minutes[0m
echo.

pause
