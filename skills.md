# Skills

## Skills이란?

**Skill**은 Claude Code에서 `/skill-name` 형태로 호출하는 **미리 정의된 프롬프트 워크플로우**입니다.

사용자가 `/support-explorer`라고 입력하면, Claude Code는 해당 Skill 파일을 읽고 프롬프트로 실행합니다. 복잡한 지시를 매번 타이핑하지 않아도 되는 **단축키** 같은 개념입니다.

## 폴더 구조

Skill은 `.md` 파일이 아니라 **디렉토리 안의 `SKILL.md`** 파일로 정의됩니다.

```
~/.claude/skills/              ← 전역 (모든 프로젝트에서 사용)
└── support-explorer/
    └── SKILL.md

.claude/skills/                ← 프로젝트 전용
└── support-explorer/
    └── SKILL.md
```

> 같은 이름의 Skill이 있으면 프로젝트 전용이 전역보다 우선합니다.

## SKILL.md 문법

SKILL.md는 두 부분으로 구성됩니다:

### 1. Frontmatter (선택)

파일 최상단에 `---`로 감싸는 YAML 메타데이터입니다.

```yaml
---
name: support-explorer
description: MOP 서비스를 처음 시작하는 사용자에게 맞춤 퀵스타트 가이드를 제공합니다
allowed-tools: WebFetch
---
```

| 필드 | 설명 |
|---|---|
| `name` | Skill 이름 (폴더명과 동일하게) |
| `description` | 언제 이 Skill을 쓰는지 설명. `/help`에서 목록으로 표시됨 |
| `allowed-tools` | 이 Skill이 사용할 수 있는 도구 제한 (쉼표 구분) |

### 2. 본문 (프롬프트)

Frontmatter 이후의 내용이 그대로 Claude에게 전달되는 프롬프트입니다. 일반 마크다운으로 작성합니다.

```markdown
---
name: daily-standup
description: 오늘의 스탠드업 내용을 git 기반으로 자동 작성합니다
allowed-tools: Bash
---

git log와 현재 수정 중인 파일을 확인하고 다음 형식으로 스탠드업을 작성해줘:

**어제 한 일**
- (최근 커밋 메시지 기준으로 요약)

**오늘 할 일**
- (현재 수정 중인 파일과 TODO 주석 기준으로 작성)

**블로커**
- 없음 (있으면 명시)
```

## 어떻게 동작하나요?

```
사용자: /support-explorer
    ↓
.claude/skills/support-explorer/SKILL.md 로드
    ↓
Frontmatter 파싱 → 허용 도구 적용
    ↓
본문 내용을 프롬프트로 실행
```

## 기본 제공 Skills

Claude Code는 자주 쓰는 작업을 위한 Skills를 기본으로 제공합니다:

| Skill | 설명 |
|---|---|
| `/commit` | 변경 내역을 분석해 커밋 메시지 작성 |
| `/help` | Claude Code 사용법 안내 |
| `/review` | 코드 리뷰 요청 |

## 언제 Skill을 써야 할까?

- 같은 작업을 반복적으로 요청할 때
- 팀원과 동일한 워크플로우를 공유하고 싶을 때
- 프롬프트가 길고 복잡해서 외우기 어려울 때
- 프로젝트 고유의 절차(배포 체크리스트, 코드 리뷰 기준 등)를 자동화할 때
