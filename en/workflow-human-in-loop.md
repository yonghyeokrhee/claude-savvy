# Human-in-the-Loop Workflow

## Concept

In long workflows, Claude can occasionally head in the wrong direction. **Human-in-the-Loop** prevents this by inserting user checkpoints at key decisions.

Claude Code can use `AskUserQuestion` to pause work, ask the user, and resume with the response.

## What is `AskUserQuestion`?

It is an internal tool that lets Claude **pause execution** and ask the user a question. After receiving an answer, work continues based on that answer.

```
Claude executes task
    ↓
Reaches critical decision point
    ↓
Call AskUserQuestion -> ask user
    ↓
Receive user answer
    ↓
Continue based on answer
```

You can prompt this behavior directly:

```
"Before each stage, show the plan first and continue after I approve."
"If anything is uncertain, do not proceed. Ask first."
```

---

## Practice example — MOP ad optimization workflow

Use MOP data in `practice/` to run a Human-in-the-Loop workflow.

### Goal

Experience a workflow that **checks direction at each stage** instead of running end-to-end without confirmation.

### Prompt

```
Analyze data in the practice/ folder and derive MOP ad optimization action items.

Follow these rules strictly:

1. **Pause after step 1**: after reviewing data, show your analysis plan first.
   Move to step 2 only if I approve.

2. **Pause after step 2**: show analysis summary.
   If I say "continue", write final action items.

3. If data is missing or uncertain, do not assume. Ask immediately.
```

### Execution flow

```
[Step 1] Understand data
  Claude: inspect data/ file structure
         -> "I plan to analyze as follows. Proceed?"
  User: "Yes" / "Exclude search ads"
         ↓ (reflect answer)

[Step 2] Run analysis
  Claude: analyze only approved scope
         -> "Here is the summary. Should I write action items?"
  User: "Yes, and sort by ROAS"
         ↓

[Step 3] Write action items
  Claude: produce final output with user feedback applied
```

### Without checkpoint vs with checkpoint

| Category | No checkpoints | Human-in-the-Loop |
|---|---|---|
| Speed | Faster | Slower |
| Course correction | Only after completion | Immediate during execution |
| Error cost | Full rerun | Rerun from current stage |
| Best for | Simple predictable work | Important/uncertain outcomes |

---

## Workflow design tips

### When to add checkpoints

- **Decision branches**: "Should we use approach A or B?"
- **Before irreversible actions**: overwrite files, call external APIs, update DB
- **Uncertain data**: "Please verify this metric before continuing"
- **Long task midpoints**: "Confirm we are still on the right path"

### When checkpoints are optional

- Read-only exploration (file structure, code analysis)
- Clearly defined repeatable tasks
- Easily reversible actions

### Prompt patterns

```
# Pattern 1 - confirm plan first
"Before starting, show the full plan first and run only after I say OK."

# Pattern 2 - stage gates
"After each stage, ask whether to proceed."

# Pattern 3 - stop on uncertainty
"If uncertain, do not assume. Ask immediately."

# Pattern 4 - delegate decisions to user
"When there are options, show choices so I can pick."
```
