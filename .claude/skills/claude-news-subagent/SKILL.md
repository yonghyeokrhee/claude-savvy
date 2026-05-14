---
name: claude-news-subagent
description: Claude Code 최신 동향을 Sub-Agent 4개로 병렬 수집·정리합니다. /claude-news의 Sub-Agent 확장 버전 — 컨텍스트 격리 + 진짜 병렬 수집.
allowed-tools: Agent, Read, Write
---

# /claude-news-subagent — Sub-Agent 병렬 수집판

기존 `/claude-news` 는 메인 Claude가 WebFetch/WebSearch를 모두 직접 호출합니다.
이 스킬은 **수집을 4개 Sub-Agent에게 위임**하고, 메인 Claude는 통합·표 작성만 담당합니다.

## 인자

`/claude-news-subagent` — 최근 4주 전체
`/claude-news-subagent <키워드>` — 키워드 필터 (예: `/claude-news-subagent loop`)

## 동작 순서

1. 인자 파싱. 키워드가 있으면 4개 Sub-Agent에게도 동일 키워드 전달.
2. `../claude-news/references/sources.md`, `../claude-news/references/competitors.md`,
   `../claude-news/references/format.md` 를 메인 Claude가 먼저 읽음
   (Sub-Agent 프롬프트에 핵심 URL을 직접 박아 넣기 위해).
3. **4개 Sub-Agent를 동시에 실행** (단일 메시지에 Agent 도구 4번 병렬 호출):

   - 🔵 **Agent 1 — official-docs-scout** (subagent_type: `general-purpose`)
     - WebFetch: `https://docs.claude.com/en/release-notes/claude-code`
     - WebFetch: `https://docs.claude.com/en/docs/claude-code`
     - 리다이렉트 발생 시 redirect URL을 한 번 더 fetch
     - 출력: 날짜·항목·요약·링크 형식 JSON 또는 표

   - 🟢 **Agent 2 — anthropic-news-scout** (subagent_type: `general-purpose`)
     - WebFetch: `https://www.anthropic.com/news`
     - 최근 4주 포스트만 추출 (날짜·제목·1줄 요약·링크)

   - 🟡 **Agent 3 — community-scout** (subagent_type: `general-purpose`)
     - WebSearch: `"Claude Code" 2026 release site:reddit.com`
     - WebSearch: `"Claude Code" new feature site:news.ycombinator.com`
     - WebSearch: `Claude Code update 2026 site:dev.to`
     - 각 결과를 `[커뮤니티]` 배지로 정리, `⚠ 검증 필요` 부착

   - 🟠 **Agent 4 — competitor-scout** (subagent_type: `general-purpose`)
     - WebSearch: `Cursor release notes 2026`
     - WebSearch: `OpenAI Codex agent feature 2026`
     - WebSearch: `Aider new release 2026`, `Cline release 2026`, `Windsurf changelog 2026`
     - 각 결과를 `[경쟁사]` 배지로 정리, `⚠ 검증 필요` 부착

4. 4개 Sub-Agent 결과 취합 후 메인 Claude가:
   - 동일 항목 중복 제거 (공식 > 블로그 > 커뮤니티 > 경쟁사 순)
   - `../claude-news/references/format.md` 템플릿대로 표 작성
   - 4주 결과가 20개 초과면 최신순 상위 20개로 컷
5. 마지막에 **다음 행동 제안** 1~3개 (GitBook 페이지 보강 후보).

## Sub-Agent 호출 시 주의

- **반드시 단일 응답 안에서 4개 Agent를 한 번에 호출**해야 병렬 수집이 됩니다.
  순차 호출하면 `/claude-news`와 시간 차이가 없어 학습 효과가 사라집니다.
- 각 Sub-Agent 프롬프트는 자기 완결적으로 작성:
  필요한 URL, 출력 형식, "200단어 이내 보고"까지 명시.
- Sub-Agent 결과는 메인 컨텍스트에 한 번에 들어오므로,
  각 Agent에게 "원문 그대로 붙이지 말고 정리된 표만 반환"하도록 지시.

## 출력 예시

```
🔔 Claude Code 최근 4주 동향 (2026-05-14 기준) — Sub-Agent 4기 수집

| 날짜 | 카테고리 | 항목 | 요약 | 링크 |
|---|---|---|---|---|
| 2026-04-16 | [공식] | Opus 4.7 GA | SWE-bench 87.6%, xhigh 효력 | https://… |
| 2026-04-20 | [공식] | /ultrareview | 클라우드 멀티 에이전트 리뷰 | https://… |
| 2026-05-04 | [공식] | --plugin-url | 원격 URL에서 플러그인 로드 | https://… |
| 2026-05-11 | [경쟁사] | Cursor in MS Teams | @Cursor 멘션으로 PR 생성 ⚠ 검증 필요 | https://… |

🧭 수집 분담
- 🔵 official-docs-scout — 공식 docs/릴리즈 노트 12건
- 🟢 anthropic-news-scout — 블로그 5건
- 🟡 community-scout — Reddit/HN/dev.to 3건
- 🟠 competitor-scout — Cursor/Codex 4건

📌 다음 보강 후보
- advanced-commands.md — `/ultrareview`, `/effort xhigh` 섹션
- install-windows.md — "Git Bash 없이 PowerShell" 절 갱신
```

## `/claude-news` 와의 차이

| | `/claude-news` | `/claude-news-subagent` |
|---|---|---|
| `allowed-tools` | `WebFetch, WebSearch, Read` | `Agent, Read, Write` |
| 처리 주체 | 메인 Claude 1개 | 메인 + Sub-Agent 4개 |
| 병렬 대상 | 도구 호출 (WebFetch/WebSearch) | 전체 수집 워크플로우 |
| 메인 컨텍스트 | 모든 페이지 원문이 누적 | 각 Agent가 요약 → 메인은 깔끔 |
| 색상 표시 | 없음 | 🔵🟢🟡🟠 4색 |
| 적합한 상황 | 빠른 확인 | 폭넓은 출처, 컨텍스트 격리 필요 |

## 주의사항

- 4개 Agent를 반드시 **동시에** 호출 (단일 메시지의 multiple tool calls).
- Sub-Agent가 WebFetch 도메인 차단을 만나면 WebSearch로 자체 fallback 지시.
- 결과 0건이면 "최근 4주간 새 변경 없음" 명시.
- 사용자가 한국어로 호출하면 최종 출력도 한국어.

## 참고 파일

이 스킬은 기존 `claude-news` 스킬의 references를 그대로 활용합니다:
- `../claude-news/references/sources.md`
- `../claude-news/references/competitors.md`
- `../claude-news/references/format.md`

별도 references 폴더는 두지 않습니다 (단일 소스 원칙).
