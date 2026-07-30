---
name: cmd-add-template
description: >
  Registers a custom CV or cover letter template (LaTeX, Typst, or another
  toolchain) and wires it into the apply workflow. This is a cross-runtime
  pointer skill that delegates to .claude/commands/add-template.md. Triggers on:
  add template, register template, custom template, typst template,
  use my own template, new cv template, new cover letter template
context: fork
---

# /add-template — Register Custom Template (Cross-Runtime Pointer)

This skill delegates to the canonical `/add-template` command specification.

## Execution

1. Read `.claude/commands/add-template.md` and follow the workflow defined there.
2. The workflow captures template instructions, runs a mandatory test compile,
   and registers the template in `templates/` for use by `/apply`.
3. Translate Claude Code tool names using `.agents/TOOL_GLOSSARY.md`.

## Arguments

The user provides the template file or describes the template to register.
In Claude Code, this arrives via `$ARGUMENTS`. In other runtimes, extract it
from the user's conversational message.
