@echo off
COLOR 0A
title BBC School - TEST FINAL AVANT PRESENTATION

echo.
echo ========================================
echo   BBC SCHOOL ALGERIA
echo   TEST FINAL AVANT PRESENTATION
echo ========================================
echo.

cd /d C:\xampp\htdocs\onestschooled-test

echo [1/5] Verification des compteurs...
"C:/xampp/php/php.exe" -r "$pdo = new PDO('mysql:host=localhost;dbname=onest_school', 'root', ''); $ct = $pdo->query('SELECT name, total_count FROM counter_translates WHERE locale=\"en\" LIMIT 5')->fetchAll(PDO::FETCH_ASSOC); foreach($ct as $c) { echo '   ' . $c['name'] . ': ' . $c['total_count'] . PHP_EOL; }"

echo.
echo [2/5] Verification de la page Contact...
"C:/xampp/php/php.exe" test_contact_page.php | findstr "Section Direction École Annexe"

echo.
echo [3/5] Nettoyage des caches...
del /Q storage\framework\views\*.php 2>nul
del /Q bootstrap\cache\*.php 2>nul
echo    Caches cleared!

echo.
echo [4/5] Verification des services...
tasklist /FI "IMAGENAME eq httpd.exe" 2>NUL | find /I /N "httpd.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo    [OK] Apache en cours d'execution
) else (
    echo    [!!] Apache NON demarre - Lancez START_ONESTSCHOOL.bat
)

tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo    [OK] MySQL en cours d'execution
) else (
    echo    [!!] MySQL NON demarre - Lancez START_ONESTSCHOOL.bat
)

echo.
echo [5/5] Ouverture des pages pour test...
timeout /t 2 /nobreak >nul
start http://localhost/onestschooled-test/public/home
timeout /t 1 /nobreak >nul
start http://localhost/onestschooled-test/public/contact

echo.
echo ========================================
echo   CHECKLIST DE VERIFICATION MANUELLE:
echo ========================================
echo.
echo PAGE HOME:
echo  [ ] Compteurs: 4, 54, 22, 304, 98%%
echo  [ ] Aucun "804++" visible
echo  [ ] Pas de mention "BAC" sur la page
echo  [ ] Chatbot fonctionne (coin droit)
echo.
echo PAGE CONTACT:
echo  [ ] Section "Nos Etablissements" visible
echo  [ ] 3 cartes: Direction, Ecole, Annexe
echo  [ ] Adresses: Bouchaoui, Ain Benian, Cheraga
echo  [ ] Telephones cliquables
echo  [ ] Horaires affiches
echo.
echo ========================================
echo   APPUYEZ SUR CTRL+F5 DANS LE NAVIGATEUR
echo   POUR FORCER LE RECHARGEMENT!
echo ========================================
echo.
pause
