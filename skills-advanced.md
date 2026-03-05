# 고급 Skill — 외부 시스템 연동

기본 Skill은 Claude에게 프롬프트를 전달하는 단순한 구조입니다.
하지만 실무에서는 외부 시스템(데이터베이스, AWS 서비스, 사내 인프라)과 연동해야 하는 복잡한 Skill이 필요합니다.

---

## 단순 Skill vs 고급 Skill

| | 단순 Skill | 고급 Skill |
|---|---|---|
| 구성 | SKILL.md 한 개 | SKILL.md + 스크립트 + 설정 파일 |
| 동작 | Claude가 프롬프트 실행 | Claude가 외부 스크립트 실행 |
| 의존성 | 없음 | 외부 패키지, 자격증명, 네트워크 |
| 실패 원인 | 거의 없음 | VPN, 권한, 환경변수 등 다양 |

---

## connect-rds — 실제 사례 분석

`connect-rds`는 RDS(데이터베이스)에 연결을 테스트하는 Skill입니다.
`SELECT 1` 이라는 가장 단순한 쿼리를 실행하는 게 목적이지만, 구조는 복잡합니다.

### 파일 구조

```
.claude/skills/connect-rds/
├── SKILL.md                       # Claude가 읽는 지침
└── scripts/
    └── rds_connect_test.py        # 실제 실행 스크립트
```

### 왜 복잡한가?

```
사용자: /connect-rds
    ↓
Claude가 SKILL.md 읽음
    ↓
스크립트 실행 전 필요한 것들:

1. VPN 연결         ← 네트워크 접근 통제
2. AWS 자격증명     ← Secrets Manager에서 DB 비밀번호 조회
3. SSL 인증서       ← 기업 내부 CA 인증서 3종 환경변수
4. 외부 패키지      ← pymysql 설치 여부
5. 환경 분기        ← dev / stg / prd 각각 다른 설정
    ↓
SELECT 1 실행
```

단순한 연결 테스트 하나를 위해 5가지 전제조건이 필요합니다.
이 복잡성을 SKILL.md 안에 숨겨두면, 사용자는 `/connect-rds` 한 번만 입력하면 됩니다.

### SKILL.md의 역할

```markdown
---
allowed-tools: Bash, Read
---

## 사전 확인
1. VPN 연결 상태 확인
2. config/rds.env 파일 존재 확인

## 실행
source config/rds.env && python3 .claude/skills/connect-rds/scripts/rds_connect_test.py

## 오류 유형별 대응
| SSL validation failed | VPN 미연결  | VPN 연결 후 재시도 |
| Could not connect     | 엔드포인트  | config/rds.env 확인 |
...
```

Claude가 오류가 나면 **SKILL.md의 오류 유형 표를 보고 스스로 판단**해서 다음 조치를 제안합니다.

---

## 민감 정보 분리 패턴

RDS 접속 정보(호스트, 비밀번호 등)는 코드와 분리해서 관리합니다:

```
practice/
├── .claude/skills/connect-rds/   ← Git에 포함 (코드)
│   └── scripts/rds_connect_test.py
└── config/
    ├── rds.env.example           ← Git에 포함 (템플릿)
    └── rds.env                   ← Git 제외 (.gitignore)
```

**`.gitignore` 설정:**
```
practice/config/rds.env
```

**처음 사용하는 팀원 온보딩:**
```bash
cp config/rds.env.example config/rds.env
# 실제 값 입력 후 사용
```

---

## 참고 — Skill이 Skill을 호출하는 패턴

SKILL.md 안에서 다른 Skill의 실행 스크립트를 먼저 호출하도록 지시할 수 있습니다. 예를 들어 `super-analyst` Skill은 DB 쿼리를 실행하기 전에 `/connect-rds`로 연결을 먼저 확립합니다.

```
/super-analyst 실행
    → /connect-rds 호출 (RDS 연결)
    → SQL 쿼리 실행
    → 분석 결과 출력
```

실습 파일: `practice/.claude/skills/super-analyst/SKILL.md`

---

## 고급 Skill 작성 원칙

**1. 오류 대응을 SKILL.md에 포함하라**
Claude가 스크립트 실패 시 SKILL.md의 오류 표를 보고 원인을 추정합니다.
스크립트만 있고 SKILL.md에 오류 대응이 없으면 Claude가 막힙니다.

**2. 민감 정보는 환경변수 파일로 분리하라**
자격증명, API 키, 엔드포인트는 `.env` 파일로 분리하고 `.gitignore`에 추가합니다.
`.env.example`을 Git에 포함해서 팀원이 어떤 값이 필요한지 알 수 있게 합니다.

**3. `allowed-tools`로 권한을 최소화하라**
RDS 연결 Skill은 `Bash`와 `Read`만 필요합니다.
`Write`나 `Edit`까지 허용하면 실수로 코드를 수정할 위험이 있습니다.

**4. dry-run 옵션을 만들어라**
실제 연결 없이 환경변수가 올바르게 설정됐는지 확인하는 옵션은
디버깅 시간을 크게 줄여줍니다.

```bash
python3 scripts/rds_connect_test.py --dry-run
```
