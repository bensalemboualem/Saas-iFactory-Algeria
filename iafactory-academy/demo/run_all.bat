@echo off
REM ============================================
REM IAFactory Academy - Lancement Complet
REM ============================================

echo.
echo ============================================
echo  IAFactory Academy - Lancement Complet
echo ============================================
echo.

REM Aller dans le repertoire demo
cd /d "%~dp0"

echo [1/4] Demarrage Demo Generique (port 8502)...
start "Demo Generique" cmd /c "python -m streamlit run minister_demo_generic.py --server.port 8502"
timeout /t 3 /nobreak > nul

echo [2/4] Demarrage Demo BBC (port 8503)...
start "Demo BBC" cmd /c "python -m streamlit run minister_demo_bbc.py --server.port 8503"
timeout /t 3 /nobreak > nul

echo [3/4] Demarrage Chatbot RAG (port 8504)...
start "Chatbot RAG" cmd /c "python -m streamlit run chatbot_rag.py --server.port 8504"
timeout /t 3 /nobreak > nul

echo [4/4] Demarrage AnythingLLM (port 3001)...
cd anythingllm
docker-compose up -d
cd ..
timeout /t 5 /nobreak > nul

echo.
echo ============================================
echo  APPLICATIONS LANCEES
echo ============================================
echo.
echo  Demo Generique : http://localhost:8502
echo  Demo BBC       : http://localhost:8503
echo  Chatbot RAG    : http://localhost:8504
echo  AnythingLLM    : http://localhost:3001
echo.
echo ============================================
echo.

REM Ouvrir le navigateur
echo Ouverture du navigateur...
start http://localhost:8503

echo.
echo Appuyez sur une touche pour fermer...
pause > nul
