---
name: cmd-rank
description: >
  Batch-scores scraped job postings into a ranked triage shortlist against candidate
  profile fit criteria. Bridges the scrape and apply workflows. This is a cross-runtime
  pointer skill that delegates to .claude/commands/rank.md. Triggers on: rank jobs,
  rank scraped, triage, shortlist, score jobs, prioritize jobs, which jobs should I apply to
context: fork
---

# /rank — Triage Scraped Jobs (Cross-Runtime Pointer)

This skill delegates to the canonical `/rank` command specification.

## Execution

1. Read `.claude/commands/rank.md` and follow the workflow defined there.
2. The workflow reads `job_scraper/seen_jobs.json`, `job_search_tracker.csv`, and
   scoring specs from `.claude/skills/job-application-assistant/`.
3. Translate Claude Code tool names using `.agents/TOOL_GLOSSARY.md`.

## Key Tool Translations for This Workflow

- `WebFetch` (fetching full posting details) → `read_url_content`
- `Agent` (parallel scoring agents) → `invoke_subagent`
- `Bash(python salary_lookup.py ...)` → `run_command`

## Arguments

The user's message may include:
- A focus area, e.g. "rank data science jobs" → filter by that category
- `--all` → re-rank all unapplied jobs (not just new ones)
- `--top N` → shortlist size (default 5)

In Claude Code, these arrive via `$ARGUMENTS`. In other runtimes, extract them
from the user's conversational message.
