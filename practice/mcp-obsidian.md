# MCP 실습 — Obsidian 연결하기

Obsidian은 로컬에 저장되는 마크다운 노트 앱입니다.
Local REST API 플러그인을 통해 Claude가 Obsidian vault의 파일을 직접 읽고 쓸 수 있습니다.

---

## 사전 준비

### Obsidian Local REST API 플러그인 설치

1. Obsidian → 설정 → 커뮤니티 플러그인 → 탐색
2. **"Local REST API"** 검색 후 설치 및 활성화
3. 플러그인 설정에서 **API Key 복사**
4. 포트는 기본값 `27124` 사용 (HTTPS) 또는 `27123` (HTTP)

### 연결 확인

터미널에서 아래 명령어로 API가 정상 동작하는지 확인합니다:

```bash
curl -sk \
  -H "Authorization: Bearer [YOUR_API_KEY]" \
  https://127.0.0.1:27124/vault/
```

vault 내 파일 목록이 JSON으로 출력되면 준비 완료입니다.

---

## Step 1. MCP 서버 등록

프로젝트 루트에 `.mcp.json` 파일을 생성합니다:

```bash
# practice/ 폴더 기준
touch .mcp.json
```

`.mcp.json` 내용:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "mcp-obsidian"],
      "env": {
        "OBSIDIAN_API_KEY": "여기에_API_KEY_입력",
        "OBSIDIAN_PROTOCOL": "https",
        "OBSIDIAN_HOST": "127.0.0.1",
        "OBSIDIAN_PORT": "27124"
      }
    }
  }
}
```

> **주의:** API Key는 로컬 전용이지만 Git에 커밋하지 않도록 `.gitignore`에 `.mcp.json`을 추가하거나, 별도 환경변수로 관리하는 것을 권장합니다.

---

## Step 2. Claude Code 재시작 후 확인

```
/mcp
```

`obsidian` 서버가 목록에 표시되면 연결 완료입니다.

---

## Step 3. 기본 동작 확인

Claude Code 대화창에서:

```
내 Obsidian vault에 있는 파일 목록을 보여줘
```

vault의 파일 목록이 표시되면 MCP가 정상 동작하는 것입니다.

---

## Step 4. 실습 — MOP 분석 결과를 Obsidian에 저장

Workflow 실습에서 만든 `report-monthly.md` 내용을 Obsidian에 저장해봅니다:

```
practice/data/report-monthly.md 파일을 읽고
Obsidian vault에 "MOP/2026-02 월간 리포트.md" 파일로 저장해줘.
```

Claude가:
1. 로컬 파일 **Read**
2. Obsidian MCP로 **Write** (vault에 파일 생성)

두 단계를 자동으로 처리합니다.

---

## Step 5. 반대 방향 — Obsidian에서 읽어오기

Obsidian에 있는 메모를 Claude가 참조하게 할 수도 있습니다:

```
Obsidian에서 "2026년 로드맵" 파일을 읽고
MOP 광고 전략과 연관된 내용이 있는지 정리해줘
```

---

## Notion vs Obsidian

| | Notion | Obsidian |
|---|---|---|
| 저장 위치 | 클라우드 | 로컬 파일 |
| 인터넷 연결 | 필요 | 불필요 |
| 팀 공유 | 쉬움 | 별도 설정 필요 |
| 개인 노트 | 가능 | 최적화됨 |
| MCP 연결 방식 | HTTP (공식 서버) | Local REST API |

개인 메모, 일기, 리서치 노트는 Obsidian — 팀과 공유하는 태스크/문서는 Notion을 권장합니다.
