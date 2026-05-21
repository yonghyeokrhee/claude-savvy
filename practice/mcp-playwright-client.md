# MCP 실습 — 직접 Playwright MCP를 사용하는 Client 만들기

지금까지의 실습은 **Claude Code(=이미 만들어진 MCP Client)**에 서버를 붙여 쓰는 쪽이었습니다.
이번에는 시선을 반대로 돌려 **MCP Client를 직접** 만들고 Microsoft의 **Playwright MCP 서버**에 연결합니다.

단, 코드를 한 줄씩 타이핑하지 않습니다. **요구사항(PRD)을 먼저 쓰게 하고, 구현은 Claude에게 맡기는 "바이브코딩"** 방식으로 만듭니다.

> 이 실습의 목표는 완성된 코드를 외우는 게 아니라, **"MCP SDK로 Client를 만들어 줘"라고 Claude에게 잘 요청하는 프롬프트**를 익히는 것입니다.

---

## MCP Client란? (개념만)

**MCP Client = MCP 프로토콜을 구현한 AI 에이전트**입니다.
Claude Code, Cursor, VS Code Copilot처럼 "MCP 서버를 불러 쓰는 쪽"이 전부 MCP Client입니다. 우리가 이번에 만드는 것도 바로 그 자리입니다.

Client가 하는 일은 결국 다음 흐름입니다.

1. MCP 서버에 연결하고 세션을 초기화한다
2. 서버가 제공하는 **도구 목록을 조회**한다
3. 사용자 입력을 LLM(Claude)에 전달한다
4. LLM이 고른 도구를 **대신 호출**하고, 결과를 다시 LLM에 넘긴다
5. LLM이 최종 답을 낼 때까지 4를 반복한다

> Server(지난 RDS 실습)는 "능력을 제공"하고, Client(이번 실습)는 "그 능력을 LLM과 연결해 실행"합니다. 둘이 만나야 MCP가 완성됩니다.

---

## 무엇을 만드나 — Playwright MCP Client

- **서버**: `@playwright/mcp` — 브라우저를 띄우고 페이지를 조작하는 공식 Playwright MCP 서버 (Node.js `npx`로 실행, **stdio** 통신)
- **클라이언트**: 우리가 Claude에게 만들게 할 Python CLI 에이전트 — Claude API로 자연어를 이해하고 Playwright MCP의 도구를 호출

```
사용자: "네이버로 이동해서 화면 캡처해줘"
   ↓
[우리가 만든 Client]  ── 자연어를 Claude에 전달
   ↓
Claude            ── "browser_navigate, browser_take_screenshot 써야겠다" (tool_use)
   ↓
[Client]          ── Playwright MCP 서버의 도구를 실제 호출
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

> Playwright MCP는 픽셀 스크린샷보다 **접근성 트리 스냅샷(`browser_snapshot`)**을 우선합니다. 비전 모델 없이도 LLM이 페이지 구조를 읽고 조작할 수 있습니다.

---

## Step 0. 사전 준비 — 처음이라면 여기부터

이 실습은 **Python**(우리가 만들 Client)과 **Node.js**(Playwright MCP 서버)를 함께 씁니다.
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

### 4) Anthropic API Key 발급

1. [console.anthropic.com](https://console.anthropic.com) 에 로그인합니다.
2. **Billing**에서 결제 수단/크레딧을 등록합니다. (API는 사용량 과금이며, **Claude Code 구독과는 별개**입니다.)
3. **API Keys → Create Key** 로 키를 생성합니다 (`sk-ant-...`).
4. 키 전체는 **생성 직후 한 번만** 보입니다. 안전한 곳에 복사해 두세요.

> ⚠️ API 키는 비밀번호입니다. 코드·스크린샷·Git 저장소에 노출하지 마세요. `.env`에만 두고 `.gitignore`로 제외합니다.

### ✅ 시작 전 체크리스트

- [ ] `python3 --version` → 3.10 이상
- [ ] `uv --version` → 출력됨
- [ ] `node --version` → v18 이상, `npx --version` → 출력됨
- [ ] Anthropic 콘솔에 결제/크레딧 등록됨
- [ ] API Key 발급 완료 (곧 `.env`에 입력)

> 첫 실행 때 `npx`가 Playwright 서버와 **Chromium 브라우저(수백 MB)**를 내려받습니다. 미리 받아두려면 `npx playwright install chromium` 을 실행하세요.

---

## 바이브코딩으로 만들기 — PRD 먼저, 구현은 Claude에게

코드를 직접 쓰는 대신 **무엇을 만들지(PRD)** 를 먼저 정리하고, 그 PRD를 기준으로 Claude가 구현하게 합니다.
PRD는 사람이 검토하기 쉽고, 구현이 틀어지면 PRD로 돌아가 고치면 됩니다.

```
1단계: PRD 작성을 요청 (무엇을 만들지)
    ↓
