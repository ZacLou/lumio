#!/usr/bin/env bash
# Creates all milestones defined in .github/project-management/milestones.json
# in the target GitHub repo, using the GitHub CLI's `gh api`.
#
# Requires: gh CLI authenticated (`gh auth login`), jq installed.
# Usage: ./scripts/setup-milestones.sh [owner/repo]

set -euo pipefail

REPO="${1:-lumio-network/lumio}"
MILESTONES_FILE="$(dirname "$0")/../.github/project-management/milestones.json"

if ! command -v gh >/dev/null 2>&1; then
  echo "Error: gh CLI not found. Install from https://cli.github.com/" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "Error: jq not found." >&2
  exit 1
fi

count=$(jq 'length' "$MILESTONES_FILE")

for i in $(seq 0 $((count - 1))); do
  title=$(jq -r ".[$i].title" "$MILESTONES_FILE")
  description=$(jq -r ".[$i].description" "$MILESTONES_FILE")
  due_on=$(jq -r ".[$i].due_on" "$MILESTONES_FILE")

  echo "Creating milestone: $title"
  gh api "repos/$REPO/milestones" \
    -f title="$title" \
    -f description="$description" \
    -f due_on="$due_on" \
    --silent || echo "  (may already exist — skipping)"
done

echo "Done. $count milestones processed for $REPO."
