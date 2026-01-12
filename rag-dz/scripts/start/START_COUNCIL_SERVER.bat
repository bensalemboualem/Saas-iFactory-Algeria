@echo off
cls
echo.
echo ===============================================
echo   LLM COUNCIL - DEMARRAGE DU SERVEUR
echo ===============================================
echo.
echo Demarrage du serveur Node.js sur http://localhost:3000
echo.

cd /d "%~dp0"
node council-server.js

pause
