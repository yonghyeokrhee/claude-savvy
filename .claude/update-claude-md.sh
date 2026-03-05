#!/bin/bash
# GitBook 구조가 변경될 때 claude.md를 자동으로 갱신한다.
# 트리거: SUMMARY.md 또는 *.md 파일이 Write/Edit 될 때

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_MD="$PROJECT_DIR/claude.md"
SUMMARY="$PROJECT_DIR/SUMMARY.md"

# SUMMARY.md가 없으면 종료
[ -f "$SUMMARY" ] || exit 0

# 현재 SUMMARY.md 내용
SUMMARY_CONTENT=$(cat "$SUMMARY")

# 루트 레벨 .md 파일 목록 (claude.md, agents.md symlink 제외)
FILES=$(cd "$PROJECT_DIR" && ls -1 *.md 2>/dev/null | grep -v '^claude\.md$' | sort | tr '\n' ' ')

# practice/ 하위 파일 목록
PRACTICE_FILES=$(cd "$PROJECT_DIR" && find practice -name "*.md" 2>/dev/null | sort | tr '\n' ' ')

cat > "$CLAUDE_MD" << EOF
# GitBook 프로젝트 — Claude 컨텍스트

> 이 파일은 SUMMARY.md 또는 .md 파일 변경 시 자동으로 갱신됩니다.
> 마지막 갱신: $(date '+%Y-%m-%d %H:%M:%S')

## 프로젝트 개요

GitHub 연동 GitBook 기반 **Claude Code 한글 강의 교재** 프로젝트.
- 저장소: github.com/yonghyeokrhee/claude-savvy
- GitBook과 GitHub main 브랜치가 실시간 동기화됨

## 작성 규칙

- 모든 문서는 **한글**로 작성
- 새 페이지 추가 시 반드시 \`SUMMARY.md\`에 등록
- 파일명은 kebab-case 사용 (예: \`core-concepts.md\`)
- \`claude.md\`는 자동 생성 파일 — 직접 수정 금지
- \`agents.md\`는 \`claude.md\`의 symlink

## 현재 목차 (SUMMARY.md)

\`\`\`
$SUMMARY_CONTENT
\`\`\`

## 루트 페이지 파일

$FILES

## practice/ 실습 파일

${PRACTICE_FILES:-없음}

## 주요 명령

\`\`\`bash
# 변경사항 푸시 (GitBook 자동 반영)
git push origin main

# 로컬 상태 확인
git status
\`\`\`
EOF

echo "[hook] claude.md 갱신 완료 ($(date '+%H:%M:%S'))"
