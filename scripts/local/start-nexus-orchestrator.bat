@echo off
title IA FACTORY - NEXUS META-ORCHESTRATOR
color 0B

echo ==================================================
echo   STARTING NEXUS META-ORCHESTRATOR (PORT 8000)
echo ==================================================
echo.

:: Define Paths
set "ROOT_DIR=%~dp0"
set "NEXUS_DIR=%ROOT_DIR%rag-dz\orchestrators\meta"

:: Check Directory
if not exist "%NEXUS_DIR%" (
    echo [ERROR] Nexus directory not found at: %NEXUS_DIR%
    pause
    exit /b 1
)

cd /d "%NEXUS_DIR%"

:: Install dependencies if needed
echo [INFO] Checking dependencies...
pip install -r requirements.txt -q

:: Set environment variables
set REDIS_URL=redis://localhost:6379
set SESSION_TTL=3600
set LOCK_TTL=300

:: Start the Nexus Meta-Orchestrator
echo.
echo [INFO] Starting Nexus Meta-Orchestrator on Port 8000...
echo [INFO] Redis URL: %REDIS_URL%
echo [INFO] Logs will appear below. Do NOT close this window.
echo.

python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

pause
