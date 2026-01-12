@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo    CONNEXION VPS IAFACTORY
echo ========================================
echo.
echo Serveur: root@46.224.3.125
echo.

REM Variables
set VPS_IP=46.224.3.125
set VPS_PW=aINSRFRA#0819692025#
set PLINK=%TEMP%\plink.exe

REM Télécharger plink si nécessaire
if not exist "%PLINK%" (
    echo Telechargement plink.exe...
    powershell -Command "Invoke-WebRequest -Uri 'https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe' -OutFile '%PLINK%' -UseBasicParsing"
    echo OK
    echo.
)

echo Connexion en cours...
echo.

REM Créer un fichier avec y pour accepter la clé
echo y > "%TEMP%\accept.txt"

REM Commandes à exécuter sur le VPS
set "CMD=echo '=== VPS CONNECTE ===' && uname -a && echo '' && docker ps --format 'table {{.Names}}\t{{.Status}}' 2>/dev/null && echo '' && systemctl is-active nginx"

REM Se connecter avec plink
type "%TEMP%\accept.txt" | "%PLINK%" -pw "%VPS_PW%" root@%VPS_IP% "%CMD%"

REM Nettoyer
del "%TEMP%\accept.txt" 2>nul

echo.
echo ========================================
echo    FIN CONNEXION
echo ========================================
echo.
pause
