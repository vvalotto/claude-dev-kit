#!/bin/bash

# Directorios
PROJECT_DIR="$CLAUDE_PROJECT_DIR"
MEMORY_DIR="$HOME/.claude/projects/-Users-victor-PycharmProjects-claude-dev-kitc/memory"

# Leer hook input desde stdin
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
REASON=$(echo "$INPUT" | jq -r '.reason // "other"')
TRANSCRIPT=$(echo "$INPUT" | jq -r '.transcript_path // ""')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Guardar metadata de la sesión
jq -n \
  --arg session_id "$SESSION_ID" \
  --arg reason "$REASON" \
  --arg transcript "$TRANSCRIPT" \
  --arg timestamp "$TIMESTAMP" \
  --arg git_status "$(cd "$PROJECT_DIR" 2>/dev/null && git status --short 2>/dev/null || echo 'N/A')" \
  --arg git_branch "$(cd "$PROJECT_DIR" 2>/dev/null && git branch --show-current 2>/dev/null || echo 'N/A')" \
  '{
    session_id: $session_id,
    exit_reason: $reason,
    transcript_path: $transcript,
    timestamp: $timestamp,
    git_status: $git_status,
    git_branch: $git_branch
  }' > "$MEMORY_DIR/session-metadata.json" 2>/dev/null

# Crear flag para indicar que necesitamos generar resumen en próxima sesión
touch "$MEMORY_DIR/session-needs-summary.flag"

echo "✅ Session saved. Summary will be ready on next start." >&2
exit 0
