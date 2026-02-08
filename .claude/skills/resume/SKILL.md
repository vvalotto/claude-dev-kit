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
- What was completed
- Current state and decisions made
- Next steps and pending tasks

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

- Add entry to `session-history.md` documenting this session resume
- Update `session-current.md` to note that context was restored
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
- Highlight any blockers or important decisions
- If there are pending tasks, list them clearly
- Always clean up the flag file after processing
