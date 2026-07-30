---
framework_version: 1.0.0
---

# Agent Guidelines: AI Job Search

This workspace is structured to manage job search activities, scraper tools, CVs, cover letters, and interview preparation.

## Thin-Pointer Design (Single Source of Truth)

To prevent duplication and configuration drift across different AI agent frameworks (Claude Code, Google Antigravity, Codex, Cursor, Gemini CLI, etc.), this workspace uses a unified thin-pointer design. All agent runtimes should load the canonical specifications and candidate profiles from the files and directories below:

1. **Personal Candidate Profile:**
   - The candidate profile, contact details, education, and target preferences are defined in [CLAUDE.md](CLAUDE.md) and the individual profile methodology files under [.claude/skills/job-application-assistant/](.claude/skills/job-application-assistant/) (specifically `01-*.md` etc.).
2. **Canonical Workflow Specifications:**
   - The step-by-step instructions and triggers for tasks (setup, scrape, rank, apply, upskill, interview) are defined in the [.claude/](.claude/) directory (specifically under `.claude/skills/` and `.claude/commands/`).
   - Do not duplicate these rules or specifications. Treat `.claude/` files as the single source of truth.
3. **Portal Search Skills:**
   - Job-portal search CLIs live under [.agents/skills/](.agents/skills/) in the portable Agent Skills format (with a `SKILL.md` per portal). Codex and Antigravity discover these automatically; the `/scrape` workflow in [.claude/skills/job-scraper/](.claude/skills/job-scraper/) orchestrates them.
4. **Cross-Runtime Workflow & Command Skills:**
   - Thin pointer skills in [.agents/skills/](.agents/skills/) expose the full workflow to non-Claude runtimes. Each pointer skill has a `SKILL.md` with proper frontmatter for auto-discovery — its body instructs the agent to read the canonical spec from `.claude/` and execute it, so methodology changes upstream flow through automatically.
   - **Workflow skills** (`job-application-assistant`, `job-scraper-workflow`, `upskill-workflow`) wrap the three core skills in `.claude/skills/`.
   - **Command skills** (`cmd-setup`, `cmd-apply`, `cmd-rank`, `cmd-interview`, `cmd-outcome`, `cmd-expand`, `cmd-html-report`, `cmd-add-portal`, `cmd-add-template`, `cmd-gmail-sync`, `cmd-notion-sync`, `cmd-reset`) wrap the slash commands in `.claude/commands/`.
5. **Tool Name Translation:**
   - The canonical specs reference Claude Code tool names (`Read`, `Write`, `WebFetch`, `Agent`, etc.). A shared [.agents/TOOL_GLOSSARY.md](.agents/TOOL_GLOSSARY.md) maps these to runtime-neutral equivalents (e.g., `WebFetch` → `read_url_content` in Antigravity). Non-Claude runtimes should consult this glossary when executing workflow steps.
