#!/usr/bin/env bash
# Bulk-creates issues from .github/project-management/issues.json in the
# target GitHub repo, using the GitHub CLI.
#
# Requires: gh CLI authenticated (`gh auth login`), jq installed.
# Run setup-labels.sh and setup-milestones.sh first so labels/milestones exist.
#
# Usage: ./scripts/seed-issues.sh [owner/repo]

set -euo pipefail

REPO="${1:-lumio-network/lumio}"
ISSUES_FILE="$(dirname "$0")/../.github/project-management/issues.json"

if ! command -v gh >/dev/null 2>&1; then
  echo "Error: gh CLI not found. Install from https://cli.github.com/" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "Error: jq not found." >&2
  exit 1
fi

# Build a milestone title -> number map from the repo.
declare -A MILESTONE_NUM
while IFS=$'\t' read -r number title; do
  MILESTONE_NUM["$title"]="$number"
done < <(gh api "repos/$REPO/milestones?state=all&per_page=100" \
  --jq '.[] | [.number, .title] | @tsv')

count=$(jq 'length' "$ISSUES_FILE")
echo "Seeding $count issues into $REPO..."

for i in $(seq 0 $((count - 1))); do
  title=$(jq -r ".[$i].title" "$ISSUES_FILE")
  body=$(jq -r ".[$i].body" "$ISSUES_FILE")
  labels=$(jq -r ".[$i].labels | join(\",\")" "$ISSUES_FILE")
  milestone_title=$(jq -r ".[$i].milestone" "$ISSUES_FILE")
  milestone_num="${MILESTONE_NUM[$milestone_title]:-}"

  args=(--repo "$REPO" --title "$title" --body "$body" --label "$labels")
  if [[ -n "$milestone_num" ]]; then
    args+=(--milestone "$milestone_title")
  fi

  echo "[$((i + 1))/$count] $title"
  gh issue create "${args[@]}" >/dev/null
done

echo "Done. $count issues created in $REPO."
