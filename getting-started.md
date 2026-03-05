# Getting Started

## Installation

Install Claude Code globally via npm:

```bash
npm install -g @anthropic-ai/claude-code
```

## Authentication

Run Claude Code for the first time and follow the login prompt:

```bash
claude
```

You will be redirected to authenticate with your Anthropic account. Once done, you are ready to go.

## Starting a Session

Navigate to your project directory and launch Claude Code:

```bash
cd your-project
claude
```

You can also pass a task directly:

```bash
claude "explain what this project does"
```

## First Commands to Try

| Command | What it does |
|---|---|
| `claude` | Start an interactive session |
| `claude "fix the bug in auth.py"` | One-shot task |
| `claude --help` | Show all options |
| `/help` | In-session help |
| `/exit` | End the session |
