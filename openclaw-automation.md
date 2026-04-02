# OpenClaw는 왜 일상 자동화가 되는가

## Claude Code와의 근본적 차이

Claude Code를 떠올려 보세요. 터미널을 열고, 질문하고, 답을 받고, 터미널을 닫으면 끝입니다. **사용자가 말을 걸어야만 동작하는 구조**입니다.

OpenClaw는 다릅니다. 터미널을 닫아도 **계속 살아 있습니다**.

```
Claude Code:
사용자가 말을 건다 → Claude가 답한다 → 세션 종료

OpenClaw:
Gateway가 항상 떠 있다 → 메시지가 오면 처리한다
                       → 크론이 울리면 스스로 일어난다
                       → 하트비트마다 할 일을 점검한다
```

이 차이를 만드는 것이 **Gateway 데몬**입니다.

## Gateway — "항상 깨어 있는 뇌"

OpenClaw의 핵심은 하나의 장기 실행 Node.js 프로세스인 **Gateway**입니다.

```
┌─────────────────────────────────────────────────┐
│                   Gateway                        │
│               ws://127.0.0.1:18789               │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ 채널 관리  │  │ 세션 관리  │  │ 크론 스케줄러│      │
│  │ Telegram  │  │ 대화 상태  │  │ 매 30분마다 │      │
│  │ Slack     │  │ 메모리    │  │ 하트비트    │      │
│  │ WhatsApp  │  │ 이력 보존  │  │ 예약 작업   │      │
│  │ Discord   │  │          │  │           │      │
│  └────┬─────┘  └────┬─────┘  └─────┬─────┘      │
│       └──────────────┼──────────────┘            │
│                      ↓                           │
│              ┌──────────────┐                    │
│              │  에이전트 루프  │                    │
│              │  LLM 호출     │                    │
│              │  도구 실행     │                    │
│              │  결과 반환     │                    │
│              └──────────────┘                    │
└─────────────────────────────────────────────────┘
```

Gateway는 OS의 서비스로 등록됩니다:
- **macOS**: LaunchAgent (부팅 시 자동 시작)
- **Linux**: systemd user service
- **Docker**: 컨테이너로 24/7 실행

```bash
# 설치 시 데몬 자동 등록
openclaw onboard --install-daemon
```

이것이 핵심입니다. Claude Code는 터미널 프로세스이고, OpenClaw Gateway는 **OS 서비스**입니다.

## 세 가지 동작 방식

Gateway가 에이전트를 깨우는 방식은 세 가지입니다:

### 1. 리액티브 — 메시지가 오면 반응

가장 기본적인 방식입니다. 사용자가 Telegram이나 Slack에서 메시지를 보내면 Gateway가 에이전트에 전달합니다.

```
사용자 → "오늘 일정 알려줘" → Gateway → 에이전트 → 캘린더 조회 → 응답
```

Claude Code도 이 방식으로 동작합니다. 차이는 **입력 채널이 터미널이 아니라 메시지 앱**이라는 점뿐입니다.

### 2. 크론잡 — 정해진 시간에 스스로 실행

Gateway 내부에 크론 스케줄러가 내장되어 있습니다. 예약 작업이 `~/.openclaw/cron/jobs.json`에 저장되고, 시간이 되면 Gateway가 **격리된 세션**을 만들어 에이전트를 실행합니다.

```bash
# 매일 오전 8시 이메일 브리핑
openclaw cron add \
  --name "inbox-briefing" \
  --cron "0 8 * * *" \
  --tz "Asia/Seoul" \
  --session isolated \
  --message "Gmail 인박스를 확인하고 긴급한 것만 요약해줘" \
  --channel telegram

# 평일 오전 9시 스탠드업 준비
openclaw cron add \
  --name "standup-prep" \
  --cron "0 9 * * 1-5" \
  --session isolated \
  --message "어제 작업 내역과 오늘 캘린더를 정리해줘"

# 매시간 서버 상태 체크
openclaw cron add \
  --name "server-health" \
  --cron "0 * * * *" \
  --session isolated \
  --message "프로덕션 서버 상태를 점검하고 이상 있으면 알려줘"
```

