# 흥미로운 Skill 만들기 — `/daily-brief` 예제 (2026 기준)

> 기존 강의 페이지의 Skill 예제는 "프롬프트 단축키" 또는 "DB 연결" 수준에 머물러 있었습니다.
> 2026년 현재 Claude Code는 **MCP 멀티서버 + 자동 트리거 + 권한 화이트리스트**가 기본이라, Skill 하나가 여러 외부 시스템을 묶는 작은 워크플로우 엔진처럼 동작합니다.
> 이 페이지는 그 변화를 보여주는 실전 예제 한 개를 새로 만들어 봅니다.

## 무엇이 달라졌나

| 시기 | 대표적인 Skill 모습 |
| --- | --- |
| 2025 초 | "긴 프롬프트를 `/foo` 한 줄로 호출" — 단순 프롬프트 매크로 |
| 2025 중 | 외부 스크립트 + `allowed-tools`로 Bash 권한 부여 (e.g. `connect-rds-python`) |
| **2026 현재** | **MCP 도구**를 직접 화이트리스트에 올려 Linear/Notion/GitHub 같은 **여러 SaaS를 한 Skill에서 오케스트레이션** + `description` 기반 자동 트리거 + `/loop`/`/schedule`과 결합한 일상 자동화 |

핵심 차이는 두 가지입니다.

1. **`allowed-tools`에 MCP 도구 이름을 직접 적을 수 있다.** `mcp__plugin_linear_linear__list_issues` 같은 풀 네임을 등록하면, 해당 Skill은 그 도구만 부를 수 있게 격리됩니다.
2. **`description`이 강력해졌다.** 사용자가 `/daily-brief`를 외우지 않아도, "오늘 뭐 했지" 같은 질문에 Claude가 description을 보고 자동으로 발동합니다.

## 예제 시나리오 — `/daily-brief`

> "오늘 한 일과 할 일을 직접 정리하지 않아도, Claude가 git/Linear/어제 저널을 모아 Notion에 데일리 페이지를 만들어 둔다."

이게 흥미로운 이유:

- **3개의 출처**(로컬 git, Linear MCP, Notion MCP)를 **한 번의 호출**로 묶는다.
- **읽기-쓰기 비대칭**: 여러 곳에서 읽지만 결과는 Notion 한 곳에만 쓴다 → 결과를 사람이 한 화면에서 본다.
- **멱등성**을 강제한다 — 같은 날 두 번 실행되어도 페이지가 중복되지 않는다.
- **자동화 친화적** — `/loop 24h /daily-brief`로 매일 아침 자동 실행할 수 있다.

### 폴더 구조

```
.claude/skills/daily-brief/
└── SKILL.md
```

코드 한 줄 없이 `SKILL.md` 하나로 동작합니다 — 외부 도구 호출은 모두 MCP가 담당하기 때문입니다.

### Frontmatter 핵심

```yaml
---
name: daily-brief
description: 오늘의 git 커밋, 내게 할당된 Linear 이슈, 어제 작성한 Notion 데일리 저널을 한 번에 묶어 오늘자 데일리 저널 페이지를 Notion에 생성합니다. "오늘 뭐했지", "데일리 브리프", "스탠드업 정리" 같은 요청에 자동 트리거됩니다.
allowed-tools: Bash, mcp__plugin_linear_linear__list_issues, mcp__notion__notion-search, mcp__notion__notion-create-pages, mcp__notion__notion-fetch
---
```

- `description`에 **자연어 트리거 후보**("오늘 뭐했지", "스탠드업 정리")를 넣어두면 자동 발동 정확도가 올라갑니다.
- `allowed-tools`에 **필요한 MCP 도구만** 명시 — 의도치 않은 페이지 삭제, 이슈 변경을 원천 차단합니다.

### 본문 — "읽기 → 합성 → 한 번의 쓰기"

본문은 4단계로 짧게 구성합니다.

```
1) git log 24h + git status
2) Linear list_issues (assignee=me, 활성 상태만)
3) Notion에서 어제 날짜의 Daily Journal 페이지를 검색·읽기
4) 위 3개를 합쳐 오늘자 Daily Journal 페이지를 한 개 생성
```

