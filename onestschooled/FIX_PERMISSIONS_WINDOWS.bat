@echo off
echo ========================================
echo CORRECTION DES PERMISSIONS WINDOWS
echo ========================================
echo.

echo 1. Attribution des droits complets sur bootstrap/cache...
icacls "C:\xampp\htdocs\onestschooled-test\bootstrap\cache" /grant Everyone:(OI)(CI)F /T
echo.

echo 2. Attribution des droits complets sur storage...
icacls "C:\xampp\htdocs\onestschooled-test\storage" /grant Everyone:(OI)(CI)F /T
echo.

echo 3. Nettoyage du cache bootstrap...
del /Q "C:\xampp\htdocs\onestschooled-test\bootstrap\cache\*.php" 2>nul
echo.

echo 4. Nettoyage du cache storage...
del /Q "C:\xampp\htdocs\onestschooled-test\storage\framework\cache\data\*" 2>nul
del /Q "C:\xampp\htdocs\onestschooled-test\storage\framework\views\*.php" 2>nul
echo.

echo ========================================
echo CORRECTION TERMINEE!
echo ========================================
echo.
echo Rechargez la page dans le navigateur avec Ctrl+Shift+R
echo.
pause
