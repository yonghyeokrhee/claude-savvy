# Sub-Agent

## What Is a Sub-Agent?

A **Sub-Agent** is a feature where Claude Code creates **separate independent Claude instances** to process complex tasks in parallel.

The main Claude acts as an orchestrator, while Sub-Agents handle assigned tasks independently.

## Why It Matters

When a single Claude instance handles a large task, two issues often appear:

1. **Context contamination**: too many files and intermediate results reduce focus
2. **Sequential bottlenecks**: independent tasks are processed one by one

Sub-Agents solve both at once.

## How It Works

```
Main Claude (orchestrator)
    ├── Sub-Agent 1: Analyze API specs
    ├── Sub-Agent 2: Design DB schema
    └── Sub-Agent 3: Write test cases
         ↓ (after all complete)
    Merge results -> final implementation
```

Each Sub-Agent:
- has an **independent context window**
- returns only final task results to main Claude
- does not interfere with other Sub-Agents

## When Sub-Agents Are Created

Claude Code decides automatically and uses the internal `Agent` tool when:

- there are multiple tasks **without dependencies**
- broad codebase exploration is needed (to protect main context)
- independent research tasks may run for a long time

## Real Example

```
User: "Run a comprehensive security audit of our project"
```

Main Claude may split work like this:

| Sub-Agent | Responsibility |
|---|---|
| Agent 1 | Search SQL injection patterns |
| Agent 2 | Analyze authentication/authorization logic |
| Agent 3 | Check external dependency vulnerabilities |
| Agent 4 | Inspect environment variable exposure |

All four run concurrently, then main Claude compiles a unified report.

## Sub-Agent vs Main Claude

| Category | Main Claude | Sub-Agent |
|---|---|---|
| Role | Work decomposition and synthesis | Focused execution of a single task |
| Context | Remembers entire conversation | Remembers assigned task only |
| Lifetime | Persists through session | Ends when task completes |
| Created by | User session | Auto-created by main Claude |

## Notes

- Sub-Agent execution incurs **additional API cost**
- Each Sub-Agent has independent context and **does not know the full main conversation**
- Main Claude summarizes returned outputs, so full intermediate reasoning may not be visible
