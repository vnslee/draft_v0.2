# 세계 지도 인터랙티브 기능

## 🗺️ 개요

S0 대시보드에 SVG 기반 인터랙티브 세계 지도가 추가되었습니다.
주요 국가 13개를 표시하며, 진출 상태에 따라 색상으로 구분됩니다.

## 📍 표시되는 국가

### 아시아·태평양 권역 (5개국)
| 국가 | 코드 | 상태 | 색상 |
|------|------|------|------|
| 🇰🇷 한국 | KR | 진출국 | 검정 |
| 🇮🇳 인도 | IN | 이식 가능 | 초록 |
| 🇮🇩 인도네시아 | ID | 심층조사 | 황색 |
| 🇨🇳 중국 | CN | 진출국 | 검정 |
| 🇦🇺 호주 | AU | 진출국 | 검정 |

### 유럽 권역 (5개국)
| 국가 | 코드 | 상태 | 색상 |
|------|------|------|------|
| 🇩🇪 독일 | DE | 진출국 | 검정 |
| 🇬🇧 영국 | UK | 이식 가능 | 초록 |
| 🇪🇸 스페인 | ES | 이식 가능 | 초록 |
| 🇵🇱 폴란드 | PL | 심층조사 | 황색 |
| 🇷🇺 러시아 | RU | 진출국 | 검정 |

### 미주 권역 (3개국)
| 국가 | 코드 | 상태 | 색상 |
|------|------|------|------|
| 🇺🇸 미국 | US | 진출국 | 검정 |
| 🇨🇦 캐나다 | CA | 진출국 | 검정 |
| 🇲🇽 멕시코 | MX | 심층조사 | 황색 |

## 🎨 색상 구분

