@echo off
echo ========================================
echo   IAFactory Algeria - Landing Page
echo ========================================
echo.
echo Demarrage du serveur...
echo.
start http://localhost:5555/landing-main-FROM-VPS/
cd /d "d:\IAFactory\rag-dz\apps"
python -m http.server 5555
