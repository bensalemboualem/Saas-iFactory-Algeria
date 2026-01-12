@echo off
echo === CONNEXION VPS ===
echo.

REM Telecharger plink si necessaire
if not exist "%TEMP%\plink.exe" (
    echo Telechargement plink...
    powershell -Command "Invoke-WebRequest -Uri 'https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe' -OutFile '%TEMP%\plink.exe'"
)

echo Connexion...
echo.

REM Connexion avec acceptation automatique
echo y | "%TEMP%\plink.exe" -pw "Ainsefra*0819692025*" root@46.224.3.125 "docker --version 2>&1 || echo 'Docker NON installe'"

echo.
echo === TERMINE ===
pause
