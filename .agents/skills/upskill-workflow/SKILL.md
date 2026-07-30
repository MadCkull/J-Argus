---
name: upskill-workflow
description: >
  Compares tracked job postings against the candidate profile to identify skill
  gaps and generate a prioritized learning plan with study resources. This is a
  cross-runtime pointer skill — it delegates to the canonical workflow specification
  maintained in .claude/skills/upskill/. Triggers on: upskill, skill gaps,
  what should I learn, learning plan, skill gap analysis, career development,
  what skills do I need
context: fork
---

# Upskill Workflow (Cross-Runtime Pointer)

This skill delegates to the canonical upskill analysis spec. Follow these steps:

## Step 1: Load the Canonical Spec

Read `.claude/skills/upskill/SKILL.md` and follow the execution steps defined there.

## Step 2: Load Supporting Files

The upskill workflow reads:
- `job_search_tracker.csv` — tracked job postings for aggregate gap analysis
- `.claude/skills/job-application-assistant/01-candidate-profile.md` — your current skills
- Previous reports in `upskill/` — to track progress over time

## Step 3: Translate Tool Names

The canonical spec uses Claude Code tool names. See `.agents/TOOL_GLOSSARY.md`
for the mapping to your runtime's equivalents. Key translations for this workflow:

- `WebSearch` → `search_web` (for finding current learning resources)
- `WebFetch` → `read_url_content` (for fetching course/resource details)

## Invocation

The user triggers this skill by saying things like:
- "What skills should I learn?"
- "Analyze my skill gaps"
- "Create a learning plan"
- "Upskill" or "upskill for [URL]"

Optional: the user may provide a single job posting URL to analyze gaps against
that specific role instead of the aggregate tracker.
