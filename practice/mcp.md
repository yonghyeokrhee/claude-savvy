# MCP 실습 — Notion 연결하기

MCP 서버를 실제로 연결하고, Claude가 Notion 워크스페이스와 직접 대화하는 걸 체험합니다.
Notion MCP는 별도 개발 없이 공식 URL 하나로 바로 연결할 수 있습니다.

---

## 전체 흐름

```
1단계: Notion MCP 서버 추가 (명령어 한 줄)
    ↓
2단계: Claude Code 재시작 → OAuth 인증
    ↓
3단계: Notion 페이지 읽기/쓰기 테스트
    ↓
4단계: MOP 캠페인 태스크를 Notion에 자동 저장
```

---

## Step 1. Notion MCP 추가

프로젝트 폴더에서 터미널에 입력:

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp -s project
```

프로젝트 루트에 `.mcp.json` 파일이 자동 생성됩니다:

```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

> **Project Scope로 저장했으므로** 이 파일을 Git에 커밋하면 팀원 모두가 같은 MCP 설정을 사용합니다.

---

## Step 2. 인증

Claude Code를 재시작한 후 대화창에서:

```
/mcp
```

입력하면 브라우저가 열립니다:
1. Notion 로그인
2. 워크스페이스 선택
3. 권한 승인

완료하면 자동으로 토큰이 저장됩니다. API 키를 직접 관리할 필요가 없습니다.

---

## Step 3. 연결 확인

Claude Code 대화창에서:

```
Notion 워크스페이스에 있는 페이지 목록을 보여줘
```

Notion 페이지 목록이 표시되면 연결 완료입니다.

---

## Step 4. MOP 태스크 자동 저장

이제 실제로 써봅니다. 아래 프롬프트를 입력합니다:

```
Notion에 "MOP 캠페인 관리" 데이터베이스를 만들어줘.

다음 속성을 포함해줘:
- 캠페인명 (제목)
- 상태 (선택: 진행중 / 검토필요 / 완료)
- ROAS (숫자)
- 담당자 (텍스트)
- 조치사항 (텍스트)
```

Claude가 Notion에 직접 데이터베이스를 생성합니다.

데이터베이스가 만들어지면, 실습 데이터를 추가해봅니다:

```
방금 만든 MOP 캠페인 관리 데이터베이스에
다음 캠페인들을 추가해줘:

- 브랜드_쇼핑검색 / 진행중 / ROAS 750% / 김마케터 / 예산 확대 검토
- 신규고객_검색 / 검토필요 / ROAS 100% / 이담당 / 소재 교체 필요
```

---

## 무엇이 달라졌나?

| | MCP 없이 | MCP 연결 후 |
|---|---|---|
| Notion 접근 | 복사·붙여넣기로 수동 입력 | Claude가 직접 읽기/쓰기 |
| 데이터베이스 생성 | Notion UI에서 직접 클릭 | 자연어 명령으로 생성 |
| 반복 입력 | 매번 수동 | 프롬프트 한 번으로 일괄 처리 |

---

## 더 나아가기

Slack MCP도 함께 연결하면 두 서비스를 연동할 수 있습니다:

```
Slack #광고팀 채널의 최근 메시지를 읽고,
"검토필요" 또는 "문제" 키워드가 포함된 메시지를
Notion MOP 캠페인 관리 데이터베이스에 태스크로 추가해줘.
```

Claude가 Slack에서 읽고 → Notion에 쓰는 작업을 자동으로 처리합니다.

---

## 참고

- Notion MCP 공식 서버: `https://mcp.notion.com/mcp`
- Slack MCP: `@modelcontextprotocol/server-slack` (npx로 실행)
- MCP 서버 목록: [modelcontextprotocol.io](https://modelcontextprotocol.io)
