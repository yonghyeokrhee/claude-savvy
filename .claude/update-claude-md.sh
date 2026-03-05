#!/bin/bash
# GitBook 구조가 변경될 때 claude.md를 자동으로 갱신한다.
# 트리거: SUMMARY.md 가 Write/Edit 될 때만 실행

INPUT_JSON=$(cat)
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_MD="$PROJECT_DIR/claude.md"
SUMMARY="$PROJECT_DIR/SUMMARY.md"

# SUMMARY.md가 없으면 종료
[ -f "$SUMMARY" ] || exit 0

# 변경된 파일이 SUMMARY.md가 아니면 종료
CHANGED_FILE=$(echo "$INPUT_JSON" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)
if [ "$(basename "$CHANGED_FILE")" != "SUMMARY.md" ]; then
  exit 0
fi

# SUMMARY.md 내용으로 CLAUDE.md의 목차 섹션만 교체
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
python3 "$PROJECT_DIR/.claude/update-claude-md.py" "$CLAUDE_MD" "$SUMMARY" "$TIMESTAMP"

echo "[hook] claude.md 갱신 완료 ($(date '+%H:%M:%S'))"
