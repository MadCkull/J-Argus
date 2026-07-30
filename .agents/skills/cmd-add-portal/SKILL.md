---
name: cmd-add-portal
description: >
  Generates a job-portal search skill for a new job board in your market.
  Investigates the portal, scaffolds the CLI skill, and test-runs a live query.
  This is a cross-runtime pointer skill that delegates to
  .claude/commands/add-portal.md. Triggers on: add portal, new job board,
  add job site, create portal skill, add a new portal, register job board
context: fork
---

# /add-portal — Scaffold a New Portal Skill (Cross-Runtime Pointer)

This skill delegates to the canonical `/add-portal` command specification.

## Execution

1. Read `.claude/commands/add-portal.md` and follow the workflow defined there.
2. The workflow investigates the target portal, scaffolds a CLI skill matching
   the portable Agent Skills format in `.agents/skills/`, and test-runs a query.
3. Translate Claude Code tool names using `.agents/TOOL_GLOSSARY.md`.

## Arguments

The user provides the job board to add (name or URL).
In Claude Code, this arrives via `$ARGUMENTS`. In other runtimes, extract it
from the user's conversational message.
