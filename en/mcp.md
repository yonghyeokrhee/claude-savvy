# MCP (Model Context Protocol)

## What Is MCP?

**MCP (Model Context Protocol)** is a **standard communication protocol** that lets Claude connect to external services and tools.

Like a USB port standard, MCP defines a common interface so almost any external tool can plug into Claude. If you build or install an MCP server, Claude can use that service like a native tool.

## Without MCP vs With MCP

**Without MCP:**
```
User: "Get today's to-do list from Notion"
Claude: "I can't access Notion directly. Please paste the content here."
```

**With MCP:**
```
User: "Get today's to-do list from Notion"
Claude: [Call Notion MCP server] -> Fetch list -> "You have 3 tasks today: ..."
```

## Architecture

```
Claude Code
    │
    └── MCP Client
            │  (MCP protocol)
            ▼
        MCP Server ---- External service
      (local process)   (Notion, GitHub,
                         DB, Slack, ...)
```

An MCP server is usually a small local process. Claude communicates safely with external services through this server.

## MCP Scope — where config is stored matters

Before adding an MCP server, choose scope:

| Scope | Storage | Applies to | Team share |
|---|---|---|---|
| **Local** (default) | Local config | Me, this project only | ❌ |
| **Project** | `.mcp.json` (git-managed) | Team, this project | ✅ |
| **User** | `~/.claude/` | Me, all projects | ❌ |

For team usage, prefer **Project scope** and commit the config.

## Add MCP servers

### Method 1 — one command (recommended)

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp -s project
```

- `--transport http`: remote server transport
- `notion`: server identifier
- `-s project`: project scope (saved in `.mcp.json`)

### Method 2 — edit config directly

Create or edit `.mcp.json` at project root:

```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-...",
        "SLACK_TEAM_ID": "T01234ABCDE"
      }
    }
  }
}
```

Restart Claude Code after configuration.

## Common MCP servers

| Server | Capability |
|---|---|
| Notion | Read/write pages, query databases |
| GitHub | Create PRs, manage issues, search code |
| Slack | Send messages, inspect channels |
| PostgreSQL | Run DB queries directly |
| Filesystem | Access files in configured directories |
| Browser | Browser automation |

## Build your own MCP server

With the standard SDK, anyone can build one:

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";

const server = new Server({ name: "my-server", version: "1.0.0" });

// Define tools Claude can call
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "get_weather",
    description: "Get current weather for a city",
    inputSchema: {
      type: "object",
      properties: {
        city: { type: "string", description: "City name" }
      }
    }
  }]
}));
```

Then Claude can call `get_weather` naturally.

## MCP vs built-in tools

| Category | Built-in tools (`Read`, `Bash`, etc.) | MCP tools |
|---|---|---|
| Provider | Anthropic (built-in) | User/community (extensible) |
| Reach | Local filesystem and terminal | Unlimited external services |
| Setup | None | MCP server setup required |
| Customizable | No | Yes, fully custom |

## Security considerations

- MCP servers access external services on Claude's behalf. Manage API keys with environment variables; never hardcode.
- Do not install MCP servers from untrusted sources.
- Verify what permissions each MCP server requires.
