#!/usr/bin/env pwsh
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "🚀 Démarrage du stack de monitoring (Prometheus + Grafana)..." -ForegroundColor Cyan

$services = @('iafactory-prometheus', 'iafactory-grafana')
docker compose --profile monitoring up -d @services
docker compose --profile monitoring ps

Write-Host ""
Write-Host "Prometheus: http://localhost:8187" -ForegroundColor Green
Write-Host ("Grafana   : http://localhost:8188 (admin / {0})" -f ($env:GRAFANA_PASSWORD ?? 'admin')) -ForegroundColor Green

