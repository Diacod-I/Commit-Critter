#!/usr/bin/env bash
# Dry-runs the workflow on your machine: same 3 commit steps, in a throwaway git repo, no push.
# Usage:  ./test_local.sh <github-username>
set -euo pipefail
USER_NAME="${1:?usage: ./test_local.sh <github-username>}"
SRC="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
cp "$SRC/pet.py" "$SRC/.gitignore" "$TMP/"
cd "$TMP"
git init -q
git config user.name "test" && git config user.email "test@example.com"
git add -A && git commit -qm "init"

export GH_USER="$USER_NAME" GITHUB_REPOSITORY="$USER_NAME/snail"
for step in feed diary trophy; do
  python3 pet.py "$step"
  git add -A
  git diff --cached --quiet && echo "[$step] nothing to commit (expected for trophy on most days)" || git commit -qF .msg
done

echo; echo "=== commits the bot would make ==="; git log --oneline -n 3 | grep -v init || true
echo; echo "=== README ==="; cat README.md
echo; echo "(scratch repo left at $TMP so you can poke around)"
