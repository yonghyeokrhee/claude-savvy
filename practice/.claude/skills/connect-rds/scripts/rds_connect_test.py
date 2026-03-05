#!/usr/bin/env python3
"""
RDS 연결 테스트 스크립트.
config/rds.env 환경변수로 연결 정보를 받아 SELECT 1 쿼리를 실행합니다.
"""

import os
import sys


def check_env():
    required = ["RDS_HOST", "RDS_PORT", "RDS_DATABASE", "RDS_USER", "RDS_PASSWORD"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        print(f"ERROR: 다음 환경변수가 없습니다: {', '.join(missing)}")
        print("config/rds.env 파일을 확인하세요.")
        return False
    return True


def main():
    if not check_env():
        return 1

    host = os.environ["RDS_HOST"]
    port = os.environ["RDS_PORT"]
    database = os.environ["RDS_DATABASE"]
    user = os.environ["RDS_USER"]
    password = os.environ["RDS_PASSWORD"]

    print("=" * 50)
    print("RDS 연결 테스트")
    print(f"Host: {host}:{port}")
    print(f"Database: {database}")
    print(f"User: {user}")
    print("=" * 50)

    try:
        import pymysql
    except ImportError:
        print("ERROR: pymysql이 설치되어 있지 않습니다.")
        print("pip install pymysql 을 실행하세요.")
        return 3

    try:
        conn = pymysql.connect(
            host=host,
            port=int(port),
            database=database,
            user=user,
            password=password,
            connect_timeout=10,
            ssl_ca=os.getenv("SSL_CA_PATH"),
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 AS ok")
            result = cursor.fetchone()
            print(f"쿼리 결과: {result}")
        conn.close()
        print("✓ RDS 연결 성공")
        return 0
    except Exception as e:
        print(f"✗ RDS 연결 실패: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
