# 알면 달라지는 Claude Code 심화 사용법

`/help` 만 알아도 Claude Code는 충분히 쓸 수 있습니다.
하지만 매일 쓰는 사람도 의외로 모르는 명령·키바인딩·설정이 많습니다. 이 챕터는 그것들을 한 번에 정리합니다.

---

## 1. 잘 모르고 지나치는 슬래시 명령

| 명령 | 무엇을 하나 | 언제 쓰면 좋나 |
|---|---|---|
| `/resume` | 직전 세션 이어서 시작 | 실수로 종료했을 때, 어제 작업 이어가고 싶을 때 |
| `/compact <지시>` | 컨텍스트를 요약·압축. 지시문을 주면 그 관점으로 요약 | 대화가 길어졌는데 끊고 싶지 않을 때 (`/compact 지금까지 한 디버깅 결과만 남기고 정리해줘`) |
| `/clear` | 컨텍스트 완전 초기화 | 작업 주제가 완전히 바뀔 때 (`/compact` 와 구분) |
| `/agents` | 서브에이전트 목록·생성·편집 | 새 sub-agent를 빠르게 만들 때 |
| `/permissions` | 도구 허용/거부 규칙 편집 | "허용 묻기" 가 너무 자주 뜰 때 |
| `/hooks` | 현재 적용된 hook 보기·편집 | 자동화(자동 포맷, 자동 커밋 등) 셋업 |
| `/model` | 세션 도중 모델 교체 | 단순 작업은 Haiku, 어려운 추론은 Opus 같이 도중 전환 |
| `/cost` | 이번 세션 토큰/비용 | 긴 작업 후 비용 확인 |
| `/mcp` | 연결된 MCP 서버 목록·재연결 | MCP가 끊어졌을 때 첫 진단 |
| `/doctor` | 설치 상태 점검 | 뭔가 동작 안 할 때 가장 먼저 |
| `/init` | 현재 레포 분석해서 `CLAUDE.md` 초안 생성 | 새 프로젝트에서 처음 1회 |
| `/memory` | 메모리 파일 직접 편집 | 사용자 선호·프로젝트 컨텍스트 누적 |
| `/output-style` | 응답 톤·형식 전환 (예: explanatory, learning) | 학습 모드 vs 실무 모드 |
| `/statusline` | 하단 상태바 커스터마이즈 | 모델·브랜치·토큰을 항상 보이게 |
| `/config` | 테마·기본 모델 등 핵심 설정 | 설정 화면을 GUI로 |
| `/bug` | 트랜스크립트 첨부해 버그 리포트 | Anthropic에 버그 신고 |
| `/vim` | vim 키바인딩 토글 | 입력창에서 vi 키를 쓰고 싶을 때 |
| `/ide` | 현재 IDE 연결 (VS Code, JetBrains) | 에디터에서 선택 영역을 즉시 컨텍스트로 |

> 명령은 점점 늘어납니다. `/help` 로 항상 최신 목록 확인.

---

## 1-2. 2026년 추가된 신규 명령 — 꼭 알아야 할 것들

위 표는 안정 명령 모음입니다. 2026년 들어 추가된 다음 기능들은 **워크플로우 자체를 바꾸는** 변화이므로 따로 정리합니다.

| 명령 | 무엇을 하나 | 언제 쓰면 좋나 |
|---|---|---|
| `/loop <간격> <프롬프트>` | 같은 프롬프트를 주기적으로 반복 실행. 간격 생략 시 모델이 직접 페이싱(self-pace) | 빌드/배포 모니터링, PR 폴링, "5분마다 deploy 확인" |
| `/schedule` | cron 또는 GitHub 이벤트로 도는 **원격 routine** 생성 | 매일 아침 신규 PR 요약, 주간 리포트 자동화 |
| `/effort <xlow\|low\|medium\|high\|xhigh>` | Opus 4.7의 추론 강도(effort) 다이얼 | 단순 작업 `xlow`로 빠르게, 복잡한 설계 `xhigh`로 깊게 |
| `/btw <질문>` | **히스토리에 남기지 않는** 곁다리 질문. 프롬프트 캐시 재사용으로 비용 ↓ | 본 작업 흐름을 끊지 않고 잠깐 다른 질문 |
| `/security-review` | 현재 브랜치 변경분 보안 감사 | 머지 직전 자동 보안 점검 |
| `/ultrareview [PR#]` | 클라우드 멀티 에이전트 코드 리뷰 (사용자 트리거·과금) | 큰 PR을 여러 관점에서 깊게 검토할 때 |
| `/auto` (research preview) | 분류기 기반 자동 권한 모드 — 안전 작업은 자동 승인, 위험 작업만 묻기 | 긴 작업에서 권한 프롬프트 피로 줄이기 |
| `/status` | 토큰/컨텍스트 사용량, 모델·프로바이더 한눈에 | 비용/컨텍스트 임계 체감 |
| `/rename` | 현재 세션 이름 지정 | `/resume` 시 빠르게 찾기 |

