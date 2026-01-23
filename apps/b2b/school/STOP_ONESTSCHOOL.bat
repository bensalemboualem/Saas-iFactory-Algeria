@echo off
COLOR 0C
title BBC School Algeria - Arret

echo.
echo ========================================
echo   BBC SCHOOL ALGERIA
echo   Arret des Services
echo ========================================
echo.

REM Arreter Apache
echo [1/2] Arret d'Apache...
taskkill /F /IM httpd.exe >nul 2>&1
echo      Apache arrete!
echo.

REM Arreter MySQL
echo [2/2] Arret de MySQL...
taskkill /F /IM mysqld.exe >nul 2>&1
echo      MySQL arrete!
echo.

echo ========================================
echo   SERVICES ARRETES!
echo ========================================
echo.
pause
