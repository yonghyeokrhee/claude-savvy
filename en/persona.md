# Persona & Output Style

## Concept

Claude Code behaves as a general assistant by default.
When you inject a **Persona**, it stays anchored to a specific role with consistent expertise and communication style.

For the same question:
- **CS Expert persona** -> concise, support-oriented answers grounded in retrieved data
- **Product Manager persona** -> answers centered on user problems and business impact

## How It Works

Use Claude Code CLI's `--append-system-prompt` option. The persona file is appended to system prompt and remains active throughout the session.

```bash
claude --append-system-prompt "$(cat ~/.claude/profiles/cs-expert.md)"
```

Unlike `--system-prompt` (full replacement), `--append-system-prompt` preserves default Claude Code behavior and adds role constraints.

## Profile file structure

Store persona profiles as Markdown under `~/.claude/profiles/` or `.claude/profiles/`:

```
~/.claude/profiles/
├── cs-expert.md
├── data-engineer.md
├── oracle-analyst.md
└── product-manager.md
```

### Profile template

```markdown
# Role name

## Persona
Describe role, expertise, and background.

## Communication Style
- Language setting (Korean/English)
- Tone and depth level

## Responsibilities
- Core duties and scope

## Principles
- Rules and conventions to follow
```

### Real example — CS Expert

```markdown
# CS Expert Profile

## Persona
Expert in resolving customer issues and support communication.
Can access service-internal data to solve customer problems.

## Communication Style
- Communicate in Korean, keep technical terms in English when needed
- Be outcome-focused, avoid overlong root-cause essays

## Responsibilities
- Query internal service data and verify configurations
- Bridge communication between Engineers and PMs

## Principles
- Always answer with accurate numeric evidence
- If uncertain, ask clarifying follow-up questions
```

## `ccp` — profile launcher

Instead of typing long options every time, use `ccp` to start Claude with a selected profile. Terminal colors can switch automatically by profile.

```bash
# add to ~/.zshrc
source "$HOME/.claude/claude-profile.sh"
```

```bash
ccp cs      # CS Expert         (navy theme)
ccp pm      # Product Manager   (purple theme)
ccp data    # Data Engineer     (green theme)
ccp oracle  # Oracle Analyst    (red theme)

ccp list    # list all profiles
ccp reset   # reset terminal color
```

Terminal color returns to original automatically when the session ends.

## Terminal themes by profile

| Profile | Background | Accent | Usage |
|---|---|---|---|
| cs-expert | `#1a1b2e` (dark navy) | `#7aa2f7` (blue) | Customer support |
| product-manager | `#1a1520` (dark purple) | `#c084fc` (violet) | Product/PM work |
| data-engineer | `#0d1117` (dark gray) | `#3fb950` (green) | Data work |
| oracle-analyst | `#1c1210` (dark brown) | `#ff6347` (red) | DB analysis |

Terminal color switching uses OSC escape sequences and works in Ghostty and iTerm2.

## Persona vs Output Style

| Category | Persona | Output Style |
|---|---|---|
| Purpose | Define role and domain expertise | Control response format and length |
| How to apply | `--append-system-prompt` | `CLAUDE.md` or prompt instructions |
| Example | "Answer as a CS specialist" | "Answer in one line", "Use table format" |

Using both gives full control over **who answers (Persona) + how they answer (Output Style)**.

## When to use Persona

- When one project needs different viewpoints by role
- When you do not want to retype role instructions for repeated tasks
- When team workflows require consistent style (support responses, reporting format)
