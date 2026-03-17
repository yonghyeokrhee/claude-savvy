# MCP Practice — Connect RDS MySQL

In this exercise, Claude connects directly to AWS RDS MySQL to query and analyze data.
A custom Python MCP server lets you run SQL through natural language.

---

## End-to-end flow

```
Step 1: Write the MCP server (server.py)
    ↓
Step 2: Register the server in .mcp.json
    ↓
Step 3: Restart Claude Code → confirm connection
    ↓
Step 4: Query the DB with natural language
```

---

## Why this MCP?

| | Without MCP | After MCP connection |
|---|---|---|
| DB queries | Log into mysql from terminal | "Show me advertisers with low ROAS" |
| Analysis | Write query → copy → paste into Claude | Claude runs the query and analyzes results |
| Repetitive work | Manual every time | One natural-language sentence |

---

## Prerequisites

- AWS credentials configured (`aws configure` or AWS Profile)
- VPN connection (if the RDS is inside a private network)
- Python 3.10+ and dependencies

```bash
pip install fastmcp pymysql boto3
```

---

## Step 1. Write the MCP server

Create `~/.claude/mcp-servers/rds-mysql/server.py`:

```python
from fastmcp import FastMCP
import pymysql, os

mcp = FastMCP("RDS MySQL")

def _get_conn():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor
    )

@mcp.tool()
def query(sql: str) -> str:
    """Execute a SELECT query and return results."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchmany(500)
            if not rows:
                return "No results."
            cols = list(rows[0].keys())
            lines = [" | ".join(cols)]
            lines += [" | ".join(str(r[c]) for c in cols) for r in rows]
            return "\n".join(lines)

@mcp.tool()
def list_tables(database: str = "") -> str:
    """List all tables in the current or specified database."""
    sql = f"SHOW TABLES FROM `{database}`" if database else "SHOW TABLES"
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return "\n".join(list(r.values())[0] for r in cur.fetchall())

@mcp.tool()
def describe_table(table: str) -> str:
    """Show the column structure of a table."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(f"DESCRIBE `{table}`")
            rows = cur.fetchall()
            cols = list(rows[0].keys())
            lines = [" | ".join(cols)]
            lines += [" | ".join(str(r[c]) for c in cols) for r in rows]
            return "\n".join(lines)

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

> **Pro tip**: Pull connection details from AWS SSM Parameter Store or Secrets Manager so credentials never appear in `.mcp.json`.

---

## Step 2. Register the MCP server

Register with the CLI or write `.mcp.json` directly:

```bash
claude mcp add rds-mysql \
  --command "/path/to/.venv/bin/python" \
  --args "/path/to/server.py" \
  --env "ENV=stg" \
  --env "AWS_PROFILE=myprofile" \
  -s user
```

Or write `~/.claude/.mcp.json` manually:

```json
{
  "mcpServers": {
    "rds-mysql": {
      "command": "/Users/yong/.claude/mcp-servers/rds-mysql/.venv/bin/python",
      "args": ["/Users/yong/.claude/mcp-servers/rds-mysql/server.py"],
      "env": {
        "ENV": "stg",
        "AWS_PROFILE": "mopstg"
      }
    }
  }
}
```

> **User vs Project scope**: Register sensitive DB servers with `user` scope (`-s user`) so they are never committed to Git. Use `project` scope for settings you want to share with your team.

---

## Step 3. Confirm connection

Restart Claude Code, then run:

```
/mcp
```

If `rds-mysql` appears in the list with status `connected`, you are done.

---

## Step 4. Available tools

| Tool | Purpose |
|---|---|
| `query` | Read-only SELECT (up to 500 rows) |
| `execute` | Write operations: INSERT / UPDATE / DELETE |
| `list_tables` | List tables in a database |
| `describe_table` | Show table column structure |
| `show_databases` | List accessible databases |
| `table_row_count` | Get row count for a table |

> `query()` only allows SELECT/SHOW/DESCRIBE. DROP DATABASE and TRUNCATE are automatically blocked.

---

## Step 5. Query the DB with natural language

In Claude Code chat:

**Explore the schema:**
```
What databases are on this RDS instance?
```

```
Show me the tables in the mop schema.
```

```
Describe the dashboard_overview table.
```

**Query and analyze:**
```
List advertiser IDs that had collection failures in the last 2 days.
```

```
Diagnose the Collection error for advertiser_id 1691.
```

Claude writes the SQL, runs it, and explains the results.

---

## Step 6. Use with the Super Analyst Skill

The `/super-analyst` skill uses this MCP to automate Collection error diagnosis:

```
/super-analyst
```

The skill automatically:
1. Asks for the advertiser ID
2. Queries `dashboard_overview` for collection status
3. Queries URL and UTM anomaly detection counts
4. Prints a diagnosis summary

Without the MCP you would have to run each query manually in a terminal. With the MCP, a single prompt handles the full diagnosis.

---

## Use it safely

In production (prd) environments, avoid accidental writes:

```
This is the prd environment. Always show me the SQL before executing.
```

Adding **"show SQL before executing"** to your prompt makes Claude display the query and wait for your approval.

---

## MCP comparison

| | Notion | Obsidian | RDS MySQL |
|---|---|---|---|
| Target | Notion workspace | Local vault | AWS RDS DB |
| Connection | HTTP (official server) | Local REST API | Custom Python server |
| Auth | OAuth | API Key | AWS credentials + VPN |
| Main use | Docs and task management | Personal notes | Data queries and analysis |

---

## References

- FastMCP: `pip install fastmcp` — write MCP servers with Python decorators
- AWS SDK: `pip install boto3` — fetch credentials from Secrets Manager / SSM
- MCP server registry: [modelcontextprotocol.io](https://modelcontextprotocol.io)
