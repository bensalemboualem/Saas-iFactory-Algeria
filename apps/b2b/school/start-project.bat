@echo off
title OneStSchooled - Demarrage Rapide
color 0A

echo ========================================
echo OneStSchooled - Demarrage du projet
echo ========================================
echo.

REM Vérifier si Apache tourne
tasklist /FI "IMAGENAME eq httpd.exe" 2>NUL | find /I /N "httpd.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Apache est deja en cours d'execution
) else (
    echo [!] Apache n'est pas demarre
    echo [*] Tentative de demarrage d'Apache...
    C:\xampp\apache\bin\httpd.exe -k start
    timeout /t 3 /nobreak >nul

    tasklist /FI "IMAGENAME eq httpd.exe" 2>NUL | find /I /N "httpd.exe">NUL
    if "%ERRORLEVEL%"=="0" (
        echo [OK] Apache demarre avec succes!
    ) else (
        echo [ERREUR] Impossible de demarrer Apache
        echo Veuillez demarrer Apache via XAMPP Control Panel
        pause
        exit /b 1
    )
)

echo.

REM Vérifier si MySQL tourne
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] MySQL est deja en cours d'execution
) else (
    echo [!] MySQL n'est pas demarre
    echo [*] Tentative de demarrage de MySQL...
    C:\xampp\mysql\bin\mysqld.exe --defaults-file=C:\xampp\mysql\bin\my.ini --standalone 2>nul
    timeout /t 3 /nobreak >nul
    echo [OK] MySQL demarre
)

echo.
echo ========================================
echo Projet pret!
echo ========================================
echo.
echo Votre application est accessible a:
echo.
echo   URL: http://onestschooled.local
echo.
echo Base de donnees MySQL:
echo   Host: localhost
echo   Port: 3306
echo   User: root
echo   Pass: (vide par defaut)
echo.
echo ========================================
echo.
echo Appuyez sur une touche pour ouvrir l'application dans votre navigateur...
pause >nul

start http://onestschooled.local

echo.
echo Pour arreter les services, fermez cette fenetre ou utilisez XAMPP Control Panel
echo.
