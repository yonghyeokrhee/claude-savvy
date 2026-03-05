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

`.claude/skills/review.md` 파일을 생성합니다.

Skill 파일은 **일반 마크다운 파일**입니다. Claude가 이 파일의 내용을 그대로 프롬프트로 실행합니다.

```markdown
# 코드 리뷰

현재 변경된 파일들을 리뷰해줘. 다음 기준으로 평가해:

1. **버그 가능성** — 예외 처리 누락, 엣지 케이스
2. **가독성** — 변수명, 함수 길이, 주석 필요 여부
3. **보안** — 입력값 검증, 민감 정보 노출
4. **개선 제안** — 더 나은 구현 방법이 있다면 제안

각 항목별로 문제가 없으면 "이상 없음"으로 표시해줘.
```

---

## Step 3. Skill 실행

Claude Code 세션에서 슬래시 명령어로 호출합니다:

```
/review
```

Claude가 `.claude/skills/review.md`를 읽고 프롬프트를 실행합니다.

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
