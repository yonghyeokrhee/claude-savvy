# Introduction to Claude Code

## What Is Claude Code?

Claude Code is Anthropic's official terminal-based AI coding agent. It works **directly inside your codebase**, not in a standalone chat window.

| Category | Chat-Based AI | Claude Code |
|---|---|---|
| Code access | Copy and paste | Direct file read/write |
| Command execution | Not available | Runs shell commands |
| Project context | Must re-explain every time | Persisted via `CLAUDE.md` |

## Claude Code as an Agent

Claude Code is not just a code generator, but an **agent**. It receives a goal, plans on its own, selects tools, executes, validates outcomes, and iterates until completion.

```
User request -> Plan -> Tool execution -> Validate result -> Complete or retry
```

## Core Tools

| Tool | Role |
|---|---|
| Read / Write / Edit | Read, create, and modify files |
| Bash | Run shell commands |
| Glob / Grep | Search files and content |
| WebSearch / WebFetch | Search the web and fetch URLs |

## `CLAUDE.md` — Project Instruction File

If placed at the project root, this file is automatically loaded at session start. Define your tech stack, conventions, and important file paths once so you do not need to repeat them.

## Practical Tips

- **Be specific**: include filenames, function names, and constraints.
- **Work in steps**: break large tasks into checkpoints.
- **Use Git as a safety net**: create a restore point with `git commit` before major changes.
- **Use `/clear`**: reset context if the session gets too long or noisy.
- **Use `/cost`**: check token usage regularly.
