# Tips & Best Practices

## Be Specific with Requests

Vague requests get vague results. Give Claude context:

**Less effective:**
> Fix the bug

**More effective:**
> The login function in `src/auth.py` throws a KeyError when the user has no email. Fix it without changing the function signature.

## Use CLAUDE.md for Repeated Context

If you find yourself explaining the same thing every session (your stack, naming conventions, how to run tests), put it in `CLAUDE.md`. Claude reads it automatically.

## Review Before Approving

When Claude wants to run a command or write a file, read it before approving. Claude is capable but not infallible — a quick review catches mistakes early.

## Break Down Large Tasks

Instead of "build me a full REST API", try:

1. "Design the database schema for a blog app"
2. "Create the FastAPI models based on this schema"
3. "Add CRUD endpoints for posts"
4. "Write tests for the posts endpoints"

Smaller steps give you checkpoints to verify correctness.

## Use `/clear` When Context Gets Stale

If Claude starts giving inconsistent answers or seems confused mid-session, run `/clear` to reset the conversation while keeping your files intact.

## Leverage Git as a Safety Net

Before letting Claude make large changes, commit your current state:

```bash
git add -A && git commit -m "checkpoint before refactor"
```

This lets you `git diff` to review all changes and `git reset` if something goes wrong.

## Useful Slash Commands

| Command | Description |
|---|---|
| `/help` | Show available commands |
| `/clear` | Clear conversation context |
| `/exit` | End the session |
| `/cost` | Show token usage for this session |

## Common Patterns

### Explain an unfamiliar codebase
```
Read the project structure and explain what this codebase does and how it's organized.
```

### Debug a failing test
```
The test `test_user_signup` in `tests/test_auth.py` is failing. Read the test and the implementation and fix the bug.
```

### Add a feature
```
Add input validation to the `/api/users` POST endpoint in `src/routes/users.py`. Return a 422 with a clear error message if email is missing or invalid.
```

### Code review
```
Review `src/payments.py` for security issues, edge cases, and code quality. List problems in order of severity.
```
