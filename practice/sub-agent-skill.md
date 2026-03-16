# Sub-Agent를 활용하는 Skill 만들기

Skill과 Sub-Agent를 함께 쓰면 반복 작업을 한 번에 자동화할 수 있습니다.

---

## 단순 버전: `/mop-report`

가장 기본적인 형태입니다. 3개 파일을 동시에 읽어 보고서를 생성합니다.

### 구조

```
/mop-report 입력
    ↓
SKILL.md 프롬프트 로드
    ↓
Claude가 판단: "3개 파일은 독립적 → 동시에 처리"
    ├── Read: campaign-search.md
    ├── Read: campaign-shopping.md
    └── Read: budget-usage.md
         ↓
    결과 취합 → report-monthly.md 생성
```

### Skill 파일

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

**한계:** 이 방식은 Read 도구를 3번 병렬 호출할 뿐입니다. 진짜 Sub-Agent(독립 Claude 인스턴스)가 아니라 **메인 Claude가 직접 처리**합니다. 파일 읽기만 하므로 순식간에 끝나서 병렬 실행을 관찰하기 어렵습니다.

---

## 발전 버전: `/mop-deep-analysis`

진짜 Sub-Agent 3개를 생성하여 **독립된 분석 작업**을 병렬로 실행합니다.

### 구조

```
/mop-deep-analysis 입력
    ↓
SKILL.md 프롬프트 로드
    ↓
Claude가 Agent 도구를 3번 동시 호출
    ├── 🔵 search-analyst  → 파일 4개 읽기 + 심층 분석 + 보고서 작성
    ├── 🟢 shopping-analyst → 파일 4개 읽기 + 심층 분석 + 보고서 작성
    └── 🟡 budget-analyst   → 파일 4개 읽기 + 심층 분석 + 보고서 작성
         ↓
    3개 보고서 취합 → Executive Summary 출력
```

### Skill 파일

`practice/.claude/skills/mop-deep-analysis/SKILL.md`:

```markdown
---
name: mop-deep-analysis
description: 3명의 전문 분석가 에이전트를 동시에 실행하여 MOP 캠페인 심층 분석을 수행합니다
allowed-tools: Agent, Read, Write
---

아래 3개 분석 작업을 **각각 별도의 Agent**로 **반드시 동시에** 실행해줘.

## Agent 1 — 검색광고 분석가 (search-analyst)
search-analyst 에이전트를 사용해서:
- data/ 폴더의 모든 파일을 읽고
- 검색광고 심층 분석 보고서를 `data/analysis-search.md`에 작성

## Agent 2 — 쇼핑검색 분석가 (shopping-analyst)
shopping-analyst 에이전트를 사용해서:
- data/ 폴더의 모든 파일을 읽고
- 쇼핑검색 심층 분석 보고서를 `data/analysis-shopping.md`에 작성

## Agent 3 — 예산 분석가 (budget-analyst)
budget-analyst 에이전트를 사용해서:
- data/ 폴더의 모든 파일을 읽고
- 예산 최적화 보고서를 `data/analysis-budget.md`에 작성

3개 보고서 완료 후, Executive Summary를 화면에 출력해줘.
```

### 핵심 차이: `allowed-tools`에 `Agent` 추가

```markdown
# /mop-report — Read와 Write만 허용
allowed-tools: Read, Write

# /mop-deep-analysis — Agent 도구까지 허용
allowed-tools: Agent, Read, Write
```

`Agent` 도구를 허용해야 Claude가 Sub-Agent를 생성할 수 있습니다. 이 한 줄이 "병렬 읽기"와 "병렬 분석"의 차이를 만듭니다.

---

## 두 방식 비교

| | `/mop-report` | `/mop-deep-analysis` |
|---|---|---|
| 처리 주체 | 메인 Claude 1개 | Sub-Agent 3개 |
| 도구 | Read, Write | Agent, Read, Write |
| 병렬 대상 | 파일 읽기 | 전체 분석 작업 |
| 실행 시간 | ~3초 | ~15초 |
| 출력물 | 보고서 1개 | 보고서 3개 + Executive Summary |
| 컨텍스트 | 모든 데이터가 메인에 쌓임 | 각 Agent가 독립 처리 |
| 색상 표시 | 없음 | 파랑 / 초록 / 노랑 |

---

## Skill에서 Sub-Agent를 유도하는 방법

### 1. `allowed-tools`에 Agent 추가

```markdown
allowed-tools: Agent, Read, Write
```

이것이 가장 중요합니다. Agent 도구가 허용되어야 Sub-Agent가 생성됩니다.

### 2. 작업을 명시적으로 분리

```markdown
# 좋은 예 — 작업이 명확히 분리됨
## Agent 1 — 검색광고 분석
## Agent 2 — 쇼핑검색 분석
## Agent 3 — 예산 분석

# 나쁜 예 — 하나의 큰 덩어리
모든 데이터를 분석하고 보고서를 만들어줘
```

### 3. "동시에" / "병렬로" 명시

```markdown
# 좋은 예
아래 3개 작업을 **각각 별도의 Agent**로 **동시에** 실행해줘

# 나쁜 예
아래 작업들을 해줘
```

### 4. 에이전트 이름 직접 지정

```markdown
# 좋은 예 — 어떤 Agent를 쓸지 명확
search-analyst 에이전트를 사용해서

# 보통 예 — Claude가 알아서 선택
검색광고를 분석해줘
```

---

## 실습 순서

### 1단계 — practice 폴더에서 Claude 시작

```bash
cd practice
claude
```

### 2단계 — 단순 버전 먼저

```
/mop-report
```

순식간에 끝나는 걸 확인합니다.

### 3단계 — 발전 버전 실행

```
/mop-deep-analysis
```

3개 Agent가 서로 다른 색상으로 동시에 실행되는 걸 관찰합니다.

### 4단계 — 결과 비교

```bash
# 단순 버전 결과
cat report-monthly.md

# 발전 버전 결과 — 3개 전문 보고서
cat data/analysis-search.md
cat data/analysis-shopping.md
cat data/analysis-budget.md
```

---

## 정리

| | 기본 Skill | Sub-Agent 활용 Skill |
|---|---|---|
| `allowed-tools` | `Read, Write` | `Agent, Read, Write` |
| 처리 방식 | 메인 Claude가 전부 처리 | 전문 Agent에게 위임 |
| 적합한 작업 | 단순 읽기 + 취합 | 복잡한 분석 + 개별 보고서 |
| 확장성 | 파일이 늘면 컨텍스트 부담 | Agent가 독립 처리하므로 확장 용이 |
