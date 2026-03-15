# Workflow Practice — MOP Monthly Review

In `practice/`, run a 5-step workflow yourself.
You will experience sequential flow, parallel execution, and checkpoints together.

---

## End-to-end flow

```
Step 1: Understand data (sequential)
    └── identify file count and content in data folder

Step 2: Analyze by channel (parallel)
    ├── search ads analysis
    └── shopping ads analysis

Step 3: [Checkpoint] review summary and decide whether to continue

Step 4: Write report (sequential)
    └── merge analysis and create report-monthly.md

Step 5: Derive action items
    └── 3 immediate actions for next month
```

---

## Run

Start Claude in `practice/`:

```bash
cd practice
claude
```

Paste this prompt:

```
Run a February MOP ad performance review in this order:

Step 1: First inspect what files exist in the data folder.

Step 2: Read campaign-search.md and campaign-shopping.md at the same time,
        then summarize strengths and problems by channel.

Step 3: Show me the analysis summary first, then ask whether to continue.

Step 4: After confirmation, write a consolidated report to report-monthly.md.
        Format: Key Summary / Top Campaigns / Campaigns Needing Improvement / Budget Proposal

Step 5: Add 3 action items at the bottom that can be executed next month immediately.
```

---

## Observation points

| Step | What to verify |
|---|---|
| Step 1 | Folder exploration via `Glob` |
| Step 2 | Two `Read` executions in parallel (Sub-Agent) |
| Step 3 | Claude pauses and waits for confirmation |
| Step 4 | `Write` creates `report-monthly.md` |
| Step 5 | Recommendations remain grounded in earlier analysis |

---

## Why split into stages?

You can request this in one line: "Analyze February ads and write a report."
But explicit stages give you:

- a checkpoint at step 3 for direction correction
- better quality by separating analysis from report writing
- immediate visibility into which stage failed
