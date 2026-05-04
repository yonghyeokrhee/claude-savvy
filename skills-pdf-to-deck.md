# 실전 Skill — PDF를 발표 덱으로 변환하기

논문 한 편, 백서 한 권을 30분 안에 발표 자료로 만들어야 한다면?
이 챕터에서는 **PDF → PPTX 발표 덱**을 자동 생성하는 `pdf-to-deck` Skill을 만들어 봅니다.

> 단순 프롬프트 단축키를 넘어, **번들 스크립트 + 참조 문서 + Progressive Disclosure** 패턴을 모두 보여주는 예제입니다.

---

## 무엇을 만드나

```
/pdf-to-deck
> https://arxiv.org/pdf/1706.03762.pdf

→ Claude가 PDF를 읽고
→ 표준 발표 구조(11장)에 맞춰 outline JSON 생성
→ python-pptx 스크립트로 .pptx 렌더링
→ 발표자 노트까지 포함된 deck.pptx 결과물 산출
```

## 왜 이 Skill이 흥미로운가

| 패턴 | 이 Skill에서의 모습 |
|---|---|
| **번들 스크립트** | `scripts/fetch_pdf.py`, `extract_text.py`, `build_deck.py` 세 개를 SKILL.md에서 호출 |
| **Progressive Disclosure** | `references/style-guide.md`, `references/pdf-sources.md` 는 필요할 때만 읽힘 |
| **자동 트리거** | description에 "PDF 발표 덱 변환" 명시 → "이 PDF로 발표자료 만들어줘"라는 자연어로도 호출됨 |
| **결과물이 눈에 보임** | 프롬프트만 출력하는 Skill과 달리 `.pptx` 파일이 떨어짐 |

---

## 이 Skill이 만들어진 과정

이 챕터는 결과물만 보여주지 않습니다. **어떻게 0에서 시작해 위 구조에 도달했는지** 의 사고 과정을 그대로 따라갈 수 있도록 5단계로 풀어둡니다.

### 1단계 — 한 문장으로 목표 정의

가장 먼저 한 일은 SKILL.md를 쓰는 게 아니라 **목표를 한 문장으로 압축**하는 것입니다.

> "PDF 한 편을 입력받아 발표 가능한 PPTX로 만든다."

이 한 줄에서 이미 네 가지가 결정됩니다:
- 입력: PDF (로컬 또는 URL)
- 출력: `.pptx`
- 가공 단계: 텍스트 추출 → 구조 설계 → 렌더링
- "발표 가능한" 이라는 품질 기준 → 표준 구조가 필요

### 2단계 — Claude가 잘하는 일 / 못하는 일 나누기

Skill의 본질은 **Claude의 지능 + 결정적 도구의 조합**입니다.
역할을 분리해보면:

| 작업 | 누가 잘하나 | 결론 |
|---|---|---|
| PDF 본문 의미 파악 | Claude | 프롬프트로 처리 |
| 11장 outline 설계 | Claude | 프롬프트로 처리 |
| PDF 다운로드 | Python (`requests`) | 스크립트 |
| 텍스트 추출 | Python (`pypdf`) | 스크립트 |
| PPTX 렌더링 | Python (`python-pptx`) | 스크립트 |

→ **SKILL.md 한 개 + 스크립트 세 개** 라는 윤곽이 자연스럽게 잡힙니다.

### 3단계 — 폴더 골격 잡기

목표와 역할 분리가 끝나면 디렉토리부터 만듭니다. 코드는 아직 한 줄도 안 짭니다.

```bash
mkdir -p .claude/skills/pdf-to-deck/{scripts,references}
touch .claude/skills/pdf-to-deck/SKILL.md
touch .claude/skills/pdf-to-deck/requirements.txt
touch .claude/skills/pdf-to-deck/scripts/{fetch_pdf,extract_text,build_deck}.py
touch .claude/skills/pdf-to-deck/references/{style-guide,pdf-sources}.md
```

`scripts/` 와 `references/` 를 분리한 이유:

