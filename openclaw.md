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

많은 사람이 "Channels가 나왔으니 OpenClaw는 끝 아닌가?"라고 묻습니다. 결론부터 말하면 **둘은 해결하는 문제가 다릅니다**.

### 핵심 차이 — 한 줄 요약

> **하루 종일 코드 레포 안에서 사는 사람이라면 Claude Code가 더 날카로운 도구이고, 자체 호스팅으로 Telegram·WhatsApp·Slack·브라우저를 넘나드는 상시 에이전트를 원한다면 OpenClaw가 더 유연한 시스템이다.**

### Channels vs OpenClaw 비교

| 항목 | Claude Code Channels | OpenClaw |
|---|---|---|
| **작동 방식** | 실행 중인 Claude Code 세션에 메시지를 "밀어넣음" | 독립된 Gateway가 메시지를 수신·라우팅 |
| **지원 채널** | Telegram, Discord (2개) | WhatsApp, Telegram, Slack, Discord, Signal, iMessage, Teams 등 (10+) |
| **LLM** | Claude 전용 | Claude, GPT, DeepSeek, 로컬 모델 등 자유 선택 |
| **비용** | Claude 구독 필요 (Pro $20 ~ Max $100/월) | 무료 (MIT). API 비용 별도 ($5~20/월) 또는 Ollama로 $0 |
| **상시 실행** | 터미널 세션이 살아 있어야 함 | 데몬/Docker로 24/7 상시 실행 |
| **권한 승인** | 메시지 앱에서 승인 불가 — 터미널에 직접 가야 함 | Gateway UI 또는 메시지 앱에서 직접 승인 |
| **보안** | Anthropic 인프라, allowlist 기반 플러그인 검증 | 자체 호스팅, 보안은 사용자 책임 |

### "그래서 뭘 쓰라고?"

커뮤니티에서 가장 많이 등장하는 선택 기준은 이렇습니다:

**Channels를 쓰는 사람:**
- 코드 작업이 주 목적이고, 이동 중 Telegram으로 "이거 고쳐줘" 정도만 보내는 경우
- 보안이 중요한 팀 환경 — Anthropic 인프라의 안정성과 보안 업데이트를 신뢰
- 별도 서버 관리 없이 바로 쓰고 싶은 경우

**OpenClaw을 쓰는 사람:**
- 코딩뿐 아니라 일상 자동화(일정 관리, 이메일, 알림 등)가 필요한 경우
- WhatsApp이나 iMessage 같은 Channels가 지원하지 않는 플랫폼을 쓰는 경우
- 여러 LLM을 섞어 쓰거나 로컬 모델을 돌리고 싶은 경우
- 자체 호스팅에 익숙하고, 데이터 주권이 중요한 경우

### 보안 — 넘기면 안 되는 이야기

OpenClaw는 2026년 들어 심각한 보안 이슈를 여러 차례 겪었습니다:

| 시기 | CVE | 심각도 | 내용 |
|---|---|---|---|
| 2026년 1월 | CVE-2026-25253 | CVSS **8.8** | 원격 코드 실행 (RCE). 135,000+개 인스턴스가 인터넷에 노출 |
| 2026년 3월 18~21일 | 9개 CVE 동시 공개 | 최대 CVSS **9.9** | 인증된 사용자가 관리자 권한 탈취 가능 |
| 2026년 3월 29일 | CVE-2026-32922 | CVSS **9.9** | 권한 상승 취약점 |

OpenClaw는 기본 설정이 **허용적(permissive)**이고, 보안은 전적으로 운영자 책임입니다. Channels는 Anthropic이 관리하는 인프라 위에서 동작하므로, 보안 팀이 없는 개인이나 소규모 팀이라면 이 차이는 결정적입니다.

> "셀프 호스팅 에이전트에 더 많은 권한을 줄수록, 보안 모델이 더 중요해진다."
> — [The Tradeoffs Nobody's Talking About (DEV Community)](https://dev.to/ji_ai/claude-code-channels-vs-openclaw-the-tradeoffs-nobodys-talking-about-2h5h)

### 함께 쓰기

둘은 배타적 선택이 아닙니다. 실제로 많은 개발자가 이렇게 조합합니다:

```
코드 작업     → Claude Code (터미널/IDE)
이동 중 트리거 → Claude Code Channels (Telegram)
일상 자동화   → OpenClaw (WhatsApp, Slack, 이메일 등)
```

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
> - [Channels vs OpenClaw: The Tradeoffs Nobody's Talking About — DEV Community](https://dev.to/ji_ai/claude-code-channels-vs-openclaw-the-tradeoffs-nobodys-talking-about-2h5h)
> - [Claude Code Channels Hands-On — ShareUHack](https://www.shareuhack.com/en/posts/claude-code-channels-telegram)
> - [CVE-2026-32922: OpenClaw Privilege Escalation — ARMO](https://www.armosec.io/blog/cve-2026-32922-openclaw-privilege-escalation-cloud-security/)
