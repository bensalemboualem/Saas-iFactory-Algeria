@echo off
title IA FACTORY - RESTART NEXUS API
color 0E

echo ==================================================
echo   RESTARTING NEXUS API SERVICE (PORT 8000)
echo ==================================================
echo.

:: Kill any process on port 8000
echo [1/3] Stopping existing processes on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do (
    echo Killing PID: %%a
    taskkill /f /pid %%a >nul 2>&1
)
timeout /t 2 /nobreak >nul

:: Navigate to API directory
set "ROOT_DIR=%~dp0"
set "API_DIR=%ROOT_DIR%rag-dz\services\api"

if not exist "%API_DIR%" (
    echo [ERROR] API directory not found at: %API_DIR%
    pause
    exit /b 1
)

cd /d "%API_DIR%"

:: Ensure .env is loaded
echo [2/3] Loading environment from .env...
if exist ".env" (
    for /f "delims=" %%x in (.env) do (
        set "%%x" 2>nul
    )
)

:: Start the API
echo [3/3] Starting Nexus API on port 8000...
echo.
echo Press Ctrl+C to stop the server.
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
