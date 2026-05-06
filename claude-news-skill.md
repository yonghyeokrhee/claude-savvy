# 신규 지식 검색 Skill — `/claude-news`

## 왜 이 Skill을 만드는가

Claude Code는 매주 새로운 명령·기능이 추가됩니다. 교재는 시간이 지나면 outdated 됩니다.
**해결책: 최신 정보를 직접 가져오는 Skill을 만들면, 교재가 늙지 않습니다.**

이 챕터에서 만드는 `/claude-news` Skill은:
- 공식 문서·릴리즈 노트·Anthropic 블로그를 한 번에 읽어
- 개발자 커뮤니티·경쟁사(Cursor, Codex, Aider 등) 동향까지 검색해
- "최근 N주 변경사항"을 표로 요약해 줍니다.

부수 효과: 본 강의에서 다룬 `/loop`, `/effort`, `/btw` 같은 명령이 실제 어떻게 등장했는지 학생이 직접 확인하게 됩니다.

---

## 1. 설계 — 4단계 파이프라인

```
[1] WebFetch  공식 docs           ──┐
[2] WebFetch  release notes        ─┤
[3] WebFetch  Anthropic news       ─┼──▶  병합 → 카테고리 태그 → 표 출력
[4] WebSearch 커뮤니티 + 경쟁사    ─┘
```

각 항목에 **소스 카테고리 배지**를 붙입니다: `[공식]` `[블로그]` `[커뮤니티]` `[경쟁사]`.

---

## 2. 디렉토리 구조

```
.claude/skills/claude-news/
├── SKILL.md
└── references/
    ├── sources.md         # 공식 URL 4개 + 검색 쿼리 패턴
    ├── competitors.md     # Cursor / Codex / Aider / Cline / Windsurf 모니터링 키워드
    └── format.md          # 출력 마크다운 템플릿 (카테고리 배지 포함)
```

**Progressive Disclosure** 적용: `references/*.md`는 SKILL.md에서 *언급*만 하고, 실제 내용은 호출 시점에만 읽습니다. 평소엔 컨텍스트를 점유하지 않음.

---

## 3. SKILL.md — 진입점

```markdown
---
name: claude-news
description: Claude Code의 최신 기능, 릴리즈 노트, 신규 명령어, 최근 업데이트, 변경 사항을 알려줘. AI 코딩 도구 동향(Cursor, Codex, Aider 등)도 함께 점검.
allowed-tools: WebFetch, WebSearch, Read
---

# /claude-news — 최근 N주 Claude Code 변경 요약

## 동작 순서

1. 인자 파싱: 키워드(예: `/claude-news loop`)가 있으면 해당 키워드 필터로 좁힘. 없으면 최근 4주 전체.
2. `references/sources.md` 를 읽어 공식 URL과 쿼리 패턴 확보.
3. **병렬 수집**:
   - WebFetch: docs.claude.com/en/docs/claude-code
   - WebFetch: docs.claude.com/en/release-notes/claude-code
   - WebFetch: www.anthropic.com/news
   - WebSearch: Reddit r/ClaudeAI / Hacker News / dev.to / X — `"Claude Code" 2026 release` 등
   - WebSearch: 경쟁사 — `references/competitors.md` 키워드별
4. 각 항목에 카테고리 배지 부여: `[공식]` `[블로그]` `[커뮤니티]` `[경쟁사]`
5. `references/format.md` 템플릿대로 표 출력. 항목별 한 줄 요약 + 링크 + (해당되면) "교재 보강 필요" 표시.
6. 마지막에 **다음 행동 제안**: 보강해야 할 GitBook 페이지 후보 1~3개.

## 출력 예시

| 날짜 | 카테고리 | 항목 | 한 줄 요약 | 링크 |
|---|---|---|---|---|
| 2026-04-13 | [공식] | `/effort xhigh` | Opus 4.7 추론 강도 다이얼 | … |
| 2026-04-20 | [공식] | `/ultrareview` | 클라우드 멀티 에이전트 리뷰 | … |
| 2026-05-01 | [경쟁사] | Cursor 0.50 | 멀티 파일 동시 편집 모드 | … |

## 주의

- 4주 이상 결과가 누적되면 자동으로 최신순 상위 20개로 자릅니다.
- 출처가 비공식(커뮤니티/경쟁사)이면 "검증 필요" 라벨을 붙입니다.
- 동일 항목이 공식+커뮤니티 양쪽에 있으면 공식 링크 우선.
```

