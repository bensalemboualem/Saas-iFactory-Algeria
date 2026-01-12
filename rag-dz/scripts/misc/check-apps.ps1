# Script de vérification des applications
$appsPath = "d:\IAFactory\rag-dz\apps"
$results = @()

Get-ChildItem -Path $appsPath -Directory | ForEach-Object {
    $appName = $_.Name
    $indexPath = Join-Path $_.FullName "index.html"
    $hasIndex = Test-Path $indexPath
    $fileCount = (Get-ChildItem -Path $_.FullName -File -Recurse | Measure-Object).Count
    $size = (Get-ChildItem -Path $_.FullName -Recurse | Measure-Object -Property Length -Sum).Sum / 1KB

    $results += [PSCustomObject]@{
        App = $appName
        HasIndex = if ($hasIndex) { "✅ OUI" } else { "❌ NON" }
        Files = $fileCount
        "Size(KB)" = [math]::Round($size, 2)
        Status = if ($hasIndex -and $fileCount -gt 0) { "COMPLETE" } else { "INCOMPLETE" }
    }
}

$results | Format-Table -AutoSize

Write-Host "`n📊 RÉSUMÉ:" -ForegroundColor Cyan
$complete = ($results | Where-Object { $_.Status -eq "COMPLETE" }).Count
$incomplete = ($results | Where-Object { $_.Status -eq "INCOMPLETE" }).Count
$total = $results.Count

Write-Host "✅ Apps complètes: $complete / $total" -ForegroundColor Green
Write-Host "❌ Apps incomplètes: $incomplete / $total" -ForegroundColor Red

Write-Host "`n❌ APPS INCOMPLÈTES:" -ForegroundColor Red
$results | Where-Object { $_.Status -eq "INCOMPLETE" } | ForEach-Object {
    Write-Host "  - $($_.App)" -ForegroundColor Yellow
}
