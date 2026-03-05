#!/usr/bin/env python3
"""Export chat history to template CSV format."""

import argparse
import csv
import io
import json
import codecs
import re
from collections import defaultdict

# Pattern to match content that is only tool references
TOOL_ONLY_PATTERN = re.compile(r'^\s*(\[Tool:\s*\w+\]\s*)+$')


def decode_bytes(data):
    """Decode bytes with encoding detection."""
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        pass

    candidates = ["cp949", "euc-kr", "latin1"]
    best_text = None
    best_repl = None
    for enc in candidates:
        text = data.decode(enc, errors="replace")
        repl_count = text.count("\ufffd")
        if best_repl is None or repl_count < best_repl:
            best_text = text
            best_repl = repl_count
    return best_text


def best_effort_json_load(raw):
    """Parse JSON with best-effort handling."""
    if raw is None:
        return None, "null"
    if not isinstance(raw, str):
        return None, "non_string"

    s = raw.strip()
    if not s:
        return None, "empty"
    if s.startswith("\ufeff"):
        s = s.lstrip("\ufeff")

    candidates = [s]
    if s.startswith('"') and s.endswith('"'):
        candidates.append(s[1:-1])
    s_dbl = s.replace('""', '"')
    candidates.append(s_dbl)
    if s_dbl.startswith('"') and s_dbl.endswith('"'):
        candidates.append(s_dbl[1:-1])

    if "\\" in s:
        try:
            candidates.append(codecs.decode(s, "unicode_escape"))
        except Exception:
            pass
    if "\\" in s_dbl:
        try:
            candidates.append(codecs.decode(s_dbl, "unicode_escape"))
        except Exception:
            pass

    seen = set()
    unique = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique.append(c)

    for cand in unique:
        try:
            return json.loads(cand), None
        except Exception:
            continue
    return None, "parse_error"


