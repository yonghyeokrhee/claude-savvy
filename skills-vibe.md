# 대화로 Skill 만들기

SKILL.md 파일을 직접 작성하는 대신, Claude와 대화하면서 Skill을 만드는 방법입니다. 원하는 동작을 말로 설명하면 Claude가 파일 구조까지 만들어줍니다.

## 방법

Claude Code 세션에서 원하는 Skill을 자연어로 요청합니다:

```
.claude/skills/standup/SKILL.md 만들어줘.

git log와 수정 중인 파일을 보고 스탠드업 내용을 자동으로 작성해주는 Skill이야.
어제 한 일 / 오늘 할 일 / 블로커 형식으로 출력해줘.
```

Claude가 디렉토리 생성부터 SKILL.md 작성까지 한 번에 처리합니다.

---

## 실습 예제

### 예제 1 — `/support-explorer` 개선하기

기존 Skill을 대화로 수정하는 방법입니다.

```
.claude/skills/support-explorer/SKILL.md를 수정해줘.

지금은 MOP 소개 페이지만 읽는데,
사용자가 광고주인지 대행사인지 먼저 물어본 다음에
그에 맞는 온보딩 순서를 안내하도록 바꿔줘.
```

### 예제 2 — 새 Skill을 대화로 처음부터 만들기

```
.claude/skills/ 아래에 mop-report라는 Skill 만들어줘.

practice/data/ 폴더의 데이터 파일들을 읽고
이번 달 광고 성과를 요약하는 리포트를 작성하는 Skill이야.

출력 형식:
- 전체 ROAS 요약
- 상위 3개 캠페인
- 다음 달 추천 액션 3가지

allowed-tools는 Read만 허용해줘.
```

Claude가 생성하는 결과:

```
.claude/skills/mop-report/SKILL.md 파일을 생성했습니다.
```

```markdown
---
name: mop-report
description: practice/data 폴더의 광고 데이터를 읽어 월간 성과 리포트를 작성합니다
allowed-tools: Read
---

# MOP 월간 성과 리포트

practice/data/ 폴더의 파일들을 읽고 이번 달 광고 성과를 요약해줘.

다음 형식으로 출력해:

## 전체 ROAS 요약
...

## 상위 3개 캠페인
...

## 다음 달 추천 액션
1.
2.
3.
```

### 예제 3 — 기존 Skill을 참고해서 새 Skill 만들기

```
.claude/skills/support-explorer/SKILL.md를 참고해서
비슷한 구조로 mop-faq라는 Skill을 만들어줘.

https://support.mop.co.kr 에서 자주 묻는 질문을 읽고
사용자 질문에 맞는 답변을 찾아주는 Skill이야.
```

---

## 직접 작성 vs 대화로 만들기

| 구분 | 직접 작성 | 대화로 만들기 |
|---|---|---|
| 속도 | 느림 | 빠름 |
| 정확도 | 내가 원하는 대로 | Claude 해석에 따라 다를 수 있음 |
| 수정 | 파일 직접 편집 | 대화로 추가 요청 |
| 적합한 상황 | 세밀한 제어가 필요할 때 | 빠르게 초안을 만들 때 |

대화로 초안을 만들고, 결과 파일을 직접 수정해 다듬는 방식이 가장 효율적입니다.

---

## 팁

**구체적인 출력 형식을 요청에 포함하세요**

```
# 덜 효과적
리포트 만드는 Skill 만들어줘.

# 더 효과적
## 섹션1: 요약 (3줄 이내)
## 섹션2: 상위 캠페인 표 (ROAS 기준 정렬)
## 섹션3: 액션 아이템 (번호 목록)
이 형식으로 출력하는 mop-report Skill 만들어줘.
```

**만든 Skill을 바로 테스트하세요**

```
/mop-report
```

결과가 마음에 들지 않으면 바로 후속 요청:

```
섹션2 표에 TACOS 컬럼도 추가해줘.
```

> 참조: [FastCampus — Clip 1: Slash Command 만들기](https://goobong.gitbook.io/fastcampus/part-1.-ai-claude-code/chapter3_claude_code_-_/clip1_slash_command_-_)
