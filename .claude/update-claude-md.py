#!/usr/bin/env python3
"""CLAUDE.md의 목차 섹션과 타임스탬프만 업데이트한다."""
import re
import sys

claude_md_path = sys.argv[1]
summary_path = sys.argv[2]
timestamp = sys.argv[3]

with open(claude_md_path, "r") as f:
    content = f.read()

with open(summary_path, "r") as f:
    summary_content = f.read()

# 타임스탬프 업데이트
content = re.sub(
    r'> 마지막 갱신: .+',
    f'> 마지막 갱신: {timestamp}',
    content
)

# 현재 목차 섹션만 교체
content = re.sub(
    r'(## 현재 목차 \(SUMMARY\.md\)\n\n```\n).*?(```)',
    lambda m: m.group(1) + summary_content.rstrip() + '\n' + m.group(2),
    content,
    flags=re.DOTALL
)

with open(claude_md_path, "w") as f:
    f.write(content)
