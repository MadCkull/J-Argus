---
name: cmd-outcome
description: >
  Records job application status updates and results (interviews, offers,
  rejections, silence). Archives submitted materials and manages follow-up
  drafts for quiet applications. This is a cross-runtime pointer skill that
  delegates to .claude/commands/outcome.md. Triggers on: record outcome,
  application result, got rejected, got an offer, followup, follow up,
  application status, what happened with, update application
context: fork
---

# /outcome — Record Application Results (Cross-Runtime Pointer)

This skill delegates to the canonical `/outcome` command specification.

## Execution

1. Read `.claude/commands/outcome.md` and follow the workflow defined there.
2. The workflow updates `job_search_tracker.csv`, archives materials to
   `documents/applications/<company>_<role>/`, and maintains `outcome.md`.
3. Translate Claude Code tool names using `.agents/TOOL_GLOSSARY.md`.

## Subcommands

The user's message may indicate:
- A status update (e.g. "I got an interview at Novo Nordisk")
- `followup` — surface open applications that have gone quiet and draft follow-ups
- A thank-you note request after recording an interview stage

In Claude Code, these arrive via `$ARGUMENTS`. In other runtimes, extract them
from the user's conversational message.
