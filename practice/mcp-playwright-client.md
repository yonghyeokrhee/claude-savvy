# MCP 실습 — 직접 Playwright MCP를 사용하는 Client 만들기

지금까지의 실습은 **Claude Code(=이미 만들어진 MCP Client)**에 서버를 붙여 쓰는 쪽이었습니다.
이번에는 시선을 반대로 돌립니다. **MCP Client를 직접 코드로 만들어** Microsoft의 **Playwright MCP 서버**에 연결하고, 자연어로 브라우저를 자동화하는 작은 AI 에이전트를 만듭니다.

> "Claude Code는 내부에서 MCP를 어떻게 쓰는 걸까?"가 궁금했다면, 이 실습이 그 답입니다. Client를 한 번 만들어 보면 MCP의 동작 원리가 손에 잡힙니다.

---

## MCP Client란?

**MCP Client = MCP 프로토콜을 구현한 AI 에이전트**입니다.
Claude Code, Cursor, VS Code Copilot처럼 "MCP 서버를 불러 쓰는 쪽"이 전부 MCP Client입니다. 우리가 이번에 만드는 것도 바로 그 자리입니다.

Client가 하는 핵심 역할은 다섯 가지입니다.

1. **연결 관리** — MCP 서버 프로세스를 띄우고 세션을 유지
2. **프로토콜 통신** — JSON-RPC 2.0 기반 요청/응답 처리
3. **Tool 탐색** — 서버가 제공하는 도구 목록(`list_tools`) 조회
4. **Tool 실행** — 도구 호출(`call_tool`)과 결과 수신
5. **LLM 연결** — 받은 도구 목록을 LLM에 넘겨, LLM이 고른 도구를 대신 실행

> Server(지난 RDS 실습)는 "능력을 제공"하고, Client(이번 실습)는 "그 능력을 LLM과 연결해 실행"합니다. 둘이 만나야 MCP가 완성됩니다.

---

## 무엇을 만드나 — Playwright MCP Client

- **서버**: `@playwright/mcp` — 브라우저를 띄우고 페이지를 조작하는 공식 Playwright MCP 서버 (Node.js `npx`로 실행, **stdio** 통신)
- **클라이언트**: 우리가 만들 Python CLI 에이전트 — Claude API로 자연어를 이해하고, Playwright MCP의 도구를 호출

```
사용자: "네이버로 이동해서 화면 캡처해줘"
   ↓
[우리가 만든 Client]  ── 자연어를 Claude에 전달
   ↓
Claude            ── "browser_navigate, browser_take_screenshot 써야겠다" (tool_use)
   ↓
[Client]          ── Playwright MCP 서버의 도구를 실제 호출 (call_tool)
   ↓
Playwright MCP    ── 브라우저 구동 → 결과 반환
   ↓
[Client]          ── 결과를 Claude에 다시 전달 → 최종 답변 출력
```

### Playwright MCP 주요 도구

| 도구 | 용도 |
|---|---|
| `browser_navigate` | URL로 이동 |
| `browser_snapshot` | 접근성 트리 스냅샷 (LLM이 페이지 구조 파악 — 스크린샷보다 선호) |
| `browser_take_screenshot` | 화면 이미지 캡처 |
| `browser_click` | 요소 클릭 |
| `browser_type` | 입력창에 텍스트 입력 |
| `browser_wait_for` | 특정 텍스트/시간 대기 |

> Playwright MCP는 픽셀 스크린샷보다 **접근성 트리 스냅샷(`browser_snapshot`)**을 우선합니다. 비전 모델 없이도 LLM이 페이지 구조를 읽고 클릭할 요소를 고를 수 있습니다.

---

## 전체 흐름

```
1단계: 프로젝트 셋업 (uv, .env)
    ↓
2단계: config.py — 설정 로드
    ↓
3단계: client.py — MCP 클라이언트 (서버 연결 · list_tools · call_tool)
    ↓
4단계: agent.py — Claude 에이전트 (도구 변환 + tool-use 루프)
    ↓
5단계: __main__.py — CLI (단일 명령 / 대화형)
    ↓
6단계: 실행 — 자연어로 브라우저 자동화
```

---

## Step 0. 사전 준비 — 처음이라면 여기부터

