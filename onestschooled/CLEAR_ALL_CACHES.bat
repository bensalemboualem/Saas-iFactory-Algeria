@echo off
COLOR 0A
title BBC School - Nettoyage Complet des Caches

echo.
echo ========================================
echo   NETTOYAGE COMPLET DES CACHES
echo ========================================
echo.

cd /d C:\xampp\htdocs\onestschooled-test

echo [1/3] Nettoyage des vues Blade...
del /Q storage\framework\views\*.php 2>nul
echo OK!

echo [2/3] Nettoyage du cache config...
del /Q bootstrap\cache\*.php 2>nul
echo OK!

echo [3/3] Nettoyage du cache navigateur (F5 + Ctrl+F5)...
echo IMPORTANT: Appuyez sur Ctrl+F5 dans votre navigateur pour rafraichir!

echo.
echo ========================================
echo   CACHES NETTOYES!
echo ========================================
echo.
echo Maintenant rechargez la page avec Ctrl+F5
echo.
pause
