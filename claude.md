# GitBook 작성 컨텍스트

이 문서는 Claude가 이 프로젝트의 GitBook 페이지를 작성할 때 참조하는 컨텍스트입니다.

## 프로젝트 구조

```
claude-savvy/
├── SUMMARY.md        # GitBook 목차 (필수)
├── README.md         # 책의 첫 페이지
└── *.md              # 각 챕터 페이지
```

## SUMMARY.md 규칙

SUMMARY.md는 GitBook의 **목차를 정의하는 핵심 파일**입니다.

### 기본 문법

```markdown
# Summary

## 섹션 제목

* [페이지 제목](파일명.md)
* [페이지 제목](폴더/파일명.md)
```

### 현재 목차 구조

```markdown
# Summary

## 강의

* [Agent 도구](agents.md)
* [Skills](skills.md)
* [Sub-Agent](sub-agent.md)
* [Workflow](workflow.md)
* [MCP](mcp.md)
```

### 규칙

- 목차에 추가하지 않은 `.md` 파일은 GitBook에서 보이지 않음
- 파일 경로는 `SUMMARY.md` 기준 상대 경로
- `##` 헤딩으로 섹션(그룹) 생성 가능
- 들여쓰기(`  *`)로 하위 페이지 구성 가능

## 페이지 작성 원칙

- 첫 번째 `#` 헤딩이 페이지 제목
- 한 페이지에 한 가지 주제만 다룸
- 코드 예시는 언어 지정 포함 (` ```bash `, ` ```markdown ` 등)
- 표, 코드블록, 헤딩 계층(##, ###)을 활용하여 가독성 확보

## 새 페이지 추가 절차

1. `.md` 파일 생성
2. `SUMMARY.md`에 링크 추가
3. commit & push