- `scripts/` — Claude가 **실행**할 파일 (Bash로 호출)
- `references/` — Claude가 **필요할 때만 읽을** 파일 (Progressive Disclosure)

이 구분이 컨텍스트 윈도우를 절약하는 핵심입니다.

### 4단계 — SKILL.md 먼저, 스크립트는 나중

직관과 반대지만 **SKILL.md를 먼저** 쓰는 게 좋습니다. 왜냐하면 SKILL.md를 쓰면서 "여기서 어떤 입력이 필요하고, 어떤 출력을 받을까"가 정해지고, 그게 곧 스크립트의 인터페이스가 되기 때문입니다.

SKILL.md에 한 줄을 적는 순간:

```markdown
python3 .claude/skills/pdf-to-deck/scripts/build_deck.py \
  --outline deck.json --output deck.pptx
```

→ `build_deck.py` 의 **CLI 시그니처가 확정**됩니다. (`--outline`, `--output` 인자)

→ outline의 **JSON 스키마도 확정**됩니다 (`title`, `subtitle`, `slides[].{title,bullets,note}`).

이후 스크립트 작성은 그저 그 계약을 구현하는 일이 됩니다.

### 5단계 — Claude와 같이 만들기 (vibe coding)

마지막 단계는 SKILL.md에 적힌 **계약**을 Claude에게 보여주고 스크립트를 같이 짜는 것입니다.

```
.claude/skills/pdf-to-deck/SKILL.md를 읽고
scripts/build_deck.py를 만들어줘.

요구사항:
- 입력: --outline deck.json, --output deck.pptx
- 16:9 (13.33 x 7.5 inch)
- 제목 슬라이드 + 본문 슬라이드 (제목 + bullet 최대 3개)
- 발표자 노트(notes) 지원
- references/style-guide.md의 색상·폰트 규칙 적용
```

이때 `references/style-guide.md` 를 먼저 작성해두면 Claude가 그걸 참고해 일관된 스타일로 구현합니다. **참조 문서가 명세서 역할**을 합니다.

### 만드는 과정 요약

```
목표 한 줄    →   역할 분리      →   폴더 골격     →   SKILL.md 작성    →   스크립트 구현
(1단계)        (Claude vs 스크립트)  (scripts/+references/)  (계약 정의)        (계약 구현)
```

이 순서를 지키면 Skill이 산만해지지 않고, 추가 기능도 SKILL.md를 먼저 수정해서 계약부터 바꾸는 식으로 안전하게 확장할 수 있습니다.

---

## 디렉토리 구조

```
.claude/skills/pdf-to-deck/
├── SKILL.md                   ← Claude가 읽는 지시서 (계약서)
├── requirements.txt           ← python-pptx, pypdf, requests
├── scripts/                   ← 실행 영역 (Bash로 호출)
│   ├── fetch_pdf.py           ← URL → 로컬 PDF
│   ├── extract_text.py        ← PDF → 페이지별 텍스트
│   └── build_deck.py          ← outline JSON → .pptx
└── references/                ← 참조 영역 (필요할 때만 Read)
    ├── style-guide.md         ← 폰트/색/여백 규칙
    └── pdf-sources.md         ← 추천 입력 PDF 모음
```

`practice/.claude/skills/pdf-to-deck/` 에 실제 파일이 들어 있습니다.

### 각 파일의 역할 — 한눈에

| 파일 | 누가 읽나 | 언제 읽히나 | 역할 |
|---|---|---|---|
| `SKILL.md` | Claude | `/pdf-to-deck` 호출 시 항상 | 전체 워크플로우 + 출력 형식 + 트러블슈팅 |
| `scripts/*.py` | Bash 셸 | SKILL.md 지시로 실행될 때만 | 결정적인 파일 변환 작업 |
| `references/*.md` | Claude | "색 바꿔줘" 같은 후속 요청 시에만 | 명세서·자원·예시 — 평소엔 컨텍스트 절약 |
| `requirements.txt` | pip | 최초 설치 시 1회 | 의존성 고정 |

### 실행 흐름 다이어그램

