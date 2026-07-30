---
framework_version: 1.0.0
---

# Runtime Tool Glossary

This file maps Claude Code tool names used in the canonical workflow specs
(`.claude/skills/` and `.claude/commands/`) to their runtime-neutral equivalents.
When a non-Claude runtime (Antigravity, Codex, Gemini CLI, etc.) executes a
workflow that references a Claude tool name, use this table to translate.

## Tool Mapping

| Claude Code Tool | What It Does | Antigravity | Codex / Gemini CLI |
|---|---|---|---|
| `Read` | Read file contents | `view_file` | Read the file |
| `Write` | Create or overwrite a file | `write_to_file` | Write the file |
| `Edit` | Edit part of an existing file | `replace_file_content` / `multi_replace_file_content` | Edit the file |
| `Glob` | Find files matching a pattern | `list_dir` + `grep_search` (by filename pattern) | List/find files |
| `Grep` | Search inside file contents | `grep_search` | Search file contents |
| `Bash(...)` | Execute a shell command | `run_command` | Run the command |
| `WebFetch` | Fetch content from a URL | `read_url_content` | Fetch the URL |
| `WebSearch` | Search the web | `search_web` | Search the web |
| `Agent` | Spawn a sub-agent for parallel work | `invoke_subagent` | Spawn a sub-agent |
| `AskUserQuestion` | Prompt the user for input | Output text directly (the runtime handles it) | Ask the user |

## Notes

- **`Bash(bun run ...)`**: All portal-search CLIs use `bun run .agents/skills/<portal>/cli/src/cli.ts`.
  In Antigravity, execute via `run_command` with the same command string.
- **`Bash(python ...)`** / **`Bash(python3 ...)`**: Scripts like `salary_lookup.py`, `lualatex`, `xelatex`,
  and `pdftotext` are invoked the same way — pass the command string to `run_command`.
- **`Agent` dispatching**: When a workflow says "spawn an agent", use `invoke_subagent` to
  create a subagent with the instructions described in the workflow spec. Pass draft content
  inline in the prompt rather than having the subagent re-read files.
- **`$ARGUMENTS`**: Claude Code slash commands receive user input via `$ARGUMENTS`. In other
  runtimes, extract the relevant arguments from the user's conversational message instead.
