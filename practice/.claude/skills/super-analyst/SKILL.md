---
name: super-analyst
description: MOP 내부 DB에 연결하여 Collection 오류 진단 및 SQL 기반 데이터 분석을 수행합니다. RDS 연결이 필요한 내부 데이터 조회에 사용하세요.
allowed-tools: Bash
---

# MOP Super Analyst

내부 DB에 접속하여 데이터를 조회하고 분석합니다.

## 시작 전 필수 작업

**반드시 `/connect-rds` Skill을 먼저 호출해서 RDS 연결을 확립해.**
연결 환경은 사용자에게 확인:
> "어떤 환경에 연결할까요? (dev / stg / prd)"

```bash
/Users/yong/mop-glue/.claude/skills/connect-rds/scripts/run_rds_connect.sh local <env>
```

---

## Collection 오류 진단

사용자가 "Collection 오류", "수집 실패", "에러 표시" 관련 문의를 하면
아래 4가지 조건을 순서대로 확인해.

### 오류 판단 기준

다음 중 **하나라도 만족**하면 Collection 에러로 표시됩니다:

| # | 조건 | 테이블 | 기준 |
|---|---|---|---|
| 1 | 미디어플랫폼 수집 실패 | `dashboard_overview` | 2일 이내 데이터 없음 |
| 2 | 분석도구 수집 실패 | `dashboard_overview` | 2일 이내 데이터 없음 |
| 3 | URL 이상 감지 데이터 발생 | `abnormal_detection_url_history` | 2일 이내 데이터 존재 |
| 4 | UTM 이상 감지 데이터 발생 | `abnormal_detection_utm_history` | 2일 이내 데이터 존재 |

### 조건 1·2 — 수집 여부 확인

```sql
-- 미디어플랫폼 / 분석도구 수집 현황 확인
SELECT
  advertiser_id,
  media_platform_collected_yn,
  analytics_collected_yn,
  created_datetime
FROM ${mop-schema}.dashboard_overview
WHERE advertiser_id = :advertiser_id
  AND created_datetime >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY)
ORDER BY created_datetime DESC
LIMIT 10;
```

### 조건 3 — URL 이상 감지 확인

```sql
SELECT COUNT(*) AS abnormal_count
FROM ${mop-schema}.abnormal_detection_url_history
WHERE advertiser_id = :advertiser_id
  AND perform_time >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY);
```

### 조건 4 — UTM 이상 감지 확인

```sql
/* SQL id: mop-be-sql\Dashboard.xml_getUtmAbnormalCount */
SELECT COUNT(*) AS abnormal_count
FROM ${mop-schema}.abnormal_detection_utm_history aduh
JOIN (
  SELECT max(ah.perform_time) AS perform_time
  FROM ${mop-schema}.abnormal_detection_utm_history ah
  WHERE ah.perform_time >= (
    SELECT max(bh.created_datetime)
    FROM ${mop-schema}.batch_history bh
    WHERE bh.created_datetime >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY)
      AND bh.batch_type = 'DETECT_UTM_ANOMALY'
      AND bh.status = 'DONE'
  )
  AND advertiser_id = :advertiser_id
) max_perform_time USING (perform_time)
INNER JOIN (
  SELECT 'NAVER' AS media_type, au.media_account_id AS account_id,
         accounts.customer_name AS account_name, au.campaign_id
  FROM ${mop-schema}.advertiser_units au
  JOIN ${mpriv-schema}.naver_authorizations accounts
    ON au.media_account_id = accounts.customer_id
  WHERE au.media_type = 'NAVER' AND au.use_yn = 'Y'
    AND au.advertiser_id = :advertiser_id AND accounts.use_yn = 'Y'
  UNION
  SELECT 'KAKAO' AS media_type, au.media_account_id AS account_id,
         accounts.account_name, au.campaign_id
  FROM ${mop-schema}.advertiser_units au
  JOIN ${mpriv-schema}.kakao_accounts accounts
    ON au.media_account_id = accounts.account_id
  WHERE au.media_type = 'KAKAO' AND au.use_yn = 'Y'
    AND au.advertiser_id = :advertiser_id AND accounts.use_yn = 'Y'
    AND accounts.platform_type = 'SA'
  UNION
  SELECT 'GOOGLE' AS media_type, au.media_account_id AS account_id,
         accounts.account_name, au.campaign_id
  FROM ${mop-schema}.advertiser_units au
  JOIN ${mpriv-schema}.google_accounts accounts
    ON au.media_account_id = accounts.account_id
  WHERE au.media_type = 'GOOGLE' AND au.use_yn = 'Y'
    AND au.advertiser_id = :advertiser_id AND accounts.use_yn = 'Y'
) accounts
  ON aduh.media_type = accounts.media_type
  AND aduh.account_id = accounts.account_id
  AND aduh.campaign_id = accounts.campaign_id
WHERE aduh.platform_type = 'SA'
  AND aduh.advertiser_id = :advertiser_id;
```

> **알려진 케이스**: 웰컴 마이데이터 SA (advertiser_id: 1691)는
> 위 UTM 쿼리 결과 이상 감지 데이터가 존재하여 Collection 에러로 표시되고 있음.

---

## 진단 절차

1. **advertiser_id 확인**
   > "진단할 광고주 ID가 어떻게 되나요?"

2. **4가지 조건 순서대로 쿼리 실행**
   - 조건 1·2: `dashboard_overview` 수집 여부
   - 조건 3: URL 이상 감지 건수
   - 조건 4: UTM 이상 감지 건수

3. **결과 요약 출력**

   ```
   [Collection 오류 진단 결과] advertiser_id: XXXX
   ─────────────────────────────────────────
   조건 1 (미디어플랫폼 수집): ✅ 정상 / ❌ 실패
   조건 2 (분석도구 수집):     ✅ 정상 / ❌ 실패
   조건 3 (URL 이상 감지):     ✅ 없음 / ❌ N건 발생
   조건 4 (UTM 이상 감지):     ✅ 없음 / ❌ N건 발생
   ─────────────────────────────────────────
   결론: 에러 표시 원인 → 조건 N
   ```

4. **원인 파악 후 다음 액션 제안**
   - 수집 실패면: 배치 히스토리(`batch_history`) 추가 확인 제안
   - 이상 감지 데이터면: 상세 내역 조회 제안

---

## 자유 쿼리 모드

Collection 진단 외 다른 데이터 조회가 필요하면:
> "어떤 데이터를 조회하고 싶으신가요?"

사용자 요청을 받아 SQL을 작성하고 실행해.
쿼리 실행 전 반드시 SQL을 먼저 보여주고 확인을 받을 것.

---

## 주의사항

- `prd` 환경은 읽기 전용(SELECT만) 쿼리만 실행할 것
- `:advertiser_id` 같은 파라미터는 실행 전 반드시 실제 값으로 치환할 것
- `${mop-schema}`, `${mpriv-schema}`는 환경별 실제 스키마명으로 치환할 것
