@echo off
COLOR 0E
title Ouverture Page Contact BBC School

echo.
echo ========================================
echo   OUVERTURE PAGE CONTACT
echo ========================================
echo.

cd /d C:\xampp\htdocs\onestschooled-test

echo [1/3] Nettoyage des caches...
"C:/xampp/php/php.exe" CLEAR_ALL_CACHES_FINAL.php

echo.
echo [2/3] Ouverture de la page Contact...
timeout /t 2 /nobreak >nul
start http://localhost/onestschooled-test/public/contact

echo.
echo [3/3] Instructions:
echo.
echo ========================================
echo   DANS LE NAVIGATEUR:
echo ========================================
echo.
echo 1. Appuyez sur CTRL + SHIFT + R
echo    (ou CTRL + F5)
echo.
echo 2. FAITES DEFILER VERS LE BAS
echo.
echo 3. Vous verrez une section avec:
echo    - Fond violet/rose en degrade
echo    - Titre: "Nos Etablissements BBC School"
echo    - 3 cartes blanches:
echo      * Direction Generale (Bouchaoui)
echo      * Ecole Principale (Ain Benian)
echo      * Annexe Maternelle (Cheraga)
echo.
echo ========================================
echo.
pause
