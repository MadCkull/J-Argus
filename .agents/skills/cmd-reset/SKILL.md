---
name: cmd-reset
description: >
  Destructively resets candidate profile data, uploaded documents, or all state
  back to a clean baseline. This is a cross-runtime pointer skill that delegates
  to .claude/commands/reset.md. Triggers on: reset, wipe profile, start over,
  clean slate, clear data, reset everything, fresh start
context: fork
---

# /reset — Reset to Clean Baseline (Cross-Runtime Pointer)

This skill delegates to the canonical `/reset` command specification.

## Execution

1. Read `.claude/commands/reset.md` and follow the workflow defined there.
2. The workflow presents interactive confirmation before any destructive action.
3. Translate Claude Code tool names using `.agents/TOOL_GLOSSARY.md`.

## Warning

This command is destructive. It clears personalized profile data, documents,
or all workspace state. The canonical spec includes safety confirmations —
always wait for explicit user approval before deleting anything.
