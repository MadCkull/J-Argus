---
name: job-scraper-workflow
description: >
  Finds new job postings matching your profile via installed portal-search CLIs
  (LinkedIn, local job boards, and any skills added with /add-portal). Deduplicates
  across runs. This is a cross-runtime pointer skill — it delegates to the canonical
  workflow specification maintained in .claude/skills/job-scraper/. Triggers on:
  job scrape, find jobs, search jobs, new jobs, job search, scrape jobs, scrape,
  any new positions
context: fork
---

# Job Scraper Workflow (Cross-Runtime Pointer)

This skill delegates to the canonical scraper orchestration spec. Follow these steps:

## Step 1: Load the Canonical Spec

Read `.claude/skills/job-scraper/SKILL.md` and follow the execution steps defined
there. Also read `.claude/skills/job-scraper/search-queries.md` for the search
strategy configuration.

## Step 2: Understand the Portal Skills

The scraper orchestrates the portal-search CLIs in `.agents/skills/`. Each portal
skill has its own `SKILL.md` with CLI usage instructions. The canonical spec
explains how to discover, invoke, and health-check them.

## Step 3: Translate Tool Names

The canonical spec uses Claude Code tool names. See `.agents/TOOL_GLOSSARY.md`
for the mapping to your runtime's equivalents. Key translations for this workflow:

- `Bash(bun run .agents/skills/*/cli/src/cli.ts ...)` → `run_command` with the same command
- `Bash(bun --version)` → `run_command` with `bun --version`
- `Agent` (for parallel portal searches) → `invoke_subagent`
- `WebSearch` (fallback when no CLI available) → `search_web`

## Invocation

The user triggers this skill by saying things like:
- "Find new jobs"
- "Scrape for jobs"
- "Any new positions?"

Optional arguments (extracted from the user's message):
- A focus area, e.g. "find data science jobs" or "scrape geophysics"
- "broad" to run all search categories
- "health" to run the portal health check only
