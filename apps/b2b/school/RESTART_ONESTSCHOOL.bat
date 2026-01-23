@echo off
COLOR 0E
title BBC School Algeria - Redemarrage

echo.
echo ========================================
echo   BBC SCHOOL ALGERIA
echo   Redemarrage Complet
echo ========================================
echo.

REM Arreter les services
echo Arret des services en cours...
call STOP_ONESTSCHOOL.bat

REM Attendre 3 secondes
timeout /t 3 /nobreak >nul

REM Redemarrer les services
echo.
echo Redemarrage des services...
call START_ONESTSCHOOL.bat
