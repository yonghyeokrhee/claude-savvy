# Build a Skill Through Conversation

This method creates Skills by chatting with Claude instead of hand-writing `SKILL.md` first. Describe behavior in natural language, and Claude builds both the structure and file for you.

## Method

In a Claude Code session, ask in plain language:

```
Create .claude/skills/standup/SKILL.md.

This Skill should automatically draft standup content using git log and currently modified files.
Output format: what I did yesterday / what I will do today / blockers.
```

Claude can create the directory and `SKILL.md` in one step.

---

## Practice Examples

### Example 1 — Improve `/support-explorer`

Update an existing Skill through conversation.

```
Update .claude/skills/support-explorer/SKILL.md.

Right now it only reads the MOP introduction page.
Change it so it first asks whether the user is an advertiser or an agency,
then guides onboarding steps accordingly.
```

### Example 2 — Create a new Skill from scratch through conversation

```
Create a Skill named mop-report under .claude/skills/.

It should read data files in practice/data/
and generate a monthly ad performance report.

Output format:
- Overall ROAS summary
- Top 3 campaigns
- 3 recommended actions for next month

Set allowed-tools to Read only.
```

Typical Claude output:

```
Created .claude/skills/mop-report/SKILL.md.
```

```markdown
---
name: mop-report
description: Reads ad data from practice/data and writes a monthly performance report
allowed-tools: Read
---

# MOP Monthly Performance Report

Read files in practice/data/ and summarize this month's ad performance.

Output in this format:

## Overall ROAS Summary
...

## Top 3 Campaigns
...

## Recommended Actions for Next Month
1.
2.
3.
```

### Example 3 — Create a new Skill by referencing an existing one

```
Use .claude/skills/support-explorer/SKILL.md as reference
and create a similar Skill named mop-faq.

This Skill should read frequently asked questions from
https://support.mop.co.kr and find answers for the user's question.
```

---

## Advanced — Build an Interactive Learning Skill

Standard Skills usually output in a fixed format. **Interactive Skills** ask and answer questions with the user step by step, which is especially effective for onboarding and teaching.

### Core Structure

In `SKILL.md`, explicitly define interaction flow and question sequence:

```markdown
## How to run
Never explain everything at once.
Proceed only through back-and-forth Q&A.

## Step 1 - User profiling
> "Are you brand new, or already using the product?"

## Step 2 - Concept quiz
After each concept explanation, ask a check question.
Do one concept at a time.

## Rules
- Ask only one question at a time
- Give feedback to the user's answer before moving on
```

### Practice Example — Advanced `support-explorer`

`practice/.claude/skills/support-explorer/SKILL.md` is enhanced as an interactive MOP learning Skill.

**Example conversation flow:**

```
/support-explorer

Claude: Are you new to MOP, or already using it?

User: I'm new.

Claude: Are you managing ads directly as an advertiser,
or managing multiple clients as an agency?

User: I'm an advertiser.

Claude: MOP automatically optimizes search and shopping ads.
What do you think is the most important capability it automates?

User: Bid adjustment?

Claude: Exactly. Target Bidding is core.
Next, let's review plans. Among Basic / Pro / API Center,
which do you think fits your current situation?
```

### Design Patterns for Interactive Skills

| Pattern | Description | Best for |
|---|---|---|
| **Profile first** | Ask role/experience, then tailor content | Onboarding, guidance |
| **Explain -> check** | Validate understanding right after explanation | Training, education |
| **Scenario prompt** | Give real situations and ask for response | Advanced learning |
| **Next-step suggestion** | Recommend next topics at session end | Ongoing learning |

### Prompt to upgrade a Skill into interactive mode

To add interactive behavior to an existing Skill:

```
Update .claude/skills/support-explorer/SKILL.md.

It currently outputs everything at once.
Change it to interactive mode as follows:

1. Ask first whether the user is an advertiser or agency.
2. Explain one core concept, then ask a comprehension question.
3. Give one practical scenario and ask how they would respond.
4. Never output everything at once.
```

---

## Writing directly vs building through conversation

| Category | Write directly | Build through conversation |
|---|---|---|
| Speed | Slower | Faster |
| Precision | Exactly what you write | Depends on Claude interpretation |
| Edits | Edit file manually | Ask follow-up changes in chat |
| Best for | Fine-grained control | Rapid first draft |

Most efficient flow: generate a draft through conversation, then refine the resulting file manually.

---

## Tips

**Include concrete output format in your request**

```
# Less effective
Create a report Skill.

# More effective
## Section 1: Summary (max 3 lines)
## Section 2: Top campaigns table (sorted by ROAS)
## Section 3: Action items (numbered list)
Create a mop-report Skill that outputs exactly this format.
```

**Test the Skill immediately**

```
/mop-report
```

If output is not right, request follow-up changes right away:

```
Add a TACOS column to the table in section 2.
```

> Reference: [FastCampus — Clip 1: Build a Slash Command](https://goobong.gitbook.io/fastcampus/part-1.-ai-claude-code/chapter3_claude_code_-_/clip1_slash_command_-_)
