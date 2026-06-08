#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

COMMIT_MESSAGE="${1:-chore: publish tracker reports}"

git add reports

if git diff --cached --quiet; then
  echo "No report changes to commit."
  exit 0
fi

git commit -m "$COMMIT_MESSAGE"
git push origin main

echo "Published reports and pushed to origin/main."
