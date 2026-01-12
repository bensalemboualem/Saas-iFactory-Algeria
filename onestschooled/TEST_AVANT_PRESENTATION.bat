@echo off
COLOR 0B
title BBC School - Test Avant Presentation

echo.
echo ========================================
echo   BBC SCHOOL - TEST AVANT PRESENTATION
echo ========================================
echo.

cd /d C:\xampp\htdocs\onestschooled-test

echo [1/4] Verification de la base de donnees...
"C:/xampp/php/php.exe" verify_final.php

echo.
echo [2/4] Nettoyage des caches...
del /Q storage\framework\views\*.php 2>nul
del /Q bootstrap\cache\*.php 2>nul
echo Caches nettoyes!

echo.
echo [3/4] Verification des services...
tasklist /FI "IMAGENAME eq httpd.exe" 2>NUL | find /I /N "httpd.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Apache est en cours d'execution
) else (
    echo [!!] Apache n'est PAS demarre - Lancez START_ONESTSCHOOL.bat
)

tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] MySQL est en cours d'execution
) else (
    echo [!!] MySQL n'est PAS demarre - Lancez START_ONESTSCHOOL.bat
)

echo.
echo [4/4] Ouverture du navigateur pour test...
timeout /t 2 /nobreak >nul
start http://localhost/onestschooled-test/public/home

echo.
echo ========================================
echo   VERIFICATIONS A FAIRE MANUELLEMENT:
echo ========================================
echo.
echo 1. Les compteurs affichent: 4, 54, 22, 304, 98%%
echo 2. Aucune mention de "BAC" sur la page
echo 3. Chatbot fonctionne (coin inferieur droit)
echo 4. Chatbot mentionne uniquement "BEM" (pas BAC)
echo 5. Demandez "tarifs" dans le chatbot
echo    - Doit montrer: Maternelle, Primaire, Cycle Moyen
echo    - NE DOIT PAS montrer: Lycee
echo.
echo ========================================
echo   Appuyez sur CTRL+F5 pour rafraichir!
echo ========================================
echo.
pause
