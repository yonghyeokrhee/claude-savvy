# MCP Practice — Connect Obsidian

Obsidian is a local Markdown note app.
With the Local REST API plugin, Claude can read and write files directly in an Obsidian vault.

---

## Prerequisites

### Install Obsidian Local REST API plugin

1. Obsidian -> Settings -> Community plugins -> Browse
2. Search for **"Local REST API"**, install and enable
3. Copy the **API Key** from plugin settings
4. Use default port `27124` (HTTPS) or `27123` (HTTP)

### Verify connection

In terminal, confirm API responds:

```bash
curl -sk \
  -H "Authorization: Bearer [YOUR_API_KEY]" \
  https://127.0.0.1:27124/vault/
```

If JSON file list is returned, setup is ready.

---

## Step 1. Register MCP server

Create `.mcp.json` at project root:

```bash
# from practice/ folder
touch .mcp.json
```

`.mcp.json` content:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "mcp-obsidian"],
      "env": {
        "OBSIDIAN_API_KEY": "PUT_API_KEY_HERE",
        "OBSIDIAN_PROTOCOL": "https",
        "OBSIDIAN_HOST": "127.0.0.1",
        "OBSIDIAN_PORT": "27124"
      }
    }
  }
}
```

> Note: API key is local-only, but still avoid committing it. Add `.mcp.json` to `.gitignore` or inject env vars separately.

---

## Step 2. Restart Claude Code and verify

Run:

```
/mcp
```

If `obsidian` appears in the list, connection is complete.

---

## Step 3. Test basic behavior

In Claude Code chat:

```
Show me the list of files in my Obsidian vault.
```

If file list appears, MCP is working.

---

## Step 4. Practice — Save MOP analysis into Obsidian

Save `report-monthly.md` from workflow practice to Obsidian:

```
Read practice/data/report-monthly.md
and save it to my Obsidian vault as
"MOP/2026-02 Monthly Report.md".
```

Claude performs:
1. local file **Read**
2. Obsidian MCP **Write** (create vault file)

Both steps are handled automatically.

---

## Step 5. Reverse direction — read from Obsidian

You can also let Claude reference notes from Obsidian:

```
Read "2026 Roadmap" from Obsidian
and summarize anything related to MOP ad strategy.
```

---

## Notion vs Obsidian

| | Notion | Obsidian |
|---|---|---|
| Storage location | Cloud | Local files |
| Internet required | Yes | No |
| Team sharing | Easy | Requires extra setup |
| Personal notes | Possible | Optimized |
| MCP connection mode | HTTP (official server) | Local REST API |

For personal memos, journals, and research notes: Obsidian.
For shared team tasks and docs: Notion.
