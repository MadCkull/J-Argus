---
name: cmd-interview
description: >
  Prepares the candidate for a real interview on a tracked application with
  stage-specific prep packs, company research, STAR story mapping, and mock
  interviews. This is a cross-runtime pointer skill that delegates to
  .claude/commands/interview.md. Triggers on: interview prep, prepare for interview,
  mock interview, practice interview, interview at, interview questions,
  getting ready for interview
context: fork
---

# /interview — Interview Preparation (Cross-Runtime Pointer)

This skill delegates to the canonical `/interview` command specification.

## Execution

1. Read `.claude/commands/interview.md` and follow the workflow defined there.
2. The workflow references `.claude/skills/job-application-assistant/07-interview-prep.md`
   for the STAR framework and roleplay protocol.
3. It also reads the application archive in `documents/applications/<company>_<role>/`
   to use the exact CV and cover letter the interviewer has seen.
4. Translate Claude Code tool names using `.agents/TOOL_GLOSSARY.md`.

## Key Tool Translations for This Workflow

- `WebFetch` (loading job posting details) → `read_url_content`
- `WebSearch` (researching company and interviewers) → `search_web`

## Arguments

The user's message should identify the application to prepare for:
- A company name, role title, or tracker reference
- Optionally: the interview stage (phone screen, technical, behavioral, etc.)

In Claude Code, this arrives via `$ARGUMENTS`. In other runtimes, extract it
from the user's conversational message.
