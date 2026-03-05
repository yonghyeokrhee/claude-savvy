# Parse Chat History Skill

Parse LLM chat session history CSV files into a structured template format with session analysis.

## When to Use

Use this skill when the user wants to:
- Parse chat history CSV files containing JSON message data
- Export chat sessions to a structured template format
- Analyze human-AI interaction quality per session
- Generate Windows Excel-compatible CSV outputs

## Prerequisites

- Python 3.x with standard library (csv, json, re, codecs, io, argparse)
- Input CSV with columns: `id`, `user_id`, `session_id`, `chat_history_id`, `message` (JSON), `message_at`, etc.

## Script Location

Copy the script from the skill directory or use the inline version below.

## Usage

```bash
python export_template.py --input <input.csv> --output <output.csv>
```

### Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--input` | `chat_history_message_202602040905.csv` | Input CSV file path |
| `--output` | `chat_history_template_output.csv` | Output CSV file path |

## Features

1. **JSON Parsing**: Best-effort parsing of the `message` column with handling for:
   - Double-quoted strings
   - BOM characters
   - Unicode escapes
   - Malformed JSON

2. **Filtering**:
   - Keeps only `human` and `ai` message types (drops `tool`)
   - Removes rows with empty content
   - Removes rows containing only `[Tool:*]` patterns

3. **Content Cleaning**:
   - Extracts text from string content
   - Unnests list content (text items, reasoning_content)
   - **Strips all `[Tool: xxx]` patterns** from content and subject columns
   - Cleans up whitespace after pattern removal

4. **Session Analysis** (first row per session):
   - Turn count (human messages)
   - AI response count
   - Total token usage
   - Engagement level (low/moderate/high)
   - Efficiency rating (efficient/moderate/token-heavy)
   - Completion indicator

5. **Output Formats**:
   - UTF-8 (default)
   - UTF-8 with BOM (for Windows Excel): add `_utf8bom` suffix
   - CP949 (legacy Windows): add `_cp949` suffix

## Output Columns

```
id, user_id, session_id, chat_history_id, Subject, message.type,
message.data.content, message.data.name, message.data.usage_metadata.total_tokens,
message_at, created_at, created_by, updated_at, updated_by, run_id,
account_id, marketplace_id, analysis
```

## Generating Windows-Compatible Versions

After running the main script, generate Excel-compatible versions:

```python
import csv

with open('output.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

# UTF-8 with BOM (recommended for modern Excel)
with open('output_utf8bom.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, doublequote=True)
    writer.writeheader()
    writer.writerows(rows)

# CP949 (legacy Windows Excel)
with open('output_cp949.csv', 'w', encoding='cp949', newline='', errors='replace') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, doublequote=True)
    writer.writeheader()
    writer.writerows(rows)
```

## Example Workflow

1. Place input CSV in working directory
2. Run: `python export_template.py --input chat_history.csv`
3. Generate Windows versions if needed
4. Open `*_utf8bom.csv` in Windows Excel

## Analysis Column Format

```
"3 turns, 8 AI responses, 25.0K tokens, high engagement (2.7 responses/turn), moderate efficiency, task addressed"
```

Only the first row of each session contains the analysis; subsequent rows have empty analysis.
