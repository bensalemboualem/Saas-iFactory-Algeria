@echo off
COLOR 0A
title BBC School Algeria - Demarrage Automatique

echo.
echo ========================================
echo   BBC SCHOOL ALGERIA
echo   Demarrage Automatique
echo ========================================
echo.

REM ===================================
REM ETAPE 1: Demarrer Apache
REM ===================================
echo [1/5] Demarrage d'Apache...
cd /d C:\xampp
start /B apache\bin\httpd.exe
timeout /t 3 /nobreak >nul
echo      Apache demarre!
echo.

REM ===================================
REM ETAPE 2: Demarrer MySQL
REM ===================================
echo [2/5] Demarrage de MySQL...
start /B mysql\bin\mysqld.exe
timeout /t 5 /nobreak >nul
echo      MySQL demarre!
echo.

REM ===================================
REM ETAPE 3: Nettoyer les caches
REM ===================================
echo [3/5] Nettoyage des caches Laravel...
cd /d C:\xampp\htdocs\onestschooled-test

del /Q storage\framework\views\*.php 2>nul
del /Q bootstrap\cache\config.php 2>nul
del /Q bootstrap\cache\routes-v7.php 2>nul

echo      Caches nettoyes!
echo.

REM ===================================
REM ETAPE 4: Verifier la base de donnees
REM ===================================
echo [4/5] Verification de la base de donnees...
C:\xampp\mysql\bin\mysql.exe -u root -e "USE onest_school; SELECT 'Base de donnees OK' as Status;" 2>nul
if %errorlevel% neq 0 (
    echo      ATTENTION: Probleme avec la base de donnees!
    pause
) else (
    echo      Base de donnees OK!
)
echo.

REM ===================================
REM ETAPE 5: Ouvrir le navigateur
REM ===================================
echo [5/5] Ouverture du navigateur...
timeout /t 2 /nobreak >nul
start http://localhost/onestschooled-test/public/login
echo      Navigateur ouvert!
echo.

echo ========================================
echo   ONESTSCHOOL EST PRET!
echo ========================================
echo.
echo   Dashboard: http://localhost/onestschooled-test/public/dashboard
echo   Site Public: http://localhost/onestschooled-test/public/home
echo.
echo   Appuyez sur une touche pour fermer cette fenetre...
echo ========================================
pause >nul
