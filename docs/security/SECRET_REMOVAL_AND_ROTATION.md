## Emergency secret removal & rotation — quick playbook

Severity: P0 — perform immediately

1) Rotate & revoke (do first) ✅
   - Revoke the exposed E2B API key(s) and any OpenAI-style keys found.
   - Rotate keys used in: IAFactory dashboard, OpenAI/partner consoles, cloud providers, CI.
   - Replace secrets in your secret store (Vault/Secrets Manager/GitHub Actions secrets) — do not commit them.

2) Make a minimal repo cleanup commit (non-history-rewriting) ✅
   - Remove tracked secrets and build artifacts from the index and add .gitignore entries.
   - Use the prepared script:
     ./scripts/remove-committed-secrets.sh
   - Push the branch and open an emergency PR titled: "Remove committed secrets + rotation checklist".

3) Purge repository history (coordinate) ⚠️
   - Use `git-filter-repo` (recommended) or `BFG Repo-Cleaner` on a mirror clone.
   - Example (git-filter-repo):
     git clone --mirror git@github.com:<org>/<repo>.git repo-mirror.git
     cd repo-mirror.git
     git filter-repo --invert-paths --paths apps/bolt-ui/.env.local --paths apps/bolt-ui/build
     git push --force
   - Notify all contributors to reclone and rotate any local/stored tokens.

4) Block regressions (done / to ship) ✅
   - Add CI secret-grep (fast, high-confidence patterns). See `.github/workflows/ci-e2b-preview.yml`.
   - Add an in-repo unit test that fails when patterns are present: `apps/bolt-ui/tests/secret-regression.spec.ts`.
   - Add pre-merge branch protection to require the secret-scan job to pass.

5) Post-incident actions
   - Audit access logs where the leaked keys could have been used.
   - Rotate downstream credentials that may have been derived from leaked keys.
   - Send incident notification to stakeholders with rotated key IDs and rotation time.

6) Communication template (short):
   - "Security incident: API keys for bolt-ui were committed to the repository. Keys have been revoked and rotated. A PR #NNN contains the repo cleanup and CI guardrails. All contributors must reclone after the history purge. See <link-to-incident-runbook>."

If you want, I can:
- Produce the exact `git-filter-repo` replacement file and command for your repo.
- Draft the emergency PR and incident notification message.
- Open a draft PR (if you provide push access) or provide the exact git commands to run locally.
