#!/usr/bin/env python3
"""Detect upstream changes that need Antigravity pointer-skill updates.

Usage: python tools/sync_pointers.py [--remote <name>] [--branch <name>] [--no-fetch]

This script compares the local fork against the upstream repository and
produces a structured Markdown report describing what changed in
.claude/commands/ and .claude/skills/ since the fork diverged (or since
the last merge).  The report is written to .agents/sync_report.md and is
designed to be consumed by an LLM (e.g. Google Antigravity) that will
create, update, or remove the corresponding thin-pointer skills in
.agents/skills/.

The script itself never modifies pointer skills — it only observes and
reports.  The LLM handles all creative work.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Naming conventions
# ---------------------------------------------------------------------------
# .claude/commands/foo-bar.md  -->  .agents/skills/cmd-foo-bar/SKILL.md
# .claude/skills/some-name/    -->  .agents/skills/some-name/SKILL.md
#   (but the 3 core skills have custom pointer names — see SKILL_MAP)

SKILL_MAP: dict[str, str] = {
    # canonical .claude/skills/ dir name  ->  pointer skill dir name
    "job-application-assistant": "job-application-assistant",
    "job-scraper": "job-scraper-workflow",
    "upskill": "upskill-workflow",
}


def run_git(args: list[str]) -> tuple[int, str, str]:
    res = subprocess.run(
        ["git"] + args,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return res.returncode, res.stdout, res.stderr


def pointer_name_for_command(cmd_stem: str) -> str:
    """Map a command filename stem to its pointer-skill directory name."""
    return f"cmd-{cmd_stem}"


def pointer_name_for_skill(skill_dir: str) -> str | None:
    """Map a canonical skill directory name to its pointer-skill directory name."""
    return SKILL_MAP.get(skill_dir)


def pointer_exists(name: str) -> bool:
    return (ROOT / ".agents" / "skills" / name / "SKILL.md").is_file()


def get_local_commands() -> set[str]:
    """Return the set of command stems present locally in .claude/commands/."""
    d = ROOT / ".claude" / "commands"
    if not d.is_dir():
        return set()
    return {p.stem for p in d.glob("*.md")}


def get_local_skills() -> set[str]:
    """Return the set of skill directory names in .claude/skills/."""
    d = ROOT / ".claude" / "skills"
    if not d.is_dir():
        return set()
    return {p.name for p in d.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()}


def get_upstream_file_content(ref: str, path: str) -> str | None:
    """Retrieve a file's content from the upstream ref."""
    rc, stdout, _ = run_git(["show", f"{ref}:{path}"])
    return stdout if rc == 0 else None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect upstream changes needing pointer-skill updates."
    )
    parser.add_argument(
        "--remote", default="upstream",
        help="Name of the git remote for the upstream repo (default: upstream)",
    )
    parser.add_argument(
        "--branch", default="master",
        help="Branch name on the upstream remote (default: master)",
    )
    parser.add_argument(
        "--no-fetch", action="store_true",
        help="Skip fetching from the remote (use cached state)",
    )
    args = parser.parse_args()

    # -----------------------------------------------------------------------
    # 1. Validate the remote
    # -----------------------------------------------------------------------
    rc, stdout, _ = run_git(["remote"])
    remotes = stdout.splitlines()
    remote = args.remote
    if remote not in remotes:
        print(f"Error: remote '{remote}' not found.  Available: {', '.join(remotes)}")
        print("Hint: git remote add upstream https://github.com/MadsLorentzen/ai-job-search.git")
        return 1

    # -----------------------------------------------------------------------
    # 2. Fetch
    # -----------------------------------------------------------------------
    if not args.no_fetch:
        print(f"Fetching {remote}...")
        rc, _, stderr = run_git(["fetch", remote])
        if rc != 0:
            print(f"Warning: fetch failed ({stderr.strip()}); using cached state.")

    ref = f"{remote}/{args.branch}"
    rc, _, _ = run_git(["rev-parse", "--verify", ref])
    if rc != 0:
        print(f"Error: ref '{ref}' does not exist.")
        return 1

    # -----------------------------------------------------------------------
    # 3. Find the merge-base (where the fork diverged)
    # -----------------------------------------------------------------------
    rc, base_hash, _ = run_git(["merge-base", "HEAD", ref])
    if rc != 0:
        print("Error: could not find merge-base between HEAD and upstream.")
        return 1
    base_hash = base_hash.strip()

    _, head_hash, _ = run_git(["rev-parse", ref])
    head_hash = head_hash.strip()

    if base_hash == head_hash:
        print("Already up to date with upstream. No sync report generated.")
        return 0

    # -----------------------------------------------------------------------
    # 4. Get the list of changed files in .claude/ between base and upstream
    # -----------------------------------------------------------------------
    _, diff_names, _ = run_git([
        "diff", "--name-status", base_hash, ref, "--", ".claude/commands/", ".claude/skills/"
    ])

    if not diff_names.strip():
        print("No changes to .claude/commands/ or .claude/skills/ since last sync.")
        print("Tip: upstream may have other changes (CLAUDE.md, tools/, etc.).")
        return 0

    # -----------------------------------------------------------------------
    # 5. Categorize changes
    # -----------------------------------------------------------------------
    new_commands: list[str] = []
    modified_commands: list[str] = []
    deleted_commands: list[str] = []
    new_skills: list[str] = []
    modified_skills: list[str] = []
    deleted_skills: list[str] = []
    other_changes: list[tuple[str, str]] = []  # (status, path)

    for line in diff_names.strip().splitlines():
        parts = line.split("\t")
        status = parts[0][0]  # A, M, D, R (first char)
        filepath = parts[-1]  # use last element (handles renames)

        posix = PurePosixPath(filepath)

        # --- Commands ---
        if posix.parent == PurePosixPath(".claude/commands") and posix.suffix == ".md":
            stem = posix.stem
            if status == "A":
                new_commands.append(stem)
            elif status == "M":
                modified_commands.append(stem)
            elif status == "D":
                deleted_commands.append(stem)
            else:
                other_changes.append((status, filepath))

        # --- Skills ---
        elif str(posix).startswith(".claude/skills/"):
            # Extract the skill directory name (e.g. "job-scraper" from
            # ".claude/skills/job-scraper/SKILL.md")
            skill_dir = posix.parts[2] if len(posix.parts) > 2 else None
            if skill_dir:
                if status == "A" and skill_dir not in [s for s, _, _ in
                    [(s, None, None) for s in new_skills]]:
                    if skill_dir not in new_skills:
                        new_skills.append(skill_dir)
                elif status == "M":
                    if skill_dir not in modified_skills:
                        modified_skills.append(skill_dir)
                elif status == "D":
                    if skill_dir not in deleted_skills:
                        deleted_skills.append(skill_dir)
                else:
                    other_changes.append((status, filepath))
        else:
            other_changes.append((status, filepath))

    # -----------------------------------------------------------------------
    # 6. Cross-reference against existing pointers
    # -----------------------------------------------------------------------
    missing_pointers: list[str] = []  # new commands with no pointer
    stale_pointers: list[str] = []    # deleted commands that still have pointers
    update_pointers: list[str] = []   # modified commands whose pointers may need refresh

    for cmd in new_commands:
        pname = pointer_name_for_command(cmd)
        if not pointer_exists(pname):
            missing_pointers.append(cmd)

    for cmd in deleted_commands:
        pname = pointer_name_for_command(cmd)
        if pointer_exists(pname):
            stale_pointers.append(cmd)

    for cmd in modified_commands:
        pname = pointer_name_for_command(cmd)
        if pointer_exists(pname):
            update_pointers.append(cmd)

    # Same for skills
    missing_skill_pointers: list[str] = []
    stale_skill_pointers: list[str] = []
    update_skill_pointers: list[str] = []

    for skill in new_skills:
        pname = pointer_name_for_skill(skill)
        if pname and not pointer_exists(pname):
            missing_skill_pointers.append(skill)
        elif not pname:
            # New skill with no mapping — needs a pointer AND a SKILL_MAP entry
            missing_skill_pointers.append(skill)

    for skill in deleted_skills:
        pname = pointer_name_for_skill(skill)
        if pname and pointer_exists(pname):
            stale_skill_pointers.append(skill)

    for skill in modified_skills:
        pname = pointer_name_for_skill(skill)
        if pname and pointer_exists(pname):
            update_skill_pointers.append(skill)

    # -----------------------------------------------------------------------
    # 7. Fetch content of new/modified command specs for LLM context
    # -----------------------------------------------------------------------
    command_contents: dict[str, str] = {}
    for cmd in new_commands + modified_commands:
        content = get_upstream_file_content(ref, f".claude/commands/{cmd}.md")
        if content:
            command_contents[cmd] = content

    # -----------------------------------------------------------------------
    # 8. Build the report
    # -----------------------------------------------------------------------
    report_lines: list[str] = []
    w = report_lines.append

    w("# Upstream Sync Report")
    w("")
    w("<!-- This report was auto-generated by tools/sync_pointers.py -->")
    w("<!-- It is designed to be read by an LLM (via the cmd-sync-upstream skill) -->")
    w("")
    w("## Metadata")
    w("")
    w(f"- **Upstream ref**: `{ref}` (`{head_hash[:10]}`)")
    w(f"- **Fork merge-base**: `{base_hash[:10]}`")
    w(f"- **Commands changed**: {len(new_commands)} new, {len(modified_commands)} modified, {len(deleted_commands)} deleted")
    w(f"- **Skills changed**: {len(new_skills)} new, {len(modified_skills)} modified, {len(deleted_skills)} deleted")
    w("")

    # --- Context for the LLM ---
    w("## Context for the LLM")
    w("")
    w("This fork adds Google Antigravity support to J-Argus via thin-pointer skills.")
    w("The pointer architecture works as follows:")
    w("")
    w("- Each `.claude/commands/<name>.md` has a matching pointer at `.agents/skills/cmd-<name>/SKILL.md`.")
    w("- Each `.claude/skills/<name>/` has a matching pointer at `.agents/skills/<pointer-name>/SKILL.md`.")
    w("- Pointer skills have YAML frontmatter (`name`, `description` with trigger phrases, `context: fork`).")
    w("- The body instructs the agent to read and execute the canonical spec from `.claude/`.")
    w("- Tool name translations reference `.agents/TOOL_GLOSSARY.md`.")
    w("- See any existing pointer in `.agents/skills/cmd-*/SKILL.md` for the exact format to follow.")
    w("")

    # --- Actions required ---
    has_actions = missing_pointers or stale_pointers or update_pointers or \
                  missing_skill_pointers or stale_skill_pointers or update_skill_pointers

    if not has_actions:
        w("## Result")
        w("")
        w("No pointer-skill changes needed. All upstream changes are already covered.")
        w("")
    else:
        w("## Actions Required")
        w("")

        if missing_pointers:
            w("### 🆕 New Commands — Create Pointer Skills")
            w("")
            w("These commands were added upstream but have no Antigravity pointer yet.")
            w("Create `.agents/skills/cmd-<name>/SKILL.md` for each:")
            w("")
            for cmd in missing_pointers:
                w(f"- **`{cmd}`** → create `.agents/skills/cmd-{cmd}/SKILL.md`")
            w("")

        if update_pointers:
            w("### ✏️ Modified Commands — Review Pointers")
            w("")
            w("These commands were modified upstream. Check if the pointer description,")
            w("trigger phrases, or tool translations need updating:")
            w("")
            for cmd in update_pointers:
                w(f"- **`{cmd}`** → review `.agents/skills/cmd-{cmd}/SKILL.md`")
            w("")

        if stale_pointers:
            w("### 🗑️ Deleted Commands — Remove Pointers")
            w("")
            w("These commands were deleted upstream. Remove the corresponding pointers:")
            w("")
            for cmd in stale_pointers:
                w(f"- **`{cmd}`** → delete `.agents/skills/cmd-{cmd}/`")
            w("")

        if missing_skill_pointers:
            w("### 🆕 New Skills — Create Pointer Skills")
            w("")
            for skill in missing_skill_pointers:
                pname = pointer_name_for_skill(skill)
                if pname:
                    w(f"- **`{skill}`** → create `.agents/skills/{pname}/SKILL.md`")
                else:
                    w(f"- **`{skill}`** → NEW skill with no mapping. Choose a pointer name")
                    w(f"  (convention: `<name>-workflow`) and create `.agents/skills/<chosen>/SKILL.md`.")
                    w(f"  Also update the `SKILL_MAP` in `tools/sync_pointers.py`.")
            w("")

        if update_skill_pointers:
            w("### ✏️ Modified Skills — Review Pointers")
            w("")
            for skill in update_skill_pointers:
                pname = pointer_name_for_skill(skill)
                w(f"- **`{skill}`** → review `.agents/skills/{pname}/SKILL.md`")
            w("")

        if stale_skill_pointers:
            w("### 🗑️ Deleted Skills — Remove Pointers")
            w("")
            for skill in stale_skill_pointers:
                pname = pointer_name_for_skill(skill)
                w(f"- **`{skill}`** → delete `.agents/skills/{pname}/`")
            w("")

    # --- Full content of new/modified command specs ---
    if command_contents:
        w("## Upstream Command Specs (for LLM reference)")
        w("")
        w("Below are the full contents of new and modified command specs.")
        w("Use these to write accurate pointer skills with proper trigger")
        w("phrases, descriptions, and tool translations.")
        w("")
        for cmd, content in sorted(command_contents.items()):
            tag = "NEW" if cmd in new_commands else "MODIFIED"
            w(f"### [{tag}] `.claude/commands/{cmd}.md`")
            w("")
            w("```markdown")
            w(content.rstrip())
            w("```")
            w("")

    # --- Other changes ---
    if other_changes:
        w("## Other Changes (informational)")
        w("")
        w("These files changed upstream but are not directly mapped to pointers:")
        w("")
        for status, path in other_changes:
            label = {"A": "added", "M": "modified", "D": "deleted", "R": "renamed"}.get(status, status)
            w(f"- `{path}` ({label})")
        w("")

    # -----------------------------------------------------------------------
    # 9. Write the report
    # -----------------------------------------------------------------------
    report_path = ROOT / ".agents" / "sync_report.md"
    report_text = "\n".join(report_lines) + "\n"
    report_path.write_text(report_text, encoding="utf-8")

    # --- Console summary ---
    print(f"\nSync report written to: {report_path.relative_to(ROOT)}")
    print(f"  Upstream: {ref} ({head_hash[:10]})")
    print(f"  Base:     {base_hash[:10]}")
    print()

    if has_actions:
        action_count = len(missing_pointers) + len(stale_pointers) + len(update_pointers) + \
                       len(missing_skill_pointers) + len(stale_skill_pointers) + len(update_skill_pointers)
        print(f"  ⚠️  {action_count} pointer action(s) needed. Tell Antigravity: \"sync upstream\"")
    else:
        print("  ✅ All pointers are up to date.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
