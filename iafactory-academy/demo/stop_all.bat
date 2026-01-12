@echo off
REM ============================================
REM IAFactory Academy - Arret Complet
REM ============================================

echo.
echo ============================================
echo  IAFactory Academy - Arret des Services
echo ============================================
echo.

REM Aller dans le repertoire demo
cd /d "%~dp0"

echo [1/2] Arret des applications Streamlit...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Demo*" 2>nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Chatbot*" 2>nul

echo [2/2] Arret de AnythingLLM...
cd anythingllm
docker-compose down
cd ..

echo.
echo ============================================
echo  TOUS LES SERVICES ARRETES
echo ============================================
echo.

pause
