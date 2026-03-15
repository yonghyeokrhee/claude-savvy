# Build a Skill Manually

In the previous chapter, you learned Skill concepts. Now you will create and run a Skill file yourself.

## Preparation

Practice in the `practice/` directory. Claude Code should already be installed.

---

## Step 1. Create a Skill directory

A Skill uses the directory structure **`<skill-name>/SKILL.md`**.

| Location | Path | Scope |
|---|---|---|
| Project-specific | `.claude/skills/<skill-name>/SKILL.md` | This project only |
| Global | `~/.claude/skills/<skill-name>/SKILL.md` | All projects |

In this exercise, create a project-specific Skill in `practice/`:

```bash
mkdir -p .claude/skills/support-explorer
```

---

## Step 2. Write `SKILL.md`

Create `.claude/skills/support-explorer/SKILL.md`.

`SKILL.md` consists of **Frontmatter + Prompt Body**:

```markdown
---
name: support-explorer
description: Provides a tailored quickstart guide for users starting MOP for the first time
allowed-tools: WebFetch
---

# MOP Quick Start Guide

Read https://support.mop.co.kr/introduce and guide the user step by step on how to start MOP.

Follow this order:

1. **One-line explanation of what MOP is** - focus on core value

2. **Recommend the right plan for the user's situation**
   - Ask "Are you an advertiser or an agency?" then recommend Basic / Pro / API Center

3. **How to start right now**
   - Basic: sign up -> choose business type -> start immediately
   - Pro/API Center: pre-adoption survey -> consultant matching -> onboarding

4. **First 3 actions to take** - concrete, practical steps

5. **Core terms to know** - brief definitions for Ad Circle, Spend Pacing, Target Bidding, etc.

Keep guidance concise and friendly, and explain jargon the first time it appears.
```

This file is already available at `practice/.claude/skills/support-explorer/SKILL.md` in this project.

---

## Step 3. Run the Skill

Start Claude Code in `practice/` and invoke it:

```bash
cd practice
claude
```

```
/support-explorer
```

Claude reads the MOP support page and provides a step-by-step getting-started guide tailored to the user's situation.

---

## Step 4. Build more useful Skills

### Example — `/standup`

`.claude/skills/standup/SKILL.md`:

```markdown
---
name: standup
description: Automatically drafts today's standup update from git history
allowed-tools: Bash
---

Check git log and currently modified files, then write a standup in this format:

**What I did yesterday**
- (summary based on recent commit messages)

**What I will do today**
- (based on modified files and TODO comments)

**Blockers**
- None (specify if any)
```

### Example — `/deploy-check`

`.claude/skills/deploy-check/SKILL.md`:

```markdown
---
name: deploy-check
description: Checks required pre-deployment items in order
allowed-tools: Bash, Read
---

Before deployment, verify these items in order:

1. [ ] Confirm all tests pass (`npm test`)
2. [ ] Confirm `.env` is included in `.gitignore`
3. [ ] Search for leftover `console.log` or debug code
4. [ ] Confirm `package.json` version is updated
5. [ ] Confirm README reflects latest changes

Return results as a checklist.
```

---

## Skill Writing Tips

**Specify output format clearly**

```markdown
# Bad
Analyze this code.

# Good
Analyze this code and return:
- Findings: (list)
- Severity: high/medium/low
- Fix suggestions: (with code examples)
```

**Minimize permissions with `allowed-tools`**

Grant only required tools so the Skill does not accidentally modify files or execute commands.

**Share with your team**

Manage `.claude/skills/` in git so everyone uses the same Skills.

```bash
git add .claude/skills/
git commit -m "add shared team Skills"
```

---

## Step 5. Build a program-based Skill

Skill bodies do not have to be plain text prompts only. They can instruct Claude to run **Python scripts**. Put script files inside the Skill directory and let Claude execute them.

### Structure

```
.claude/skills/parse-chat-history/
├── SKILL.md            <- instructs Claude to run export_template.py
└── export_template.py  <- Python script that does the work
```

### Practice Example — `parse-chat-history`

This Skill parses MOP chat history CSV and converts it into an analyzable template format.

**Input file:** `data/chat_history_message_202602040905.csv`
- Complex nested JSON inside `message` column
- Mixed `human` / `ai` / `tool` message types

**Core `SKILL.md` content:**

```markdown
---
name: parse-chat-history
description: Parses LLM chat history CSV into a structured template format
allowed-tools: Bash
---

Run this command:

python export_template.py --input <input.csv> --output <output.csv>

Script location: .claude/skills/parse-chat-history/export_template.py
```

**Run:**

```bash
cd practice
claude
```

```
/parse-chat-history
```

Claude runs `export_template.py` and returns the result.

**Output:** `data/chat_history_template_output.csv` (153 rows)

```
id, session_id, Subject, message.type, message.data.content,
message.data.usage_metadata.total_tokens, analysis, ...
```

- Removes `tool`-type message noise and cleans `[Tool: xxx]` patterns
- Automatically injects summary into the first row of each session

```
"3 turns, 8 AI responses, 25.0K tokens, high engagement, moderate efficiency, task addressed"
```

### Prompt-only Skill vs Program-based Skill

| Category | Prompt-only | Program-based |
|---|---|---|
| Structure | `SKILL.md` only | `SKILL.md` + script files |
| `allowed-tools` | `WebFetch`, `Read`, etc. | `Bash` required |
| Best for | Analysis, guidance, summarization | Data transforms, file processing, repeated jobs |
| Reproducibility | Output may vary by run | Script guarantees consistent output |

---

## Summary

| Step | Action |
|---|---|
| 1 | Create `.claude/skills/<skill-name>/` |
| 2 | Write `SKILL.md` (frontmatter + prompt) |
| 3 | Call `/<skill-name>` in Claude Code |
| 4 | Review output and refine prompt |
