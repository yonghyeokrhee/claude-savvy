# Skills

## What Is a Skill?

A **Skill** is a **predefined prompt workflow** in Claude Code, invoked as `/skill-name`.

When a user types `/support-explorer`, Claude Code loads that Skill file and executes it as a prompt. You can think of Skills as shortcuts for complex instructions you do not want to type repeatedly.

## When Skills Run

Skills run in two ways:

| Mode | Description |
|---|---|
| **Explicit invocation** | User directly types `/skill-name` |
| **Auto-trigger** | Claude chooses a matching Skill from conversation context |

Auto-trigger behavior is based on the `description` field in `SKILL.md`. If Claude judges that the current request matches the description, it can run the Skill without explicit input.

```yaml
---
description: Provides a tailored quickstart guide for users starting MOP for the first time
---
```

> If someone asks, "How do I get started with MOP?", Claude may automatically run the `support-explorer` Skill.

## Folder Structure

A Skill is not a single `.md` file at root. It is defined as **`SKILL.md` inside a directory**.

```
~/.claude/skills/              <- Global (all projects)
└── support-explorer/
    └── SKILL.md

.claude/skills/                <- Project-specific
└── support-explorer/
    └── SKILL.md
```

> If both exist with the same name, the project-specific Skill takes precedence over the global one.

## `SKILL.md` Syntax

A `SKILL.md` file has two parts:

### 1. Frontmatter (optional)

YAML metadata wrapped by `---` at the top of the file.

```yaml
---
name: support-explorer
description: Provides a tailored quickstart guide for users starting MOP for the first time
allowed-tools: WebFetch
---
```

| Field | Description |
|---|---|
| `name` | Skill name (match directory name) |
| `description` | When to use this Skill. Shown in `/help`. |
| `allowed-tools` | Restrict tools this Skill can use (comma-separated) |

### 2. Body (prompt)

Everything after frontmatter is the prompt passed to Claude. Write it in standard Markdown.

```markdown
---
name: daily-standup
description: Automatically drafts today's standup update from git history
allowed-tools: Bash
---

Check git log and currently modified files, then write a standup in this format:

**What I did yesterday**
- (summary based on recent commit messages)

**What I will do today**
- (based on modified files and TODO comments)

**Blockers**
- None (specify if any)
```

## How It Works

```
User: /support-explorer
    ↓
Load .claude/skills/support-explorer/SKILL.md
    ↓
Parse frontmatter -> apply allowed tools
    ↓
Execute body content as prompt
```

## Built-In Skills

Claude Code includes built-in Skills for common tasks:

| Skill | Description |
|---|---|
| `/commit` | Analyze changes and draft a commit message |
| `/help` | Show Claude Code usage guidance |
| `/review` | Run a code review |

## When You Should Use Skills

- You repeat the same request pattern often
- You want a shared workflow across teammates
- The prompt is too long/complex to remember
- You want to automate project-specific procedures (deploy checklist, review criteria, etc.)
