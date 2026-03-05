# 핵심 개념

## Claude Code의 작동 방식

Claude Code는 터미널에서 실행되며 로컬 파일 시스템에 직접 접근한다. 다음과 같은 작업이 가능하다:

- 프로젝트 내 파일 읽기/쓰기
- 셸 명령 실행 (승인 후)
- glob·grep 패턴으로 코드 검색
- 웹 브라우징 및 URL 내용 가져오기
- 세션 내 대화 컨텍스트 유지

## 권한 모드

Claude Code는 잠재적으로 위험한 작업을 실행하기 전에 승인을 요청한다. 세 가지 모드로 제어할 수 있다:

- **자동 승인** — 묻지 않고 실행 (주의해서 사용)
- **수동 승인** — 파일 쓰기 또는 명령 실행 시 직접 확인
- **읽기 전용** — 읽기만 허용, 수정 불가

## CLAUDE.md — 프로젝트 지침서

프로젝트 루트에 `CLAUDE.md` 파일을 두면 Claude가 매 세션 시작 시 자동으로 읽는다:

```markdown
# 내 프로젝트

## 기술 스택
- Python 3.12, FastAPI, PostgreSQL

## 컨벤션
- 변수명: snake_case
- 모든 함수에 타입 힌트 필수
- 커밋 전 `pytest` 실행

## 중요 파일
- `src/main.py` — 진입점
- `src/config.py` — 환경 설정
```

`CLAUDE.md`를 활용하면 좋은 경우:
- 기술 스택과 아키텍처 설명
- 코딩 컨벤션 및 스타일 규칙 정의
- 중요 파일 위치 안내
- 테스트·빌드 실행 방법 명시

## 컨텍스트 창

Claude Code는 세션 내 대화 내용을 컨텍스트로 유지한다. 세션이 길어질 때:

- `/clear` — 컨텍스트 초기화 (파일은 그대로 유지)
- 요청을 구체적으로 — 집중된 요청일수록 결과가 좋다
- 큰 작업은 작은 단계로 나눠서 진행

## Claude가 내부적으로 사용하는 도구

Claude Code는 상황에 따라 아래 도구를 자동으로 선택해 사용한다:

| 도구 | 역할 |
|---|---|
| Read | 파일 내용 읽기 |
| Write | 파일 생성 또는 덮어쓰기 |
| Edit | 기존 파일 부분 수정 |
| Bash | 셸 명령 실행 |
| Glob | 패턴으로 파일 검색 |
| Grep | 파일 내용 검색 |
| WebSearch | 웹 검색 |
| WebFetch | URL 내용 가져오기 |

## Skill

**Skill**은 `/skill-name` 형태로 호출하는 재사용 가능한 프롬프트 워크플로우다. 반복 작업을 명령어 하나로 자동화하고, `.claude/skills/` 폴더에 저장하여 팀 전체가 공유할 수 있다.

```
/review      → 코드 리뷰 실행
/standup     → 스탠드업 자동 작성
/deploy-check → 배포 전 체크리스트 확인
```

Skill 파일은 `SKILL.md`로 작성하며, frontmatter의 `description`을 보고 Claude가 적절한 상황에서 자동으로 선택하기도 한다.

> 자세한 내용 → [Skills](skills.md) · [Skill 직접 만들기](skills-practice.md)
>
> 참조: [FastCampus — Clip 1: Slash Command 만들기](https://goobong.gitbook.io/fastcampus/part-1.-ai-claude-code/chapter3_claude_code_-_/clip1_slash_command_-_)

## Agent vs Workflow

Claude Code를 활용할 때 작업의 성격에 따라 접근 방식이 달라진다.

| 구분 | Workflow | Agent |
|---|---|---|
| 제어 방식 | 사전 정의된 순서 | 동적 의사결정 |
| 예측 가능성 | 높음 | 낮음 |
| 유연성 | 낮음 | 높음 |
| 적합한 작업 | 문서 파이프라인, ETL, 정기 리포트 | 코드 리뷰, 리서치, 복잡한 문제 해결 |

**Workflow**: 단계가 미리 정해진 반복 가능한 작업에 사용. 디버깅과 모니터링이 쉽다.

**Agent**: 해결 경로를 미리 알 수 없는 개방형 문제에 사용. 스스로 도구를 선택하고 경로를 결정한다.

> *"가장 정교한 시스템이 아니라, 요구사항에 맞는 올바른 시스템을 구축하는 것이 중요하다."*
> — Anthropic, Building Effective Agents

실제로는 두 방식을 결합하는 하이브리드 접근이 효과적인 경우가 많다: Workflow로 데이터를 전처리하고, Agent가 분석하고, Workflow로 결과를 포맷팅하는 방식.

> 자세한 내용 → [Workflow](workflow.md) · [Sub-Agent](sub-agent.md)
>
> 참조: [FastCampus — Clip 1: Agent vs Workflow 개념 이해하기](https://goobong.gitbook.io/fastcampus/part-2.-agent/chapter1_agent_-_/clip1_agent_vs_workflow_-_)
