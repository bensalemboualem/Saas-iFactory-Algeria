@echo off
:: ============================================
:: Start Bolt.diy + BMAD Stack (Local Docker)
:: Windows Version
:: ============================================

setlocal enabledelayedexpansion

echo ========================================
echo   Bolt.diy + BMAD Stack Launcher
echo ========================================
echo.

:: Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

:: Navigate to docker directory
cd /d "%~dp0..\infrastructure\docker"

echo Creating Docker network...
docker network create iafactory-net 2>nul

echo.
echo Starting databases...
docker-compose up -d iafactory-postgres iafactory-redis iafactory-qdrant

echo.
echo Waiting for databases to initialize (15 seconds)...
timeout /t 15 /nobreak >nul

echo.
echo Starting backend API...
docker-compose up -d iafactory-backend

echo.
echo Waiting for backend to be ready (20 seconds)...
timeout /t 20 /nobreak >nul

echo.
echo Starting Bolt.diy Studio with BMAD integration...
docker-compose -f docker-compose.yml -f docker-compose.bolt.yml up -d iafactory-bolt-studio

echo.
echo Waiting for Bolt.diy to be ready (30 seconds)...
timeout /t 30 /nobreak >nul

echo.
echo ========================================
echo   Stack is running!
echo ========================================
echo.
echo   Backend API:     http://localhost:8180
echo   Bolt.diy Studio: http://localhost:8185
echo   API Docs:        http://localhost:8180/docs
echo.
echo   BMAD Agents available in Bolt.diy:
echo     - Winston (Architect)
echo     - John (PM)
echo     - Amelia (Developer)
echo     - Mary (Analyst)
echo     - Murat (Test Architect)
echo.
echo To view logs: docker-compose logs -f
echo To stop:      docker-compose -f docker-compose.yml -f docker-compose.bolt.yml down
echo.

:: Open browser
start http://localhost:8185

pause
