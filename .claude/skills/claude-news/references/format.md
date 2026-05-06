# 출력 마크다운 템플릿

## 헤더

```
🔔 Claude Code 최근 4주 동향 ({YYYY-MM-DD} 기준)
```

키워드 필터가 있으면:
```
🔔 Claude Code 최근 동향 — 키워드: "{keyword}" ({YYYY-MM-DD})
```

## 본문 표

```
| 날짜 | 카테고리 | 항목 | 요약 | 링크 |
|---|---|---|---|---|
| 2026-04-13 | [공식] | /effort xhigh | Opus 4.7 추론 강도 다이얼 | https://... |
```

## 카테고리 배지

- `[공식]` — docs.claude.com / anthropic.com
- `[블로그]` — Anthropic news 포스트, 공식 미디엄
- `[커뮤니티]` — Reddit / HN / dev.to / X / 개인 블로그
- `[경쟁사]` — Cursor / Codex / Aider / Cline / Windsurf 등

비공식 출처는 항목 끝에 `⚠ 검증 필요` 부착.

## 푸터

```
📌 다음 보강 후보
- {gitbook-page}.md — 신규 명령 X, Y 섹션 추가
- 신규 페이지 — {새 기능} 별도 챕터 검토
```

## 작성 규칙

- 한 줄 요약은 40자 이내
- 날짜 형식: `YYYY-MM-DD`
- 동일 항목이 여러 출처에 있으면 공식 우선, 나머지는 합치기
- 결과 0건이면 "최근 4주간 새 변경 없음" 명시
