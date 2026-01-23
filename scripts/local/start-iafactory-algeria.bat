@echo off
echo Starting IA Factory Services...

echo [1/2] Starting API Gateway (Port 3001)...
start "IA Factory API" cmd /k "pnpm --filter api dev"

echo [2/2] Starting Frontend (Port 3000)...
start "IA Factory Web" cmd /k "pnpm --filter web dev"

echo Both services launched!
echo API: http://localhost:3001
echo Web: http://localhost:3000
pause
