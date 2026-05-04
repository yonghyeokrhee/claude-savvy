# 추천 입력 PDF 모음

`pdf-to-deck` Skill을 시연할 때 쓰기 좋은 공개 PDF 링크.
모두 직링크라 `scripts/fetch_pdf.py` 로 바로 받을 수 있다.

## AI / ML 고전 논문

| 제목 | URL | 추천 이유 |
|---|---|---|
| Attention Is All You Need (Transformer) | https://arxiv.org/pdf/1706.03762.pdf | 구조가 명확해 슬라이드 분할이 깔끔 |
| BERT | https://arxiv.org/pdf/1810.04805.pdf | 비교 표가 풍부 → Results 슬라이드 잘 나옴 |
| GPT-3 (Language Models are Few-Shot Learners) | https://arxiv.org/pdf/2005.14165.pdf | 길이가 길어 `extract_text.py` 데모용으로 좋음 |

## 산업 리포트 / 백서

| 제목 | URL | 추천 이유 |
|---|---|---|
| Stanford AI Index Report 2024 (Executive Summary) | https://aiindex.stanford.edu/wp-content/uploads/2024/04/HAI_AI-Index-Report-2024.pdf | 차트와 수치 위주 — 임원 보고용 덱 변환 데모 |
| Anthropic Responsible Scaling Policy | https://www-cdn.anthropic.com/files/4zrzovbb/website/2c5f094db75c5c4c2f0f62a27c7a9a7e3a4a6f70.pdf | 정책 문서 → 의사결정용 1페이지 요약 |

## 사용 예시

```
/pdf-to-deck

URL: https://arxiv.org/pdf/1706.03762.pdf
```

또는

```
~/Downloads/aiindex-2024.pdf 이걸로 발표 덱 만들어줘
```
