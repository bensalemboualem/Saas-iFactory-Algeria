### bolt-ui — Security

- **Fixed**: Prevent command injection in E2B proxy API by validating and escaping shell/command input. (apps/bolt-ui/app/routes/api.e2b.ts)
- **Fixed**: Removed hardcoded E2B API key from test helper and fail-fast when key missing. (apps/bolt-ui/test-e2b.ts)
- **Dev**: Devcontainer: set `docker-outside-of-docker.moby = false` to support Debian 'trixie'. (.devcontainer/devcontainer.json)

References: docs/audit/2026-02-01-bolt-ui/audit-report.md
