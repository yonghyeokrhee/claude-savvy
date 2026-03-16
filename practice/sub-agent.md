# Sub-Agent 실습

Sub-Agent가 실제로 어떻게 동작하는지 확인합니다. 3개의 전문 분석 에이전트가 **서로 다른 색상**으로 동시에 실행되는 모습을 관찰합니다.

## 준비

`practice/` 디렉토리에 아래 파일들이 있어야 합니다:

```
practice/
├── data/
│   ├── campaign-search.md    # 검색광고 현황
│   ├── campaign-shopping.md  # 쇼핑검색광고 현황
│   └── budget-usage.md       # 예산 집행 현황
└── .claude/
    └── agents/
        ├── search-analyst.md    # 검색광고 분석가 (파란색)
        ├── shopping-analyst.md  # 쇼핑검색 분석가 (초록색)
        └── budget-analyst.md    # 예산 분석가 (노란색)
```

`practice/` 에서 Claude를 시작합니다:

```bash
cd practice
claude
```

---

## 실습 1 — Sub-Agent 없이 순차 처리

먼저 파일 하나씩 분석을 요청합니다:

```
campaign-search.md 파일을 읽고 문제 캠페인이 뭔지 알려줘
```

Claude가 파일 1개를 읽고 답합니다. 왼쪽 도구 목록에서 `Read` 1번 실행되는 걸 확인합니다.

---

## 실습 2 — 3개 Sub-Agent 병렬 실행

이번엔 3명의 전문 분석가를 동시에 실행합니다:

```
검색광고, 쇼핑검색광고, 예산 현황을 각각 전문 에이전트로 동시에 심층 분석해줘.
각 분석 결과를 data/ 폴더에 별도 파일로 저장하고, 마지막에 종합 의견을 알려줘.
```

### 관찰 포인트

왼쪽 패널에 **3개 Agent가 서로 다른 색상**으로 동시에 나타납니다:

```
┌─────────────────────────────────────┐
│  🔵 search-analyst    실행 중...     │
│  🟢 shopping-analyst  실행 중...     │
│  🟡 budget-analyst    실행 중...     │
└─────────────────────────────────────┘
```

각 Agent가 독립적으로 작업하는 모습을 관찰합니다:

| Agent | 색상 | 하는 일 |
|---|---|---|
| search-analyst | 파란색 | 데이터 파일 4개 읽기 → 검색광고 심층 분석 → 보고서 작성 |
| shopping-analyst | 초록색 | 데이터 파일 4개 읽기 → 쇼핑검색 심층 분석 → 보고서 작성 |
| budget-analyst | 노란색 | 데이터 파일 4개 읽기 → 예산 최적화 분석 → 보고서 작성 |

> **이전 실습과 다른 점:** `/mop-report`은 단순히 Read를 3번 병렬 호출할 뿐이라 눈 깜짝할 사이에 끝났습니다. 이번엔 각 Agent가 **4개 파일을 읽고, 교차 분석하고, 보고서까지 작성**하므로 실행 과정을 충분히 관찰할 수 있습니다.

### 결과 확인

3개 Agent가 모두 완료되면 `data/` 폴더에 보고서 3개가 생성됩니다:

```bash
ls data/analysis-*.md
```

```
data/analysis-search.md     # 검색광고 심층 분석 보고서
data/analysis-shopping.md   # 쇼핑검색 심층 분석 보고서
data/analysis-budget.md     # 예산 최적화 분석 보고서
```

그리고 메인 Claude가 3개 보고서를 종합한 **Executive Summary**를 화면에 출력합니다.

---

## 실습 3 — Skill로 한 번에 실행

매번 긴 프롬프트를 입력하는 대신, Skill을 사용합니다:

```
/mop-deep-analysis
```

한 단어로 동일한 3-Agent 병렬 분석이 실행됩니다.

> `/mop-deep-analysis` Skill은 내부적으로 Claude에게 "3개 Agent를 동시에 실행하라"고 지시합니다. Skill과 Sub-Agent가 결합된 패턴입니다.

---

## 실습 결과 비교

| | 실습 1 (순차) | 실습 2 (병렬 Sub-Agent) |
|---|---|---|
| Agent 수 | 0 (메인만) | 3개 |
| 파일 읽기 | 1개 | 4개 × 3 = 12개 (중복 포함) |
| 출력물 | 화면 답변 1개 | 보고서 파일 3개 + Executive Summary |
| 색상 표시 | 없음 | 파랑 / 초록 / 노랑 |
| 소요 시간 | ~5초 | ~15초 (하지만 3배의 작업량) |
| 적합한 상황 | 빠른 확인 | 다각도 심층 분석 |

---

## 핵심 정리

**Sub-Agent는 단순한 병렬 읽기가 아닙니다.**

| 병렬 Read (기존 /mop-report) | Sub-Agent (이번 실습) |
|---|---|
| 메인 Claude가 Read를 3번 동시 호출 | 별도 Claude 인스턴스 3개가 독립 실행 |
| 파일 내용이 메인 컨텍스트에 쌓임 | 각 Agent가 자기 컨텍스트에서 처리 |
| 간단한 작업에 적합 | 복잡한 분석 작업에 적합 |
| 색상 구분 없음 | Agent마다 다른 색상 |

Sub-Agent의 진짜 가치는 **컨텍스트 격리**입니다. 12개 파일 읽기 + 3개 보고서 작성을 메인 Claude 하나로 하면 컨텍스트가 오염되지만, Sub-Agent 3개로 나누면 각자 깔끔한 환경에서 집중합니다.
