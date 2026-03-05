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

---

# MOP 월간 성과 보고서

## 핵심 요약
(전체 성과를 3줄 이내로 요약)

## 잘 되고 있는 캠페인
(ROAS 300% 이상 캠페인 목록 — 캠페인명 / ROAS / 한 줄 코멘트)

## 개선이 필요한 캠페인
(ROAS 200% 미만 캠페인 목록 — 캠페인명 / ROAS / 원인 추정)

## 예산 제안
(다음 달 예산 배분 조정 제안 — 채널별 증감 방향)

## 다음 달 액션 아이템
1. (가장 시급한 조치)
2. (두 번째 조치)
3. (세 번째 조치)

---

보고서는 마케터가 바로 팀에 공유할 수 있도록 간결하고 명확하게 작성해줘.
