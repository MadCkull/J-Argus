---
name: cmd-gmail-sync
description: >
  Scans Gmail for job application status updates (interviews, rejections, offers)
  and proposes sourced updates to the tracker. Requires a Gmail MCP server
  connection. This is a cross-runtime pointer skill that delegates to
  .claude/commands/gmail-sync.md. Triggers on: gmail sync, check gmail,
  email status updates, scan email, check my email for updates
context: fork
---

# /gmail-sync — Gmail Application Status Sync (Cross-Runtime Pointer)

This skill delegates to the canonical `/gmail-sync` command specification.

## Execution

1. Read `.claude/commands/gmail-sync.md` and follow the workflow defined there.
2. Translate Claude Code tool names using `.agents/TOOL_GLOSSARY.md`.

## MCP Dependency

This workflow requires a Gmail MCP server connection. The canonical spec
references Claude-specific MCP tool names (`mcp__claude_ai_Gmail__*`).

For other runtimes, configure the equivalent Gmail MCP server and use
your runtime's MCP tool invocation pattern. The operations needed are:
- List/search emails by query
- Read email content
- The workflow never sends emails — it is read-only

If no Gmail MCP server is available, this command cannot run. Inform the user
that they need to set up Gmail MCP integration first.