```
사용자: /pdf-to-deck https://arxiv.org/pdf/1706.03762.pdf
         │
         ▼
┌─────────────────────────────────────┐
│ Claude Code가 SKILL.md 로드          │
│  - description, allowed-tools 적용   │
│  - 본문(워크플로우)을 프롬프트로 사용 │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Step 1. fetch_pdf.py <url> attention.pdf │   ← Bash
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Step 2. Read attention.pdf           │   ← Claude가 직접 읽음
│         또는 extract_text.py (대용량) │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Step 3. Claude가 outline 설계        │   ← 11장 표준 구조 적용
│         deck.json 작성 (Write)        │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Step 4. build_deck.py                │   ← Bash
│         --outline deck.json          │
│         --output deck.pptx           │
└─────────────────────────────────────┘
         │
         ▼
   deck.pptx (12 slides + 발표자 노트)

  ※ "색을 회색 톤으로" 후속 요청이 오면
     → references/style-guide.md 를 그제서야 Read
```

### SKILL.md ↔ 스크립트 ↔ JSON outline 의 계약 관계

세 요소가 서로 어떻게 맞물리는지 보면 Skill이 왜 "안정적으로" 동작하는지 보입니다.

```
        ┌──────────────────────────┐
        │       SKILL.md           │
        │  "deck.json을 이 형식으로 │
        │   써서 build_deck.py에   │
        │   넘겨라"                 │
        └────────┬─────────────────┘
                 │ 정의
                 ▼
        ┌──────────────────────────┐
        │      deck.json (계약)     │
        │  { title, subtitle,      │
        │    slides:[{title,       │
        │    bullets, note}] }     │
        └────────┬─────────────────┘
        Claude가  │   build_deck.py가
        이 형식으로│   이 형식을
        쓴다       │   읽는다
                 ▼
        ┌──────────────────────────┐
        │     build_deck.py        │
        │  --outline deck.json     │
        │  --output deck.pptx      │
        └──────────────────────────┘
```

**`deck.json` 이 인터페이스**입니다. Claude는 자유롭게 외형(예쁜 outline)을 만들고, 스크립트는 그걸 결정적으로 렌더링합니다. 둘 사이가 JSON으로 분리돼 있어, 한쪽을 바꿔도 다른 쪽이 깨지지 않습니다.

---

## Step 1. 의존성 설치

```bash
cd practice
pip install -r .claude/skills/pdf-to-deck/requirements.txt
```

| 패키지 | 용도 |
|---|---|
| `python-pptx` | PPTX 파일 작성 |
| `pypdf` | PDF 텍스트 추출 (대용량 PDF 대응) |
| `requests` | URL에서 PDF 다운로드 |

---

## Step 2. 추천 입력 PDF

처음 시연할 때 가장 깔끔하게 변환되는 직링크들입니다.

| 제목 | URL | 추천 이유 |
|---|---|---|
| **Attention Is All You Need** (Transformer) | https://arxiv.org/pdf/1706.03762.pdf | 구조가 명확 → 11장 슬라이드 분할이 깔끔 |
| **BERT** | https://arxiv.org/pdf/1810.04805.pdf | 비교 표 풍부 → Results 슬라이드가 잘 나옴 |
| **GPT-3** (Few-Shot Learners) | https://arxiv.org/pdf/2005.14165.pdf | 길이가 길어 `extract_text.py` 데모용 |
| **Stanford AI Index 2024** | https://aiindex.stanford.edu/wp-content/uploads/2024/04/HAI_AI-Index-Report-2024.pdf | 산업 리포트 → 임원 보고용 덱 변환 |

> 강의에서는 **Attention Is All You Need**로 시연하기를 권장합니다. 짧고(15p), 그림이 유명하고, 청중이 결과물을 바로 이해할 수 있습니다.

---

## Step 3. 실행하기

`practice/` 에서 Claude Code를 실행합니다.

```bash
cd practice
claude
```

```
/pdf-to-deck

https://arxiv.org/pdf/1706.03762.pdf 이걸로 발표 덱 만들어줘.
```

