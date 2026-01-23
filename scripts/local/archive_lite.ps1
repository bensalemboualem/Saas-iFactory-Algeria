# archive_lite.ps1
Write-Host "Creating LITE archive for IA Factory Chat..."

# Define what to include as a single string for arguments
# Note: In PowerShell passing arrays to external commands varies. Best to join them or pass explicitly.

$includes = "apps/web packages scripts locales package.json pnpm-workspace.yaml turbo.json Dockerfile* docker-compose* .env.staging.example tsconfig.json next.config.ts"

# Use tar
Write-Host "Compressing select folders..."
Invoke-Expression "tar --exclude='node_modules' --exclude='.next' --exclude='.git' --exclude='dist' --exclude='build' --exclude='coverage' -czvf iafactory-lite.tar.gz $includes"

Write-Host "Lite Archive created: iafactory-lite.tar.gz"
Write-Host "Use this for staging deployment to avoid uploading unrelated projects."