이 실습은 **Python**(우리가 만들 Client 코드)과 **Node.js**(Playwright MCP 서버)를 함께 씁니다.
아래 4가지를 먼저 갖추고, 각 **확인 명령**으로 점검하세요. 하나라도 빠지면 실습 도중 막힙니다.

| 준비물 | 왜 필요한가 | 확인 명령 |
|---|---|---|
| Python 3.10+ | Client 코드 실행 | `python3 --version` |
| uv | Python 패키지·실행 관리 | `uv --version` |
| Node.js (npx 포함) | `npx @playwright/mcp` 서버 실행 | `node --version` · `npx --version` |
| Anthropic API Key | Claude API 호출 | 콘솔에서 발급 |

### 1) Python 3.10 이상

```bash
python3 --version    # Python 3.10.x 이상이면 OK
```

없거나 버전이 낮으면 설치합니다.

- **macOS**: `brew install python@3.12`
- **Windows**: [python.org](https://www.python.org/downloads/) 설치 시 **"Add python.exe to PATH"** 체크 필수
- uv를 먼저 깔았다면 `uv python install 3.12` 로도 받을 수 있습니다.

### 2) uv — Python 패키지 매니저

`pip`보다 빠르고 가상환경·실행까지 한 번에 처리합니다.

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 또는 (공통) pip 사용
pip install uv
```

```bash
uv --version    # 설치 확인
```

> `command not found: uv` 가 뜨면 터미널을 새로 열거나, 설치 후 안내된 PATH 설정을 적용하세요.

### 3) Node.js (npx 포함)

Playwright MCP 서버는 Node로 실행됩니다. Node를 설치하면 `npx`가 함께 깔립니다.

```bash
node --version    # v18 이상 권장
npx --version
```

- **macOS**: `brew install node`
- **Windows**: [nodejs.org](https://nodejs.org) 의 **LTS** 버전 설치
- 여러 버전을 관리하려면 nvm 사용

### 4) Anthropic API Key 발급

1. [console.anthropic.com](https://console.anthropic.com) 에 로그인합니다.
2. **Billing**에서 결제 수단/크레딧을 등록합니다. (API는 사용량 과금이며, **Claude Code 구독과는 별개**입니다.)
3. **API Keys → Create Key** 로 키를 생성합니다 (`sk-ant-...`).
4. 키 전체는 **생성 직후 한 번만** 보입니다. 안전한 곳에 복사해 두세요.

> ⚠️ API 키는 비밀번호입니다. 코드·스크린샷·Git 저장소에 노출하지 마세요. 아래처럼 `.env`에만 두고 `.gitignore`로 제외합니다.

### 5) 프로젝트 생성 & 의존성 설치

```bash
mkdir playwright-mcp-client && cd playwright-mcp-client
uv init
uv add mcp anthropic python-dotenv
```

### 6) 환경변수 파일 `.env`

프로젝트 루트에 `.env`를 만들고 발급받은 키를 넣습니다.

```bash
ANTHROPIC_API_KEY=sk-ant-...
PLAYWRIGHT_MCP_SERVER_PATH=npx
PLAYWRIGHT_MCP_SERVER_ARGS=@playwright/mcp@latest
```

키가 새지 않도록 `.gitignore`에 추가합니다.

```bash
echo ".env" >> .gitignore
echo "output/" >> .gitignore
```

> 서버 실행 명령을 환경변수로 빼두면(`npx @playwright/mcp@latest`), 나중에 다른 MCP 서버로 바꿔 끼우기 쉽습니다.

### 7) 프로젝트 구조 (최종 모습)

```
playwright-mcp-client/
├── pyproject.toml
├── .env                     # API 키 (Git 커밋 금지)
├── .gitignore
├── output/                  # 스크린샷 저장 (자동 생성)
└── src/playwright_mcp_client/
    ├── __init__.py
    ├── __main__.py          # CLI 엔트리포인트
    ├── client.py            # MCP 클라이언트 (핵심)
    ├── agent.py             # Claude 에이전트
    └── config.py            # 설정 관리
```

### ✅ 시작 전 체크리스트

- [ ] `python3 --version` → 3.10 이상
- [ ] `uv --version` → 출력됨
- [ ] `node --version` → v18 이상, `npx --version` → 출력됨
- [ ] Anthropic 콘솔에 결제/크레딧 등록됨
- [ ] `.env`에 `ANTHROPIC_API_KEY` 입력됨
- [ ] `.gitignore`에 `.env` 추가됨

> 첫 실행 때 `npx`가 Playwright 서버와 **Chromium 브라우저(수백 MB)**를 내려받습니다. 네트워크가 되는 환경에서 처음 한 번은 시간이 걸립니다. 미리 받아두려면 `npx playwright install chromium` 을 실행하세요.

---

## Step 1. 설정 — `config.py`

`.env`를 읽어 설정 객체로 만듭니다.

```python
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv


@dataclass
class Config:
    anthropic_api_key: str
    playwright_server_path: str
    playwright_server_args: str
    output_dir: Path = Path("./output")

    @classmethod
    def from_env(cls) -> "Config":
        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        return cls(
            anthropic_api_key=api_key,
            playwright_server_path=os.getenv("PLAYWRIGHT_MCP_SERVER_PATH", "npx"),
            playwright_server_args=os.getenv("PLAYWRIGHT_MCP_SERVER_ARGS", "@playwright/mcp@latest"),
        )

    def ensure_output_dir(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
```

---

## Step 2. MCP 클라이언트 — `client.py` (핵심)

이 파일이 **MCP의 심장**입니다. MCP Python SDK의 `stdio_client`로 서버 프로세스를 띄우고, `ClientSession`으로 도구를 조회·호출합니다.

```python
from typing import Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from .config import Config


class PlaywrightMCPClient:
    def __init__(self, config: Config):
        self.config = config
        self.session: ClientSession | None = None
        self._stdio_context = None

    async def connect(self) -> None:
        # 1) 서버 실행 파라미터 구성 (예: npx @playwright/mcp@latest)
        server_params = StdioServerParameters(
            command=self.config.playwright_server_path,
            args=self.config.playwright_server_args.split(),
            env=None,
        )
        # 2) stdio로 서버 프로세스를 띄우고 읽기/쓰기 스트림 확보
        self._stdio_context = stdio_client(server_params)
        read, write = await self._stdio_context.__aenter__()
        # 3) 세션 생성 후 초기화 핸드셰이크
        self.session = ClientSession(read, write)
        await self.session.__aenter__()
        await self.session.initialize()

    async def list_tools(self) -> list[Any]:
        if not self.session:
            raise RuntimeError("Not connected to MCP server")
        response = await self.session.list_tools()
        return response.tools

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        if not self.session:
            raise RuntimeError("Not connected to MCP server")
        return await self.session.call_tool(tool_name, arguments)

    async def disconnect(self) -> None:
        if self.session:
            await self.session.__aexit__(None, None, None)
        if self._stdio_context:
            await self._stdio_context.__aexit__(None, None, None)

    async def __aenter__(self) -> "PlaywrightMCPClient":
        await self.connect()
        return self

    async def __aexit__(self, *exc) -> None:
        await self.disconnect()
```

> **여기가 핵심입니다.** `initialize()`(핸드셰이크) → `list_tools()`(도구 탐색) → `call_tool()`(실행). 이 세 호출이 MCP 프로토콜의 전부입니다. Claude Code도 내부적으로 정확히 이 흐름을 수행합니다.

---

## Step 3. Claude 에이전트 — `agent.py`

에이전트는 두 가지를 합니다. ① MCP 도구를 **Anthropic 도구 형식으로 변환**하고, ② Claude가 도구를 다 쓸 때까지 **tool-use 루프**를 돕니다.

```python
import anthropic
from anthropic.types import Message, TextBlock, ToolUseBlock
from .client import PlaywrightMCPClient
from .config import Config

SYSTEM_PROMPT = """당신은 Playwright MCP 서버를 활용하여 웹 브라우저 자동화를 수행하는 전문가입니다.
사용자의 요청을 분석하고 적절한 MCP tool을 선택하여 작업을 수행하세요.
각 단계에서 어떤 tool을 사용했는지 명확히 설명하세요."""


class ClaudeAgent:
    def __init__(self, config: Config, mcp_client: PlaywrightMCPClient):
        self.config = config
        self.mcp_client = mcp_client
        self.client = anthropic.Anthropic(api_key=config.anthropic_api_key)
        self.tools: list[dict] = []

    async def initialize(self) -> None:
        # MCP 도구 목록 → Anthropic tools 형식으로 변환
        mcp_tools = await self.mcp_client.list_tools()
        self.tools = [
            {
                "name": t.name,
                "description": t.description or "",
                "input_schema": t.inputSchema,   # MCP의 inputSchema를 그대로 사용
            }
            for t in mcp_tools
        ]

    async def process_request(self, user_message: str) -> str:
        messages = [{"role": "user", "content": user_message}]
        response_text = ""

        while True:
            response: Message = self.client.messages.create(
                model="claude-sonnet-4-6",        # 현재 사용 가능한 최신 모델로 교체 가능
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=self.tools,
                messages=messages,
            )

            # 더 쓸 도구가 없으면 텍스트를 모아 종료
            if response.stop_reason == "end_turn":
                for block in response.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text
                break

            # Claude가 도구를 쓰겠다고 하면(tool_use) 실제로 실행
            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})
                tool_results = []
                for block in response.content:
                    if isinstance(block, ToolUseBlock):
                        result = await self.mcp_client.call_tool(block.name, block.input)
                        response_text += f"\n[Tool: {block.name}]\n"
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(result.content),
                        })
                # 도구 실행 결과를 다시 대화에 넣어 루프 계속
                messages.append({"role": "user", "content": tool_results})
            else:
                break

        return response_text.strip()
