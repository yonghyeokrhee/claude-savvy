# AGENTS.md

<!-- Codex CLI equivalent of CLAUDE.md. Keep both files in sync. -->

This file provides guidance to Codex CLI (OpenAI) when working with code in this repository.

## Context

This directory is the `practice/` subdirectory of an English-language coding agent tutorial (GitBook). It contains hands-on exercise files that students run through interactively.

Parent repo: `github.com/yonghyeokrhee/claude-savvy` — changes pushed to `main` sync automatically to GitBook.

## Directory purpose

Each `.md` file here is a **practice exercise** paired with a concept page in the parent `en/` directory. The exercises use a fictional ad optimization service called **MOP** (LG CNS's AI ad optimization platform) as the teaching domain.

Expected subdirectory used in exercises:

```
data/
├── campaign-search.md    # search ad performance data
├── campaign-shopping.md  # shopping ad performance data
└── budget-usage.md       # budget usage data
```

These data files are consumed by sub-agent, workflow, and skills exercises. If they are missing, create them with realistic ad metrics (CTR, ROAS, budget, campaign names).

## Writing rules

- All content is in **English** (the parent `en/` tree; Korean lives in the sibling Korean tree)
- File names use kebab-case
- New exercise files must be registered in `../SUMMARY.md`
- Keep exercises self-contained: each file should state what prerequisites to set up and what commands to run

## Key domain terms used in exercises

| Term | Meaning |
|------|---------|
| CTR | Click-Through Rate — clicks / impressions |
| ROAS | Return on Ad Spend — revenue / ad spend (e.g. 500% = 5x return) |
| Bid | Amount paid to rank ads higher; MOP adjusts automatically |

## Multi-agent support

This directory supports multiple LLM coding agents:

| Concern | Claude Code | Codex CLI |
|---------|-------------|-----------|
| Project instructions | `CLAUDE.md` | `AGENTS.md` (this file) |
| Agents | `.claude/agents/*.md` | `.claude/agents/*.md` (shared) |
| Skills | `.claude/skills/*/SKILL.md` | `.claude/skills/*/SKILL.md` (shared) |
| MCP servers | `.mcp.json` (project-level) | `~/.codex/config.toml` (global) |
| Permissions | `.claude/settings.local.json` | `~/.codex/config.toml` [projects] |

### MCP configuration mapping

Both tools support the MCP protocol — the same server binary works, only the config format differs.

**Claude Code** — project-level `.mcp.json`:

```json
{
  "mcpServers": {
    "rds-mysql": {
      "command": "python",
      "args": ["server.py"],
      "env": { "ENV": "stg" }
    }
  }
}
```

**Codex CLI** — global `~/.codex/config.toml`:

```toml
[mcp_servers.rds-mysql]
command = "python"
args = ["server.py"]
env = { ENV = "stg" }
```

For remote/HTTP MCP servers (e.g. Linear):

```toml
[mcp_servers.linear]
url = "https://mcp.linear.app/mcp"
```

## Publish

```bash
# from repo root
git push origin main   # triggers GitBook sync
```
