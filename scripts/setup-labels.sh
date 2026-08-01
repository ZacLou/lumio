#!/usr/bin/env bash
# Creates/updates all labels defined in .github/project-management/labels.yml
# in the target GitHub repo, using the GitHub CLI.
#
# Requires: gh CLI authenticated (`gh auth login`), yq installed.
# Usage: ./scripts/setup-labels.sh [owner/repo]

set -euo pipefail

REPO="${1:-lumio-network/lumio}"
LABELS_FILE="$(dirname "$0")/../.github/project-management/labels.yml"

if ! command -v gh >/dev/null 2>&1; then
  echo "Error: gh CLI not found. Install from https://cli.github.com/" >&2
  exit 1
fi

if ! command -v yq >/dev/null 2>&1; then
  echo "Error: yq not found. Install from https://github.com/mikefarah/yq" >&2
  exit 1
fi

count=$(yq eval '. | length' "$LABELS_FILE")

for i in $(seq 0 $((count - 1))); do
  name=$(yq eval ".[$i].name" "$LABELS_FILE")
  color=$(yq eval ".[$i].color" "$LABELS_FILE")
  description=$(yq eval ".[$i].description" "$LABELS_FILE")

  echo "Upserting label: $name"
  gh label create "$name" \
    --repo "$REPO" \
    --color "$color" \
    --description "$description" \
    --force
done

echo "Done. $count labels synced to $REPO."