```

### tool-use 루프가 핵심 원리입니다

```
[user 메시지]
   → Claude 호출 (tools 함께 전달)
   → stop_reason == "tool_use" ?
        예 → MCP call_tool 실행 → tool_result를 대화에 추가 → 다시 Claude 호출 (반복)
        아니오(end_turn) → 최종 텍스트 반환
```

LLM은 **직접 브라우저를 만지지 않습니다.** "이 도구를 이 인자로 써줘"라고 말할 뿐이고, 실제 실행은 **Client(우리 코드)가 MCP 서버에 위임**합니다. 이 분리가 MCP의 본질입니다.

> MCP의 `inputSchema`가 그대로 Anthropic의 `input_schema`로 들어가는 점에 주목하세요. 도구 정의가 표준화돼 있어 **변환이 거의 복사 수준**입니다 — 표준의 힘입니다.

---

## Step 4. CLI — `__main__.py`

단일 명령과 대화형 모드를 제공합니다. 연결 → 에이전트 초기화 → 요청 처리 순서입니다.

```python
import argparse, asyncio, sys
from .agent import ClaudeAgent
from .client import PlaywrightMCPClient
from .config import Config


async def run_single_command(user_input: str) -> None:
    config = Config.from_env()
    config.ensure_output_dir()
    async with PlaywrightMCPClient(config) as mcp_client:   # 연결/종료 자동 관리
        agent = ClaudeAgent(config, mcp_client)
        await agent.initialize()                            # 도구 목록 로드
        print(f"\n> {user_input}\n")
        print(await agent.process_request(user_input))


