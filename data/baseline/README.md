# baseline (진출 실측 기간/비용) — MVP 목업

> ⚠️ **이 폴더의 데이터는 전부 목업(가짜)입니다.** 1차 MVP 데모용으로 임의값을 채웠습니다.
> 실제 진출 실적 데이터가 확보되면 아래 안내대로 교체하세요.

## 무엇인가

진출 소요기간/비용 추정 모델의 **출발점(baseline)** 입니다.
같은 권역(region)에 이미 진출한 기준국가가 실제로 쓴 기간·비용을 담고,
후보국과 기준국의 유사도로 배수를 매겨 추정합니다.

```
추정기간 = baseline_기간 × multiplier(유사도)
추정비용 = baseline_비용 × multiplier(유사도)
```

예) 멕시코(미주) 추정 = 미국 baseline 12개월 × 1.2(유사도 0.8) = **약 14.4개월**

관련 설계: [reports/agent_similarity_design.md](../../reports/agent_similarity_design.md) §7.2

---

## 파일

| 파일 | 내용 |
|---|---|
| `entry_baseline.json` | 권역별 기준국가의 진출 기간(`duration_months`)·비용(`cost_usd`) + 유사도 배수표(`multiplier_table`) |

권역별 대표 baseline(`is_region_default: true`):
- 미주 → **미국**
- 유럽 → **독일**
- 아시아 & 태평양 → **한국**

---

## 🔧 나중에 교체할 곳 (실데이터 연결 시)

목업 → 실데이터 전환 시 **이 3가지**만 바꾸면 됩니다.

### 1. baseline 기간/비용 실측치
`entry_baseline.json` 의 각 국가 항목에서:
- `duration_months.value` → 실제 진출 소요 개월 수
- `cost_usd.value` → 실제 누적 진출 비용(USD)
- `estimated` → `true` → **`false`** 로 변경 (실측 확정 표시)
- `source` → `"MOCKUP"` → 실제 출처(예: `"사내 진출실적 DB / 2023 미국법인"`)
- `note` 의 `[목업]` 문구 제거

### 2. 유사도 배수표
`entry_baseline.json` 의 `multiplier_table.bands` 구간별 `duration_x` 값을
실제 진출 실적으로 보정. `multiplier_table.estimated` → `false`.

### 3. (선택) 데이터 소스 자체를 DB로
MVP는 JSON 파일을 직접 읽습니다. 운영 단계에서 DB로 옮길 경우,
AGENT의 baseline 로더가 이 JSON 대신 DB 테이블(예: `entry_baseline`)을 읽도록 교체.
→ 로더 인터페이스만 동일하게 유지하면 상위 로직(유사도·배수·보고서)은 무변경.

---

## ⚠️ 목업임을 알리는 표식 (검색용)

코드/데이터에서 아래 키워드로 목업 잔재를 찾을 수 있습니다:
- `"_REPLACE_ME"` — 교체 지점 마커
- `"source": "MOCKUP"` — 목업 값
- `"[목업]"` — note 내 목업 표시
- `"estimated": true` (이 폴더 한정) — 미확정 값

실데이터 전환 후 위 표식이 남아있지 않은지 확인하세요.
