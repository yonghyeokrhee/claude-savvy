# Core Concepts

## How Claude Code Works

Claude Code runs in the terminal and can directly access your local filesystem. It can:

- Read and write project files
- Run shell commands (with approval)
- Search code with `glob` and `grep` patterns
- Browse the web and fetch URL content
- Maintain conversation context within a session

## Permission Modes

Claude Code asks for approval before potentially risky actions. You can control behavior with three modes:

- **Auto-approve**: execute without asking (use carefully)
- **Manual approval**: confirm before writing files or running commands
- **Read-only**: allow reading only, no modifications

## `CLAUDE.md` — Project Instruction File

If you place a `CLAUDE.md` file at the project root, Claude reads it automatically at the start of every session:

```markdown
# My Project

## Tech Stack
- Python 3.12, FastAPI, PostgreSQL

## Conventions
- Variables: snake_case
- Type hints are required for all functions
- Run `pytest` before committing

## Important Files
- `src/main.py` - entry point
- `src/config.py` - environment settings
```

Great use cases for `CLAUDE.md`:
- Explain tech stack and architecture
- Define coding conventions and style rules
- Point to important files
- Document test/build commands

## Context Window

Claude Code keeps in-session conversation as context. When sessions get long:

- `/clear` - reset conversation context (files stay unchanged)
- Be specific in requests - focused prompts produce better output
- Break large tasks into smaller steps

## Tools Claude Uses Internally

Claude Code automatically selects tools depending on the task:

| Tool | Role |
|---|---|
| Read | Read file contents |
| Write | Create or overwrite files |
| Edit | Modify parts of existing files |
| Bash | Run shell commands |
| Glob | Pattern-based file search |
| Grep | Search file contents |
| WebSearch | Search the web |
| WebFetch | Fetch URL content |

## Skill

A **Skill** is a reusable prompt workflow invoked as `/skill-name`. It automates repeated tasks with one command and can be shared through `.claude/skills/`.

```
/review       -> run a code review
/standup      -> generate a standup update
/deploy-check -> run a pre-deploy checklist
```

A Skill is written in `SKILL.md`. Claude can also auto-select it based on the frontmatter `description`.

> Learn more -> [Skills](skills.md) · [Build a Skill Manually](skills-practice.md)
>
> Reference: [FastCampus — Clip 1: Build a Slash Command](https://goobong.gitbook.io/fastcampus/part-1.-ai-claude-code/chapter3_claude_code_-_/clip1_slash_command_-_)

## Agent vs Workflow

When using Claude Code, your approach depends on task type.

| Category | Workflow | Agent |
|---|---|---|
| Control model | Predefined sequence | Dynamic decision-making |
| Predictability | High | Low |
| Flexibility | Low | High |
| Best for | Document pipelines, ETL, scheduled reports | Code review, research, complex problem solving |

**Workflow**: best for repeatable tasks with fixed steps. Easier to debug and monitor.

**Agent**: best for open-ended tasks where solution paths are unknown. It chooses tools and paths autonomously.

> *"It's not about building the most sophisticated system. It's about building the right system for your needs."*
> — Anthropic, Building Effective Agents

In practice, hybrid patterns are often most effective: preprocess with Workflow, analyze with Agent, and format results with Workflow.

> Learn more -> [Workflow](workflow.md) · [Sub-Agent](sub-agent.md)
>
> Reference: [FastCampus — Clip 1: Understanding Agent vs Workflow](https://goobong.gitbook.io/fastcampus/part-2.-agent/chapter1_agent_-_/clip1_agent_vs_workflow_-_)
