# fix(bolt-ui): block unsafe E2B commands + remove hardcoded E2B key

## Summary

- Adds a conservative `isSafeCommand()` validator and enforces it at the API boundary to block command‑injection vectors against the E2B sandbox.
- Removes a hard-coded E2B test API key and makes the helper fail‑fast when no key is present.
- Adds unit + integration tests that prove the validator blocks malicious input and that allowed commands still run.
- Small devcontainer fix: set `docker-outside-of-docker.moby = false` to avoid MOBY install on Debian 'trixie'.

## Why

Critical P0 fix — server previously forwarded unvalidated shell commands to E2B (remote sandbox). This patch prevents immediate remote command injection and adds regression tests.

## Scope

- `apps/bolt-ui/app/routes/api.e2b.ts` (validator + enforcement)
- `apps/bolt-ui/tests/api-e2b-security.spec.ts` (new)
- `apps/bolt-ui/test-e2b.ts` (remove hardcoded key)
- `.devcontainer/devcontainer.json` (moby=false)

## Testing / QA checklist ✅

- [ ] Unit tests: `pnpm -w -F @iafactory/bolt-ui test -- tests/api-e2b-security.spec.ts` ✅
- [ ] Typechecks for `apps/bolt-ui` (local) ✅
- [ ] No E2B API keys checked into repo (`grep -R "e2b_[0-9a-f]\{20,\}" apps/bolt-ui`) ✅
- [ ] Reviewers: `@bolt-ui-maintainers`, `@security-owner`

## Rollout / Rollback

- Rollout: merge to `main` → CI will run full suite; monitor errors and sandbox telemetry for 24h.
- Rollback: `git revert <commit>` if emergency.

## Acceptance criteria

- `isSafeCommand()` blocks metacharacters, quotes, and disallowed npm/pnpm scripts.
- Tests asserting unsafe commands receive HTTP 400 pass.
- No hardcoded E2B keys remain in `apps/bolt-ui`.

---

If you want the prototype PR opened now too, tell me and I will create a draft once the pre-commit issues are resolved.