async def run_interactive() -> None:
    config = Config.from_env()
    config.ensure_output_dir()
    async with PlaywrightMCPClient(config) as mcp_client:
        agent = ClaudeAgent(config, mcp_client)
        await agent.initialize()
        print(f"Connected. Available tools: {len(agent.tools)}")
        while True:
            user_input = input("> ").strip()
            if user_input.lower() in ("exit", "quit"):
                break
            print("\n" + await agent.process_request(user_input) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Playwright MCP Client")
    parser.add_argument("command", nargs="?", help="실행할 명령 (없으면 대화형)")
    parser.add_argument("--interactive", "-i", action="store_true")
    args = parser.parse_args()
    if args.interactive or args.command is None:
        asyncio.run(run_interactive())
    else:
        asyncio.run(run_single_command(args.command))


if __name__ == "__main__":
    main()
```

`pyproject.toml`에 실행 스크립트를 등록하면 `uv run`으로 바로 호출됩니다.

```toml
[project.scripts]
playwright-mcp-client = "playwright_mcp_client.__main__:main"
```

---

## Step 5. 실행

```bash
# 대화형 모드
uv run playwright-mcp-client

# 단일 명령
uv run playwright-mcp-client "네이버 메인 페이지로 이동해줘"
```

출력 예시:

```
> 네이버 메인 페이지로 이동해줘

[Tool: browser_navigate]
https://www.naver.com 으로 이동했습니다.

[Tool: browser_take_screenshot]
스크린샷 저장됨: output/screenshot_20260520_103000.png
```

> 첫 실행 시 `npx`가 Playwright MCP 서버와 브라우저 런타임을 내려받느라 시간이 걸릴 수 있습니다.

---

## 자주 막히는 문제 (Troubleshooting)

| 증상 | 원인 | 해결 |
|---|---|---|
| `command not found: uv` | PATH 미적용 | 터미널 재시작, 또는 설치 안내의 PATH 적용 / `pip install uv` |
| `ANTHROPIC_API_KEY environment variable is required` | `.env` 누락·위치 오류 | 프로젝트 루트에 `.env` 두고 키 이름 정확히 입력 |
| `npx: command not found` | Node.js 미설치 | Node LTS 설치 후 `npx --version` 확인 |
| 첫 실행이 멈춘 듯 느림 | 브라우저 최초 다운로드 | 잠시 대기, 또는 `npx playwright install chromium` 선실행 |
| `401 authentication_error` | API 키 오타·만료 | 콘솔에서 키 재확인/재발급 |
| `429 rate_limit` 또는 크레딧 부족 | 결제·크레딧 미등록 | 콘솔 **Billing**에서 크레딧 충전 |
| `ModuleNotFoundError: mcp` | 의존성 미설치 | `uv add mcp anthropic python-dotenv` |
| Python 3.9 이하 에러 | 버전 낮음 | 3.10+ 설치, `uv python install 3.12` |

---

## 핵심 학습 포인트

1. **MCP Client = MCP 프로토콜을 구현한 AI 에이전트**다. 우리가 만든 코드는 Claude Code가 내부에서 하는 일의 축소판이다.
2. MCP 통신은 결국 **세 단계** — `initialize()` → `list_tools()` → `call_tool()` — 로 압축된다.
3. **LLM은 도구를 고르고, Client가 실행한다.** `tool_use` → `call_tool` → `tool_result`를 반복하는 **tool-use 루프**가 에이전트의 엔진이다.
4. 도구 정의가 표준화(`inputSchema`)돼 있어 **MCP → LLM 변환이 거의 복사 수준**이다. 한 번 만든 Client에 어떤 MCP 서버든 갈아 끼울 수 있다.
5. **Tool 중심으로 생각하라.** 거의 모든 클라이언트가 Tools를 지원하지만 Resources/Prompts/Sampling은 지원이 제각각이다 — 서버를 만들 땐 Tool로 구현하는 게 가장 안전하다.

---

## 더 나아가기

- **서버 교체**: `.env`의 `PLAYWRIGHT_MCP_SERVER_ARGS`만 바꾸면 다른 stdio MCP 서버(예: 지난 실습의 RDS MySQL 서버)에 그대로 붙는다.
- **여러 서버 동시 연결**: `PlaywrightMCPClient`를 여러 개 띄워 도구 목록을 합치면, 한 에이전트가 브라우저 + DB를 함께 다룬다.
- **바이브코딩으로 만들기**: 위 구조를 직접 타이핑하는 대신, PRD(요구사항 명세)를 먼저 작성하고 Claude Code에 넘겨 한 번에 생성하게 한다. FastCampus 강의의 `playwright-mcp-client`가 바로 이 방식으로 만들어졌다.

---

## 참고

- MCP Python SDK: [github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
- Playwright MCP: [github.com/microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)
- MCP Client 개념·개발 가이드: [modelcontextprotocol.io/docs/develop/build-client](https://modelcontextprotocol.io/docs/develop/build-client), [클라이언트 목록](https://modelcontextprotocol.io/clients)

> 참조: FastCampus AI Agent 바이브코딩 강의 — *Part 2. Agent 개념과 아키텍처 > MCP Client 사용하기 / 바이브코딩으로 MCP AI 에이전트 만들기* ([goobong.gitbook.io/fastcampus](https://goobong.gitbook.io/fastcampus), [GitHub](https://github.com/Koomook/fastcampus-ai-agent-vibecoding))
