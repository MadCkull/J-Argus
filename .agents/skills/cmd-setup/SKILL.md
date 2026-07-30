---
name: cmd-setup
description: >
  Runs onboarding setup to collect candidate professional details and build
  profile files. Offers three paths: scan a documents folder, import a pasted CV,
  or walk through an interactive interview. This is a cross-runtime pointer skill
  that delegates to .claude/commands/setup.md. Triggers on: setup, set up profile,
  onboarding, configure profile, build profile, get started, initialize,
  set up my profile, run setup
context: fork
---

# /setup — Profile Onboarding (Cross-Runtime Pointer)

This skill delegates to the canonical `/setup` command specification.

## Execution

1. Read `.claude/commands/setup.md` and follow the workflow defined there.
2. The workflow populates files under `.claude/skills/job-application-assistant/`
   and `CLAUDE.md` — these are the canonical profile locations read by all other
   workflows.
3. Translate Claude Code tool names using `.agents/TOOL_GLOSSARY.md`.

## Key Tool Translations for This Workflow

- `Glob` (scanning `documents/`) → use `list_dir` recursively + `grep_search`
- `Read` → `view_file`
- `Write` / `Edit` → `write_to_file` / `replace_file_content`
- `AskUserQuestion` → output your question as text and wait for the user's reply

## Arguments

The user's message may include context about which setup path to take:
- Mentioning "documents" or "folder" → Path A (scan documents/)
- Pasting a CV or mentioning "CV" → Path B (import pasted CV)
- No specific path → the workflow auto-detects or asks

In Claude Code, user input arrives via `$ARGUMENTS`. In other runtimes,
extract the equivalent from the user's conversational message.
