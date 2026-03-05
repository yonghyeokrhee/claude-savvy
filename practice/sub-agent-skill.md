# Sub-Agent를 활용하는 Skill 만들기

Skill과 Sub-Agent를 함께 쓰면 반복 작업을 한 번에 자동화할 수 있습니다.
이번 실습에서는 `/mop-report` 한 번으로 3개 파일을 동시에 분석하고 보고서까지 생성하는 Skill을 만듭니다.

---

## 구조 이해

일반 Skill은 Claude에게 프롬프트를 전달합니다.
여기에 **"동시에 읽어줘"** 같은 지시를 넣으면 Claude가 Sub-Agent를 생성해 병렬로 처리합니다.

```
/mop-report 입력
    ↓
SKILL.md 프롬프트 로드
    ↓
Claude가 판단: "3개 파일은 독립적 → 동시에 처리"
    ├── Sub-Agent 1: campaign-search.md 읽기
    ├── Sub-Agent 2: campaign-shopping.md 읽기
    └── Sub-Agent 3: budget-usage.md 읽기
         ↓
    결과 취합 → report-monthly.md 생성
```

---

## Skill 파일 구조

`practice/.claude/skills/mop-report/SKILL.md`:

```markdown
---
name: mop-report
description: data 폴더의 캠페인 파일을 병렬로 분석해 월간 종합 보고서를 생성합니다
allowed-tools: Read, Write
---

data/ 폴더에 있는 아래 3개 파일을 **동시에** 읽어줘:
- data/campaign-search.md
- data/campaign-shopping.md
- data/budget-usage.md

파일을 모두 읽은 뒤, 다음 형식으로 `report-monthly.md` 파일을 생성해줘:

(보고서 형식 지정...)
```

**포인트:**
- `allowed-tools: Read, Write` — 파일 읽기와 쓰기만 허용 (불필요한 권한 차단)
- `**동시에** 읽어줘` — Claude가 Sub-Agent로 병렬 처리하도록 유도
- 출력 형식을 구체적으로 지정 — 매번 다른 형식으로 나오는 것 방지

---

## 실습 순서

### 1단계 — practice 폴더에서 Claude 시작

```bash
cd practice
claude
```

### 2단계 — Skill 호출

```
/mop-report
```

### 3단계 — 관찰 포인트

왼쪽 도구 목록에서 확인:

| 관찰 항목 | 확인 내용 |
|---|---|
| `Read` 실행 횟수 | 3번이 거의 동시에 실행되는지 |
| `Write` 실행 | `report-monthly.md` 파일이 생성되는지 |
| 전체 처리 시간 | 3개 파일을 순서대로 읽을 때보다 빠른지 |

### 4단계 — 결과 확인

```bash
cat report-monthly.md
```

보고서가 정해진 형식대로 생성되었는지 확인합니다.

---

## Skill에서 Sub-Agent를 유도하는 방법

Skill 프롬프트에 아래 표현을 쓰면 Claude가 병렬 처리를 선택합니다:

| 표현 | 효과 |
|---|---|
| `동시에 읽어줘` | 파일 여러 개를 병렬 읽기 |
| `각각 분석해줘` | 항목별 독립 분석 |
| `모든 파일을 한 번에 확인해줘` | 폴더 내 전체 병렬 탐색 |

반대로 **순서가 중요할 때**는 명시적으로 순서를 지정합니다:

```markdown
1. 먼저 campaign-search.md를 읽고
2. 그 결과를 바탕으로 budget-usage.md를 분석해줘
```

---

## 정리

| | 기본 Skill | Sub-Agent 활용 Skill |
|---|---|---|
| 처리 방식 | 순차 실행 | 병렬 실행 |
| 적합한 작업 | 단일 파일, 단계별 작업 | 독립적인 여러 파일 분석 |
| 속도 | 파일 수에 비례 | 파일 수에 관계없이 일정 |
| 작성 방법 | 일반 프롬프트 | "동시에", "각각" 표현 추가 |
