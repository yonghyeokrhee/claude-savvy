# Sub-Agent로 Skill 확장하기 — `/claude-news` → `/claude-news-subagent`

이미 만들어진 `/claude-news` Skill을 가지고, **Sub-Agent를 끼워 넣어 병렬 수집판으로 확장**하는 실습입니다.

> 선행 학습: [신규 지식 검색 Skill — /claude-news](../claude-news-skill.md), [Sub-Agent + Skill 활용](sub-agent-skill.md)

---

## 왜 이 실습인가

뉴스·릴리즈 노트 수집은 다음과 같은 특성이 있습니다.

- **출처가 독립적**: 공식 docs, 블로그, Reddit/HN, 경쟁사 changelog — 서로 의존하지 않음
- **읽을 양이 큼**: WebFetch 한 번에 페이지 전체가 메인 컨텍스트에 들어옴
- **시간이 오래 걸림**: 4개 출처를 순차로 돌면 1분 이상

이 세 가지는 Sub-Agent가 가장 잘 푸는 문제입니다. **독립 작업 × 큰 결과물 × 병렬 가능** — 메인 Claude가 직접 하는 대신 Sub-Agent에게 "수집해서 요약만 돌려줘"라고 시키면 됩니다.

---

## Before — `/claude-news` (기존)

### 구조

```
/claude-news 입력
    ↓
SKILL.md 로드
    ↓
메인 Claude가 직접:
    ├── WebFetch: docs.claude.com/release-notes
    ├── WebFetch: anthropic.com/news
    ├── WebSearch: Reddit/HN
    └── WebSearch: Cursor/Codex
         ↓
    표 작성 → 출력
```

### `allowed-tools`

```yaml
allowed-tools: WebFetch, WebSearch, Read
```

### 한계

- WebFetch 결과(페이지 전체 마크다운)가 **메인 컨텍스트에 누적**됨
- 도구 호출은 병렬로 묶을 수 있지만, 결과 파싱·중복 제거는 메인이 한 컨텍스트에서 처리
- 출처가 늘면 비례해서 메인 컨텍스트가 무거워짐

---

## After — `/claude-news-subagent` (확장)

### 구조

```
/claude-news-subagent 입력
    ↓
SKILL.md 로드
    ↓
references/* 파일을 메인이 먼저 읽음
    ↓
메인 Claude가 Agent 도구를 4번 동시 호출
    ├── 🔵 official-docs-scout    → docs.claude.com 2개 페이지 수집
    ├── 🟢 anthropic-news-scout   → anthropic.com/news 4주치 추출
    ├── 🟡 community-scout        → Reddit/HN/dev.to 검색
    └── 🟠 competitor-scout       → Cursor/Codex/Aider/Cline 검색
         ↓
    각 Agent가 정리된 표 반환 (원문은 안 보냄)
         ↓
    메인 Claude가 중복 제거 + 최종 표 + 다음 행동 제안
```

### `allowed-tools`

```yaml
allowed-tools: Agent, Read, Write
```

> WebFetch·WebSearch는 메인이 직접 안 씁니다. Sub-Agent가 알아서 자기 도구를 호출.

### 핵심 한 줄

> **수집은 Sub-Agent, 통합은 메인.** 메인 Claude는 4개 요약본만 보고 합치므로 컨텍스트가 깔끔합니다.

---

## 두 스킬 비교

| | `/claude-news` | `/claude-news-subagent` |
|---|---|---|
| `allowed-tools` | `WebFetch, WebSearch, Read` | `Agent, Read, Write` |
| 처리 주체 | 메인 Claude 1개 | 메인 + Sub-Agent 4개 |
| 병렬 대상 | 도구 호출 | 전체 수집 워크플로우 |
| 메인 컨텍스트에 들어오는 것 | 페이지 원문 전체 | 정리된 표 4개 |
| 색상 표시 | 없음 | 🔵🟢🟡🟠 |
| 새 출처 추가 비용 | 메인 프롬프트 늘어남 | Sub-Agent 1개 추가 |
| 적합한 상황 | 가볍게 한 번 보기 | 정기 모니터링, 출처 다양 |

---

## 실습 순서

### 1단계 — 두 스킬 모두 등록 확인

```bash
ls -la .claude/skills/claude-news/SKILL.md
ls -la .claude/skills/claude-news-subagent/SKILL.md
```

둘 다 존재해야 합니다. `claude-news-subagent`는 `claude-news`의 `references/`를 공유 참조합니다.

### 2단계 — 기존 `/claude-news` 실행

```
/claude-news
```

관찰 포인트:
- WebFetch / WebSearch 호출이 **메인 Claude 라인**에서만 보임
- 좌측 패널에 Sub-Agent가 안 뜸
- 페이지 원문이 메인 컨텍스트에 들어와 있음 (이후 대화에 영향)

### 3단계 — 신규 `/claude-news-subagent` 실행

```
/claude-news-subagent
```

관찰 포인트:
- 좌측 패널에 **4개 Sub-Agent가 동시에** 다른 색상으로 뜸
- 각 Sub-Agent가 자기 WebFetch/WebSearch를 호출
- 메인 Claude는 마지막에 표만 그림
- 같은 출력을 만들지만 메인 컨텍스트가 훨씬 가벼움

### 4단계 — 출력 비교

두 결과를 나란히 놓고:

- 항목 수 / 카테고리 분포가 유사한지
- `[커뮤니티]`·`[경쟁사]` 항목이 `/claude-news-subagent`에서 더 풍부한지
- "다음 행동 제안" 품질 차이

### 5단계 — 키워드 필터 테스트

```
/claude-news-subagent loop
/claude-news loop
```

같은 키워드로 두 스킬을 실행. Sub-Agent 버전은 각 Agent가 키워드를 받아 자기 영역에서 필터링하므로 누락이 더 적습니다.

---

## Sub-Agent로 확장할 때 체크리스트

이 실습 패턴을 다른 Skill에 적용할 때 동일하게 쓸 수 있습니다.

1. **출처/하위 작업이 독립적인가?** — 의존이 있으면 병렬 안 됨
2. **각 작업의 결과물이 큰가?** — 작으면 굳이 Sub-Agent 쓸 필요 없음
3. **`allowed-tools`에 `Agent` 추가했는가?**
4. **Sub-Agent 프롬프트가 자기 완결적인가?** — 메인 컨텍스트를 모름
5. **"단일 메시지에서 동시 호출"을 SKILL.md에 명시했는가?**
6. **각 Sub-Agent에게 "요약본만 반환"을 강제했는가?** — 원문이 돌아오면 컨텍스트 격리 효과 없음

---

## 정리

| 단계 | 한 것 |
|---|---|
| 기존 `/claude-news` | 메인이 WebFetch/WebSearch 직접 호출 — 컨텍스트 비대 |
| 신규 `/claude-news-subagent` | `Agent` 권한 추가 + 4개 Scout 동시 호출 — 컨텍스트 격리 |
| 핵심 변경 | `allowed-tools`에 `Agent` 추가 + 작업을 4개 Scout으로 분리 |
| 학습 포인트 | 이미 있는 Skill도 한 줄 + 프롬프트 분리로 Sub-Agent 패턴으로 확장 가능 |

Sub-Agent는 처음부터 설계할 때만 쓰는 게 아닙니다. **기존 Skill에 출처가 늘어나거나 컨텍스트가 무거워질 때, `allowed-tools`에 `Agent`를 추가하고 워크플로우를 쪼개는 것만으로 자연스럽게 확장**됩니다.
