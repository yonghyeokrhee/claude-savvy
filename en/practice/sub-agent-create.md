# Build a Sub-Agent Manually

A Sub-Agent is a Claude instance specialized for a specific role.
In this exercise, you will create `campaign-analyzer`, a specialist agent for MOP campaign analysis.

---

## Skill vs Sub-Agent

| | Skill | Sub-Agent |
|---|---|---|
| Purpose | Shortcut for repeated workflows | Specialist role for a specific domain |
| Invocation | `/skill-name` | Auto-selected by main Claude |
| Characteristic | Fixed output pattern | Own persona and decision criteria |
| Best for | Repeated tasks with known format | Analysis requiring expert judgment |

---

## Step 1. File location

Store Sub-Agent files in one of these locations:

| Location | Path | Scope |
|---|---|---|
| Project-specific | `.claude/agents/<agent-name>.md` | This project only |
| Global | `~/.claude/agents/<agent-name>.md` | All projects |

For this practice, create a project-specific agent:

```bash
mkdir -p .claude/agents
```

---

## Step 2. Write the agent file

`.claude/agents/campaign-analyzer.md`:

```markdown
---
name: campaign-analyzer
description: Specialist agent that analyzes MOP campaign data and recommends improvements.
             Evaluates based on ROAS, CTR, and budget efficiency, then suggests actionable steps.
tools: Read, Write
model: sonnet
color: purple
---

You are an expert in MOP ad performance analysis.

## Role
- ROAS >= 300% = strong / 200~300% = average / < 200% = needs improvement
- Explain in marketer language (no developer jargon)
- Recommendations must be immediately actionable

## Analysis format
1. One-line summary
2. What's working (with metrics)
3. Problem campaigns (with likely causes)
4. 1~3 actions for this week
```

### Frontmatter fields explained

| Field | Purpose | Notes |
|---|---|---|
| `name` | Agent identifier | Use lowercase English and hyphens |
| `description` | Selection criteria Claude uses to invoke this agent | More specific -> better auto-selection |
| `tools` | Allowed tool list | Keep minimum required |
| `model` | Claude model to use | `sonnet` / `haiku` |
| `color` | Color shown in Claude Code UI | Optional |

---

## Step 3. Verify execution

Start Claude in `practice/`:

```bash
cd practice
claude
```

Test both invocation styles:

**Method 1 — Explicitly request agent:**
```
Use the campaign-analyzer agent to analyze data/campaign-search.md.
```

**Method 2 — Let Claude auto-select:**
```
Analyze February search-ad campaign performance with expert depth.
```

In method 2, confirm whether Claude auto-selects `campaign-analyzer` based on `description`.

---

## Step 4. Run multiple Sub-Agents in parallel

If you have multiple specialist agents, parallel execution is possible. Example with an additional `budget-analyzer`:

```
Analyze search-ad and budget status concurrently using specialist agents.
```

```
Main Claude
    ├── campaign-analyzer -> analyze data/campaign-search.md
    └── budget-analyzer   -> analyze data/budget-usage.md
         ↓
    Merge outputs -> consolidated recommendation
```

---

## What makes a good Sub-Agent

**`description` is the most critical field.**
Claude decides when to use an agent primarily from this text.
If it is vague, the agent may not be invoked even if it exists.

```markdown
# Bad
description: Campaign analysis agent

# Good
description: Specialist agent that analyzes MOP campaign data and recommends improvements.
             Evaluates based on ROAS, CTR, and budget efficiency, then suggests actionable steps.
```

**Define decision rules in the system prompt body.**
Provide numeric thresholds, output format, and forbidden patterns so the agent stays consistent.