**격리된 세션(isolated session)**이 중요합니다. 크론잡은 `cron:<jobId>` 세션에서 실행되므로, 메인 대화의 컨텍스트를 오염시키지 않습니다. 매일 아침 실행되는 브리핑 에이전트가 어제 밤 나눈 대화를 방해하지 않습니다.

### 3. 하트비트 — 스스로 판단하고 행동

크론잡이 "정해진 시간에 정해진 일"이라면, 하트비트는 **"주기적으로 깨어나서 할 일이 있는지 스스로 판단"**하는 메커니즘입니다.

기본 30분 간격으로 Gateway가 에이전트를 깨우면, 에이전트는 워크스페이스의 `HEARTBEAT.md` 파일을 읽습니다:

```markdown
# HEARTBEAT.md

## 체크리스트
- Gmail에 긴급 메일이 왔는지 확인
- GitHub에 내가 리뷰해야 할 PR이 있는지 확인
- 서버 CPU가 80% 넘었는지 확인
- 내일 미팅이 있으면 미리 알려주기
```

에이전트는 이 체크리스트를 보고:
- 할 일이 있으면 → 작업 수행 후 메시지 전송
- 할 일이 없으면 → `HEARTBEAT_OK` 반환 (사용자에게 전달되지 않음)

```
하트비트 흐름:

30분마다: Gateway → 에이전트 깨움
          에이전트 → HEARTBEAT.md 읽음
          에이전트 → 체크리스트 항목 점검
              ↓
         할 일 있음?
         ├── YES → 작업 수행 → 사용자에게 알림
         └── NO  → HEARTBEAT_OK (조용히 다시 잠듦)
```

더 강력한 점은, **에이전트가 HEARTBEAT.md를 스스로 업데이트할 수 있다**는 것입니다:

```
"HEARTBEAT.md에 매일 환율 체크 항목 추가해줘"
→ 에이전트가 파일을 수정
→ 다음 하트비트부터 환율도 자동 체크
```

## 메모리 — 어제 대화를 오늘도 기억

OpenClaw는 세션 메모리를 호스트 머신에 저장합니다. **어제 WhatsApp에서 한 대화를 오늘 Slack에서 이어갈 수 있습니다.**

```
월요일 (Telegram): "이번 주 금요일 팀 회식 예약해야 해"
→ 에이전트가 기억

수요일 (하트비트): "금요일 회식 레스토랑 아직 안 정했네요. 예약할까요?"
→ 스스로 리마인드

금요일 (Slack): "회식 장소가 어디였지?"
→ "강남역 근처 OO식당, 7시로 예약해뒀습니다"
```

Claude Code도 `auto-memory`가 있지만, **세션 간 연속성**과 **채널 간 연속성**에서 차이가 납니다.

| 항목 | Claude Code | OpenClaw |
|---|---|---|
| 세션 내 기억 | ✅ | ✅ |
| 세션 간 기억 | ✅ (auto-memory) | ✅ (Gateway 메모리) |
| 채널 간 기억 | ❌ (터미널만) | ✅ (WhatsApp → Slack → Telegram) |
| 능동적 리마인드 | ❌ | ✅ (하트비트) |

## 사람들은 실제로 어떻게 쓰고 있나

### 구조 1: 개인 비서형 (가장 흔함)

```
┌──────────────┐
│  Telegram Bot │ ← 유일한 채널
└──────┬───────┘
       ↓
   Gateway (맥북 or VPS)
       │
       ├── 크론: 매일 오전 8시 브리핑
       ├── 크론: 매일 오후 6시 하루 요약
       ├── 하트비트: 30분마다 이메일 체크
       └── 리액티브: 메시지 오면 즉시 응답
```

Telegram 하나에 모든 것을 연결하는 가장 단순한 구조입니다. 많은 사람이 여기서 시작합니다.

### 구조 2: 개발자 DevOps형

```
┌──────────┐  ┌──────────┐
│  Slack   │  │ Telegram │
│ #devops  │  │ 개인 채팅  │
└────┬─────┘  └────┬─────┘
     └──────┬──────┘
            ↓
       Gateway (VPS)
            │
            ├── Slack 메시지: "@bot staging 배포해줘"
            │     → exec: 배포 스크립트 실행
            │     → 결과를 Slack 스레드에 게시
            │
            ├── 크론: 매시간 CI 파이프라인 상태 체크
            │     → 실패 시 Telegram으로 알림
            │
            └── 하트비트: GitHub PR 리뷰 대기 목록 점검
                  → 새 PR 발견 시 알림
```

