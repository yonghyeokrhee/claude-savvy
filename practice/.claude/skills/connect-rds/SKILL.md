---
name: connect-rds
description: RDS 연결 테스트를 실행합니다. VPN 연결 + AWS 자격증명이 필요합니다. config/rds.env 파일이 있어야 합니다.
allowed-tools: Bash, Read
---

# RDS 연결 테스트

## 사전 확인

1. VPN 연결 상태 확인
2. `config/rds.env` 파일 존재 확인 (`.gitignore`로 제외된 설정 파일)

## 실행

```bash
source config/rds.env && python3 .claude/skills/connect-rds/scripts/rds_connect_test.py
```

연결 성공 시: `✓ RDS 연결 성공` 출력
연결 실패 시: 오류 메시지와 함께 원인 표시

## 오류 유형별 대응

| 오류 | 원인 | 조치 |
|---|---|---|
| SSL validation failed | VPN 미연결 | VPN 연결 후 재시도 |
| Could not connect to server | RDS 엔드포인트 오류 | config/rds.env 호스트 확인 |
| Access denied | 계정/비밀번호 오류 | AWS Secrets Manager 값 확인 |
| No module named | 패키지 미설치 | pip install -r requirements.txt |
