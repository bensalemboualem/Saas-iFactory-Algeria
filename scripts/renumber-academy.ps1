# Script de renumerotation des ports - iafactory-academy
$projectPath = "D:\IAFactory\iafactory-academy"

$replacements = @{
    ":8000" = ":8200"
    "8000/" = "8200/"
    "localhost:8000" = "localhost:8200"
    ":3000" = ":3100"
    "3000/" = "3100/"
    "localhost:3000" = "localhost:3100"
    ":5432" = ":5434"
    ":6379" = ":6381"
}

$files = Get-ChildItem -Path $projectPath -Recurse -Include "docker-compose*.yml","*.env*",".env*","package.json" -File

Write-Host "Renumeration ports: iafactory-academy" -ForegroundColor Cyan
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
        Write-Host "  Modifie: $($file.Name)" -ForegroundColor Green
        $total++
    }
}

Write-Host "Total fichiers modifies: $total" -ForegroundColor Yellow