---

## 4. `references/sources.md`

```markdown
# 데이터 소스

## 공식 (WebFetch — 항상 우선)
- https://docs.claude.com/en/docs/claude-code
- https://docs.claude.com/en/release-notes/claude-code
- https://www.anthropic.com/news

## 커뮤니티 (WebSearch — 보조)
- 쿼리: `"Claude Code" 2026 release site:reddit.com`
- 쿼리: `"Claude Code" new feature site:news.ycombinator.com`
- 쿼리: `Claude Code update 2026 site:dev.to`
- 쿼리: `"Claude Code" site:x.com OR site:twitter.com`

## 경쟁사·대안 도구 (WebSearch)
- 쿼리: `Cursor release notes 2026`
- 쿼리: `OpenAI Codex agent feature 2026`
- 쿼리: `Aider new release 2026`
- 쿼리: `Cline release 2026`
- 쿼리: `Windsurf changelog 2026`

## 갱신 주기 메모
- 공식 docs: 매주 변경
- 릴리즈 노트: 화요일 전후
- 커뮤니티: 새로운 기능 공개 후 24시간 이내 토론 활발
```

---

## 5. `references/competitors.md`

```markdown
# 경쟁/대안 코딩 에이전트 모니터링

| 도구 | 비교 포인트 | 키워드 |
|---|---|---|
| Cursor | IDE 통합, 멀티파일 편집 | `Cursor 0.x release`, `Cursor agent mode` |
| OpenAI Codex / ChatGPT agents | 에이전트 모드, 코드 실행 | `OpenAI Codex feature`, `ChatGPT agent coding` |
| Aider | 터미널 워크플로우 | `Aider 0.x changelog`, `Aider git integration` |
| Cline (이전 Claude Dev) | VS Code 확장 | `Cline release`, `Cline new model` |
| Windsurf | Cascade 기능 | `Windsurf Cascade update` |
| Devin / Cognition | 자율 에이전트 | `Devin feature 2026` |

## 비교 출력 템플릿
"Claude Code 의 X에 대응하는 <도구>의 Y는 …" 형태로 1줄.
```

---

## 6. `references/format.md`

```markdown
# 출력 마크다운 템플릿

## 헤더
> 🔔 Claude Code 최근 4주 동향 ({YYYY-MM-DD} 기준)

## 본문 표
| 날짜 | 카테고리 | 항목 | 한 줄 요약 | 링크 |
|---|---|---|---|---|

## 카테고리 배지
- `[공식]` — docs.claude.com / anthropic.com
- `[블로그]` — Anthropic news, 공식 미디엄
- `[커뮤니티]` — Reddit, HN, dev.to, X
- `[경쟁사]` — Cursor, Codex, Aider 등

## 푸터
> 다음 보강 후보:
> - <gitbook-페이지>.md — 신규 명령 X, Y 추가
```

---

## 7. 강의 시나리오 — 라이브 시연 4분

1. **만들기 (1분)** — 위 4개 파일을 그대로 복사해 `.claude/skills/claude-news/`에 저장
2. **실행 (1분)** — 새 세션에서 `/claude-news` 입력. 표 출력 확인
3. **필터링 (1분)** — `/claude-news loop` 으로 좁혀 호출. `/loop` 등장 시점 확인
4. **응용 (1분)** — `/claude-news Cursor` 로 경쟁사 동향만 보기

---

## 8. 학생 응용 과제

본인 도메인의 "신규 정보를 가져오는 Skill"을 동일 패턴으로 만들기:
- 마케터: `/marketing-news` — Google Ads / Meta Ads 신기능
- 데이터 엔지니어: `/data-news` — dbt / Snowflake / DuckDB 릴리즈
- 백엔드: `/backend-news` — FastAPI / Bun / Deno 변경사항

핵심은 **WebFetch(공식) + WebSearch(커뮤니티) + references 분리** 라는 3박자.

---

## 정리

- `/claude-news`는 교재가 늙는 문제를 학생이 스스로 푸는 도구입니다.
- 4개 데이터 소스를 카테고리 배지로 구분해 신뢰도를 표시합니다.
- Progressive Disclosure 로 평소 컨텍스트는 가볍게 유지합니다.
- 동일 패턴을 본인 도메인에 응용하면, 어떤 분야든 "최신 동향 Skill" 한 개를 가지게 됩니다.
