#!/usr/bin/env bash
# Runs inside the user's checked-out repo. Makes 1-3 commits, then pushes.
set -euo pipefail
CRITTER="python3 ${GITHUB_ACTION_PATH:-$(dirname "$0")}/critter.py"

mapfile -t who < <($CRITTER whoami)
git config user.name "${who[0]}"
git config user.email "${who[1]}"
echo "Committing as ${who[0]} <${who[1]}>"

made=0
for step in feed diary trophy; do
  $CRITTER "$step"
  if [ -s .critter-msg ]; then
    git add -A -- . ':!.critter-msg'
    if ! git diff --cached --quiet; then
      git commit -q -F .critter-msg
      echo "✔ $(head -1 .critter-msg)"
      made=$((made + 1))
    fi
  fi
done
rm -f .critter-msg

if [ "$made" -eq 0 ]; then
  echo "Already fed today, nothing to commit."
elif [ "${CRITTER_PUSH:-true}" = "true" ]; then
  git push
else
  echo "push: false, so leaving $made commit(s) unpushed."
fi
