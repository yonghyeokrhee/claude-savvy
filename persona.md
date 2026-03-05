# Persona & Output Style

## 개념

Claude Code는 기본적으로 범용 어시스턴트로 동작하지만, **Persona**를 주입하면 특정 역할에 맞는 전문성과 커뮤니케이션 스타일로 고정시킬 수 있다.

같은 질문을 해도:
- **CS Expert** 페르소나 → 고객 응대 관점에서 데이터 조회 후 간결한 답변
- **Product Manager** 페르소나 → 사용자 문제와 비즈니스 임팩트 중심의 답변

## 동작 방식

Claude Code CLI의 `--append-system-prompt` 옵션을 사용한다. 페르소나 파일 내용을 시스템 프롬프트에 추가하면 세션 전체에 걸쳐 역할이 유지된다.

```bash
claude --append-system-prompt "$(cat ~/.claude/profiles/cs-expert.md)"
```

`--system-prompt`(전체 교체)와 달리 `--append-system-prompt`는 Claude Code의 기본 동작은 유지하면서 역할만 추가한다.

## 프로필 파일 구조

프로필은 `~/.claude/profiles/` 또는 `.claude/profiles/`에 마크다운 파일로 저장한다:

```
~/.claude/profiles/
├── cs-expert.md
├── data-engineer.md
├── oracle-analyst.md
└── product-manager.md
```

### 프로필 파일 템플릿

```markdown
# 역할 이름

## 페르소나
역할, 전문성, 배경을 설명한다.

## 커뮤니케이션 스타일
- 언어 설정 (한국어/영어)
- 톤과 상세 수준

## 역할
- 주요 책임과 업무

## 원칙
- 지켜야 할 규칙과 컨벤션
```

### 실제 예시 — CS Expert

```markdown
# CS Expert 프로필

## 페르소나
고객 문제 해결 및 고객 응대 전문가.
서비스 내부 데이터에 접근하여 고객의 문제를 해결한다.

## 커뮤니케이션 스타일
- 한국어로 소통, 기술 용어는 영어 원문 병기
- 결과 중심으로 설명, 지나치게 복잡한 원인 분석 지양

## 역할
- 서비스 내부 데이터 조회 및 설정 확인
- Engineer·PM과의 커뮤니케이션 브릿지

## 원칙
- 반드시 정확한 수치 기반으로 답변
- 잘 모를 때는 피드백 질문으로 명확히 소통
```

## ccp — 프로필 런처

매번 긴 옵션을 입력하는 대신, `ccp` 명령어로 프로필을 선택해 Claude를 실행한다. 터미널 색상도 프로필별로 자동 변경된다.

```bash
# ~/.zshrc에 추가
source "$HOME/.claude/claude-profile.sh"
```

```bash
ccp cs      # CS Expert        (네이비 테마)
ccp pm      # Product Manager  (보라 테마)
ccp data    # Data Engineer     (초록 테마)
ccp oracle  # Oracle Analyst    (붉은 테마)

ccp list    # 전체 프로필 목록
ccp reset   # 터미널 색상 초기화
```

세션 종료 시 터미널 색상은 자동으로 원래대로 복원된다.

## 프로필별 터미널 테마

| 프로필 | 배경색 | 강조색 | 용도 |
|---|---|---|---|
| cs-expert | `#1a1b2e` (다크 네이비) | `#7aa2f7` (블루) | 고객 지원 |
| product-manager | `#1a1520` (다크 퍼플) | `#c084fc` (바이올렛) | 기획/PM 업무 |
| data-engineer | `#0d1117` (다크 그레이) | `#3fb950` (그린) | 데이터 처리 |
| oracle-analyst | `#1c1210` (다크 브라운) | `#ff6347` (레드) | DB 분석 |

터미널 색상은 OSC 이스케이프 시퀀스를 사용하며 Ghostty·iTerm2에서 동작한다.

## Output Style과의 차이

| 구분 | Persona | Output Style |
|---|---|---|
| 목적 | 역할과 전문성 정의 | 응답 형식과 길이 제어 |
| 적용 방식 | `--append-system-prompt` | CLAUDE.md 또는 프롬프트 내 지시 |
| 예시 | "CS 전문가처럼 답변" | "한 줄로만 답변", "표 형식으로 출력" |

두 가지를 함께 사용하면 **누가(Persona) + 어떻게(Output Style)** 답변할지 모두 제어할 수 있다.

## 언제 Persona를 쓸까?

- 같은 프로젝트에서 역할에 따라 다른 관점이 필요할 때
- 반복 작업에서 매번 역할 설명을 타이핑하고 싶지 않을 때
- 팀 내 특정 업무 표준(응대 방식, 보고 형식)을 Claude에게 강제할 때