2단계: PRD 검토 & 보완 (사람)
    ↓
3단계: 구현을 요청 (MCP SDK로 어떻게 만들지)
    ↓
4단계: 실행 & 디버깅 (사람이 에러를 다시 Claude에게)
```

작업 폴더에서 Claude Code를 시작합니다.

```bash
mkdir playwright-mcp-client && cd playwright-mcp-client
claude
```

### Step 1 — PRD 작성을 요청하는 프롬프트

```
Playwright MCP 서버를 사용하는 "MCP Client"를 만들 거야.
바로 코딩하지 말고, 먼저 PRD(제품 요구사항 문서)를 PRD.md 로 작성해줘.

다음 조건을 반영해:
- 언어: Python 3.10+, 패키지 관리: uv
- MCP 통신: 공식 MCP Python SDK(mcp 패키지) 사용
- 연결 대상: Playwright MCP 서버 (npx @playwright/mcp@latest, stdio 전송)
- LLM: Anthropic Claude API(anthropic 패키지)로 자연어를 이해해 도구를 선택·실행
- 인터페이스: CLI — 단일 명령 실행과 대화형 모드 모두 지원
- 동작 흐름: 서버 연결 → 도구 목록 조회 → 사용자 입력 → Claude가 도구 선택·실행 → 결과 출력
- 비밀정보: ANTHROPIC_API_KEY 등은 .env 환경변수로 관리

PRD에는 다음 섹션을 포함해줘:
개요 / 기술 스펙 / 핵심 요구사항 / 실행 흐름 / 프로젝트 구조 /
환경변수 / 제약사항 / 테스트 범위 / 성공 기준
```

> 핵심은 **"MCP SDK를 쓰고, Playwright MCP에 stdio로 붙으며, Claude로 도구를 호출한다"**는 의도를 분명히 적는 것입니다. 그래야 Claude가 정확한 PRD를 만듭니다.

### Step 2 — PRD 검토 & 보완

Claude가 PRD 초안을 주면 사람이 읽고 한두 가지만 조정합니다.

```
PRD를 다음만 보완해줘:
- 스크린샷은 ./output 폴더에만 저장하도록 제약 추가
- 외부 라이브러리는 mcp, anthropic, python-dotenv 로 최소화
- 도구 이름은 서버가 제공하는 browser_* 도구를 그대로 사용한다고 명시
```

> PRD를 `PRD.md`로 남겨두면, 이후 구현·수정의 **기준 문서**가 됩니다. 결과가 마음에 안 들면 코드가 아니라 PRD를 고치세요.

### Step 3 — 구현을 요청하는 프롬프트

```
방금 만든 PRD.md 대로 MCP Client를 구현해줘.

구현 시 다음을 지켜:
- 공식 MCP Python SDK로 stdio 연결을 만들고,
  "세션 초기화 → 도구 목록 조회(list_tools) → 도구 호출(call_tool)" 흐름을 구현해.
- MCP 도구 목록을 Anthropic tools 형식으로 변환해 Claude에 전달하고,
  Claude가 tool_use를 반환하면 실제 도구를 호출한 뒤 결과를 다시 모델에 넘기는 루프를 구현해.
