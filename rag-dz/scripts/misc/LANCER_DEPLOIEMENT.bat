@echo off
REM ################################################################################
REM 🚀 DÉPLOIEMENT EN UN CLIC - RAG-DZ
REM Version: 3.0
REM Description: Double-cliquez sur ce fichier pour tout déployer!
REM ################################################################################

echo ================================
echo 🚀 DÉPLOIEMENT EN UN CLIC
echo ================================
echo.

REM Vérifier si PowerShell est disponible
where powershell >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ PowerShell n'est pas installé!
    pause
    exit /b 1
)

REM Lancer le script PowerShell ultra-automatique
echo 🔥 Lancement du déploiement automatique...
echo.

powershell.exe -ExecutionPolicy Bypass -File "%~dp0deploy-ultra-auto.ps1"

echo.
echo ✅ Terminé!
pause
