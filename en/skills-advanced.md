# Advanced Skills — Integrating External Systems

Basic Skills are simple prompt wrappers for Claude.
In production, you often need advanced Skills integrated with external systems (databases, AWS services, internal infra).

---

## Basic Skill vs Advanced Skill

| | Basic Skill | Advanced Skill |
|---|---|---|
| Structure | One `SKILL.md` | `SKILL.md` + scripts + config files |
| Execution model | Claude runs a prompt | Claude runs external scripts |
| Dependencies | None | External packages, credentials, network |
| Failure causes | Rare | VPN, permissions, env vars, etc. |

---

## `connect-rds-python` — Real Case Study

`connect-rds-python` is a global Skill that connects to AWS RDS MySQL and runs SQL.
It is installed in `~/.claude/skills/connect-rds-python/` and callable from any project via `/connect-rds-python`.

### File structure

```
~/.claude/skills/connect-rds-python/
├── SKILL.md           # instructions + usage + troubleshooting
├── dbconnection.py    # SQLAlchemy-based DB connection class
└── requirements.txt   # dependencies such as sqlalchemy, pymysql
```

### Why is this complex?

The visible goal is simple: **"run one SELECT 1 query."**
But hidden complexity includes:

```
User: /connect-rds-python
    ↓
1. VPN connection          <- required for internal network (10.2.x.x)
2. AWS profile setup       <- ENV=stg, AWS_PROFILE=mopstg
3. SSM Parameter Store     <- fetch RDS endpoint automatically
4. Secrets Manager         <- fetch DB password automatically (not in code)
5. SQLAlchemy Pool         <- manage 3-8 pooled connections
6. Environment branch      <- different config for dev/stg/prd
    ↓
Actual DB connection + query execution
```

**Key point: no password is stored in code.**
The password is fetched from AWS Secrets Manager at runtime.

### Credential flow

```
Local environment variables
  AWS_PROFILE=mopstg
  ENV=stg
       ↓
AWS Secrets Manager
  sm-ap-northeast-2-stg-mop-mopapp_pw
       ↓
Auto-fetch in DbConnection
       ↓
SQLAlchemy connection (password lives in memory only)
```

### Usage

```bash
export ENV=stg
export AWS_PROFILE=mopstg
```

```
/connect-rds-python
```

```python
# Claude executes this automatically
with DbConnection() as db:
    results = db.query('SELECT * FROM mop.advertiser_units LIMIT 10')
    for row in results:
        print(row)
```

### Core `DbConnection` features

| Feature | Details |
|---|---|
| Connection pooling | SQLAlchemy QueuePool (default 3, max 8) |
| Auto reconnect | `pool_pre_ping` recovers broken connections |
| Thread safety | Safe in parallel workloads |
| Retry logic | Exponential backoff on AWS `ThrottlingException` (up to 5 retries) |
| Class caching | Minimizes repeated AWS API calls |

### Troubleshooting structure

The Skill embeds a troubleshooting table in `SKILL.md`. When errors happen, Claude can infer cause and remediation from this table.

| Error | Cause | Action |
|---|---|---|
| Connection timeout | VPN disconnected | Connect VPN, then run `aws sts get-caller-identity` |
| AWS credential error | Profile mismatch | Verify `ENV` and `AWS_PROFILE` mapping |
| `ModuleNotFoundError` | Missing package | `pip install -r requirements.txt` |
| Pool exhaustion | Connection leak | Use `with DbConnection()` context manager |

---

## Sensitive Data Separation Pattern

Pattern used by `connect-rds-python`: **credentials are fetched from AWS services, not stored in code**.

```
Code (in Git)               Cloud services (outside code)
─────────────────           ─────────────────────────────
dbconnection.py      ->     SSM: RDS endpoint
SKILL.md             ->     Secrets Manager: DB password
requirements.txt
```

If cloud services are not available, use `.env` pattern:

```
project/
├── .claude/skills/connect-rds/
│   └── scripts/rds_connect_test.py   <- in Git (code)
└── config/
    ├── rds.env.example               <- in Git (template)
    └── rds.env                       <- excluded via .gitignore
```

Onboarding for a new teammate:

```bash
cp config/rds.env.example config/rds.env
# Fill in real values
```

---

## Skill calling another Skill

Inside `SKILL.md`, you can instruct Claude to run another Skill's script first.
For example, `super-analyst` establishes DB connectivity through `connect-rds-python` before analysis.

```
Run /super-analyst
    -> establish RDS connection via connect-rds-python
    -> execute SQL queries
    -> output analysis results
```

---

## Principles for advanced Skill design

**1. Include failure handling in `SKILL.md`**
When scripts fail, Claude relies on your troubleshooting guidance. Without it, execution often stalls.

**2. Keep credentials out of code**
AWS: Secrets Manager / SSM Parameter Store
Elsewhere: `.env` + `.gitignore`
Never hardcode credentials.

**3. Minimize privileges with `allowed-tools`**
An RDS connection Skill typically only needs `Bash` and `Read`.

**4. Provide a dry-run mode**
Let users validate environment variables before real connection attempts.

```bash
python3 scripts/rds_connect_test.py --dry-run
```

**5. Use connection pools**
SQLAlchemy pooling is more stable than raw `pymysql.connect()`.
Use context managers (`with DbConnection()`) to prevent leaks.
