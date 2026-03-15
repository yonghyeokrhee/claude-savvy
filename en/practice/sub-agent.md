# Sub-Agent Practice

This exercise demonstrates how Sub-Agents work in practice using an MOP ad analysis scenario.

## Preparation

Make sure these three files exist in `practice/`:

```
practice/
└── data/
    ├── campaign-search.md    # search ad status
    ├── campaign-shopping.md  # shopping ad status
    └── budget-usage.md       # budget usage status
```

Start Claude in `practice/`:

```bash
cd practice
claude
```

---

## Exercise 1 — Sequential processing without Sub-Agents

Ask Claude to analyze one file first:

```
Read campaign-search.md and tell me which campaigns are problematic.
```

Claude reads one file and answers. In the left tool list, you should see one `Read` execution.

---

## Exercise 2 — Parallel processing with Sub-Agents

Now request all three files at once:

```
Analyze all three files in data (search ads, shopping ads, and budget status)
and generate a consolidated February performance report.
Separate what is performing well from what needs improvement.
```

This time, in the left tool list, you should see `Read` executed **three times almost simultaneously**.

> **This is Sub-Agent behavior.** Claude assigns each file analysis to an independent instance in parallel, then merges results into one report.

---

## Compare results

| | Exercise 1 (Sequential) | Exercise 2 (Parallel) |
|---|---|---|
| File reads | One at a time | Three at once |
| Execution model | Single Claude | Three Sub-Agents |
| Speed | Slower | Faster |
| Best for | When next step depends on previous result | Independent tasks |

---

## When are Sub-Agents auto-created?

Claude decides internally after reading the request:

- **"Are tasks interdependent?"** If not, split in parallel
- **"Is data volume large enough to pollute context?"** If yes, isolate with Sub-Agents

You do not need to explicitly command Sub-Agent creation.

---

## Try at larger scale

Parallel gains become clearer as file count increases. Try this prompt:

```
Inspect the entire practice folder and summarize what exercises are available.
```

Watch Claude explore many files concurrently.
