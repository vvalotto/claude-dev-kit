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
HUMAN_TIMESTAMP=$(date +"%Y-%m-%d %H:%M")

# Capturar info de git
cd "$PROJECT_DIR" 2>/dev/null || exit 0
GIT_STATUS=$(git status --short 2>/dev/null || echo 'N/A')
GIT_BRANCH=$(git branch --show-current 2>/dev/null || echo 'N/A')

# Leer timestamp de sesión anterior para capturar commits desde entonces
LAST_TIMESTAMP=""
if [ -f "$MEMORY_DIR/session-metadata.json" ]; then
  LAST_TIMESTAMP=$(jq -r '.timestamp // ""' "$MEMORY_DIR/session-metadata.json" 2>/dev/null)
fi

# Capturar commits desde la última sesión
COMMITS=""
if [ -n "$LAST_TIMESTAMP" ]; then
  COMMITS=$(git log --since="$LAST_TIMESTAMP" --pretty=format:"- %h %s" 2>/dev/null)
fi

# Si no hay commits desde última sesión, intentar últimos 20 commits del día
if [ -z "$COMMITS" ]; then
  COMMITS=$(git log --since="24 hours ago" --pretty=format:"- %h %s" -20 2>/dev/null)
fi

# Guardar metadata de la sesión
jq -n \
  --arg session_id "$SESSION_ID" \
  --arg reason "$REASON" \
  --arg transcript "$TRANSCRIPT" \
  --arg timestamp "$TIMESTAMP" \
  --arg git_status "$GIT_STATUS" \
  --arg git_branch "$GIT_BRANCH" \
  '{
    session_id: $session_id,
    exit_reason: $reason,
    transcript_path: $transcript,
    timestamp: $timestamp,
    git_status: $git_status,
    git_branch: $git_branch
  }' > "$MEMORY_DIR/session-metadata.json" 2>/dev/null

# Actualizar session-current.md con los commits de esta sesión
if [ -n "$COMMITS" ]; then
  cat >> "$MEMORY_DIR/session-current.md" <<EOF

---

## 📝 Sesión Finalizada: $HUMAN_TIMESTAMP

**Branch:** $GIT_BRANCH
**Exit Reason:** $REASON

### Commits en esta sesión:
$COMMITS

**Próxima sesión:** Ejecutar \`/resume\` para restaurar contexto completo.

EOF
fi

# Crear flag para indicar que necesitamos generar resumen en próxima sesión
touch "$MEMORY_DIR/session-needs-summary.flag"

echo "✅ Session saved with $(echo "$COMMITS" | wc -l | tr -d ' ') commits tracked." >&2
exit 0
