# Practice: Creating `CLAUDE.md`

`CLAUDE.md` is automatically read when Claude starts in a project.
If written well once, Claude keeps your project context without repeated explanation.

## Practice scenario

Assume a marketer responsible for MOP (an AI ad optimization service) works with Claude.
Without `CLAUDE.md`, Claude does not know what MOP is. With it, Claude understands immediately.

## Steps

### Step 1 - Create a new folder and start Claude

In terminal:

```bash
mkdir mop-project
cd mop-project
claude
```

Ask Claude:

```
CTR suddenly dropped. What should I check?
```

Without project context, Claude gives only generic advice.

### Step 2 - Write `CLAUDE.md`

Create `CLAUDE.md` in the same folder.

```markdown
# MOP Project

MOP is LG CNS's AI ad optimization service.
It automatically optimizes search and shopping ads.

## Key terms

- CTR (Click-Through Rate): clicks divided by impressions. Higher is better.
- ROAS: revenue divided by ad spend. 500% means 1 spent, 5 earned.
- Bid: amount paid to rank ads higher. MOP adjusts this automatically.

## Users

Primary users are advertiser managers and agency account executives.

## Response rules

- Do not use developer jargon (target audience: marketers)
- Use realistic examples based on ad industry metrics
```

### Step 3 - Compare behavior

Open a new Claude session and ask the same question again:

```
CTR suddenly dropped. What should I check?
```

Now Claude answers in MOP ad-platform context and marketer-friendly language.

## Key point

| | Without `CLAUDE.md` | With `CLAUDE.md` |
|---|---|---|
| Service awareness | Unknown | Understands MOP ad platform |
| Response quality | Generic explanation | Operationally relevant advice |
| Repeated explanation | Required | Not required |

## Tips for writing well

- **Service description**: what work you do and in what domain
- **Key terms**: common vocabulary and definitions
- **Response rules**: tone, length, banned expressions
- **Frequent commands**: document recurring tasks
