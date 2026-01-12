# Connect to IAFactory VPS
# Usage: .\connect-vps.ps1

$VPS_IP = "46.224.3.125"
$VPS_USER = "root"

Write-Host "🔌 Connecting to IAFactory VPS..." -ForegroundColor Cyan
Write-Host "VPS: $VPS_USER@$VPS_IP" -ForegroundColor Yellow
Write-Host ""

# Check if SSH is available
if (Get-Command ssh -ErrorAction SilentlyContinue) {
    # Use OpenSSH
    ssh "${VPS_USER}@${VPS_IP}"
} else {
    Write-Host "❌ OpenSSH not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "1. Install OpenSSH: Settings > Apps > Optional Features > OpenSSH Client"
    Write-Host "2. Use PuTTY: Download from https://putty.org/"
    Write-Host "3. Use existing scripts: .\connect-and-diagnose.ps1"
    Write-Host ""
    Write-Host "PuTTY Connection Details:" -ForegroundColor Cyan
    Write-Host "  Host: $VPS_IP"
    Write-Host "  Port: 22"
    Write-Host "  User: $VPS_USER"
}
