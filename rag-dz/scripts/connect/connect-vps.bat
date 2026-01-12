@echo off
echo ========================================
echo   CONNEXION VPS IAFACTORY
echo ========================================
echo.
echo Serveur: root@46.224.3.125
echo.

REM Télécharger plink si nécessaire
if not exist "%TEMP%\plink.exe" (
    echo Telechargement de plink.exe...
    powershell -Command "Invoke-WebRequest -Uri 'https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe' -OutFile '%TEMP%\plink.exe'"
    echo OK
    echo.
)

echo Connexion en cours...
echo.

REM Créer fichier pour accepter la clé
echo y > "%TEMP%\yes.txt"

REM Se connecter
type "%TEMP%\yes.txt" | "%TEMP%\plink.exe" -pw "Ainsefra+0819692025" root@46.224.3.125 "echo '=== VPS CONNECTE ===' && uname -a && echo '' && docker ps --format 'table {{.Names}}\t{{.Status}}' 2>/dev/null"

del "%TEMP%\yes.txt" 2>nul

echo.
echo ========================================
echo   Connexion terminee
echo ========================================
pause
