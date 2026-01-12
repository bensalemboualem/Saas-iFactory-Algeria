@echo off
REM ################################################################################
REM 🔧 FIX SSL URGENT - iafactoryalgeria.com
REM Corrige ERR_CERT_COMMON_NAME_INVALID
REM ################################################################################

color 0C
echo ================================
echo 🔧 FIX SSL URGENT
echo ================================
echo.
echo Problème: ERR_CERT_COMMON_NAME_INVALID
echo Site: iafactoryalgeria.com
echo.
echo Ce script va corriger le certificat SSL
echo.
pause

powershell.exe -ExecutionPolicy Bypass -File "%~dp0fix-ssl-maintenant.ps1"

pause
