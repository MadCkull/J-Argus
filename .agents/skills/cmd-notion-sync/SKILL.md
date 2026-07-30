---
name: cmd-notion-sync
description: >
  Publishes a read-only presentation view of ranked jobs and application status
  to a Notion database via the Notion MCP server. Requires a Notion MCP server
  connection. This is a cross-runtime pointer skill that delegates to
  .claude/commands/notion-sync.md. Triggers on: notion sync, sync to notion,
  publish to notion, update notion, notion dashboard
context: fork
---

# /notion-sync — Notion Pipeline View (Cross-Runtime Pointer)

This skill delegates to the canonical `/notion-sync` command specification.

## Execution

1. Read `.claude/commands/notion-sync.md` and follow the workflow defined there.
2. Translate Claude Code tool names using `.agents/TOOL_GLOSSARY.md`.

## MCP Dependency

This workflow requires a Notion MCP server connection. The canonical spec
references Claude-specific MCP tool names (`mcp__notion__*`).

For other runtimes, configure the equivalent Notion MCP server and use
your runtime's MCP tool invocation pattern. The operations needed are:
- Query/create/update database entries
- Create pages with content blocks
- The sync is one-way (repo → Notion), nothing syncs back

If no Notion MCP server is available, this command cannot run. Inform the user
that they need to set up Notion MCP integration first.
