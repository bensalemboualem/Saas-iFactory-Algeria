# archive_project.ps1
Write-Host "Creating source archive for deployment..."

$exclude = @(
    "node_modules",
    ".next",
    ".git",
    "dist",
    ".turbo",
    "build",
    "coverage"
)

# Use tar to respect .gitignore if possible, or just manual exclusion
tar --exclude="node_modules" --exclude=".next" --exclude=".git" --exclude="dist" --exclude=".turbo" -czvf iafactory-source.tar.gz .

Write-Host "Archive created: iafactory-source.tar.gz"
Write-Host "Ready to transfer to VPS!"