### `/loop` 활용 예

```
/loop 5m bun run build && bun test
```

5분마다 빌드+테스트 실행. 모델이 결과를 보고 깨지면 알려줍니다. 간격 생략(`/loop`만)하면 모델이 빌드 길이에 맞춰 다음 체크 시점을 스스로 정합니다(캐시 TTL 5분 고려).

### `/effort` 가이드

| 상황 | 권장 |
|---|---|
| 파일 한 개 단순 수정 | `xlow` |
| 일반 구현 | `medium` (기본) |
| 새 아키텍처 설계, 복잡 디버깅 | `high`~`xhigh` |

Opus 4.7에서만 동작. 비용·시간이 강도에 비례하므로 무조건 `xhigh`보다 **작업 난이도에 맞춰 토글**하는 게 정석입니다.

### `/btw` — 히스토리를 더럽히지 않는 질문

```
/btw 방금 import한 zod 라이브러리 v3와 v4 차이가 뭐였지?
```

본 작업 컨텍스트는 그대로 둔 채 답만 받습니다. 캐시 재사용으로 비용도 거의 안 듦.

---

## 2. 입력창 단축키 — 손이 빨라지는 비결

| 키 | 동작 |
|---|---|
| `!` 접두사 | 한 줄을 **셸 명령**으로 실행 (예: `!git status`). 결과가 그대로 컨텍스트에 들어감 |
| `#` 접두사 | 메모리에 즉시 추가 (예: `# 이 프로젝트는 Bun 사용`) |
| `@경로` | 파일/폴더를 컨텍스트로 첨부 (탭 자동완성 지원) |
| `Shift + Tab` | 모드 순환: 일반 → 자동 수락 → **플랜 모드** |
| `Esc` | 현재 응답/도구 호출 인터럽트 |
| `Esc Esc` | 메시지 히스토리 열기 (이전 프롬프트 골라 재실행) |
| `Ctrl + R` | 입력 히스토리 역방향 검색 |
| `Ctrl + _` | 직전 편집 되돌리기 |
| `Ctrl + V` | 클립보드 이미지 붙여넣기 (스크린샷 즉시 첨부) |
| `Ctrl + O` | 트랜스크립트 토글 (도구 호출 전체 펼쳐 보기) |
| `Ctrl + T` | 작업 목록(Task list) 표시 토글 |
| `Ctrl + B` | bash 명령 백그라운드 실행 (긴 빌드/서버) |
| `Option + P` | 모델 즉시 교체 (프롬프트 유지) |
| `Option + T` | 확장 사고(extended thinking) 토글 |

### 멀티라인 입력 — 5가지 방법

긴 프롬프트를 여러 줄로 입력할 때:

| 방법 | 비고 |
|---|---|
| `\` + Enter | 어디서나 동작 (가장 호환성 좋음) |
| `Shift + Enter` | iTerm2 / WezTerm / Kitty / Warp 기본 (VS Code는 `/terminal-setup` 한 번 실행) |
| `Option + Enter` (Mac) / `Alt + Enter` | "Option as Meta" 활성화 후 |
| `Ctrl + J` | 어떤 터미널에서도 동작 |
| 외부 에디터 (`Ctrl + G` / `Ctrl + X Ctrl + E`) | `$EDITOR`(vim 등)로 길게 작성 후 복귀 |

특히 **플랜 모드(Shift+Tab 두 번)** 는 알아두면 큰 차이입니다. Claude가 코드를 건드리기 전에 먼저 계획을 보여주고 승인을 기다립니다. 위험한 리팩터링 / 마이그레이션 전에 켜세요.

---

## 3. CLI 옵션 — 터미널에서 바로 쓰기

```bash
# 마지막 세션 이어서
claude --resume

