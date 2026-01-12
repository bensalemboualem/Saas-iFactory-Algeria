@echo off
echo.
echo ========================================
echo   COUNCIL PERSONNALISABLE - DEMARRAGE
echo ========================================
echo.

:: Verifier si le backend tourne
echo [1/2] Verification backend...
curl -s http://localhost:8180/health >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Backend non demarre sur le port 8180
    echo.
    echo Demarrez d'abord le backend avec:
    echo   cd backend/rag-compat
    echo   docker-compose up backend
    echo.
    echo ou:
    echo   python -m uvicorn app.main:app --reload --port 8180
    echo.
    pause
    exit /b 1
)
echo OK - Backend actif sur :8180

:: Lancer le serveur Council
echo.
echo [2/2] Demarrage serveur Council...
echo.
echo ========================================
echo   URLs disponibles:
echo   - Standard: http://localhost:3000/
echo   - Custom:   http://localhost:3000/custom
echo ========================================
echo.
echo Appuyez sur Ctrl+C pour arreter
echo.

node council-server.js
