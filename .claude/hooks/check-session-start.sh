#!/bin/bash

MEMORY_DIR="$HOME/.claude/projects/-Users-victor-PycharmProjects-claude-dev-kitc/memory"
FLAG_FILE="$MEMORY_DIR/session-needs-summary.flag"

if [ -f "$FLAG_FILE" ]; then
  echo "IMPORTANT: Session summary needed. The file session-needs-summary.flag exists."
  echo "You MUST generate a session summary before proceeding with any other task."
  echo ""
  echo "Steps:"
  echo "1. Read session-metadata.json for basic context"
  echo "2. Generate summary of previous session"
  echo "3. Show summary to user"
  echo "4. Ask about next activities"
  echo "5. Remove the flag file"
  exit 0
else
  # No flag, normal session start
  exit 0
fi
