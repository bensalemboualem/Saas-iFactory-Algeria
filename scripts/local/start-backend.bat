@echo off
title IA FACTORY - BACKEND ENGINE (API)
color 0A

echo ==================================================
echo   STARTING IA FACTORY BACKEND (RAG AGENTS)
echo ==================================================
echo.

:: 1. Define Paths
set "ROOT_DIR=%~dp0"
set "API_DIR=%ROOT_DIR%rag-dz\services\api"
set "VENV_DIR=%API_DIR%\venv"

:: 2. Check API Directory
if not exist "%API_DIR%" (
    echo [ERROR] API directory not found at: %API_DIR%
    pause
    exit /b 1
)

cd /d "%API_DIR%"

:: 3. Setup Python Environment (Simplified for now - assumes python is in PATH)
echo [INFO] checking dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo [WARNING] No requirements.txt found in %API_DIR%
)

:: 4. Start the Server
echo.
echo [INFO] Starting FastAPI Server on Port 8189...
echo [INFO] Logs will appear below. Do NOT close this window.
echo.

python main.py

pause
