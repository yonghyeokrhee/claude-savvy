---
name: pdf-to-deck
description: PDF 논문/리포트/백서를 읽고 발표용 PPTX 슬라이드 덱으로 변환합니다. 사용자가 PDF 경로 또는 URL을 주면 핵심 메시지를 추출해 10~12장 분량의 발표 자료를 생성합니다.
allowed-tools: Bash, Read, Write, WebFetch
---

# PDF → 발표 덱 변환 Skill

PDF 한 편을 입력받아 **발표 가능한 PPTX**로 만드는 Skill입니다.
요약·구조화는 Claude가, 슬라이드 렌더링은 `python-pptx` 스크립트가 담당합니다.

## 입력

다음 중 하나:
- 로컬 PDF 경로 (예: `~/Downloads/attention.pdf`)
- PDF 직링크 URL (예: `https://arxiv.org/pdf/1706.03762.pdf`)

URL이면 먼저 `scripts/fetch_pdf.py <url> <out.pdf>` 로 다운로드해.

## 처리 순서

1. **PDF 텍스트 추출** — `Read` 도구로 PDF를 직접 읽거나, 길이가 30페이지를 넘으면
   `scripts/extract_text.py <pdf>` 로 본문만 추출.
2. **구조 설계** — 다음 표준 구조에 맞춰 슬라이드 outline을 만들어:

   | # | 슬라이드 | 내용 |
   |---|---|---|
   | 1 | Title | 제목 + 저자 + 한 줄 요약 |
   | 2 | Why this matters | 문제 정의 (3 bullet) |
   | 3 | Background | 사전 지식 / 기존 방식의 한계 |
   | 4 | Key Idea | 논문/문서의 핵심 아이디어 1문장 + 다이어그램 설명 |
   | 5-7 | Method | 방법을 단계별로 (각 슬라이드 3 bullet 이내) |
   | 8 | Results | 핵심 수치 / 비교 표 |
   | 9 | Limitations | 한계 또는 미해결 과제 |
   | 10 | Takeaways | 청중이 가져갈 3가지 |
   | 11 | References | 원문 링크 + 추가 자료 |

3. **JSON outline 작성** — 위 구조를 그대로 따라 `deck.json`을 생성:

   ```json
   {
     "title": "Attention Is All You Need",
     "subtitle": "Vaswani et al., 2017 — Transformer 아키텍처",
     "slides": [
       {"title": "Why this matters", "bullets": ["...", "...", "..."]},
       {"title": "Key Idea", "bullets": ["...", "..."], "note": "발표자 노트"}
     ]
   }
   ```

4. **PPTX 렌더링** — 다음 명령 실행:

   ```bash
   python3 .claude/skills/pdf-to-deck/scripts/build_deck.py \
     --outline deck.json \
     --output deck.pptx
   ```

5. **결과 보고** — 생성된 `.pptx` 경로와 슬라이드 수, 그리고 outline 미리보기를
   사용자에게 출력해.

## 작성 원칙

- **한 슬라이드 = 한 메시지.** bullet은 슬라이드당 최대 3개, 각 30자 이내.
- **숫자 살리기.** 결과 슬라이드는 정성 표현보다 정량 수치 위주.
- **발표자 노트(`note`)** 에는 그 슬라이드를 1분간 말로 풀 때 쓸 문장을 적어.
- 원문 인용은 짧게, 출처 페이지 번호를 함께 표기.

## 트러블슈팅

| 오류 | 원인 | 조치 |
|---|---|---|
| `ModuleNotFoundError: pptx` | python-pptx 미설치 | `pip install python-pptx pypdf requests` |
| PDF 본문이 비어있음 | 스캔본 (이미지 PDF) | 사용자에게 OCR된 PDF가 필요하다고 알리고 종료 |
| URL 404 | 링크 만료 | 사용자에게 새 링크 요청 |

## 참조 문서

추가 디자인 가이드는 필요할 때만 읽어 (Progressive Disclosure):

- `references/style-guide.md` — 폰트/색상/여백 규칙
- `references/pdf-sources.md` — 추천 입력 PDF 모음 (강의 예제용)
