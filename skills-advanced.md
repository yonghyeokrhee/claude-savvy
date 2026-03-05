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

## connect-rds-python — 실제 사례 분석

`connect-rds-python`은 AWS RDS MySQL에 연결하여 SQL을 실행하는 글로벌 Skill입니다.
`~/.claude/skills/connect-rds-python/`에 설치되어 모든 프로젝트에서 `/connect-rds-python`으로 호출합니다.

### 파일 구조

```
~/.claude/skills/connect-rds-python/
├── SKILL.md           # Claude가 읽는 지침 + 사용법 + 트러블슈팅
├── dbconnection.py    # SQLAlchemy 기반 DB 연결 클래스
└── requirements.txt   # sqlalchemy, pymysql 등 의존성
```

### 왜 복잡한가?

**"DB에 SELECT 1 쿼리 한 번 실행하기"**가 이 Skill의 목표지만, 그 뒤에 숨은 복잡성은 다음과 같습니다:

```
사용자: /connect-rds-python
    ↓
1. VPN 연결           ← 내부 네트워크(10.2.x.x) 접근 필요
2. AWS Profile 설정   ← ENV=stg, AWS_PROFILE=mopstg
3. SSM Parameter Store  ← RDS 엔드포인트 자동 조회
4. Secrets Manager    ← DB 비밀번호 자동 조회 (코드에 없음)
5. SQLAlchemy Pool    ← 커넥션 풀 3~8개 관리
6. 환경 분기          ← dev / stg / prd 각각 다른 설정
    ↓
실제 DB 연결 + 쿼리 실행
```

**핵심: 비밀번호가 코드 어디에도 없습니다.**
코드가 실행될 때 AWS Secrets Manager에서 자동으로 가져옵니다.

### 자격증명 흐름

```
로컬 환경변수
  AWS_PROFILE=mopstg
  ENV=stg
       ↓
AWS Secrets Manager
  sm-ap-northeast-2-stg-mop-mopapp_pw
       ↓
DbConnection 내부에서 자동 조회
       ↓
SQLAlchemy 연결 (비밀번호 메모리에서만 존재)
```

### 사용 방법

```bash
export ENV=stg
export AWS_PROFILE=mopstg
```

```
/connect-rds-python
```

```python
# Claude가 이 코드를 자동 실행
with DbConnection() as db:
    results = db.query('SELECT * FROM mop.advertiser_units LIMIT 10')
    for row in results:
        print(row)
```

### DbConnection 주요 기능

| 기능 | 내용 |
|---|---|
| 커넥션 풀링 | SQLAlchemy QueuePool (기본 3개, 최대 8개) |
| 자동 재연결 | `pool_pre_ping`으로 끊긴 연결 자동 복구 |
| 스레드 안전 | 병렬 처리 환경에서도 안전하게 동작 |
| 재시도 로직 | AWS ThrottlingException 시 지수 백오프 (최대 5회) |
| 클래스 캐시 | AWS API 호출 최소화 |

### 트러블슈팅 구조

SKILL.md 안에 트러블슈팅 표가 내장되어 있습니다. Claude가 오류 발생 시 자동으로 원인을 찾아 조치합니다:

| 오류 | 원인 | 조치 |
|---|---|---|
| Connection timeout | VPN 미연결 | VPN 연결 후 `aws sts get-caller-identity` 확인 |
| AWS credential error | Profile 불일치 | `ENV`와 `AWS_PROFILE` 매핑 확인 |
| ModuleNotFoundError | 패키지 미설치 | `pip install -r requirements.txt` |
| Pool exhaustion | 커넥션 누수 | `with DbConnection()` 컨텍스트 매니저 사용 |

---

## 민감 정보 분리 패턴

`connect-rds-python`이 채택한 방식 — **자격증명을 코드가 아닌 AWS 서비스에서 조회**:

```
코드 (Git에 포함)          AWS 클라우드 (코드 밖)
─────────────────          ──────────────────────
dbconnection.py     →      SSM: RDS 엔드포인트
SKILL.md            →      Secrets Manager: DB 비밀번호
requirements.txt
```

클라우드 서비스를 쓰지 않는 환경이라면 `.env` 파일 패턴을 사용합니다:

```
프로젝트/
├── .claude/skills/connect-rds/
│   └── scripts/rds_connect_test.py   ← Git에 포함 (코드)
└── config/
    ├── rds.env.example               ← Git에 포함 (템플릿)
    └── rds.env                       ← Git 제외 (.gitignore)
```

처음 사용하는 팀원 온보딩:

```bash
cp config/rds.env.example config/rds.env
# 실제 값 입력 후 사용
```

---

## Skill이 Skill을 호출하는 패턴

SKILL.md 안에서 다른 Skill의 스크립트를 먼저 호출하도록 지시할 수 있습니다.
`super-analyst` Skill은 데이터 분석 전에 `connect-rds-python`으로 연결을 먼저 확립합니다:

```
/super-analyst 실행
    → connect-rds-python으로 RDS 연결
    → SQL 쿼리 실행
    → 분석 결과 출력
```

---

## 고급 Skill 작성 원칙

**1. 오류 대응을 SKILL.md에 포함하라**
Claude가 스크립트 실패 시 SKILL.md의 트러블슈팅 표를 보고 원인을 추정합니다.
오류 대응이 없으면 Claude가 막힙니다.

**2. 자격증명은 코드 밖에서 관리하라**
AWS 환경: Secrets Manager / SSM Parameter Store
그 외: `.env` 파일 + `.gitignore`
절대 코드에 하드코딩하지 마세요.

**3. `allowed-tools`로 권한을 최소화하라**
RDS 연결 Skill은 `Bash`와 `Read`만 필요합니다.

**4. dry-run 옵션을 만들어라**
실제 연결 없이 환경변수가 올바르게 설정됐는지 확인할 수 있어야 합니다.

```bash
python3 scripts/rds_connect_test.py --dry-run
```

**5. 커넥션 풀을 사용하라**
단순 `pymysql.connect()`보다 SQLAlchemy 커넥션 풀이 안정적입니다.
컨텍스트 매니저(`with DbConnection()`)로 연결 누수를 방지하세요.
