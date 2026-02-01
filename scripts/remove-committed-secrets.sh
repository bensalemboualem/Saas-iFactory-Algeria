#!/usr/bin/env bash
set -euo pipefail

# WARNING: history-rewrite is destructive. Read the instructions below before running.
# Usage:
#   ./scripts/remove-committed-secrets.sh --dry-run
#   ./scripts/remove-committed-secrets.sh
#
# What this does (safe default):
# 1. Removes sensitive files from the current index (keeps working tree) and creates a commit.
# 2. Adds a branch you can push to open an emergency PR.
#
# For FULL history purge (recommended after rotation): follow the 'HISTORY PURGE' section below.

DRY_RUN=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) sed -n '1,160p' "$0"; exit 0 ;;
    *) echo "Unknown arg: $1"; exit 2 ;;
  esac
done

echo "This script will prepare a non-history-rewriting cleanup branch to remove tracked secrets and build artifacts from apps/bolt-ui."
read -p "Proceed (type 'yes' to continue)? " confirm
if [[ "$confirm" != "yes" ]]; then
  echo "Aborted."; exit 1
fi

BRANCH="chore/bulk/remove-committed-secrets"

if [[ $DRY_RUN -eq 1 ]]; then
  echo "DRY RUN: listing files that would be removed from git index..."
  git ls-files -- "apps/bolt-ui/.env.local" "apps/bolt-ui/build" || true
  echo
  echo "Suggested next command to run (non-dry-run):"
  echo "  ./scripts/remove-committed-secrets.sh"
  exit 0
fi

# 1) Remove tracked sensitive files (keep working copy)
git checkout -b "$BRANCH" || git switch "$BRANCH"

git rm --cached --ignore-unmatch apps/bolt-ui/.env.local || true
git rm -r --cached --ignore-unmatch apps/bolt-ui/build || true

# Ensure .gitignore contains entries (it already should; this is idempotent)
if ! grep -q "^/build$" apps/bolt-ui/.gitignore 2>/dev/null; then
  printf "%s\n" "/build" >> apps/bolt-ui/.gitignore
fi
if ! grep -q "^\.env.local$" apps/bolt-ui/.gitignore 2>/dev/null; then
  printf "%s\n" ".env.local" >> apps/bolt-ui/.gitignore
fi

# 2) Commit the cleanup
git add apps/bolt-ui/.gitignore || true
if git diff --staged --quiet; then
  echo "No staged changes to commit (nothing to remove)."
else
  git commit -m "chore(bolt-ui): remove tracked build artifacts and local env; add .gitignore entries" || true
fi

cat <<'INSTR'
NEXT STEPS (manual):

A) Immediately rotate/revoke the exposed keys (E2B, OpenAI-style, IAFactory) from provider consoles.
   - Do NOT reuse the leaked keys anywhere.
   - Replace them in your secret manager / CI (do not commit to repo).

B) Push this branch and open an emergency PR with the rotation checklist.
   git push -u origin HEAD
   gh pr create --title "chore(bolt-ui): remove committed secrets + rotation checklist" --body-file pr_bodies/security.md --label security,p0,bolt-ui

C) To purge secrets from git history (coordination required):
   - Preferred: use git-filter-repo on a mirrored clone (recommended for large repos)

     # Example (dry-run -- create a backup first):
     git clone --mirror git@github.com:<org>/<repo>.git repo-mirror.git
     cd repo-mirror.git
     # remove paths from history
     git filter-repo --invert-paths --paths apps/bolt-ui/.env.local --paths apps/bolt-ui/build
     # force-push the cleaned mirror (ALL collaborators must re-clone afterwards)
     git push --force

   - Alternative (BFG):
     git clone --mirror git@github.com:<org>/<repo>.git repo-mirror.git
     java -jar bfg.jar --delete-files apps/bolt-ui/.env.local repo-mirror.git
     cd repo-mirror.git
     git reflog expire --expire=now --all && git gc --prune=now --aggressive
     git push --force

D) After history purge, coordinate with all repo contributors to reclone and rotate any personal tokens.

If you want, I can generate the exact git-filter-repo replace/--paths file and the PR body (I already drafted one).
INSTR