# 특정 세션 ID 이어서
claude --resume <session-id>

# 프롬프트 1회 실행 후 종료 (파이프 친화적)
echo "이 로그 분석해줘" | claude -p

# JSON 결과로 받기 (스크립트 자동화용)
claude -p "TODO 주석 모두 찾아줘" --output-format json

# 권한 묻기 비활성화 (CI/배치 작업)
claude --dangerously-skip-permissions -p "..."

# 특정 모델 강제
claude --model claude-opus-4-7

# 작업 디렉터리 지정
claude --cwd /path/to/repo
```

**`-p` (print 모드)** 는 Claude를 유닉스 파이프라인에 끼워 넣는 핵심 기능입니다.

```bash
# git diff를 Claude로 요약 → 클립보드
git diff main | claude -p "이 변경의 위험 요소만 bullet로" | pbcopy

# 로그 파일에서 의심 패턴 추출
tail -1000 server.log | claude -p "에러 패턴만 묶어서 표로"
```

---

## 4. 세션 안에서 즉시 빛나는 패턴

### 한 줄 자동화: `!` + `#` 조합

```
!npm test 2>&1 | tail -50
# 테스트 깨진 컴포넌트는 항상 Button.tsx 와 Form.tsx 두 개
```

테스트 실행 결과를 컨텍스트에 넣고, 발견된 패턴을 즉시 메모리화.

### `@` 다중 첨부

```
@src/auth/ @docs/auth-flow.md 이 두 개 비교해서 문서가 코드와 다른 부분 짚어줘.
```

폴더 자체도 첨부 가능. 하위 파일이 한 번에 컨텍스트로 들어갑니다.

### `/compact` 로 긴 세션을 살리기

```
/compact 지금까지의 결정사항만 남기고 디버깅 시도들은 다 지워줘
```

`/clear` 와 달리 컨텍스트가 사라지지 않고 **요약된 상태로 계속됨**.

---

## 5. 실험적 — Agent Team 구성 잡기

마지막으로, 평범한 한 명의 Claude를 넘어 **여러 에이전트가 협업하는 팀**을 셋업하는 방법입니다.
자세한 내용은 [Agent Team 챕터](agent-team.md)에서 다루지만, 여기서는 **설정 파일이 어떻게 짜여 있어야 하는가** 를 압축해서 보여줍니다.

### 5-1. 디렉토리 구조

```
.claude/
├── agents/                          ← 역할별 sub-agent 정의
│   ├── researcher.md                ← 사전 조사 담당
│   ├── implementer.md               ← 코드 작성 담당
│   ├── reviewer.md                  ← 변경사항 리뷰 담당
│   └── doc-writer.md                ← 문서/CHANGELOG 담당
├── skills/                          ← 팀이 공유하는 도구 모음
│   └── pdf-to-deck/SKILL.md
├── commands/                        ← 팀 워크플로우 슬래시 명령
│   └── ship-it.md                   ← /ship-it: 위 4명을 순차 호출
├── hooks/                           ← 자동 트리거
│   └── pre-commit.sh                ← 커밋 전 reviewer 자동 실행
└── settings.json                    ← 권한·기본 모델·hook 등록
```

### 5-2. sub-agent 한 명의 정의 (예시: `reviewer.md`)

```markdown
---
name: reviewer
description: 변경된 파일만 보고 보안·성능·가독성 관점에서 리뷰. PR 머지 직전에 호출.
tools: Read, Grep, Bash
model: claude-opus-4-7
---

너는 코드 리뷰어다.
- `git diff` 만 보고 판단해, 다른 파일은 열지 마라
- 각 지적은 [심각/권고/제안] 라벨을 붙여라
- 코드 예시 없는 지적은 금지
- 수정은 절대 하지 마라. 의견만 출력
```

핵심 필드:

| 필드 | 의미 |
|---|---|
| `name` | 호출 시 식별자 (Task tool로 `subagent_type: reviewer`) |
| `description` | 다른 에이전트가 "언제 너를 부를지" 판단하는 근거 |
| `tools` | 도구 화이트리스트 — 좁힐수록 안전 |
| `model` | 작업 난이도에 맞는 모델 (단순작업은 Haiku, 추론은 Opus) |

