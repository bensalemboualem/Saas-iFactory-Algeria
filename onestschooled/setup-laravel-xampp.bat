@echo off
echo ========================================
echo Configuration automatique Laravel + XAMPP
echo ========================================
echo.

REM Vérifier les droits administrateur
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERREUR: Ce script doit etre execute en tant qu'administrateur!
    echo Faites un clic droit sur le fichier et selectionnez "Executer en tant qu'administrateur"
    pause
    exit /b 1
)

echo [1/4] Configuration du Virtual Host Apache...
echo.

REM Sauvegarder le fichier httpd-vhosts.conf
copy /Y C:\xampp\apache\conf\extra\httpd-vhosts.conf C:\xampp\apache\conf\extra\httpd-vhosts.conf.backup

REM Créer le nouveau fichier httpd-vhosts.conf
(
echo # Virtual Hosts
echo #
echo # Required modules: mod_log_config
echo.
echo # Laravel Project - OneStSchooled
echo ^<VirtualHost *:80^>
echo     ServerAdmin admin@onestschooled.local
echo     DocumentRoot "C:/xampp/htdocs/onestschooled-test/public"
echo     ServerName onestschooled.local
echo     ServerAlias www.onestschooled.local
echo.
echo     ^<Directory "C:/xampp/htdocs/onestschooled-test/public"^>
echo         Options Indexes FollowSymLinks MultiViews
echo         AllowOverride All
echo         Require all granted
echo     ^</Directory^>
echo.
echo     ErrorLog "logs/onestschooled-error.log"
echo     CustomLog "logs/onestschooled-access.log" common
echo ^</VirtualHost^>
echo.
echo # Default localhost
echo ^<VirtualHost *:80^>
echo     DocumentRoot "C:/xampp/htdocs"
echo     ServerName localhost
echo     ^<Directory "C:/xampp/htdocs"^>
echo         Options Indexes FollowSymLinks MultiViews
echo         AllowOverride All
echo         Require all granted
echo     ^</Directory^>
echo ^</VirtualHost^>
) > C:\xampp\apache\conf\extra\httpd-vhosts.conf

echo Configuration Apache creee avec succes!
echo.

echo [2/4] Activation du Virtual Host dans httpd.conf...
echo.

REM Vérifier si le vhost est déjà activé
findstr /C:"Include conf/extra/httpd-vhosts.conf" C:\xampp\apache\conf\httpd.conf | findstr /V "#" >nul
if %errorLevel% neq 0 (
    REM Sauvegarder httpd.conf
    copy /Y C:\xampp\apache\conf\httpd.conf C:\xampp\apache\conf\httpd.conf.backup

    REM Activer le vhost (décommenter la ligne)
    powershell -Command "(Get-Content C:\xampp\apache\conf\httpd.conf) -replace '#Include conf/extra/httpd-vhosts.conf', 'Include conf/extra/httpd-vhosts.conf' | Set-Content C:\xampp\apache\conf\httpd.conf"
    echo Virtual Host active dans httpd.conf
) else (
    echo Virtual Host deja active
)
echo.

echo [3/4] Modification du fichier hosts Windows...
echo.

REM Vérifier si l'entrée existe déjà
findstr /C:"onestschooled.local" C:\Windows\System32\drivers\etc\hosts >nul
if %errorLevel% neq 0 (
    REM Sauvegarder le fichier hosts
    copy /Y C:\Windows\System32\drivers\etc\hosts C:\Windows\System32\drivers\etc\hosts.backup

    REM Ajouter l'entrée
    echo 127.0.0.1 onestschooled.local >> C:\Windows\System32\drivers\etc\hosts
    echo 127.0.0.1 www.onestschooled.local >> C:\Windows\System32\drivers\etc\hosts
    echo Entree ajoutee au fichier hosts
) else (
    echo Entree deja presente dans le fichier hosts
)
echo.

echo [4/4] Redemarrage d'Apache...
echo.

REM Arrêter Apache
C:\xampp\apache\bin\httpd.exe -k stop 2>nul
timeout /t 2 /nobreak >nul

REM Démarrer Apache
C:\xampp\apache\bin\httpd.exe -k start

echo.
echo ========================================
echo Configuration terminee avec succes!
echo ========================================
echo.
echo Votre projet Laravel est maintenant accessible a:
echo   http://onestschooled.local
echo   http://www.onestschooled.local
echo.
echo XAMPP reste accessible via:
echo   http://localhost
echo.
echo IMPORTANT: Assurez-vous que Apache est demarre dans XAMPP Control Panel
echo.
pause
