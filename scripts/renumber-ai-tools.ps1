$projectPath = "D:\IAFactory\iafactory-ai-tools"
$replacements = @{
    '"8002:8000"' = '"8220:8000"'
    'localhost:8002' = 'localhost:8220'
    ':8002' = ':8220'
    '"3000:3000"' = '"3110:3000"'
    'localhost:3000' = 'localhost:3110'
    ':3000/' = ':3110/'
    ':5432' = ':5435'
    ':6379' = ':6382'
    '"9000:9000"' = '"9002:9000"'
    '"9001:9001"' = '"9003:9001"'
}
$files = Get-ChildItem -Path $projectPath -Recurse -Include "docker-compose*.yml","*.env*" -File
Write-Host "Renumeration: iafactory-ai-tools" -ForegroundColor Cyan
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
