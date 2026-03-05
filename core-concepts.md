# Core Concepts

## How Claude Code Works

Claude Code runs in your terminal with access to your local filesystem. It can:

- Read and write files in your project
- Execute shell commands (with your permission)
- Search code with grep and glob patterns
- Browse the web and fetch URLs
- Remember context across a session

## Permission Modes

Claude Code asks before taking potentially risky actions. You control what it can do:

- **Auto-approve** — Claude executes actions without prompting (use with caution)
- **Manual approval** — You confirm each file write or command run
- **Read-only** — Claude can read but not modify anything

## CLAUDE.md — Project Instructions

Place a `CLAUDE.md` file at the root of your project to give Claude persistent instructions:

```markdown
# My Project

## Stack
- Python 3.12, FastAPI, PostgreSQL

## Conventions
- Use snake_case for variables
- All functions must have type hints
- Run `pytest` before committing

## Important Files
- `src/main.py` — entry point
- `src/config.py` — environment config
```

Claude reads this file at the start of every session. Use it to:
- Describe your tech stack and architecture
- Set coding conventions and style rules
- Point to important files
- Define how to run tests and builds

## Context Window

Claude Code maintains conversation context within a session. For long sessions:

- Use `/clear` to reset context if Claude seems confused
- Be specific — the more focused your request, the better the result
- Break large tasks into smaller steps

## Tools Claude Uses Internally

Claude Code has built-in tools it selects automatically:

| Tool | Purpose |
|---|---|
| Read | Read file contents |
| Write | Create or overwrite files |
| Edit | Make targeted edits to existing files |
| Bash | Run shell commands |
| Glob | Find files by pattern |
| Grep | Search file contents |
| WebSearch | Search the web |
| WebFetch | Fetch a URL |
