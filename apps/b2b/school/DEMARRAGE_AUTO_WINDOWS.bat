@echo off
REM Ce script configure le demarrage automatique au demarrage de Windows

echo.
echo ========================================
echo   CONFIGURATION DEMARRAGE AUTOMATIQUE
echo ========================================
echo.
echo Cette operation va ajouter BBC School au demarrage automatique de Windows
echo.
echo Voulez-vous continuer? (O/N)
set /p choice="> "

if /i "%choice%"=="O" (
    echo.
    echo Configuration en cours...

    REM Copier le script dans le dossier Startup
    copy /Y "%~dp0START_ONESTSCHOOL.bat" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\BBC_School_Auto.bat" >nul

    echo.
    echo ========================================
    echo   CONFIGURATION TERMINEE!
    echo ========================================
    echo.
    echo BBC School demarrera automatiquement au prochain demarrage de Windows
    echo.
) else (
    echo.
    echo Operation annulee.
    echo.
)

pause
