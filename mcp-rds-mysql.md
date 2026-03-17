# MCP 실습 — RDS MySQL 연결하기

AWS RDS MySQL에 Claude가 직접 접속해 데이터를 조회하고 분석하는 실습입니다.
직접 만든 Python MCP 서버를 통해 자연어로 SQL을 실행할 수 있습니다.

---

## 전체 흐름

```
1단계: MCP 서버 파일 작성 (server.py)
    ↓
2단계: .mcp.json에 서버 등록
    ↓
3단계: Claude Code 재시작 → 연결 확인
    ↓
4단계: 자연어로 DB 조회 실습
```

---

## 이 MCP가 필요한 이유

| | MCP 없이 | MCP 연결 후 |
|---|---|---|
| DB 조회 | 터미널에서 직접 mysql 접속 | "ROAS 낮은 광고주 조회해줘" |
| 분석 | 쿼리 작성 → 복사 → Claude에 붙여넣기 | Claude가 직접 쿼리 실행 후 분석 |
| 반복 작업 | 매번 수동 | 자연어 한 마디로 처리 |

---

## 사전 준비

- AWS 자격증명 설정 (`aws configure` 또는 AWS Profile)
- VPN 연결 (사내 RDS 접근 시)
- Python 3.10+ 및 의존 패키지 설치

```bash
pip install fastmcp pymysql boto3
```

---

## Step 1. MCP 서버 작성

`~/.claude/mcp-servers/rds-mysql/server.py`를 작성합니다.

```python
from fastmcp import FastMCP
import pymysql, os

mcp = FastMCP("RDS MySQL")

def _get_conn():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor
    )

@mcp.tool()
def query(sql: str) -> str:
    """SELECT 쿼리를 실행하고 결과를 반환합니다."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchmany(500)
            if not rows:
                return "결과 없음"
            cols = list(rows[0].keys())
            lines = [" | ".join(cols)]
            lines += [" | ".join(str(r[c]) for c in cols) for r in rows]
            return "\n".join(lines)

@mcp.tool()
def list_tables(database: str = "") -> str:
    """테이블 목록을 반환합니다."""
    sql = f"SHOW TABLES FROM `{database}`" if database else "SHOW TABLES"
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return "\n".join(list(r.values())[0] for r in cur.fetchall())

@mcp.tool()
def describe_table(table: str) -> str:
    """테이블 컬럼 구조를 반환합니다."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(f"DESCRIBE `{table}`")
            rows = cur.fetchall()
            cols = list(rows[0].keys())
            lines = [" | ".join(cols)]
            lines += [" | ".join(str(r[c]) for c in cols) for r in rows]
            return "\n".join(lines)

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

> **실전 팁**: AWS SSM Parameter Store나 Secrets Manager에서 접속 정보를 가져오면 `.mcp.json`에 자격증명을 노출하지 않아도 됩니다.

---

## Step 2. MCP 서버 등록

`.mcp.json`에 직접 작성하거나 CLI 명령어로 등록합니다:

```bash
claude mcp add rds-mysql \
  --command "/path/to/.venv/bin/python" \
  --args "/path/to/server.py" \
  --env "ENV=stg" \
  --env "AWS_PROFILE=myprofile" \
  -s user
```

또는 `~/.claude/.mcp.json`에 직접 작성:

```json
{
  "mcpServers": {
    "rds-mysql": {
      "command": "/Users/yong/.claude/mcp-servers/rds-mysql/.venv/bin/python",
      "args": ["/Users/yong/.claude/mcp-servers/rds-mysql/server.py"],
      "env": {
        "ENV": "stg",
        "AWS_PROFILE": "mopstg"
      }
    }
  }
}
```

> **User vs Project Scope**: DB 접속 정보처럼 민감한 서버는 `user` 스코프(`-s user`)로 등록해 Git에 커밋되지 않게 합니다. 팀과 공유할 설정은 `project` 스코프로 등록합니다.

---

## Step 3. 연결 확인

Claude Code를 재시작한 후:

```
/mcp
```

`rds-mysql` 서버가 목록에 표시되고 상태가 `connected`이면 완료입니다.

---

## Step 4. 사용 가능한 도구

| 도구 | 용도 |
|---|---|
| `query` | SELECT 조회 (읽기 전용, 최대 500행) |
| `execute` | INSERT / UPDATE / DELETE (쓰기) |
| `list_tables` | 테이블 목록 조회 |
| `describe_table` | 테이블 컬럼 구조 확인 |
| `show_databases` | 접근 가능한 DB 목록 |
| `table_row_count` | 테이블 행 수 확인 |

> `query()`는 SELECT/SHOW/DESCRIBE만 허용합니다. DROP DATABASE / TRUNCATE는 자동 차단됩니다.

---

## Step 5. 실습 — 자연어로 DB 조회

Claude Code 대화창에서 직접 물어봅니다:

**DB 구조 파악:**
```
RDS에 어떤 데이터베이스가 있어?
```

```
mop 스키마의 테이블 목록을 보여줘
```

```
dashboard_overview 테이블 구조를 설명해줘
```

**데이터 조회 및 분석:**
```
최근 2일간 수집 실패한 광고주 ID 목록을 조회해줘
```

```
advertiser_id가 1691인 광고주의 Collection 오류 원인을 진단해줘
```

Claude가 SQL을 작성·실행하고 결과를 해석해 줍니다.

---

## Step 6. Super Analyst Skill과 연동

`/super-analyst` Skill은 이 MCP를 활용해 Collection 오류 진단을 자동화합니다:

```
/super-analyst
```

Skill이 자동으로:
1. advertiser_id 확인
2. `dashboard_overview` 수집 여부 조회
3. URL/UTM 이상 감지 건수 조회
4. 진단 결과 요약 출력

MCP가 없으면 각 쿼리를 터미널에서 직접 실행해야 했지만, MCP 연결 후에는 자연어 한 마디로 전체 진단이 가능합니다.

---

## 안전하게 사용하기

운영(prd) 환경에서는 쓰기 쿼리를 실수로 실행하지 않도록 주의합니다:

```
prd 환경 조회야. 쿼리 실행 전에 반드시 SQL을 먼저 보여줘.
```

프롬프트에 **"실행 전 SQL 확인"** 조건을 추가하면 Claude가 쿼리를 보여주고 승인을 기다립니다.

---

## MCP 비교

| | Notion | Obsidian | RDS MySQL |
|---|---|---|---|
| 대상 | Notion 워크스페이스 | 로컬 vault | AWS RDS DB |
| 연결 방식 | HTTP (공식 서버) | Local REST API | 직접 만든 Python 서버 |
| 인증 | OAuth | API Key | AWS 자격증명 + VPN |
| 주 용도 | 문서·태스크 관리 | 개인 노트 | 데이터 조회·분석 |

---

## 참고

- FastMCP: `pip install fastmcp` — Python 데코레이터로 MCP 서버를 간단히 작성
- AWS SDK: `pip install boto3` — Secrets Manager / SSM에서 접속 정보 자동 조회
- MCP 서버 목록: [modelcontextprotocol.io](https://modelcontextprotocol.io)
