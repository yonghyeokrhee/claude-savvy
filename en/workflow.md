# Workflow

## What Is a Workflow?

A **Workflow** is an execution flow that connects multiple steps **sequentially or in parallel** to achieve a complex objective.

When "just do this" is too vague, Workflow breaks work into logical stages for reliable completion.

## Why Workflow Is Needed

```
Bad: "Add payment functionality to our service"
    -> too ambiguous for execution

Good: define staged Workflow
    1. Analyze requirements
    2. Design DB schema
    3. Implement API endpoints
    4. Write tests
    5. Update docs
```

Each stage output becomes input for the next, producing consistent outcomes.

## Two Workflow patterns

### 1. Sequential execution

Use this when the next step depends on the previous step:

```
Analyze -> Design -> Implement -> Test -> Deploy
```

Each stage must finish before the next starts.

### 2. Parallel execution

Use this when tasks are independent:

```
           ┌── Frontend implementation
Analysis ──┼── Backend implementation   -> Integration test
           └── DB migration
```

Use Sub-Agents for parallelization.

## Designing Workflows in Claude Code

When requesting complex work, explicitly define stages for better results:

```
"Proceed in this order:
1. Read existing auth code and map structure.
2. Draft a JWT refactor plan.
3. Start implementation after plan approval.
4. Run tests after implementation."
```

Add **checkpoints** between stages to avoid unexpected drift.

## Pinning Workflows in `CLAUDE.md`

If a project repeats the same workflow, encode it in `CLAUDE.md` so you do not repeat instructions:

```markdown
## Feature Development Workflow
Always follow this order for new features:
1. Review relevant spec docs in `docs/`
2. Identify affected existing code
3. Write tests first (TDD)
4. Implement
5. Run `npm test` and confirm full pass
```

## Human-in-the-Loop

Pattern where human approvals are inserted at critical decision points:

```
Analysis done -> [User approval] -> Implementation -> [User approval] -> Deploy
```

If Claude encounters uncertainty, it can stop and ask. Use that deliberately:

```
"Before each stage, show the plan first and continue only after I confirm."
```

## Practical tips

- **The larger the task, the smaller the stage size**: failures become easier to isolate
- **Save intermediate outputs as files**: work can continue even if context resets
- **Define success criteria per stage**: e.g., "Proceed only if tests pass"
