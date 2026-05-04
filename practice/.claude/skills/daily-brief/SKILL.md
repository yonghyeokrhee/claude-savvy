---
name: daily-brief
description: 오늘의 git 커밋, 내게 할당된 Linear 이슈, 어제 작성한 Notion 데일리 저널을 한 번에 묶어 오늘자 데일리 저널 페이지를 Notion에 생성합니다. "오늘 뭐했지", "데일리 브리프", "스탠드업 정리" 같은 요청에 자동 트리거됩니다.
allowed-tools: Bash, mcp__plugin_linear_linear__list_issues, mcp__notion__notion-search, mcp__notion__notion-create-pages, mcp__notion__notion-fetch
---

# Daily Brief

매일 아침(또는 퇴근 직전) **단 한 번의 호출**로 다음을 수행합니다.

1. **Git 컨텍스트 수집** — 현재 작업 디렉토리에서 지난 24h 동안의 내 커밋과 미커밋 변경사항을 요약
2. **Linear 컨텍스트 수집** — 내게 할당된 활성 이슈(Backlog/Todo/In Progress) 목록
3. **어제 저널 회상** — Notion에서 어제 날짜의 데일리 저널 페이지를 찾아 "어제 할 일" 항목을 가져옴
4. **합성 → 적재** — 위 3개 입력을 종합해 오늘자 데일리 저널 페이지를 Notion `Daily Journal` DB에 생성

## 실행 절차

### Step 1. Git 컨텍스트

```bash
git log --author="$(git config user.email)" --since="24 hours ago" --pretty=format:"- %s (%h)"
git status --short
```

빈 결과여도 진행합니다 (그 자체가 "코드 작업이 없었던 날"이라는 신호).

### Step 2. Linear 컨텍스트

```
mcp__plugin_linear_linear__list_issues
  assignee: "me"
  state: "Backlog,Todo,In Progress"
  limit: 50
  orderBy: "updatedAt"
```

### Step 3. 어제 저널 검색

오늘 날짜를 `YYYY-MM-DD`로 계산하고, `어제 = 오늘 - 1일`을 검색어로 사용:

```
mcp__notion__notion-search
  query: "Daily Journal {{어제 날짜}}"
  query_type: "internal"
  page_size: 3
  filters: {}
```

찾은 페이지를 `notion-fetch`로 읽어 "오늘 할 일" 섹션만 추출합니다. 없으면 빈 리스트로 처리.

### Step 4. 오늘 저널 생성

`Daily Journal` DB의 `data_source_id`를 모르면 먼저 한 번 검색해 캐시 안내를 출력하고 사용자에게 ID를 물어보세요. ID가 확보되면:

```
mcp__notion__notion-create-pages
  parent: { type: "data_source_id", data_source_id: "<DB id>" }
  pages: [{
    properties: {
      "Title": "Daily Brief — {{오늘 날짜}}",
      "date:Date:start": "{{오늘 날짜}}"
    },
    content: <아래 템플릿>
  }]
```

### 본문 템플릿 (Markdown)

```markdown
## 어제 한 일 (Git)
{{git log 24h 결과를 그대로}}

## 진행 중 (Linear)
{{내게 할당된 이슈를 `- [PRJ-123] 제목 (상태)` 형식으로}}

## 오늘 할 일
{{어제 저널에서 가져온 항목 + Linear 우선순위 High 이상 + 미커밋 변경사항 기반 제안}}

## 메모
- 자동 생성: `/daily-brief`
```

## 동작 원칙

- **읽기 → 합성 → 한 번의 쓰기**. 중간 산출물을 따로 저장하지 않고, Notion에 만든 페이지가 유일한 출력입니다.
- **멱등성**: 같은 날 두 번 실행되면 새 페이지를 만들기 전에 `notion-search`로 오늘자 페이지가 있는지 확인하고, 있으면 사용자에게 "덮어쓸까요 / 추가 섹션을 붙일까요"를 물어봅니다.
- **빈 입력 허용**: git/Linear/어제 저널 중 어느 하나가 비어도 실행을 계속합니다 — 빈 섹션은 `_없음_`으로 채웁니다.
- **민감 정보**: 커밋 메시지에 토큰/이메일이 보이면 마스킹한 뒤 Notion에 올립니다.

## 트러블슈팅

| 증상 | 원인 | 조치 |
| --- | --- | --- |
| `list_issues`가 빈 배열 | Linear MCP 미인증 | `/mcp`로 상태 확인 |
| `notion-create-pages` 실패 (`property not found`) | Daily Journal DB 스키마와 키가 다름 | `notion-fetch`로 스키마 확인 후 properties 키 보정 |
| 같은 날짜 페이지 중복 생성 | 멱등성 체크 누락 | 실행 전 `notion-search query="Daily Brief {{오늘}}"` 먼저 호출 |

## 확장

- `/loop 24h /daily-brief` — 매일 자동 실행
- 부모 프로젝트 `CLAUDE.md`에 `data_source_id`를 적어두면 Step 4의 사용자 질문을 생략
- 조직 단위로 쓸 때는 `assignee: "me"` 대신 사용자 ID 매트릭스를 받아 팀 브리프로 확장
