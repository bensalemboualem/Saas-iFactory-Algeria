@echo off
echo ========================================
echo   Browser Automation - IA Factory
echo ========================================
echo.

REM Vérifier Ollama
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Ollama non installe. Telecharger sur https://ollama.ai
    pause
    exit /b 1
)

REM Vérifier modèle
echo [1/3] Verification modele Qwen2.5...
ollama list | findstr "qwen2.5" >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Telechargement qwen2.5:7b...
    ollama pull qwen2.5:7b
)

REM Démarrer Ollama
echo [2/3] Demarrage Ollama...
start /B ollama serve

REM Attendre
timeout /t 3 /nobreak >nul

REM Démarrer API
echo [3/3] Demarrage API sur http://localhost:8100
echo.
python main.py
