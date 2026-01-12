$projectPath = "D:\IAFactory\iafactory-video-platform"
$replacements = @{
    '"8000:8000"' = '"8240:8000"'
    'localhost:8000' = 'localhost:8240'
    ':8000/' = ':8240/'
    '"3000:3000"' = '"3120:3000"'
    'localhost:3000' = 'localhost:3120'
    ':3000/' = ':3120/'
    ':5432' = ':5436'
    ':6379' = ':6383'
    '"5555:5555"' = '"5556:5555"'
    '"9000:9000"' = '"9004:9000"'
    '"9001:9001"' = '"9005:9001"'
}
$files = Get-ChildItem -Path $projectPath -Recurse -Include "docker-compose*.yml","*.env*" -File
Write-Host "Renumeration: iafactory-video-platform" -ForegroundColor Cyan
$total = 0
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $modified = $false
    foreach ($old in $replacements.Keys) {
        if ($content -match [regex]::Escape($old)) {
            $content = $content -replace [regex]::Escape($old), $replacements[$old]
            $modified = $true
        }
    }
    if ($modified) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        Write-Host "  $($file.Name)" -ForegroundColor Green
        $total++
    }
}
Write-Host "Total: $total" -ForegroundColor Yellow
