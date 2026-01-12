@echo off
color 0C
cls
echo ================================
echo FIX SSL - DOUBLE CLIC
echo ================================
echo.
powershell.exe -ExecutionPolicy Bypass -File "%~dp0fix-vps-simple.ps1"
