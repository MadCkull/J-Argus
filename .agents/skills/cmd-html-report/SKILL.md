---
name: cmd-html-report
description: >
  Generates a self-contained HTML dashboard from job_search_tracker.csv and
  application outcome archives for deep pipeline review. Opens directly in a
  browser, fully offline. This is a cross-runtime pointer skill that delegates
  to .claude/commands/html-report.md. Triggers on: html report, generate report,
  dashboard, application tracker, pipeline report, job search report,
  show my applications
context: fork
---

# /html-report — Application Dashboard (Cross-Runtime Pointer)

This skill delegates to the canonical `/html-report` command specification.

## Execution

1. Read `.claude/commands/html-report.md` and follow the workflow defined there.
2. The workflow reads `job_search_tracker.csv` and application archives to
   generate a self-contained HTML file with charts and a filterable table.
3. Translate Claude Code tool names using `.agents/TOOL_GLOSSARY.md`.

## Output

The generated HTML file opens directly in the browser with no external
dependencies (inline SVG charts, no CDN links).
