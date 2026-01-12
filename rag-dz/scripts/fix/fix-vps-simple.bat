@echo off
echo Telechargement plink...
if not exist "%TEMP%\plink.exe" (
    powershell -Command "Invoke-WebRequest -Uri 'https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe' -OutFile '%TEMP%\plink.exe'"
)

echo Connexion au VPS...
echo.

echo y | "%TEMP%\plink.exe" -batch -pw "Ainsefra+0819692025" root@46.224.3.125 "echo '=== DIAGNOSTIC VPS ===' && docker ps 2>/dev/null || echo 'Docker pas installé' && echo '' && ls -la ~/rag-dz 2>/dev/null || echo 'Code pas cloné'"

pause
