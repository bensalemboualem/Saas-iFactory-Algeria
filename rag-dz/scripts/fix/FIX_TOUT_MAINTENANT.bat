@echo off
color 0C
cls
echo ================================
echo 🔥 FIX AUTOMATIQUE VPS
echo ================================
echo.
echo Ce script va corriger:
echo   ✅ Configuration Nginx
echo   ✅ Certificats SSL
echo   ✅ Headers Multi-Tenant
echo.
echo Preparation...
echo.

powershell.exe -ExecutionPolicy Bypass -File "%~dp0EXECUTER_FIX_MAINTENANT.ps1"

echo.
echo ================================
echo ✅ Terminé!
echo ================================
echo.
pause
