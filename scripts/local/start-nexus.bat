@echo off
setlocal
title IA FACTORY NEXUS LAUNCHER

echo ==================================================
echo   IA FACTORY - NEXUS SAAS LAUNCHER
echo ==================================================
echo.

set "ROOT_DIR=%~dp0"
set "BOLT_DIR=%ROOT_DIR%rag-dz\bolt-diy"
set "LANDING_FILE=%ROOT_DIR%rag-dz\apps\iafactory-landing\index.html"

:: 0. CLEANUP: Kill textually to avoid PID lookup
echo [0/3] Cleaning up old ports (5183, 5184, 8188, 8189)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5183" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5184" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8188" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8189" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1
echo Ports cleaned.

:: 1. Check if Bolt exists
if not exist "%BOLT_DIR%" (
    echo [ERROR] Bolt directory not found at: %BOLT_DIR%
    echo Please verify the installation.
    pause
    exit /b 1
)

:: 2. Start Bolt Frontend (Nexus)
echo [1/3] Starting Bolt Nexus (Frontend)...

cd /d "%BOLT_DIR%"

if not exist "package.json" (
    echo [ERROR] FAIL: No package.json found in %BOLT_DIR%
    pause
    exit /b 1
)

if not exist "node_modules" (
    echo [WARNING] Dependencies missing. Installing...
    call pnpm install
)

set PORT=5184
start "IA Factory Nexus" cmd /k "pnpm run dev"

:: 3. Start Python Backend (Agents)
echo [2/3] Starting AI Agents Backend...
start "IA Factory Backend" "%ROOT_DIR%start-backend.bat"

:: 4. Launch Landing Page (Integrated)
echo [3/3] Landing Page is integrated into Bolt (public/landing).
timeout /t 2 /nobreak >nul

echo.
echo ==================================================
echo   NEXUS IS RUNNING!
echo   - App: http://localhost:5184
echo   - Landing: http://localhost:5184/landing/index.html
echo ==================================================
echo.
pause
