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

## OpenClaw로 무엇을 할 수 있는가

OpenClaw의 핵심은 **24/7 자율 실행**입니다. 사용자가 없어도 크론잡으로 돌아가고, 실패하면 스스로 재시도하고, 시간이 지나면 행동을 자체 개선합니다. 이 "상시 가동" 특성이 Claude Code와 결정적으로 다른 점입니다.

### 일상 자동화

**아침 브리핑 에이전트:**
```
매일 오전 7시 → 이메일 인박스 스캔 → 캘린더 확인 → 날씨 조회
→ 요약을 Telegram으로 전송
```

```bash
openclaw cron add \
  --name "Morning briefing" \
  --cron "0 7 * * *" \
  --tz "Asia/Seoul" \
  --session isolated \
  --message "이메일, 캘린더, 날씨를 확인하고 오늘의 브리핑을 작성해줘" \
  --channel telegram
```

크론잡은 **격리된 세션**에서 실행되므로 메인 대화의 컨텍스트를 오염시키지 않습니다.

**이 패턴으로 확장 가능한 것들:**
- 매일 아침 팀 슬랙에 스탠드업 준비 노트 게시
- 주간 지출 리포트를 WhatsApp으로 전송
- GA4 + Stripe + GitHub를 조합한 일일 비즈니스 대시보드 이메일

### 개발 자동화

OpenClaw의 `exec` 도구(셸 명령)와 `github` 스킬을 결합하면 메시지 한 줄로 개발 워크플로우를 트리거할 수 있습니다:

```
Slack에서: "@openclaw staging 배포해줘"
→ 테스트 스위트 실행 → 통과 시 배포 → 결과를 Slack 스레드에 게시
```

```
Telegram에서: "PR #142 리뷰해줘"
→ diff 분석 → 보안/성능/테스트 관점 코드 리뷰 → 코멘트 작성
```

**밤새 코딩 에이전트:**

자기 전에 태스크를 할당하고, 아침에 결과를 확인하는 패턴입니다:

```
잠들기 전: "내일까지 이 3개 이슈 처리해줘. 각각 브랜치 만들어서 PR 올려"
→ 밤새 서브에이전트 3개가 병렬 실행
→ 아침에 Telegram으로 "PR 3개 올렸습니다" 알림
```

### 1인 창업자의 AI 팀

한 솔로 파운더가 VPS 하나에 **4개 에이전트**를 구성한 사례입니다:

```
┌───────────────────────────────────────────┐
│        Strategy Agent (메인)               │
│  "전체 전략, 기획, 다른 에이전트 조율"       │
└──┬──────────┬──────────┬─────────────────┘
   ↓          ↓          ↓
┌────────┐ ┌────────┐ ┌────────┐
│  Dev   │ │Marketing│ │Business│
│ Agent  │ │ Agent  │ │ Agent  │
│코딩·배포│ │리서치·콘│ │재무·분석│
│아키텍처│ │텐츠 제작│ │고객 응대│
└────────┘ └────────┘ └────────┘
```

모든 에이전트가 **공유 메모리**를 가지고, 크론잡으로 매일 할 일을 자동 생성하며, Telegram 하나로 전체를 지휘합니다. 사실상 **1인이 4인 팀의 아웃풋**을 내는 구조입니다.

### 극단적 활용 사례

**자율 트레이딩:**

한 사용자가 OpenClaw을 Polymarket에 연결해 $100로 15분 단위 비트코인 시장을 거래했습니다. 에이전트가 밤새 뉴스와 센티먼트를 스캔하고 변동성에 반응한 결과, 아침에 **$347**이 되어 있었습니다.

**Moltbook — AI만의 소셜 네트워크:**

2026년 1월 등장한 Moltbook은 OpenClaw 에이전트들이 사용자로 가입해 서로 게시글을 쓰고 댓글을 달고 서브포럼을 만드는 온라인 커뮤니티입니다. 인간 개입 없이 AI 봇들만으로 운영됩니다.

**밤새 앱 빌더:**

목표(유튜브 채널, SaaS, 프리랜스 사업)를 적어두면 밤새 프로젝트 폴더에 작동하는 미니앱을 만들어 놓고, 아침에 Telegram으로 "이렇게 만들었습니다"라고 설명을 보냅니다.

**아이디어 → 리서치 → 코드 파이프라인:**

낮 동안 떠오르는 아이디어를 캡처하면, 매일 밤 서브에이전트가 자동으로 리서치와 코드 실험을 수행하고, 아침에 **구조화된 의사결정 문서**를 만들어 놓습니다.

### OpenClaw Skills 생태계

커뮤니티 스킬 레지스트리 **ClawHub**에 2026년 2월 기준 **13,729개** 스킬이 등록되어 있습니다:

| 레벨 | 설명 | 예시 |
|---|---|---|
| **Bundled** | 기본 내장 | 파일 읽기/쓰기, 셸 실행, 웹 검색 |
| **Managed** | 커뮤니티 공유 (npm) | Gmail, Jira, GA4, Stripe, Notion |
| **Workspace** | 사용자 커스텀 | 사내 API, 자사 시스템 연동 |

GA4 스킬 같은 걸 **20분 만에** 만들어 ClawHub에 퍼블리시한 사례도 있습니다.

### ⚠️ 극단적 활용의 대가

자율성이 높아질수록 리스크도 커집니다:

- Cisco 보안팀이 서드파티 스킬을 테스트한 결과, **데이터 유출과 프롬프트 인젝션**이 발견됨 — 스킬 저장소의 검증이 아직 불충분
- 가짜 스킬 패키지, 계정 탈취, 스캠 캠페인이 OpenClaw 인기를 악용
- 밤새 자율 실행한 에이전트가 **예상치 못한 비용**을 발생시킬 수 있음 (API 호출 한도 설정 필수)

> 극단적 자동화의 원칙: **자율성을 높이기 전에 반드시 가드레일(비용 한도, 권한 제한, 알림 설정)부터 세우세요.**

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
> - [What People Are Actually Doing With OpenClaw: 25+ Use Cases — Forward Future](https://forwardfuture.ai/p/what-people-are-actually-doing-with-openclaw-25-use-cases)
> - [10 Wild Things People Are Building — TechRadar](https://www.techradar.com/pro/wild-things-people-are-building-with-openclaw)
> - [OpenClaw as a Force Multiplier for Solo Founders — Towards Data Science](https://towardsdatascience.com/using-openclaw-as-a-force-multiplier-what-one-person-can-ship-with-autonomous-agents/)
> - [9 OpenClaw Projects to Build — DataCamp](https://www.datacamp.com/blog/openclaw-projects)
> - [OpenClaw Cron Jobs Guide — Stack Junkie](https://www.stack-junkie.com/blog/openclaw-cron-jobs-automation-guide)
