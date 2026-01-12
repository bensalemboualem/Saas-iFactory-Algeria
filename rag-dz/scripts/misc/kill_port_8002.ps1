$connections = Get-NetTCPConnection -LocalPort 8002 -ErrorAction SilentlyContinue
if ($connections) {
    $connections | ForEach-Object {
        $processId = $_.OwningProcess
        Write-Host "Killing process PID: $processId on port 8002"
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 2
    Write-Host "Done"
} else {
    Write-Host "Port 8002 is free"
}
