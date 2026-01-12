Get-Process | Where-Object {$_.ProcessName -eq 'python'} | ForEach-Object {
    Write-Host "Killing Python process PID: $($_.Id)"
    Stop-Process -Id $_.Id -Force
}
Start-Sleep -Seconds 2
Write-Host "Done"
