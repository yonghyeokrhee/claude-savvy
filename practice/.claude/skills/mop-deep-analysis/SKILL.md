---
name: mop-deep-analysis
description: 3명의 전문 분석가 에이전트(검색광고/쇼핑검색/예산)를 동시에 실행하여 MOP 캠페인 심층 분석을 수행합니다
allowed-tools: Agent, Read, Write
---

아래 3개 분석 작업을 **각각 별도의 Agent**로 **반드시 동시에** 실행해줘.
3개 Agent가 병렬로 실행되어야 합니다.

## Agent 1 — 검색광고 분석가 (search-analyst)

search-analyst 에이전트를 사용해서:
- CLAUDE.md를 읽고 MOP 서비스 맥락 파악
- data/ 폴더의 모든 .md 파일을 읽기
- 검색광고 캠페인별 심층 분석 수행
- 쇼핑검색 데이터와의 비교 분석 포함
- 분석 결과를 `data/analysis-search.md`에 작성

## Agent 2 — 쇼핑검색 분석가 (shopping-analyst)

shopping-analyst 에이전트를 사용해서:
- CLAUDE.md를 읽고 MOP 서비스 맥락 파악
- data/ 폴더의 모든 .md 파일을 읽기
- 쇼핑검색광고 캠페인별 심층 분석 수행
- 검색광고 대비 효율성 비교 분석 포함
- 분석 결과를 `data/analysis-shopping.md`에 작성

## Agent 3 — 예산 분석가 (budget-analyst)

budget-analyst 에이전트를 사용해서:
- CLAUDE.md를 읽고 MOP 서비스 맥락 파악
- data/ 폴더의 모든 .md 파일을 읽기
- 채널별 예산 효율성 교차 분석 수행
- 3월 예산 시나리오 3가지 작성
- 분석 결과를 `data/analysis-budget.md`에 작성

## 완료 후

3개 보고서가 모두 완료되면:
1. 각 보고서의 핵심 결론을 읽기
2. 3명의 분석가 의견을 종합하여 **경영진 보고용 Executive Summary**를 화면에 출력

Executive Summary 형식:
```
## Executive Summary — 2월 MOP 캠페인 종합 분석

### 핵심 발견 (3줄)
1.
2.
3.

### 채널별 한 줄 진단
- 검색광고: (search-analyst 핵심 결론)
- 쇼핑검색: (shopping-analyst 핵심 결론)
- 예산 배분: (budget-analyst 핵심 결론)

### 즉시 실행 액션 TOP 3
1.
2.
3.
```
