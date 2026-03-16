---
name: mop-deep-analysis
description: Runs 3 specialist analyst agents (search ads / shopping search / budget) simultaneously for deep MOP campaign analysis
allowed-tools: Agent, Read, Write
---

Run the following 3 analysis tasks as **separate Agents**, all **in parallel**.
All 3 Agents MUST launch simultaneously.

## Agent 1 — Search Ad Analyst (search-analyst)

Use the search-analyst agent to:
- Read CLAUDE.md for MOP service context
- Read all .md files in the data/ folder
- Perform deep analysis of each search ad campaign
- Include comparative analysis against shopping search data
- Write results to `data/analysis-search.md`

## Agent 2 — Shopping Search Analyst (shopping-analyst)

Use the shopping-analyst agent to:
- Read CLAUDE.md for MOP service context
- Read all .md files in the data/ folder
- Perform deep analysis of each shopping search campaign
- Include efficiency comparison against search ads
- Write results to `data/analysis-shopping.md`

## Agent 3 — Budget Analyst (budget-analyst)

Use the budget-analyst agent to:
- Read CLAUDE.md for MOP service context
- Read all .md files in the data/ folder
- Perform cross-channel budget efficiency analysis
- Build 3 budget scenarios for March
- Write results to `data/analysis-budget.md`

## After Completion

Once all 3 reports are done:
1. Read the key conclusions from each report
2. Synthesize the 3 analysts' findings into an **Executive Summary** and print it to screen

Executive Summary format:
```
## Executive Summary — February MOP Campaign Analysis

### Key Findings (3 lines)
1.
2.
3.

### Channel-Level Diagnosis
- Search Ads: (search-analyst key conclusion)
- Shopping Search: (shopping-analyst key conclusion)
- Budget Allocation: (budget-analyst key conclusion)

### Immediate Action Items — TOP 3
1.
2.
3.
```