각 단계의 입력이 비어 있어도 멈추지 말고 빈 섹션(`_없음_`)으로 채우라고 명시해 두는 게 중요합니다 — 그래야 "코드를 안 짠 날", "휴가 다음 날"에도 깔끔하게 동작합니다.

전체 SKILL.md는 레포의 [`practice/.claude/skills/daily-brief/SKILL.md`](https://github.com/yonghyeokrhee/claude-savvy/blob/main/practice/.claude/skills/daily-brief/SKILL.md)에서 확인할 수 있습니다.

## 만들면서 배우는 4가지 패턴

### 1) MCP 도구를 `allowed-tools`로 격리

```yaml
allowed-tools: mcp__plugin_linear_linear__list_issues, mcp__notion__notion-create-pages
```

이 Skill은 절대로 Linear 이슈를 수정하거나 Notion 페이지를 삭제할 수 없습니다. **권한을 코드가 아닌 메타데이터로 제한**하는 것이 2026 패턴의 핵심입니다.

### 2) 자연어 트리거 (`description` 디자인)

좋은 description = 그대로 사용자 발화로 옮겨 적어도 어색하지 않은 문장 + 트리거 후보 키워드.

> ❌ "데일리 브리핑을 만든다" — 너무 짧음, 발동 잘 안 됨
> ✅ "...`오늘 뭐했지`, `데일리 브리프`, `스탠드업 정리` 같은 요청에 자동 트리거됩니다."

### 3) 멱등성을 SKILL.md에 명문화

LLM이 같은 작업을 두 번 했을 때 부작용이 누적되지 않도록, "쓰기 전에 search → 있으면 사용자에게 분기 질문"을 본문에 박아 둡니다. 코드가 없는 Skill에서는 이게 유일한 방어선입니다.

### 4) 부모 `CLAUDE.md`와의 결합

DB ID, 팀 ID 같은 **환경별 상수**는 SKILL.md가 아니라 부모 `CLAUDE.md`에 적습니다. 그러면 같은 SKILL.md를 다른 워크스페이스에서도 그대로 재사용할 수 있습니다.

```markdown
<!-- CLAUDE.md -->
- Daily Journal DB data_source_id: `xxxxxxxx-xxxx-...`
- 내 Linear assignee 별칭: `me`
```

## 실행해 보기

```bash
# 처음 한 번
/mcp     # linear, notion 모두 connected 확인

# 호출
/daily-brief

# 또는 자동 트리거 — 그냥 물어보기
오늘 뭐했지 정리해줘
```

매일 자동으로 돌리고 싶다면:

```
/loop 24h /daily-brief
```

또는 cron 기반:

```
/schedule "0 9 * * *" /daily-brief
```

## 더 흥미롭게 확장하기

| 확장 | 방법 |
| --- | --- |
| **팀 단위 브리프** | `assignee=me` → 팀원 ID 배열로 바꾸고 사람별 섹션 생성 |
| **PR 자동 첨부** | `gh pr list --author @me --state merged --search "merged:>=yesterday"` 추가 |
| **회의 결정사항 합치기** | 클립보드 또는 특정 Notion 페이지에서 액션 아이템을 함께 끌어오기 |
| **Slack 발행** | 마지막 단계에 Slack MCP 추가 — 단, `allowed-tools`에 명시적으로 추가해야 함 |
| **회고 모드** | 주간/월간 모드 옵션 — `Daily Journal`을 7개/30개씩 모아 합성 |

## 정리

2026년의 Skill은 더 이상 "긴 프롬프트의 단축키"가 아닙니다. **MCP 도구 호출을 권한 단위로 묶고, 자연어 트리거로 발동되며, `/loop`·`/schedule`로 일상에 끼어드는 작은 워크플로우 엔진**입니다. `/daily-brief`는 그중 가장 작고 흔한 형태이지만, 같은 패턴으로 코드 리뷰 큐레이터·고객 지원 일일 다이제스트·운영 인시던트 보드 등 임팩트 큰 자동화로 그대로 확장됩니다.