def extract_content_text(content):
    """Extract text from content (string or list)."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
                continue
            if not isinstance(item, dict):
                continue
            item_type = item.get("type")
            if item_type == "text" and isinstance(item.get("text"), str):
                parts.append(item["text"])
            elif item_type == "reasoning_content":
                rc = item.get("reasoning_content")
                if isinstance(rc, dict) and isinstance(rc.get("text"), str):
                    parts.append(rc["text"])
            elif item_type == "tool_use":
                # Extract meaningful content from tool input, skip tool name marker
                tool_input = item.get("input", "")
                if isinstance(tool_input, str) and tool_input:
                    try:
                        parsed_input = json.loads(tool_input)
                        if isinstance(parsed_input, dict):
                            msg = parsed_input.get("ask_message") or parsed_input.get("message", "")
                            if msg:
                                parts.append(msg)
                    except Exception:
                        pass
        return "\n".join(parts)
    return ""


# Pattern to match [Tool: xxx] anywhere in text
TOOL_PATTERN = re.compile(r'\[Tool:\s*\w+\]\s*')


def strip_tool_patterns(text):
    """Remove all [Tool: xxx] patterns from text."""
    if not text:
        return text
    cleaned = TOOL_PATTERN.sub('', text)
    # Clean up extra whitespace/newlines left behind
    cleaned = re.sub(r'\n\s*\n', '\n', cleaned)
    return cleaned.strip()


def generate_subject(msg_type, content_text, name):
    """Generate a subject/title for the row."""
    if not content_text:
        if name:
            return name
        return ""
    
    # Clean up content for subject
    text = content_text.strip()
    # Remove any remaining [Tool: xxx] patterns
    text = strip_tool_patterns(text)
    # Remove markdown formatting for subject
    text = text.replace("**", "").replace("##", "").replace("#", "")
    # Get first line or first 80 chars
    first_line = text.split("\n")[0].strip()
    
    if not first_line:
        if name:
            return name
        return ""
    
    if msg_type == "human":
        # For human, use the question/content as subject
        if len(first_line) <= 80:
            return first_line
        return first_line[:77] + "..."
    else:
        # For ai, use agent name if available and content is long
        if name and len(first_line) > 50:
            return name
        if len(first_line) <= 80:
            return first_line
        return first_line[:77] + "..."


def is_tool_only_content(content_text):
    """Check if content contains only [Tool:*] references."""
    if not content_text or not content_text.strip():
        return False
    return bool(TOOL_ONLY_PATTERN.match(content_text.strip()))


def generate_session_analysis(session_rows):
    """Generate text analysis summary for a session."""
    human_count = sum(1 for r in session_rows if r["_msg_type"] == "human")
    ai_count = sum(1 for r in session_rows if r["_msg_type"] == "ai")
    
    # Calculate total tokens
    total_tokens = 0
    for r in session_rows:
        tok = r.get("_tokens")
        if tok and isinstance(tok, (int, float)):
            total_tokens += int(tok)
    
    # Calculate content lengths for substantive response check
    ai_content_lengths = [
        len(r.get("message.data.content ", "") or "")
        for r in session_rows if r["_msg_type"] == "ai"
    ]
    has_substantive_response = any(l > 100 for l in ai_content_lengths)
    
    # Determine engagement level
    if human_count == 0:
        response_ratio = 0
    else:
        response_ratio = ai_count / human_count
    
    if response_ratio >= 3:
        engagement = "high engagement"
    elif response_ratio >= 1.5:
        engagement = "moderate engagement"
    else:
        engagement = "low engagement"
    
    # Determine efficiency
    if human_count > 0 and total_tokens > 0:
        tokens_per_turn = total_tokens / human_count
        if tokens_per_turn < 5000:
            efficiency = "efficient"
        elif tokens_per_turn < 15000:
            efficiency = "moderate efficiency"
        else:
            efficiency = "token-heavy"
    else:
        efficiency = "minimal"
        tokens_per_turn = 0
    
    # Completion indicator
    if has_substantive_response:
        completion = "task addressed"
    else:
        completion = "brief interaction"
    
    # Format token count
    if total_tokens >= 1000:
        token_str = f"{total_tokens / 1000:.1f}K tokens"
    else:
        token_str = f"{total_tokens} tokens"
    
    # Build summary
    parts = [
        f"{human_count} turn{'s' if human_count != 1 else ''}",
        f"{ai_count} AI response{'s' if ai_count != 1 else ''}",
        token_str,
        f"{engagement} ({response_ratio:.1f} responses/turn)",
        efficiency,
        completion,
    ]
    
    return ", ".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Export chat history to template CSV format.")
    parser.add_argument(
        "--input",
        default="chat_history_message_202602040905.csv",
        help="Path to chat history CSV",
    )
    parser.add_argument(
        "--output",
        default="chat_history_template_output.csv",
        help="Output CSV path",
    )
    args = parser.parse_args()

    # Read input file with encoding detection
    with open(args.input, "rb") as f:
        raw_bytes = f.read()
    decoded_text = decode_bytes(raw_bytes)

    # Parse CSV
    reader = csv.DictReader(io.StringIO(decoded_text))
    rows = list(reader)

    # Process rows
    output_rows = []
    for row in rows:
        raw_msg = row.get("message", "")
        parsed, err = best_effort_json_load(raw_msg)

        if parsed is None:
            continue

        msg_type = parsed.get("type") if isinstance(parsed, dict) else None
        
        # Filter to human and ai only
        if msg_type not in ("human", "ai"):
            continue

        data = parsed.get("data", {}) if isinstance(parsed, dict) else {}
        if not isinstance(data, dict):
            data = {}

        # Extract content
        content = data.get("content")
        content_text = extract_content_text(content)
        
        # Strip [Tool: xxx] patterns from content
        content_text = strip_tool_patterns(content_text)

        # Filter out tool-only content rows (now should be empty after stripping)
        if is_tool_only_content(content_text):
            continue

        # Filter out empty content rows
        if not content_text or not content_text.strip():
            continue

        # Extract name
        name = data.get("name", "")
        if name is None:
            name = ""

        # Extract total_tokens
        usage = data.get("usage_metadata", {})
        if not isinstance(usage, dict):
            usage = {}
        total_tokens = usage.get("total_tokens", "")
        if total_tokens is None:
            total_tokens = ""

        # Parse tokens as number for analysis
        tokens_num = None
        if total_tokens:
            try:
                tokens_num = int(total_tokens)
            except (ValueError, TypeError):
                pass

        # Generate subject
        subject = generate_subject(msg_type, content_text, name)

        output_row = {
            "id": row.get("id", ""),
            "user_id": row.get("user_id", ""),
            "session_id": row.get("session_id", ""),
            "chat_history_id": row.get("chat_history_id", ""),
            "Subject": subject,
            "message.type\n(human, tool, ai 구분)": msg_type,
            "message.data.content ": content_text,
            "message.data.name": name,
            "message.data.usage_metadata.total_tokens": total_tokens,
            "message_at": row.get("message_at", ""),
            "created_at": row.get("created_at", ""),
            "created_by": row.get("created_by", ""),
            "updated_at": row.get("updated_at", ""),
            "updated_by": row.get("updated_by", ""),
            "run_id": row.get("run_id", ""),
            "account_id": row.get("account_id", ""),
            "marketplace_id": row.get("marketplace_id", ""),
            # Temporary fields for analysis calculation
            "_msg_type": msg_type,
            "_tokens": tokens_num,
        }
        output_rows.append(output_row)

    # Sort by session_id, chat_history_id, then message_at
    def sort_key(r):
        sid = r.get("session_id", "") or ""
        chid = r.get("chat_history_id", "") or ""
        ts = r.get("message_at", "") or ""
        return (sid, chid, ts)

    output_rows.sort(key=sort_key)

    # Group rows by session for analysis
    session_groups = defaultdict(list)
    for row in output_rows:
        key = (row.get("session_id", ""), row.get("chat_history_id", ""))
        session_groups[key].append(row)

    # Calculate analysis for each session
    session_analysis = {}
    for key, session_rows in session_groups.items():
        session_analysis[key] = generate_session_analysis(session_rows)

    # Add analysis to first row of each session only, remove temporary fields
    seen_sessions = set()
    for row in output_rows:
        key = (row.get("session_id", ""), row.get("chat_history_id", ""))
        if key not in seen_sessions:
            row["analysis"] = session_analysis.get(key, "")
            seen_sessions.add(key)
        else:
            row["analysis"] = ""
        # Remove temporary fields
        row.pop("_msg_type", None)
        row.pop("_tokens", None)

    # Write output CSV
    fieldnames = [
        "id",
        "user_id",
        "session_id",
        "chat_history_id",
        "Subject",
        "message.type\n(human, tool, ai 구분)",
        "message.data.content ",
        "message.data.name",
        "message.data.usage_metadata.total_tokens",
        "message_at",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "run_id",
        "account_id",
        "marketplace_id",
        "analysis",
    ]

    with open(args.output, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_ALL,
            escapechar="\\",
            doublequote=True,
        )
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Exported {len(output_rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
