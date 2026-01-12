@echo off
chcp 65001 >nul
cls
echo ============================================
echo   SETUP COMPLET AUTO
echo ============================================
echo.

echo [1/3] PostgreSQL...
docker run -d --name postgres-iafactory -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:15-alpine 2>nul
timeout /t 10 /nobreak >nul
docker exec postgres-iafactory psql -U postgres -c "CREATE DATABASE iafactory_dz;" 2>nul
echo   OK

echo [2/3] JWT Secret...
for /f %%i in ('python -c "import secrets; print(secrets.token_urlsafe(64))"') do set JWT=%%i
echo   OK

echo [3/3] Fichier .env.local...
(
echo GROQ_API_KEY=REMPLACER_PAR_TA_CLE
echo DATABASE_URL=postgresql://postgres:postgres@localhost:5432/iafactory_dz
echo REDIS_URL=redis://localhost:6379/0
echo JWT_SECRET_KEY=%JWT%
echo ENVIRONMENT=development
) > .env.local
echo   OK

echo.
echo ============================================
echo   TERMINE - 1 action restante:
echo ============================================
echo.
echo 1. Va sur: https://console.groq.com/keys
echo 2. Cree une cle (gratuit)
echo 3. Ouvre: notepad .env.local
echo 4. Remplace: REMPLACER_PAR_TA_CLE par ta vraie cle
echo 5. Sauvegarde et ferme
echo 6. Lance: python check_ready.py
echo.
pause
