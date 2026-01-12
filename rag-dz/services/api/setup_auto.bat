@echo off
echo ============================================
echo   SETUP AUTOMATIQUE - IA FACTORY ALGERIA
echo ============================================
echo.

REM 1. PostgreSQL
echo [1/4] Demarrage PostgreSQL...
docker run -d --name postgres-iafactory -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:15-alpine >nul 2>&1
timeout /t 10 /nobreak >nul
docker exec -it postgres-iafactory psql -U postgres -c "CREATE DATABASE iafactory_dz;" >nul 2>&1
echo   OK PostgreSQL demarre

REM 2. Generer JWT secret
echo [2/4] Generation JWT secret...
for /f "delims=" %%i in ('python -c "import secrets; print(secrets.token_urlsafe(64))"') do set JWT_SECRET=%%i
echo   OK Secret genere

REM 3. Creer .env.local
echo [3/4] Creation .env.local...
(
echo GROQ_API_KEY=METTRE_TA_CLE_GROQ_ICI
echo DATABASE_URL=postgresql://postgres:postgres@localhost:5432/iafactory_dz
echo REDIS_URL=redis://localhost:6379/0
echo JWT_SECRET_KEY=%JWT_SECRET%
echo ENVIRONMENT=development
) > .env.local
echo   OK Fichier cree

REM 4. Verification
echo [4/4] Verification...
python check_ready.py

echo.
echo ============================================
echo   PROCHAINE ETAPE:
echo ============================================
echo.
echo 1. Obtenir cle Groq: https://console.groq.com/keys
echo 2. Editer .env.local et remplacer: METTRE_TA_CLE_GROQ_ICI
echo 3. Lancer: python check_ready.py
echo 4. Si OK: uvicorn app.main:app --reload --port 8000
echo.
pause
