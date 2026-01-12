<#
    Check docker-compose files for misplaced env_file entries

    This script checks the root docker-compose.yml and potential compose files under the repo for 'env_file' entries
    that are placed outside service definitions (e.g., under volumes). This helps avoid YAML validation errors.
#>

Write-Host "Checking docker-compose files for misplaced 'env_file' entries..."

$files = Get-ChildItem -Path . -Recurse -Include 'docker-compose*.yml','docker-compose*.yaml' -ErrorAction SilentlyContinue
if (-not $files){
    Write-Host "No docker-compose files found in the repo root or subfolders."
    exit 0
}

foreach ($f in $files){
    Write-Host "Inspecting: $($f.FullName)"
    $lines = Get-Content -Path $f.FullName -ErrorAction SilentlyContinue
    for ($i=0; $i -lt $lines.Length; $i++){
        if ($lines[$i] -match "^\s*env_file:\s*$"){
            # Find last non-empty header preceding this line
            $j = $i - 1
            while ($j -ge 0 -and $lines[$j] -match '^\s*$') { $j-- }
            $headerLine = $lines[$j]
            if ($headerLine -match '^\s*volumes:\s*$' -or $headerLine -match '^\s*networks:\s*$' -or $headerLine -match '^\s*secrets:\s*$'){
                Write-Warning "Found env_file under a non-service section in file $($f.FullName) at line $($i+1). This is invalid for docker-compose."
            } else {
                # Also try to detect top-level env_file (top-level mapping key) by checking indent using regex match groups
                $m = [regex]::Match($lines[$i], '^(\s*)env_file')
                $indent = $m.Groups[1].Value
                if ($indent.Length -eq 0 -and $headerLine -match '^\s*services:\s*$'){
                    Write-Warning "Found top-level env_file entry at line $($i+1) - ensure it's under a service block, not top-level."
                }
            }
        }
    }
}

Write-Host "Done. If warnings were printed, consider moving 'env_file:' lines under the 'services' entries only." -ForegroundColor Cyan

Exit 0
