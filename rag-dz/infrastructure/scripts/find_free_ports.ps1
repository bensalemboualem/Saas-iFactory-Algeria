# Find free ports for RAG.dz services
$portsNeeded = @{
    "Frontend" = 5173
    "Backend" = 8180
    "PostgreSQL" = 5432
    "Redis" = 6379
    "Qdrant" = 6333
    "Qdrant-gRPC" = 6334
    "Prometheus" = 9090
    "Grafana" = 3001
    "Postgres-Exporter" = 9187
    "Redis-Exporter" = 9121
}

$freePorts = @{}

function Test-PortAvailable {
    param([int]$Port)
    $listener = $null
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, $Port)
        $listener.Start()
        $listener.Stop()
        return $true
    }
    catch {
        return $false
    }
    finally {
        if ($listener) { $listener.Stop() }
    }
}

Write-Host "==================================="
Write-Host "VERIFICATION DES PORTS RAG.DZ"
Write-Host "==================================="
Write-Host ""

foreach ($service in $portsNeeded.GetEnumerator()) {
    $serviceName = $service.Key
    $currentPort = $service.Value

    if (Test-PortAvailable -Port $currentPort) {
        Write-Host "[OK] $serviceName : $currentPort (LIBRE)" -ForegroundColor Green
        $freePorts[$serviceName] = $currentPort
    }
    else {
        Write-Host "[CONFLICT] $serviceName : $currentPort (OCCUPE)" -ForegroundColor Red

        # Find alternative port
        $newPort = $currentPort + 1000
        $maxAttempts = 100
        $attempt = 0

        while ((-not (Test-PortAvailable -Port $newPort)) -and ($attempt -lt $maxAttempts)) {
            $newPort++
            $attempt++
        }

        if ($attempt -lt $maxAttempts) {
            Write-Host "    -> PORT LIBRE TROUVE: $newPort" -ForegroundColor Yellow
            $freePorts[$serviceName] = $newPort
        }
        else {
            Write-Host "    -> ERREUR: Aucun port libre trouve!" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "==================================="
Write-Host "RESUME DES PORTS"
Write-Host "==================================="
Write-Host ""

foreach ($service in $freePorts.GetEnumerator() | Sort-Object Name) {
    Write-Host "$($service.Key.PadRight(20)) : $($service.Value)"
}

# Export to JSON
$json = $freePorts | ConvertTo-Json
$json | Out-File -FilePath "C:\Users\bbens\rag-dz\ports_config.json" -Encoding UTF8

Write-Host ""
Write-Host "Configuration exportee vers: ports_config.json" -ForegroundColor Cyan
