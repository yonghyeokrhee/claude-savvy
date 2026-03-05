#!/bin/bash
# Auto-commit watcher for claude-savvy GitBook
# Watches for file changes and commits automatically

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
DEBOUNCE_SECONDS=3
LAST_COMMIT_TIME=0

echo "Watching $REPO_DIR for changes..."
echo "Press Ctrl+C to stop."

# Requires: fswatch (install with: brew install fswatch)
if ! command -v fswatch &>/dev/null; then
  echo "Error: fswatch is not installed."
  echo "Install it with: brew install fswatch"
  exit 1
fi

fswatch -r --exclude="\.git" "$REPO_DIR" | while read -r changed_file; do
  NOW=$(date +%s)
  ELAPSED=$((NOW - LAST_COMMIT_TIME))

  # Debounce: skip if last commit was within DEBOUNCE_SECONDS
  if [ "$ELAPSED" -lt "$DEBOUNCE_SECONDS" ]; then
    continue
  fi

  cd "$REPO_DIR" || exit 1

  # Skip if nothing to commit
  if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    continue
  fi

  git add -A

  COMMIT_MSG="auto: update $(basename "$changed_file") at $(date '+%Y-%m-%d %H:%M:%S')"
  git commit -m "$COMMIT_MSG"

  echo "Committed: $COMMIT_MSG"
  LAST_COMMIT_TIME=$(date +%s)
done
