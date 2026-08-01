#!/usr/bin/env bash
# Creates a GitHub Projects (v2) Kanban board for Lumio and links it to the repo.
# GitHub Projects v2 has no declarative file format, so this is scripted via
# `gh project` rather than checked-in config.
#
# Requires: gh CLI authenticated with `project` scope
#   (gh auth refresh -s project), owner must be an org or user you admin.
# Usage: ./scripts/setup-project-board.sh [owner] [repo]

set -euo pipefail

OWNER="${1:-lumio-network}"
REPO="${2:-lumio}"

if ! command -v gh >/dev/null 2>&1; then
  echo "Error: gh CLI not found. Install from https://cli.github.com/" >&2
  exit 1
fi

echo "Creating project board..."
PROJECT_JSON=$(gh project create --owner "$OWNER" --title "Lumio Roadmap" --format json)
PROJECT_NUMBER=$(echo "$PROJECT_JSON" | jq -r '.number')

echo "Linking repo $OWNER/$REPO to project #$PROJECT_NUMBER..."
gh project link "$PROJECT_NUMBER" --owner "$OWNER" --repo "$OWNER/$REPO"

echo "Adding standard status field options (Backlog, Ready, In Progress, In Review, Done)..."
# The default "Status" field already ships with Todo/In Progress/Done; add the
# rest to match our workflow via gh project field-create for a single-select field.
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" \
  --name "Difficulty" \
  --data-type "SINGLE_SELECT" \
  --single-select-options "Good first issue,Intermediate,Advanced" || true

echo "Project #$PROJECT_NUMBER created and linked."
echo "Next: run scripts/setup-labels.sh, scripts/setup-milestones.sh, then scripts/seed-issues.sh"
echo "so the board has real cards. Add the repo's issues to the board with:"
echo "  gh issue list --repo $OWNER/$REPO --limit 200 --json number --jq '.[].number' | \\"
echo "    xargs -I{} gh project item-add $PROJECT_NUMBER --owner $OWNER --url https://github.com/$OWNER/$REPO/issues/{}"