| 상태 | 색상 | CSS 변수 | 의미 |
|------|------|----------|------|
| 진출국 | 검정 | `--ink` (#16201c) | 이미 진출 완료 |
| 이식 가능 | 초록 | `--green` (#2d7a5f) | 진출 권장 (70점 이상) |
| 심층조사 | 황색 | `--amber` (#b88324) | 추가 조사 필요 (50-70점) |
| 차단 | 적색 | `--signal` (#c5562e) | 킬스위치 작동 |
| 미조사 | 회색 | `--line-soft` (#e7e3d8) | 데이터 없음 |

## 🖱️ 인터랙션

### 1. 마우스 오버 (Hover)
```
동작: 국가 위에 마우스 올림
결과: 
  - 국가가 약간 밝아짐 (brightness 1.1)
  - 툴팁 표시: "인도 (이식 가능)"
  - 툴팁 위치: 국가 마커 위쪽
```

### 2. 클릭 (Click)
```
동작: 국가 마커 클릭
결과:
  - 우측 "국가 상세 카드" 업데이트
  - 국가명, 권역, 상태 표시
  - 상태별 액션 버튼 표시
  - 카드 위치로 자동 스크롤
```

### 3. 상세 카드 업데이트

**진출국 클릭 시:**
```
┌─────────────────────────────┐
│ 🇰🇷 한국                    │
│ 아시아·태평양               │
│ [진출]                      │
│                             │
│ 진출 시점: 2020-03          │
│ 진출 비용: $1,500,000       │
│                             │
│ [실적 데이터 보기]          │
└─────────────────────────────┘
```

**분석 가능 국가 클릭 시:**
```
┌─────────────────────────────┐
│ 🇮🇳 인도                    │
│ 아시아·태평양               │
│ [이식 가능]                 │
│                             │
│ 종합 점수: 74점             │
│ 판정: 이식 가능             │
│                             │
│ [단일 진단 보기] [조사 데이터]│
└─────────────────────────────┘
```

## 💻 기술 구현

### SVG 구조
```svg
<svg viewBox="0 0 1000 500">
  <!-- 국가 마커 (원형) -->
  <circle 
    cx="650" 
    cy="230" 
    r="30" 
    class="country-marker transplantable" 
    data-country="india" 
    data-status="transplantable"
  />
  
  <!-- 국가 코드 라벨 -->
  <text x="650" y="235" class="country-label">IN</text>
</svg>
```

### CSS 클래스
```css
.country-marker {
  cursor: pointer;
  transition: all 0.2s;
  stroke: white;
  stroke-width: 1;
}

.country-marker:hover {
  opacity: 0.8;
  filter: brightness(1.1);
}

.country-marker.transplantable {
  fill: var(--green);
}
```

### JavaScript 이벤트
```javascript
function initWorldMap() {
  const markers = document.querySelectorAll('.country-marker');
  
  markers.forEach(marker => {
    // Hover: 툴팁 표시
    marker.addEventListener('mouseenter', (e) => {
      showTooltip(e);
    });
    
    // Click: 상세 카드 업데이트
    marker.addEventListener('click', (e) => {
      const country = e.target.getAttribute('data-country');
      const status = e.target.getAttribute('data-status');
      selectCountryOnMap(country, status);
    });
  });
}
```

## 🔄 화면 전이

### 지도 → S1 (단일 진단)
```
1. 지도에서 "인도" 클릭
   ↓
2. 상세 카드 업데이트
   "🇮🇳 인도 (이식 가능)"
   ↓
3. "단일 진단 보기" 버튼 클릭
   ↓
4. S1 화면으로 이동
   대상 국가가 "인도"로 자동 선택됨
```

### 지도 → S5 (데이터 관리)
```
1. 지도에서 "한국" 클릭 (진출국)
   ↓
2. 상세 카드 업데이트
   "🇰🇷 한국 (진출)"
   ↓
3. "실적 데이터 보기" 버튼 클릭
   ↓
4. S5 화면으로 이동
```

## 📏 레이아웃

```
S0 대시보드
├── 상단: 요약 통계 (4개 카드)
├── 중단: 세계 지도 ← 새로 추가
│   ├── SVG 지도 (1000×500)
│   ├── 툴팁 (호버 시 표시)
│   └── 범례 (5가지 색상)
└── 하단: 
    ├── 국가 상세 카드
    └── 최근 분석 목록
```

## 🎯 사용자 여정

### 여정 1: 지도에서 국가 탐색
```
1. S0 대시보드 접속
2. 지도 위에서 마우스 이동
   → 각 국가 툴팁으로 상태 확인
3. 관심 국가 클릭 (예: 영국)
4. 우측 카드에서 상세 정보 확인
   - 점수: 78점
   - 판정: 이식 가능
5. "단일 진단 보기" 버튼 클릭
6. S1에서 영국 진단 실행
```

### 여정 2: 권역별 현황 파악
```
1. 지도에서 유럽 권역 확인
   - 독일 (진출) ← 검정
   - 영국 (이식 가능) ← 초록
   - 스페인 (이식 가능) ← 초록
   - 폴란드 (심층조사) ← 황색
   - 러시아 (진출) ← 검정
2. 초록색 국가들 클릭해서 점수 비교
3. 최고 점수 국가 선택 → 진단 실행
```

## 🔧 확장 가능성

### 향후 개선 사항
- [ ] 실제 세계지도 SVG Path 사용 (더 정교한 국경선)
- [ ] 국가 추가 (현재 13개 → 50개 이상)
- [ ] 애니메이션 효과 (최근 분석 국가 펄스 효과)
- [ ] 줌/팬 기능 (D3.js 활용)
- [ ] 권역별 필터링 (유럽만 보기 등)
- [ ] 점수 히트맵 (색상 농도로 점수 표현)

### 라이브러리 활용 (선택사항)
```javascript
// D3.js + TopoJSON 활용 예시
import * as d3 from 'd3';
import * as topojson from 'topojson-client';

// 실제 세계지도 렌더링
const worldData = await fetch('/data/world-110m.json');
const countries = topojson.feature(worldData, worldData.objects.countries);

svg.selectAll('path')
  .data(countries.features)
  .enter().append('path')
  .attr('d', pathGenerator)
  .attr('class', d => getCountryStatus(d.id))
  .on('click', handleCountryClick);
```

## 📊 데이터 구조

### 국가 상태 매핑
```javascript
const countryStatus = {
  'korea': 'entered',
  'india': 'transplantable',
  'indonesia': 'investigate',
  'uk': 'transplantable',
  'spain': 'transplantable',
  'poland': 'investigate',
  'mexico': 'investigate',
  // ...
};

const countryScores = {
  'india': 74,
  'uk': 78,
  'spain': 81,
  'indonesia': 68,
  'poland': 70,
  'mexico': 62
};
```

## 🎨 디자인 가이드

### 색상 접근성
- 색상만으로 구분하지 않음 (아이콘/텍스트 병기)
- 색맹 사용자 고려 (초록/적색 대비 명확)
- 툴팁으로 상태 명시

### 반응형
```css
@media (max-width: 860px) {
  .world-map {
    height: 300px; /* 모바일에서 높이 축소 */
  }
  
  .country-label {
    font-size: 8px; /* 텍스트 크기 축소 */
  }
}
```

## 📝 관련 파일

- `dashboard.html` - SVG 지도 구조 + JavaScript
- `04_화면설계흐름.md` - 지도 인터랙션 설계
- `MULTI_AGENT_README.md` - 사용 가이드
- `WORLD_MAP_FEATURE.md` - 본 문서

---

**Version**: v1.0
**Date**: 2026-06-16
**Status**: ✅ 구현 완료
**Feature**: 🗺️ Interactive World Map
