# Sub-Agent 직접 만들기

Sub-Agent는 특정 역할에 특화된 Claude 인스턴스입니다.
이번 실습에서는 MOP 캠페인 분석 전문 에이전트 `campaign-analyzer`를 직접 만들어봅니다.

---

## Sub-Agent vs Skill 차이

| | Skill | Sub-Agent |
|---|---|---|
| 역할 | 반복 작업을 단축키로 실행 | 특정 분야의 전문가 역할 |
| 호출 | `/skill-name` | 메인 Claude가 자동 판단해서 실행 |
| 특징 | 정해진 형식의 출력 | 고유한 성격과 판단 기준 보유 |
| 적합한 상황 | 포맷이 정해진 반복 작업 | 전문 지식이 필요한 분석 작업 |

---

## Step 1. 파일 위치

Sub-Agent 파일은 아래 두 곳에 저장합니다:

| 위치 | 경로 | 적용 범위 |
|---|---|---|
| 프로젝트 전용 | `.claude/agents/에이전트명.md` | 해당 프로젝트에서만 |
| 전역 | `~/.claude/agents/에이전트명.md` | 모든 프로젝트에서 |

이번 실습은 프로젝트 전용으로 만듭니다:

```bash
mkdir -p .claude/agents
```

---

## Step 2. Agent 파일 작성

`.claude/agents/campaign-analyzer.md`:

```markdown
---
name: campaign-analyzer
description: MOP 캠페인 데이터를 분석하고 개선 제안을 제공하는 전문 에이전트.
             ROAS, CTR, 예산 효율을 기준으로 평가하고 즉시 실행 가능한 액션을 제안한다.
tools: Read, Write
model: sonnet
color: purple
---

당신은 MOP 광고 성과 분석 전문가입니다.

## 역할
- ROAS 300% 이상 = 우수 / 200~300% = 보통 / 200% 미만 = 개선 필요
- 마케터 언어로 설명 (개발 용어 사용 금지)
- 제안은 즉시 실행 가능한 형태로

## 분석 형식
1. 한 줄 요약
2. 잘 되고 있는 것 (수치 포함)
3. 문제 캠페인 (원인 추정)
4. 이번 주 액션 1~3가지
```

### Frontmatter 항목 설명

| 항목 | 역할 | 비고 |
|---|---|---|
| `name` | 에이전트 식별자 | 영문 소문자, 하이픈 사용 |
| `description` | 언제 이 에이전트를 쓸지 Claude가 판단하는 기준 | 구체적일수록 정확히 호출됨 |
| `tools` | 허용할 도구 목록 | 필요한 것만 최소로 지정 |
| `model` | 사용할 Claude 모델 | `sonnet` / `haiku` 선택 가능 |
| `color` | Claude Code UI에서 표시되는 색상 | 선택 사항 |

---

## Step 3. 실행 확인

`practice/` 폴더에서 Claude를 시작합니다:

```bash
cd practice
claude
```

아래 두 가지 방식으로 호출해봅니다:

**방법 1 — 직접 지정:**
```
campaign-analyzer 에이전트를 써서 data/campaign-search.md를 분석해줘
```

**방법 2 — Claude가 자동 선택:**
```
2월 검색광고 캠페인 성과를 전문적으로 분석해줘
```

두 번째 방법에서 Claude가 `description`을 보고 `campaign-analyzer`를 자동으로 선택하는지 확인합니다.

---

## Step 4. 여러 Sub-Agent 동시 실행

에이전트가 2개 이상이면 병렬 처리가 가능합니다. 만약 `budget-analyzer` 에이전트도 만든다면:

```
검색광고와 예산 현황을 각각 전문 에이전트로 동시에 분석해줘
```

```
메인 Claude
    ├── campaign-analyzer → data/campaign-search.md 분석
    └── budget-analyzer   → data/budget-usage.md 분석
         ↓
    결과 취합 → 종합 의견 제시
```

---

## Sub-Agent를 잘 만드는 핵심

**`description`이 가장 중요합니다.**
Claude가 어떤 상황에서 이 에이전트를 써야 하는지 `description`만 보고 판단합니다.
애매하면 에이전트가 있어도 호출되지 않습니다.

```markdown
# 나쁜 예
description: 캠페인 분석 에이전트

# 좋은 예
description: MOP 캠페인 데이터를 분석하고 개선 제안을 제공하는 전문 에이전트.
             ROAS, CTR, 예산 효율을 기준으로 평가하고 즉시 실행 가능한 액션을 제안한다.
```

**시스템 프롬프트(본문)에 판단 기준을 명시합니다.**
에이전트가 일관된 기준으로 판단하도록 수치 기준, 출력 형식, 금지 사항을 적어둡니다.
