# MCP 실습 — Linear 이슈를 Notion DB로 옮기기

> 두 개의 MCP 서버(Linear, Notion)를 동시에 사용해 한쪽 시스템의 데이터를 다른 쪽으로 옮기는 실습.
> 교육 목적이며, 한 번의 일회성 마이그레이션 시나리오를 다룹니다.

## 시나리오

- **출발지**: Linear 워크스페이스의 `codex-hackathon` 팀 이슈
- **도착지**: Notion 워크스페이스에 새로 만든 데이터베이스 — `Linear Issues — codex-hackathon`
- **목적**: Linear 이슈를 Notion DB로 미러링해 비개발자 팀원도 열람·필터링할 수 있게 한다

## 사전 준비

`/mcp` 명령으로 두 서버가 모두 인증되어 있어야 합니다.

```
/mcp
> linear: connected
> notion: connected
```

## 단계별 실행

### 1) 양쪽 워크스페이스 구조 확인

먼저 어느 팀의 이슈를 옮길지, Notion에 어떤 부모 페이지가 있는지 확인합니다.

```
linear: list_teams
notion: get_teams
```

이번 실습에서 Linear에는 `codex-hackathon`, `Lgcns` 두 팀이 있었고, Notion에는 별도 teamspace가 없어 워크스페이스 루트(private)에 DB를 만들기로 결정했습니다.

### 2) Linear 이슈 가져오기

```
linear: list_issues team="codex-hackathon" limit=250
```

이슈가 1건 — `COD-7 Keyword rank monitoring missing hourly data for 3+ hours` — 으로 확인됐습니다.
이슈 본문은 `list_issues`가 잘라서 반환하므로, 본문 전체가 필요한 경우 `get_issue`로 한 번 더 가져옵니다.

```
linear: get_issue id="COD-7"
```

### 3) Notion 데이터베이스 스키마 설계

Linear 이슈의 핵심 필드를 Notion 컬럼으로 매핑합니다.

| Linear 필드 | Notion 컬럼 | 타입 |
| --- | --- | --- |
| `title` | Title | `TITLE` |
| `id` (e.g. COD-7) | Identifier | `RICH_TEXT` |
| `status` | Status | `SELECT` |
| `priority.name` | Priority | `SELECT` |
| `labels` | Labels | `MULTI_SELECT` |
| `team` | Team | `RICH_TEXT` |
| `assignee` | Assignee | `RICH_TEXT` |
| `createdBy` | Created By | `RICH_TEXT` |
| `url` | Linear URL | `URL` |
| `createdAt` | Created At | `DATE` |
| `updatedAt` | Updated At | `DATE` |

Notion DDL은 다음과 같습니다.

```sql
CREATE TABLE (
  "Title" TITLE,
  "Identifier" RICH_TEXT,
  "Status" SELECT('Backlog':gray, 'Todo':blue, 'In Progress':yellow, 'Done':green, 'Canceled':red),
  "Priority" SELECT('Urgent':red, 'High':orange, 'Normal':blue, 'Low':gray, 'None':default),
  "Labels" MULTI_SELECT('Bug':red, 'Feature':blue, 'Improvement':green),
  "Team" RICH_TEXT,
  "Assignee" RICH_TEXT,
  "Created By" RICH_TEXT,
  "Linear URL" URL,
  "Created At" DATE,
  "Updated At" DATE
)
```

`notion: create_database`로 생성하면 응답에 `data_source_id`가 함께 돌아옵니다. 이후 페이지를 만들 때 이 ID를 부모로 지정합니다.

### 4) 이슈를 Notion 페이지로 변환해 일괄 생성

각 Linear 이슈를 한 개의 Notion 페이지로 변환합니다. 본문(`description`)은 페이지 컨텐츠에 Markdown으로 넣고, 메타데이터는 `properties`로 넣습니다.

```
notion: create_pages
  parent = { type: "data_source_id", data_source_id: "<생성한 DB의 data source id>" }
  pages = [
    {
      properties: {
        "Title": "Keyword rank monitoring missing hourly data for 3+ hours",
        "Identifier": "COD-7",
        "Status": "Backlog",
        "Priority": "High",
        "Labels": "[\"Bug\"]",
        "Team": "codex-hackathon",
        "Created By": "Yong Rhee",
        "Linear URL": "https://linear.app/lgcns/issue/COD-7/...",
        "date:Created At:start": "2026-04-21T07:44:28.341Z",
        "date:Created At:is_datetime": 1,
        "date:Updated At:start": "2026-04-22T00:04:13.356Z",
        "date:Updated At:is_datetime": 1
      },
      content: "## Description\n\n..."
    }
  ]
```

> 💡 `MULTI_SELECT` 값은 JSON 배열을 **문자열로** 넘겨야 합니다 (`"[\"Bug\"]"`).
> 💡 `DATE` 컬럼은 `date:<컬럼명>:start`, `date:<컬럼명>:is_datetime` 같은 확장 키 형식으로 전달합니다.

## 결과

- Notion DB: `Linear Issues — codex-hackathon` (워크스페이스 루트)
- 옮겨진 이슈: 1건 (`COD-7`)

## 다음 단계로 확장하기

- **주기 동기화**: `/loop` 또는 `/schedule` skill로 일정 주기마다 Linear → Notion으로 변경분만 반영
- **양방향 동기화**: Notion에서 상태가 바뀌면 Linear `save_issue` 호출로 역동기화
- **여러 팀**: `list_issues`를 팀별로 호출하고, 팀 컬럼 값을 다르게 채워 같은 DB에 통합
- **첨부/관계**: Linear `attachments`, `relations`, `parentId` 정보를 Notion `RELATION` 컬럼으로 연결

## 핵심 학습 포인트

1. **두 MCP 서버를 한 대화에서 함께 사용**할 수 있다 — Claude가 양쪽 도구를 자연스럽게 오간다.
2. Notion DB 생성은 **DDL 문자열**로 한 번에 표현된다.
3. 페이지 생성 시 `properties`는 **데이터 소스 스키마와 정확히 일치**해야 한다 (특히 `MULTI_SELECT`/`DATE`).
4. 미러링은 결국 **필드 매핑 + 일괄 생성**이라는 단순한 패턴이다 — 프로덕션화하려면 변경 감지와 멱등성을 추가하면 된다.
