# Tips & Best Practices

## Ask Specific Questions

Vague requests produce vague results. Include context.

**Less effective:**
> Fix this bug.

**More effective:**
> In `src/auth.py`, the `login` function throws `KeyError` when a user has no email. Please fix it without changing the function signature.

## Eliminate Repeated Explanations with `CLAUDE.md`

If you repeat the same details every session (stack, naming conventions, test commands), put them in `CLAUDE.md`. Claude reads it automatically.

## Always Review Before Approving

When Claude asks to run commands or write files, inspect first. Claude is capable, but mistakes happen. A quick review catches issues early.

## Split Large Tasks into Steps

Instead of "Build the entire REST API," use:

1. "Design the DB schema for a blog app."
2. "Create FastAPI models from this schema."
3. "Add CRUD endpoints for posts."
4. "Write tests for post endpoints."

Stepwise execution gives you checkpoints for validation.

## Use `/clear` When Context Gets Noisy

If long sessions cause inconsistent or confused responses, run `/clear`. Your files remain unchanged.

## Use Git as a Safety Net

Before large changes, create a checkpoint commit:

```bash
git add -A && git commit -m "checkpoint before refactor"
```

Then review with `git diff`. If needed, roll back with `git reset`.

## Useful Slash Commands

| Command | Description |
|---|---|
| `/help` | Show available commands |
| `/clear` | Reset conversation context |
| `/cost` | Check current session token usage |
| `/exit` | End session |

## Frequently Used Prompt Patterns

### Understand an unfamiliar codebase
```
Read the project structure and explain what this codebase does and how it is organized.
```

### Debug a failing test
```
`test_user_signup` in `tests/test_auth.py` is failing. Read both the test and implementation and fix the bug.
```

### Add a feature
```
Add input validation to the `POST /api/users` endpoint in `src/routes/users.py`. If email is missing or invalid, return 422 with a clear error message.
```

### Request a code review
```
Review `src/payments.py` for security issues, edge cases, and code quality. List findings by severity.
```