### 5-3. 팀 워크플로우 명령 (`commands/ship-it.md`)

```markdown
---
name: ship-it
description: 변경사항을 researcher → implementer → reviewer → doc-writer 순서로 처리해 PR까지 만든다
---

다음 순서로 진행해. 각 단계는 Task tool 로 해당 sub-agent를 호출해.

1. **researcher** — 변경 대상 영역의 기존 코드/관행 조사 (200자 요약)
2. **implementer** — 위 조사 결과를 받아 실제 구현. 테스트 포함
3. **reviewer** — git diff 기반 리뷰. 심각 지적이 있으면 implementer에게 다시 위임
4. **doc-writer** — CHANGELOG 항목 1줄 + README 영향 부분 갱신
5. 마지막에 PR 본문 초안을 출력 (사용자가 직접 push)

병렬화: 1번이 끝나면 2번 시작과 동시에 doc-writer에게 "예상 변경 요약" 을 미리 부탁할 수 있다.
```

이 한 줄: `/ship-it 결제 모듈에 retry 추가` 만으로 4명이 순차 동작합니다.

### 5-4. settings.json — 팀이 공유하는 설정

```jsonc
{
  "model": "claude-sonnet-4-6",
  "permissions": {
    "allow": [
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(npm test:*)",
      "Read(./**)",
      "WebFetch(domain:docs.anthropic.com)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(git push --force:*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "command": ".claude/hooks/log-bash.sh" }
    ],
    "Stop": [
      { "command": ".claude/hooks/notify-done.sh" }
    ]
  },
  "env": {
    "ENV": "stg"
  }
}
```

핵심 포인트:

- **`permissions.allow` 에 자주 쓰는 안전 명령을 넣으면** 매번 묻지 않음
- **`deny` 는 강제 — allow보다 우선** 적용. 위험 명령은 무조건 차단
- **`hooks`** 로 PreToolUse(도구 호출 직전), Stop(세션 종료) 시점에 셸 스크립트 실행
- `env` 로 sub-agent 모두에게 동일 환경변수 전달

### 5-5. 설정 적용 우선순위

```
프로젝트 .claude/settings.local.json   (개인, .gitignore)
        │  ↑ 우선
프로젝트 .claude/settings.json         (팀 공유, git 포함)
        │  ↑ 우선
사용자 ~/.claude/settings.json         (전역 기본값)
```

**팀 공유 = `settings.json`, 개인 비밀 = `settings.local.json`** 으로 나누는 게 표준입니다.

### 5-6. 디버깅 팁 — 팀이 안 굴러갈 때

| 증상 | 첫 번째 점검 |
|---|---|
| sub-agent가 호출되지 않음 | `description` 이 모호하지 않은지. "언제 쓰는지"가 한 문장으로 분명해야 함 |
| 도구 권한 거부 반복 | `/permissions` 로 allow에 추가, 또는 settings.json `permissions.allow` |
| hook이 동작 안 함 | `chmod +x .claude/hooks/*.sh`, 그리고 `/hooks` 로 등록 확인 |
| 모델이 자꾸 다른 거 씀 | `/model` 로 강제, 또는 sub-agent별 `model` 필드 명시 |
| 컨텍스트 폭주 | sub-agent의 `tools` 를 좁히고, `description` 에 "결과는 200자 이내 요약" 명시 |

---

## 정리

이 챕터에서 다룬 것:

1. **잘 모르는 슬래시 명령 17개** — `/resume`, `/compact`, `/agents`, `/permissions`, `/hooks` 등
2. **입력창 단축키** — `!`, `#`, `@`, Shift+Tab(플랜 모드), Esc Esc(히스토리)
3. **CLI 옵션** — `--resume`, `-p` 파이프 모드, `--output-format json`
4. **세션 내 활용 패턴** — `!`+`#` 조합, `@` 다중 첨부, `/compact` 로 긴 세션 유지
5. **Agent Team 구성** — `.claude/{agents,skills,commands,hooks}/` + `settings.json` 표준 골격

다음 챕터([핵심 개념](core-concepts.md))에서는 이 명령들이 동작하는 **내부 모델 — 컨텍스트, 도구, 메모리** 를 다룹니다.
