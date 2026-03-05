# Skill 직접 만들기

앞 챕터에서 Skill의 개념을 배웠습니다. 이제 실제로 Skill 파일을 만들고 실행해봅니다.

## 준비

Claude Code가 설치된 상태에서 실습할 프로젝트 디렉토리가 있으면 됩니다.

```bash
mkdir my-project && cd my-project
claude
```

---

## Step 1. Skill 파일 위치 결정

Skill 파일은 두 곳에 저장할 수 있습니다:

| 위치 | 경로 | 적용 범위 |
|---|---|---|
| 프로젝트 전용 | `.claude/skills/` | 해당 프로젝트에서만 사용 |
| 전역 | `~/.claude/skills/` | 모든 프로젝트에서 사용 |

이번 실습은 프로젝트 전용 Skill을 만듭니다.

```bash
mkdir -p .claude/skills
```

---

## Step 2. Skill 파일 작성

`practice/.claude/skills/support-explorer.md` 파일을 생성합니다.

Skill 파일은 **일반 마크다운 파일**입니다. Claude가 이 파일의 내용을 그대로 프롬프트로 실행합니다.

> **frontmatter는 필수가 아닙니다.**
> 파일 맨 위에 `---`로 감싼 메타데이터(frontmatter)를 추가할 수 있지만 없어도 Skill은 정상 작동합니다.
> 단, `description`을 넣으면 `/help` 목록에 설명이 표시되어 팀과 공유할 때 편리합니다.
>
> ```markdown
> ---
> description: "MOP 신규 사용자 온보딩 안내"
> ---
> ```

이번 실습에서 만들 Skill은 **`support-explorer`** — MOP 서비스를 처음 시작하는 사람이 빠르게 온보딩할 수 있도록 안내해주는 Skill입니다.

```markdown
# MOP 빠른 시작 가이드

https://support.mop.co.kr/introduce 페이지를 읽고, 사용자가 MOP를 처음 시작하는 데 필요한 내용을 단계별로 안내해줘.

다음 순서로 진행해:

1. **MOP가 무엇인지 한 줄로 설명** — 핵심 가치 중심으로

2. **내 상황에 맞는 플랜 추천**
   - "광고주인가요, 대행사인가요?" 질문 후 답변에 따라 Basic / Pro / API Center 중 추천

3. **지금 바로 시작하는 법 안내**
   - Basic이면: 회원가입 → 비즈니스 유형 입력 → 즉시 사용
   - Pro/API Center면: 도입 사전 설문 → 컨설턴트 매칭 → 온보딩

4. **첫 번째로 해야 할 3가지 액션** — 구체적인 행동 단계로 제시

5. **알아두면 좋은 핵심 용어** — 애드써클, Spend Pacing, 목표입찰 등 간단 설명

안내는 간결하고 친근하게, 전문 용어는 처음 나올 때 바로 설명해줘.
```

이 파일은 `practice/.claude/skills/support-explorer.md`에 실제로 저장되어 있습니다.

---

## Step 3. Skill 실행

`practice/` 디렉토리에서 Claude Code를 시작한 뒤 호출합니다:

```bash
cd practice
claude
```

```
/support-explorer
```

Claude가 MOP 지원 페이지를 직접 읽고, 사용자의 상황에 맞는 시작 가이드를 단계별로 안내합니다.

---

## Step 4. 더 유용한 Skill 만들기

Skill 파일 안에서 **현재 컨텍스트를 활용하는 지시**를 작성할 수 있습니다.

### 예시 — `/standup`

`.claude/skills/standup.md`:

```markdown
# 스탠드업 작성

git log와 현재 수정 중인 파일을 확인하고 다음 형식으로 스탠드업을 작성해줘:

**어제 한 일**
- (최근 커밋 메시지 기준으로 요약)

**오늘 할 일**
- (현재 수정 중인 파일과 TODO 주석 기준으로 작성)

**블로커**
- 없음 (있으면 명시)
```

### 예시 — `/deploy-check`

`.claude/skills/deploy-check.md`:

```markdown
# 배포 전 체크리스트

배포 전에 다음 항목을 순서대로 확인해줘:

1. [ ] 테스트 전체 통과 여부 확인 (`npm test`)
2. [ ] `.env` 파일이 `.gitignore`에 포함되어 있는지 확인
3. [ ] `console.log` 또는 디버그 코드 남아있는지 검색
4. [ ] package.json의 버전이 업데이트되었는지 확인
5. [ ] README의 변경 사항이 반영되었는지 확인

각 항목 결과를 체크리스트 형식으로 알려줘.
```

---

## Skill 작성 팁

**구체적인 출력 형식을 지정하세요**
Claude가 매번 다른 형식으로 답하지 않도록, 원하는 형식을 명시합니다.

```markdown
# 나쁜 예
코드를 분석해줘.

# 좋은 예
코드를 분석하고 다음 형식으로 결과를 줘:
- 발견된 문제: (목록)
- 심각도: 높음/중간/낮음
- 수정 제안: (코드 예시 포함)
```

**Skill은 짧고 명확하게**
하나의 Skill이 하나의 역할만 하도록 작성합니다. 여러 역할이 필요하면 Skill을 분리합니다.

**팀과 공유하기**
`.claude/skills/` 폴더를 git으로 관리하면 팀 전체가 동일한 Skill을 사용할 수 있습니다.

```bash
git add .claude/skills/
git commit -m "팀 공용 Skills 추가"
```

---

## 정리

| 단계 | 내용 |
|---|---|
| 1 | `.claude/skills/` 폴더 생성 |
| 2 | `skill-name.md` 파일 작성 |
| 3 | Claude Code에서 `/skill-name` 호출 |
| 4 | 결과 확인 후 프롬프트 개선 |
