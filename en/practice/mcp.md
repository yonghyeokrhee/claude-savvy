# MCP Practice — Connect Notion

In this exercise, you connect a real MCP server and see Claude interact directly with your Notion workspace.
Notion MCP can be connected immediately with its official URL.

---

## End-to-end flow

```
Step 1: Add Notion MCP server (single command)
    ↓
Step 2: Restart Claude Code -> OAuth authorization
    ↓
Step 3: Test Notion read/write
    ↓
Step 4: Save MOP campaign tasks to Notion automatically
```

---

## Step 1. Add Notion MCP

Run in your project directory:

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp -s project
```

This automatically creates `.mcp.json` at project root:

```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

> Because this is saved in **Project scope**, committing this file lets the whole team share the same MCP setup.

---

## Step 2. Authenticate

Restart Claude Code, then in chat run:

```
/mcp
```

A browser window opens:
1. Log in to Notion
2. Select workspace
3. Approve permissions

Token storage is automatic. You do not need to manage API keys manually.

---

## Step 3. Confirm connection

In Claude Code chat, run:

```
Show me the list of pages in my Notion workspace.
```

If pages are returned, the connection is complete.

---

## Step 4. Save MOP tasks automatically

Now use it for a real case. Enter:

```
Create a Notion database called "MOP Campaign Management".

Include these properties:
- Campaign Name (title)
- Status (select: In Progress / Needs Review / Done)
- ROAS (number)
- Owner (text)
- Action Item (text)
```

Claude creates the database directly in Notion.

Then add sample rows:

```
In the MOP Campaign Management database you just created,
add these campaigns:

- Brand_Shopping / In Progress / ROAS 750% / Kim Marketer / Review budget increase
- NewCustomer_Search / Needs Review / ROAS 100% / Lee Owner / Replace creatives
```

---

## What changed?

| | Without MCP | After MCP connection |
|---|---|---|
| Notion access | Manual copy-paste | Claude can read/write directly |
| DB creation | Click manually in Notion UI | Create with natural language |
| Repeated entry | Manual every time | Batch operations via one prompt |

---

## Next level

If you also connect Slack MCP, you can chain services:

```
Read recent messages from Slack #ad-team,
and if a message contains "needs review" or "issue",
add it as a task in the Notion MOP Campaign Management database.
```

Claude can read from Slack and write to Notion automatically.

---

## References

- Official Notion MCP server: `https://mcp.notion.com/mcp`
- Slack MCP: `@modelcontextprotocol/server-slack` (run via npx)
- MCP server list: [modelcontextprotocol.io](https://modelcontextprotocol.io)
