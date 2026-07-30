---
name: cmd-sync-upstream
description: >
  Syncs Antigravity pointer skills with upstream J-Argus changes. Detects new,
  modified, or deleted commands and skills, then creates, updates, or removes
  pointer skills to keep the fork's Antigravity support in sync. This is a
  fork-maintenance skill — it does not exist in the upstream repository.
  Triggers on: sync upstream, check for updates, update pointers, sync pointers,
  upstream sync, what changed upstream, are my pointers up to date
context: fork
---

# /sync-upstream — Antigravity Pointer Maintenance

This skill keeps your fork's Antigravity pointer skills in sync with the
upstream J-Argus repository after you pull new changes.

## Step 1: Run the Detection Script

Run `python tools/sync_pointers.py` via `run_command`. This script:
- Fetches upstream and finds the divergence point
- Compares `.claude/commands/` and `.claude/skills/` for changes
- Cross-references against existing pointers in `.agents/skills/`
- Writes a structured report to `.agents/sync_report.md`

If the script says "Already up to date" or "No pointer-skill changes needed",
tell the user and stop.

## Step 2: Read the Report

Read `.agents/sync_report.md` with `view_file`. The report contains:
- **Metadata**: upstream ref, merge-base, change counts
- **Context**: how the pointer architecture works (for your reference)
- **Actions Required**: exactly which pointers to create, update, or delete
- **Upstream Command Specs**: full content of new/modified commands so you can
  write accurate pointer skills without extra file reads

## Step 3: Execute the Actions

For each action in the report:

### Creating New Pointer Skills
1. Read the full command spec included in the report
2. Create `.agents/skills/cmd-<name>/SKILL.md` following the exact format used
   by the existing pointer skills (see any `cmd-*` skill for reference)
3. Include proper YAML frontmatter: `name`, `description` with trigger phrases,
   `context: fork`
4. Write the body with: delegation instructions, tool translations referencing
   `.agents/TOOL_GLOSSARY.md`, and argument handling notes
5. If the command uses tools not already in `TOOL_GLOSSARY.md`, add them

### Updating Existing Pointer Skills
1. Compare the old and new command spec
2. Check if the pointer's description, trigger phrases, or tool translations
   need updating (e.g. new subcommands, changed arguments)
3. Update the pointer skill only if something meaningful changed

### Removing Stale Pointer Skills
1. Confirm the command was truly deleted upstream (not just renamed)
2. Delete the `.agents/skills/cmd-<name>/` directory

## Step 4: Update AGENTS.md (if needed)

If you created new pointers or removed old ones, update the command list in
section 4 of `AGENTS.md` to reflect the current set.

## Step 5: Verify

Run `python tools/lint_skills.py` to confirm all skills pass linting.
Run `python tools/security_guards.py` to confirm no unauthorized changes.

## Step 6: Report to User

Present a SHORT summary to the user:
- What changed upstream
- What pointer actions you took (created/updated/removed)
- Remind them to review and push if happy

Do NOT dump the full report — keep it concise.
