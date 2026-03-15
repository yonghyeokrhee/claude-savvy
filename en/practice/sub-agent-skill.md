# Building a Skill That Uses Sub-Agents

Combining Skills and Sub-Agents lets you automate repeated multi-file work in one command.
In this exercise, you will build `/mop-report` to analyze three files in parallel and generate a report.

---

## Understand the structure

A standard Skill passes a prompt to Claude.
If that prompt includes instructions like **"read these at the same time"**, Claude can create Sub-Agents and process in parallel.

```
User runs /mop-report
    ↓
Load SKILL.md prompt
    ↓
Claude decides: "3 files are independent -> process in parallel"
    ├── Sub-Agent 1: read campaign-search.md
    ├── Sub-Agent 2: read campaign-shopping.md
    └── Sub-Agent 3: read budget-usage.md
         ↓
    Merge results -> generate report-monthly.md
```

---

## Skill file structure

`practice/.claude/skills/mop-report/SKILL.md`:

```markdown
---
name: mop-report
description: Analyzes campaign files in data folder in parallel and generates a monthly report
allowed-tools: Read, Write
---

Read these three files in `data/` **at the same time**:
- data/campaign-search.md
- data/campaign-shopping.md
- data/budget-usage.md

After reading all files, create `report-monthly.md` in this format:

(report format specification...)
```

**Key points:**
- `allowed-tools: Read, Write` -> only file read/write allowed
- `**at the same time**` -> nudges Claude toward Sub-Agent parallel processing
- Define output format explicitly -> avoids inconsistent outputs

---

## Exercise steps

### Step 1 — Start Claude in `practice`

```bash
cd practice
claude
```

### Step 2 — Invoke Skill

```
/mop-report
```

### Step 3 — What to observe

Check the left tool panel:

| Observation | What to confirm |
|---|---|
| `Read` count | Are 3 reads executed almost simultaneously? |
| `Write` execution | Is `report-monthly.md` created? |
| Total duration | Is it faster than sequentially reading 3 files? |

### Step 4 — Validate result

```bash
cat report-monthly.md
```

Verify the report follows the required format.

---

## How to encourage Sub-Agent use inside a Skill

These prompt phrases often lead Claude to choose parallel execution:

| Phrase | Effect |
|---|---|
| `read at the same time` | Parallel reads across multiple files |
| `analyze each separately` | Independent per-item analysis |
| `check all files at once` | Parallel folder-wide exploration |

When **order matters**, explicitly force sequence:

```markdown
1. First read campaign-search.md.
2. Then analyze budget-usage.md based on that result.
```

---

## Summary

| | Basic Skill | Sub-Agent-enabled Skill |
|---|---|---|
| Execution mode | Sequential | Parallel |
| Best for | Single-file, stepwise tasks | Independent multi-file analysis |
| Speed | Grows with file count | More stable regardless of file count |
| How to write | Standard prompt | Add phrases like "at the same time", "each" |
