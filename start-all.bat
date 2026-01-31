@echo off
echo ========================================
echo   IA FACTORY - Demarrage Automatique
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Demarrage du Gateway (port 5191)...
start "Gateway" cmd /k "cd apps\gateway && pnpm dev"
timeout /t 5 /nobreak > nul

echo [2/2] Demarrage de Bolt-UI (port 5190)...
start "Bolt-UI" cmd /k "cd apps\bolt-ui && pnpm dev"

echo.
echo ========================================
echo   Tous les services sont en cours de demarrage!
echo ========================================
echo.
echo Gateway:  http://localhost:5191
echo Bolt-UI:  http://localhost:5190
echo.
echo Attendez 30 secondes puis ouvrez:
echo http://localhost:5190
echo.
pause
