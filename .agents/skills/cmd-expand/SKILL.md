---
name: cmd-expand
description: >
  Enriches candidate profiles by discovering hidden competencies across local
  documents and online presence (GitHub, portfolio, Kaggle, Google Scholar).
  This is a cross-runtime pointer skill that delegates to
  .claude/commands/expand.md. Triggers on: expand profile, enrich profile,
  discover skills, find hidden skills, scan my documents, what else can I add
context: fork
---

# /expand — Profile Enrichment (Cross-Runtime Pointer)

This skill delegates to the canonical `/expand` command specification.

## Execution

1. Read `.claude/commands/expand.md` and follow the workflow defined there.
2. The workflow scans documents in `documents/` and public online sources linked
   in the candidate profile to discover competencies not yet captured.
3. Discovered skills are added to `01-candidate-profile.md` with source tags.
4. Translate Claude Code tool names using `.agents/TOOL_GLOSSARY.md`.

## Key Tool Translations

- `WebFetch` / `WebSearch` (scanning online presence) → `read_url_content` / `search_web`
- `Glob` (scanning `documents/`) → `list_dir` recursively + `grep_search`
