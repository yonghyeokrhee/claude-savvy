# MCP (Model Context Protocol)

## MCP란?

**MCP(Model Context Protocol)**는 Claude가 외부 서비스와 도구에 연결하기 위한 **표준 통신 프로토콜**입니다.

USB 포트처럼, MCP는 어떤 외부 도구든 Claude에 연결할 수 있는 **공통 규격**을 정의합니다. MCP 서버를 만들면 Claude가 그 서비스를 네이티브 도구처럼 사용할 수 있습니다.

## MCP 없이 vs MCP 있을 때

**MCP 없이:**
```
사용자: "Notion에서 오늘 할 일 목록 가져와줘"
Claude: "저는 Notion에 직접 접근할 수 없습니다. 내용을 직접 붙여넣어 주세요."
```

**MCP 있을 때:**
```
사용자: "Notion에서 오늘 할 일 목록 가져와줘"
Claude: [Notion MCP 서버 호출] → 목록 조회 → "오늘 할 일은 3개입니다: ..."
```

## 구조

```
Claude Code
    │
    └── MCP Client
            │  (MCP 프로토콜)
            ▼
        MCP Server ──── 외부 서비스
      (로컬 프로세스)    (Notion, GitHub,
                         DB, Slack, ...)
```

MCP 서버는 보통 로컬에서 실행되는 작은 프로세스입니다. Claude는 이 서버를 통해 외부 서비스와 안전하게 통신합니다.

## MCP Scope — 어디에 설정하느냐가 중요

MCP 서버를 추가할 때 **범위(Scope)**를 먼저 결정해야 합니다:

| Scope | 저장 위치 | 적용 범위 | 팀 공유 |
|---|---|---|---|
| **Local** (기본) | 로컬 설정 | 나만, 이 프로젝트에서만 | ❌ |
| **Project** | `.mcp.json` (Git 관리) | 팀원 모두, 이 프로젝트에서 | ✅ |
| **User** | `~/.claude/` | 나만, 모든 프로젝트에서 | ❌ |

팀과 함께 쓰는 MCP는 **Project Scope**로 설정하고 Git에 커밋하면 됩니다.

## MCP 서버 추가하기

### 방법 1 — 명령어 한 줄 (권장)

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp -s project
```

- `--transport http` : 원격 서버 연결 방식
- `notion` : 서버 식별 이름
- `-s project` : Project Scope (`.mcp.json`에 저장)

### 방법 2 — 파일 직접 편집

프로젝트 루트에 `.mcp.json` 파일을 만들어 추가합니다:

```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-...",
        "SLACK_TEAM_ID": "T01234ABCDE"
      }
    }
  }
}
```

설정 후 Claude Code를 재시작하면 해당 도구들을 사용할 수 있습니다.

## 주요 MCP 서버 예시

| 서버 | 기능 |
|---|---|
| Notion | 페이지 읽기/쓰기, 데이터베이스 쿼리 |
| GitHub | PR 생성, 이슈 관리, 코드 검색 |
| Slack | 메시지 전송, 채널 조회 |
| PostgreSQL | DB 직접 쿼리 실행 |
| Filesystem | 지정된 디렉토리 파일 접근 |
| Browser | 웹 브라우저 자동화 |

## MCP 서버 직접 만들기

표준 SDK를 사용하면 누구나 MCP 서버를 만들 수 있습니다:

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";

const server = new Server({ name: "my-server", version: "1.0.0" });

// Claude가 사용할 수 있는 도구 정의
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "get_weather",
    description: "특정 도시의 현재 날씨를 가져옵니다",
    inputSchema: {
      type: "object",
      properties: {
        city: { type: "string", description: "도시 이름" }
      }
    }
  }]
}));
```

이렇게 정의하면 Claude가 `get_weather` 도구를 자연스럽게 호출합니다.

## MCP vs 기본 도구

| 구분 | 기본 도구 (Read, Bash 등) | MCP 도구 |
|---|---|---|
| 제공 주체 | Anthropic (내장) | 사용자/커뮤니티 (확장) |
| 접근 범위 | 로컬 파일시스템, 터미널 | 외부 서비스 무제한 |
| 설정 필요 | 없음 | MCP 서버 설치 필요 |
| 커스터마이즈 | 불가 | 직접 개발 가능 |

## 보안 고려사항

- MCP 서버는 Claude 대신 외부 서비스에 접근합니다. **API 키를 환경변수로 관리**하고 코드에 하드코딩하지 마세요.
- 신뢰할 수 없는 출처의 MCP 서버는 설치하지 마세요.
- 각 MCP 서버가 **어떤 권한**을 요구하는지 확인하세요.