Claude가 다음 순서로 동작합니다:

1. `scripts/fetch_pdf.py` 로 PDF 다운로드 → `attention.pdf`
2. PDF 내용을 읽고 분석
3. 11장 표준 구조에 맞춰 `deck.json` outline 작성
4. `scripts/build_deck.py --outline deck.json --output deck.pptx` 실행
5. 슬라이드 수와 outline 미리보기를 보고

```
✓ wrote 12 slides -> deck.pptx
```

`open deck.pptx` 로 확인하면 사이드바 강조 + 발표자 노트가 들어간 16:9 덱이 열립니다.

---

## Step 4. SKILL.md가 하는 일 — 읽어보기

`practice/.claude/skills/pdf-to-deck/SKILL.md` 의 핵심은 **"무엇을, 어떤 순서로, 어떤 형식으로"** 를 명시한 것입니다.

```markdown
---
name: pdf-to-deck
description: PDF 논문/리포트/백서를 읽고 발표용 PPTX 슬라이드 덱으로 변환합니다.
allowed-tools: Bash, Read, Write, WebFetch
---

## 처리 순서
1. PDF 텍스트 추출
2. 표준 11장 구조에 맞춰 outline 설계
3. deck.json 작성
4. build_deck.py 실행
5. 결과 보고
```

여기서 중요한 포인트:

- `allowed-tools` 가 `Bash, Read, Write, WebFetch` 로 최소화되어 있어 Skill이 다른 파일을 건드리지 않음
- **표준 11장 구조 표**가 SKILL.md에 박혀 있어 Claude가 매번 같은 품질의 outline을 만듦
- 트러블슈팅 표 덕분에 `ModuleNotFoundError` 가 나도 Claude가 스스로 `pip install` 을 제안

---

## Step 5. Progressive Disclosure 확인하기

`references/` 폴더는 SKILL.md에 **존재만 언급**되고, 평소엔 컨텍스트로 읽히지 않습니다.

```markdown
## 참조 문서

추가 디자인 가이드는 필요할 때만 읽어 (Progressive Disclosure):

- `references/style-guide.md` — 폰트/색상/여백 규칙
- `references/pdf-sources.md` — 추천 입력 PDF 모음
```

사용자가 "색상 좀 회색 톤으로 바꿔줘" 라고 요청하면 그제서야 Claude가 `style-guide.md` 를 열어봅니다. 컨텍스트 윈도우를 절약하는 핵심 패턴입니다.

---

## Step 6. 응용 — 발표 덱을 비디오 스크립트로

만든 `deck.pptx` 의 발표자 노트만 모아 5분짜리 유튜브 스크립트로 변환하고 싶다면, 후속 Skill을 추가합니다:

```
.claude/skills/deck-to-script/ 만들어줘.
deck.pptx의 노트(notes)만 이어붙여서 5분 분량의 1인칭 발표 스크립트로 만들어주는 Skill이야.
```

Skill 두 개를 체이닝하면:

```
PDF → /pdf-to-deck → deck.pptx → /deck-to-script → script.md
```

논문 한 편이 발표자료 + 발표 대본까지 자동화됩니다.

---

## 정리

| 학습 포인트 | 어디에 구현됐나 |
|---|---|
| 프롬프트 + 스크립트 결합 | `SKILL.md` 가 `scripts/*.py` 호출 |
| 표준 출력 형식 강제 | SKILL.md의 11장 구조 표 |
| Progressive Disclosure | `references/` 의 lazy-load |
| 자동 트리거 | description 에 "PDF 발표 덱 변환" 명시 |
| 권한 최소화 | `allowed-tools: Bash, Read, Write, WebFetch` |
| 실수에 강한 설계 | SKILL.md 트러블슈팅 표 |

이 Skill 한 개에 **2026년 기준 Claude Code Skill의 모범 패턴**이 모두 들어있습니다. 자신의 도메인(논문 → 덱, 회의록 → 액션 아이템, 코드베이스 → 아키텍처 다이어그램)에 맞게 변형해 보세요.