### 구조 3: 1인 창업자 멀티에이전트형

```
                 Telegram (지휘 채널)
                        │
                   Gateway (VPS)
                        │
         ┌──────────────┼──────────────┐
         ↓              ↓              ↓
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │ Dev Agent │  │Marketing │  │ Biz Agent│
   │          │  │  Agent   │  │          │
   │ SOUL:    │  │ SOUL:    │  │ SOUL:    │
   │ 코딩·배포 │  │ 콘텐츠·SNS│  │ 재무·분석 │
   └──────────┘  └──────────┘  └──────────┘

각 에이전트의 크론:
- Dev: 매일 밤 12시 → 이슈 처리, PR 생성
- Marketing: 매일 오전 10시 → SNS 콘텐츠 작성·예약
- Biz: 매주 월요일 → 주간 매출 리포트
```

각 에이전트가 **독립된 SOUL.md**를 가지고, 독립된 세션에서 실행됩니다. Strategy Agent가 전체를 조율하고, Telegram으로 지시를 내립니다.

### 구조 4: 팀 협업형

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Slack   │  │  Slack   │  │  Slack   │
│ #support │  │ #dev     │  │ #sales   │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     ↓              ↓              ↓
┌──────────┐  ┌──────────┐  ┌──────────┐
│ CS Agent │  │ Dev Agent│  │Sales Agent│
│고객 응대  │  │코드 리뷰  │  │리드 분석  │
└──────────┘  └──────────┘  └──────────┘
     └──────────────┼──────────────┘
                    ↓
              Gateway (사내 서버)
```

Slack 채널별로 다른 에이전트가 배정되어, 각 팀의 요청을 전문적으로 처리합니다.

## Claude Code에서 비슷하게 하려면?

Claude Code도 일부 자동화가 가능합니다:

| OpenClaw 기능 | Claude Code 대안 | 한계 |
|---|---|---|
| 크론잡 | `claude schedule` (Remote Triggers) | 서버 필요, Channels 전용 |
| 하트비트 | `/loop` 명령 | 터미널 세션이 살아 있어야 함 |
| 멀티 채널 | Claude Code Channels | Telegram·Discord만 지원 |
| 상시 실행 | `tmux` + Claude Code | 수동 구성, 공식 지원 아님 |

> "Claude Code는 날카로운 메스이고, OpenClaw는 24시간 돌아가는 자동화 공장이다. 둘 다 필요한 순간이 다르다."

## 정리 — 왜 일상 자동화가 되는가

```
1. Gateway 데몬    → 항상 깨어 있다 (OS 서비스)
2. 크론 스케줄러    → 정해진 시간에 스스로 일어난다
3. 하트비트        → 주기적으로 할 일을 스스로 판단한다
4. 세션 메모리     → 어제 대화를 오늘도 기억한다
5. 멀티 채널      → 어디서든 접근할 수 있다
```

이 다섯 가지가 합쳐져서, OpenClaw는 "물어보면 답하는 도구"가 아니라 **"스스로 일하고 보고하는 에이전트"**가 됩니다.

> 참조:
> - [OpenClaw Gateway 공식 문서](https://docs.openclaw.ai/gateway)
> - [OpenClaw Heartbeat 공식 문서](https://docs.openclaw.ai/gateway/heartbeat)
> - [Inside OpenClaw: How a Persistent AI Agent Actually Works — DEV Community](https://dev.to/entelligenceai/inside-openclaw-how-a-persistent-ai-agent-actually-works-1mnk)
> - [OpenClaw Architecture, Explained — ppaolo](https://ppaolo.substack.com/p/openclaw-system-architecture-overview)
> - [The Complete OpenClaw Architecture That Actually Scales — Medium](https://medium.com/@rentierdigital/the-complete-openclaw-architecture-that-actually-scales-memory-cron-jobs-dashboard-and-the-c96e00ab3f35)
> - [OpenClaw Heartbeats: Proactive Agents — Sam's Playbook](https://openclawsetup.info/en/blog/openclaw-heartbeat-proactive-agents)
> - [OpenClaw Cron Jobs Guide — Stack Junkie](https://www.stack-junkie.com/blog/openclaw-cron-jobs-automation-guide)
