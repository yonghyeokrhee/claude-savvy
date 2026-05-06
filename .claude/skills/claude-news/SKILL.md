---
name: claude-news
description: Claude Code의 최신 기능, 릴리즈 노트, 신규 명령어, 최근 업데이트, 변경 사항을 알려줘. AI 코딩 도구 동향(Cursor, Codex, Aider 등)도 함께 점검.
allowed-tools: WebFetch, WebSearch, Read
---

# /claude-news — 최근 N주 Claude Code 변경 요약

## 인자

`/claude-news` — 최근 4주 전체
`/claude-news <키워드>` — 키워드 필터 (예: `/claude-news loop`, `/claude-news Cursor`)

## 동작 순서

1. 인자 파싱. 키워드가 있으면 모든 결과를 해당 키워드로 후필터링.
2. `references/sources.md` 를 읽어 공식 URL과 커뮤니티 쿼리 패턴을 확보.
3. **병렬 수집** (가능하면 동시에):
   - WebFetch: `https://docs.claude.com/en/docs/claude-code`
   - WebFetch: `https://docs.claude.com/en/release-notes/claude-code`
   - WebFetch: `https://www.anthropic.com/news`
   - WebSearch: Reddit / HN / dev.to / X — `"Claude Code" 2026 release` 등
   - WebSearch: 경쟁사 — `references/competitors.md`의 키워드별 (필요 시 읽기)
4. 각 항목에 카테고리 배지 부여:
   - `[공식]` — docs.claude.com / anthropic.com 도메인
   - `[블로그]` — anthropic.com/news 의 포스트
   - `[커뮤니티]` — Reddit / HN / dev.to / X / 블로그 게시글
   - `[경쟁사]` — Cursor / Codex / Aider / Cline / Windsurf 관련
5. `references/format.md` 템플릿대로 표 출력. 항목별:
   - 날짜 (YYYY-MM-DD)
   - 카테고리 배지
   - 항목명 (예: `/effort`, "Computer Use on CLI")
   - 한 줄 요약 (40자 이내)
   - 링크
6. **검증 필요 라벨**: 비공식 출처(커뮤니티/경쟁사)면 항목 끝에 `⚠ 검증 필요` 표시.
7. **중복 제거**: 동일 기능이 공식+커뮤니티 양쪽에 있으면 공식 우선, 커뮤니티는 합치기.
8. **상위 N개로 자르기**: 4주 결과가 20개 이상이면 최신순 상위 20개만.
9. 마지막에 **다음 행동 제안**: 보강해야 할 GitBook 페이지 후보 1~3개 (예: "advanced-commands.md 에 `/X` 섹션 추가").

## 출력 예시

```
🔔 Claude Code 최근 4주 동향 (2026-05-06 기준)

| 날짜 | 카테고리 | 항목 | 요약 | 링크 |
|---|---|---|---|---|
| 2026-04-13 | [공식] | /effort xhigh | Opus 4.7 추론 강도 다이얼 | https://… |
| 2026-04-20 | [공식] | /ultrareview | 클라우드 멀티 에이전트 리뷰 | https://… |
| 2026-05-01 | [경쟁사] | Cursor 0.50 | 멀티 파일 동시 편집 ⚠ 검증 필요 | https://… |

📌 다음 보강 후보
- advanced-commands.md — `/effort`, `/ultrareview` 섹션 보강
- 신규 페이지 — 컴퓨터 사용(Computer Use) 별도 챕터
```

## 주의사항

- WebFetch는 도메인 차단으로 실패할 수 있다. 실패 시 WebSearch로 fallback.
- 결과가 빈 경우 "최근 4주간 새 변경 없음" 명시.
- 사용자가 한국어로 호출했으면 출력도 한국어로.

## 참고 파일

- `references/sources.md` — URL 및 검색 쿼리 전체 목록
- `references/competitors.md` — 경쟁/대안 도구 모니터링 키워드
- `references/format.md` — 마크다운 출력 템플릿
