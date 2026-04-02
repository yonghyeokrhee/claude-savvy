# OpenClaw

## OpenClaw이란?

**OpenClaw**은 오픈소스 AI 에이전트로, LLM을 실제 소프트웨어와 연결해 주는 **로컬 퍼스트(local-first) 자율 에이전트**입니다.

오스트리아 개발자 Peter Steinberger가 만들었으며, 2026년 1월 OpenClaw로 이름을 바꾼 후 단 두 달 만에 GitHub 스타 **247,000개**를 돌파하며 폭발적으로 성장했습니다.

## 핵심 개념

Claude Code가 터미널에서 개발자와 협업하는 도구라면, OpenClaw는 **메시지 플랫폼 어디서든** AI 에이전트를 실행할 수 있게 해 줍니다.

```
사용자 (Telegram / Slack / WhatsApp / Discord / ...)
        │
        ▼
  OpenClaw Gateway  ←── 로컬 또는 서버에서 실행
        │
        ▼
     LLM (Claude, GPT 등)
        │
        ▼
  파일, 터미널, 브라우저, API, 이메일 ...
```

채팅 명령 하나로 에이전트가 필요한 작업을 스스로 판단하고 실행합니다.

## 주요 기능

| 기능 | 설명 |
|---|---|
| **멀티 채널 인박스** | WhatsApp, Telegram, Slack, Discord, Signal, iMessage 등 한 곳에서 관리 |
| **로컬 퍼스트 Gateway** | 세션·채널·툴·이벤트를 하나의 컨트롤 플레인으로 관리 |
| **파일 읽기/쓰기** | 로컬 파일시스템 직접 접근 |
| **셸 명령 실행** | 터미널 명령을 에이전트가 직접 실행 |
| **웹 브라우징** | 웹사이트 탐색 및 데이터 수집 |
| **멀티 에이전트 라우팅** | 채널·계정별로 격리된 에이전트에 요청을 라우팅 |
| **음성 모드** | macOS/iOS, Android에서 음성으로 에이전트 호출 |
| **Live Canvas** | 에이전트 주도 시각적 워크스페이스 |

## SOUL.md — OpenClaw의 CLAUDE.md

OpenClaw에는 에이전트의 성격과 행동을 정의하는 **SOUL.md** 파일이 있습니다. Claude Code의 `CLAUDE.md`와 같은 역할입니다.

```markdown
# SOUL.md 예시

이름: Savvy
역할: 개인 비서 에이전트
말투: 간결하고 실용적으로 답변
금지: 개인 파일을 허락 없이 외부로 전송하지 않는다
```

커뮤니티에서 공유하는 [awesome-openclaw-agents](https://github.com/mergisi/awesome-openclaw-agents) 레포에 19개 카테고리, 162개 프로덕션 레디 SOUL.md 템플릿이 있습니다.

## Claude Code vs OpenClaw

| 항목 | Claude Code | OpenClaw |
|---|---|---|
| **제공 주체** | Anthropic (공식) | 오픈소스 커뮤니티 |
| **주요 인터페이스** | 터미널 / IDE | 메시지 앱 (Telegram 등) |
| **주요 용도** | 코드 작성·리팩터링·디버깅 | 일상 자동화·멀티 플랫폼 에이전트 |
| **LLM** | Claude 전용 | Claude, GPT 등 멀티모델 |
| **설치** | `npm install -g @anthropic-ai/claude-code` | 자체 호스팅 or Docker |
| **SOUL 파일** | `CLAUDE.md` | `SOUL.md` |

두 도구는 경쟁 관계이기도 하지만, Claude Code를 OpenClaw의 채널로 연결하는 방식으로 **함께 사용**할 수도 있습니다.

## Claude Code Channels — Anthropic의 대응

2026년 Anthropic은 **Claude Code Channels**를 출시했습니다. Telegram·Discord 메시지를 실행 중인 Claude Code 세션으로 직접 연결하는 기능으로, OpenClaw가 강점으로 내세웠던 "메시지 앱에서 코딩 에이전트 실행"을 Claude Code 공식 기능으로 흡수했습니다.

## 시작하기

```bash
# Docker로 빠르게 실행
docker run -it --rm \
  -e ANTHROPIC_API_KEY=your_key \
  openclaw/openclaw

# 또는 GitHub에서 클론
git clone https://github.com/openclaw/openclaw
cd openclaw
```

> 참조:
> - [GitHub — openclaw/openclaw](https://github.com/openclaw/openclaw)
> - [OpenClaw vs Claude Code — AnalyticsVidhya](https://www.analyticsvidhya.com/blog/2026/03/openclaw-vs-claude-code/)
> - [OpenClaw Explained — KDnuggets](https://www.kdnuggets.com/openclaw-explained-the-free-ai-agent-tool-going-viral-already-in-2026)