- uv 프로젝트로 만들고, `uv run` 으로 실행 가능한 CLI 엔트리포인트를 추가해.
- .env.example 과 간단한 사용법(README)도 함께 만들어줘.
- 마지막에 실행 방법을 알려줘.
```

Claude가 `pyproject.toml`, 설정·클라이언트·에이전트·CLI 파일, `.env.example`을 알아서 생성합니다.
**우리는 코드를 타이핑하지 않고, "무엇을·어떻게"를 지시했을 뿐입니다.**

### Step 4 — 실행 & 디버깅

`.env`에 발급받은 키를 넣고 실행합니다.

```bash
# .env 작성 (Claude가 만든 .env.example 참고)
# ANTHROPIC_API_KEY=sk-ant-...

uv run playwright-mcp-client "네이버로 이동해서 화면 캡처해줘"
```

에러가 나면 메시지를 **그대로 복사해 Claude에게** 붙여 넣고 고쳐 달라고 합니다.

```
실행했더니 이런 에러가 나:
<에러 메시지 붙여넣기>
원인을 찾아 수정해줘.
```

> 바이브코딩의 핵심은 **사람이 실행·검증하고, 고치는 일은 Claude에게 위임**하는 반복 루프입니다.

---

## Claude가 만든 Client, 무엇을 확인할까 (이해용)

생성된 코드를 한 줄씩 외울 필요는 없지만, **무엇이 핵심인지**는 알아야 검수할 수 있습니다.

1. **MCP 통신 3요소** — 세션 초기화 → 도구 목록 조회 → 도구 호출. 이 셋이 MCP 프로토콜의 전부입니다. Claude Code도 내부에서 정확히 이 일을 합니다.
2. **tool-use 루프** — 에이전트의 엔진입니다.

```
[사용자 입력]
  → Claude 호출 (MCP 도구 목록 함께 전달)
  → "도구를 쓰겠다(tool_use)" ?
       예  → 도구 실행 → 결과를 대화에 추가 → 다시 Claude 호출 (반복)
       아니오(끝) → 최종 답변 출력
```

핵심: **LLM은 도구를 "고르고", 실제 실행은 Client가 MCP 서버에 위임합니다.** 이 분리가 MCP의 본질입니다. 생성된 코드에서 이 루프가 제대로 들어갔는지만 확인하면 됩니다.

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
| 구현이 의도와 다름 | PRD가 모호함 | 코드 말고 **PRD.md를 고치고** 다시 구현 요청 |

---

## 핵심 학습 포인트

1. MCP Client는 직접 타이핑하지 않아도 된다 — **PRD로 명세하고, 구현은 Claude에게 맡긴다(바이브코딩)**.
2. 좋은 요청의 핵심은 **"MCP SDK 사용 + Playwright MCP에 stdio 연결 + 도구 조회/호출 + tool-use 루프"**를 프롬프트에 분명히 적는 것이다.
3. **PRD는 기준 문서**다 — 결과가 틀어지면 코드가 아니라 PRD로 돌아가 고친다.
4. 완성된 Client는 **host(Claude Code)가 내부에서 하는 일의 축소판**이다.
5. 다른 MCP 서버로 바꾸려면 PRD의 "연결 대상"만 바꿔 다시 요청하면 된다.

---

## 더 나아가기

- **서버 교체**: PRD에서 연결 대상을 다른 stdio MCP 서버(예: 지난 실습의 RDS MySQL 서버)로 바꿔 다시 구현을 요청하면, 같은 구조의 Client가 다른 서버에 붙는다.
- **여러 서버 동시 연결**: "두 개의 MCP 서버에 동시에 연결해 도구 목록을 합쳐 달라"고 PRD에 적으면, 한 에이전트가 브라우저 + DB를 함께 다룬다.

---

## 참고

- MCP Python SDK: [github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
- Playwright MCP: [github.com/microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)
- MCP Client 개념·개발 가이드: [modelcontextprotocol.io/docs/develop/build-client](https://modelcontextprotocol.io/docs/develop/build-client)

> 참조: FastCampus AI Agent 바이브코딩 강의 — *Part 2. Agent 개념과 아키텍처 > 바이브코딩으로 MCP AI 에이전트 만들기 > Clip 1. MCP Client 구현을 위한 PRD 프롬프트 만들기* ([GitBook](https://goobong.gitbook.io/fastcampus/part-2.-agent/chapter4_-_mcp_ai_-_/clip1_mcp_client_-_-_prd_-_), [GitHub](https://github.com/Koomook/fastcampus-ai-agent-vibecoding))
