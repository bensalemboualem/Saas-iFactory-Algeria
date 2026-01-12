# Scripts to manage development environment

This folder contains helpful PowerShell automation scripts used to safely start and validate the project services locally.

Files:
- `start-all-interfaces.ps1` - Start Docker Compose, make sure a `.env.local` exists for the backend, wait for backend to become healthy, and open the frontends in your browser.
- `check-docker-compose-envfile.ps1` - Inspect docker-compose files and warn for invalid `env_file` placement (e.g., under volumes/networks or as top-level keys).

Usage examples:

PowerShell (from repo root):
    # Check for misplaced env_file entries (non-destructive)
    pwsh.exe -NoProfile -Command "./scripts/check-docker-compose-envfile.ps1"

    # Start services and open frontends (creates .env.local from .env if missing)
    pwsh.exe -NoProfile -Command "./scripts/start-all-interfaces.ps1"

Notes & Safety:
- The scripts create safe backups of existing `.env.local` as `.env.local.bak.YYYYMMDD-HHMMSS`.
- The scripts do not overwrite `.env`. They only create `.env.local` by copying `.env` if needed (safe default behavior).
- Always verify `.env` content to ensure the correct environment variables and secrets are present before running.
- These scripts are intended to help in local development only.
