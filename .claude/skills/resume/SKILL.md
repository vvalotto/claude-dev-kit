---
name: resume
description: Restore session context from previous work. Use when starting a new session to get context about what was done previously.
disable-model-invocation: false
---

# Resume Session Context

Restore and display context from the previous session.

## Instructions

When this skill is invoked:

### 1. Check for session data

Look for session files in `~/.claude/projects/<project-path>/memory/`:
- `session-metadata.json` - Last session metadata
- `session-current.md` - Current session state
- `session-history.md` - Historical sessions

If `session-metadata.json` doesn't exist, inform the user:
> "No previous session found. This appears to be a fresh start."

### 2. Read and parse session files

Read all three session files to gather:
- Last session timestamp and branch
- Exit reason (normal, error, timeout, etc.)
- **Commits from the last session** (captured automatically by SessionEnd hook at the end of session-current.md)
- What was completed
- Current state and decisions made
- Next steps and pending tasks

**IMPORTANT:** The SessionEnd hook automatically appends commits to the end of `session-current.md`. Look for a section like:
```
## 📝 Sesión Finalizada: YYYY-MM-DD HH:MM
### Commits en esta sesión:
- hash commit message
- hash commit message
```
These commits are the PRIMARY indicator of what was accomplished in the last session.

### 3. Generate comprehensive summary

Display a structured summary:

```markdown
# 📋 Session Context Restored

**Last Session:** <timestamp from metadata>
**Branch:** <git branch from metadata>
**Exit Reason:** <exit_reason from metadata>

## ✅ Previous Session Summary

<Extract completion status from session-current.md>

## 🔍 Key Decisions & Context

<Extract important decisions or context>

## 🎯 Current State

<Extract current state description>

## 🚀 Next Activities

<Extract and list next steps>

---

**Context restored successfully. Ready to continue work.**
```

### 4. Update session tracking

- Add entry to `session-history.md` documenting the completed session (use commits as evidence)
- **Reset `session-current.md`** - Create a fresh template for the new session:
  ```markdown
  # Sesión Actual - Claude Dev Kit

  ## 📝 Sesión Iniciada: <current date/time>
  **Branch:** <current branch>
  **Contexto Restaurado:** ✅ /resume ejecutado

  ### 🎯 Objetivo de Esta Sesión
  <To be determined based on what's next>

  ### ✅ Completado
  <Will be filled as work progresses>

  ### 🚀 Próximos Pasos
  <To be determined>
  ```
- Remove `session-needs-summary.flag` if it exists

### 5. Handle edge cases

- **No metadata file:** "No previous session to resume."
- **Corrupted JSON:** Show error and read what you can from .md files
- **Empty session files:** "Session files exist but are empty. Starting fresh."

## File Locations

All session files are in:
```
~/.claude/projects/<project-hash>/memory/
├── session-metadata.json
├── session-current.md
├── session-history.md
└── session-needs-summary.flag (optional)
```

## Example Usage

User types:
```bash
/resume
```

You respond with the full context summary as specified above.

## Tips

- Be concise but complete - show what matters
- **Use commits as the primary source of truth** for what was accomplished
- Analyze commit messages to understand the scope of work (feat, fix, docs, test, etc.)
- Check CLAUDE.md or project documentation to understand what should come next
- Highlight any blockers or important decisions
- If there are pending tasks, list them clearly
- Always clean up the flag file after processing
- Reset session-current.md to prepare for the new session
