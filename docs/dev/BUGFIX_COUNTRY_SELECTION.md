# 버그 수정: 국가 선택 데이터 동기화

## 🐛 문제 상황

**증상:**
- S1에서 "영국" 선택 후 진단 실행
- 결과는 항상 "인도" 데이터로 표시됨
- S4 보고서도 "인도" 데이터로 고정됨

**원인:**
1. S1 결과 패널에 하드코딩된 "인도" 데이터
2. S4 보고서에 하드코딩된 "인도" 데이터
3. 선택된 국가 정보가 전역 상태에 저장되지 않음
4. UI 컴포넌트가 선택된 국가 데이터를 참조하지 않음

## ✅ 수정 내용

### 1. 설계 문서 업데이트 (04_화면설계흐름.md)

**추가된 원칙:**
```markdown
> **데이터 동기화 원칙:**
> - 사용자가 S1에서 선택한 국가 정보는 전역 상태(analysisState)에 저장
> - 상태 카드, 팝업, 결과 패널, 보고서 모두 동일한 국가 데이터 참조
> - 국가 변경 시 모든 UI 컴포넌트 동시 업데이트
> - 하드코딩된 국가 데이터 사용 금지 (Mock 데이터도 선택한 국가 기반으로 생성)
```

### 2. 전역 상태 확장

**Before:**
```javascript
analysisState = {
  isRunning: false,
  country: '',
  countryFlag: '',
  startTime: null,
  agents: { ... }
}
```

**After:**
```javascript
analysisState = {
  isRunning: false,
  country: '',
  countryCode: '', // 추가: 선택된 국가 코드 저장
  countryFlag: '',
  startTime: null,
  agents: { ... }
}
```

### 3. 국가 데이터 구조 추가

```javascript
const countryData = {
  'india': {
    name: '인도',
    flag: '🇮🇳',
    region: '아시아·태평양',
    score: 74,
    license: 'NBFC-ICC 등록',
    licenseDetail: '(Investment and Credit Company)',
    capital: 'NOF ₹10 crore',
    capitalUSD: '(약 $1.2M USD)',
    authority: 'Reserve Bank of India',
    restriction: '외국인 지분 한도 49%'
  },
  'uk': {
    name: '영국',
    flag: '🇬🇧',
    region: '유럽',
    score: 78,
    license: 'FCA 인가',
    licenseDetail: '(Financial Conduct Authority)',
    capital: '£1M',
    capitalUSD: '(약 $1.3M USD)',
    authority: 'Financial Conduct Authority',
    restriction: '외국인 지분 제한 없음'
  },
  // ... 기타 국가
}
```

### 4. 함수 수정

#### `showAnalysisStatus()` - 국가 코드 저장
```javascript
function showAnalysisStatus(country, countryCode) {
  // 전역 상태에 선택된 국가 정보 저장
  analysisState.country = name;
  analysisState.countryCode = countryCode; // 추가
  analysisState.countryFlag = flag;
  
  console.log(`[showAnalysisStatus] 국가 설정: ${name} (${countryCode})`);
  // ...
}
```

#### `showDiagnosisResults()` - 동적 데이터 로딩
```javascript
function showDiagnosisResults(countryCode) {
  const country = countryData[countryCode] || countryData['india'];
  
  console.log(`[showDiagnosisResults] 결과 표시: ${country.name}`);
  
  // Update all UI elements with selected country data
  document.querySelector('.score-details h3').textContent = country.name;
  document.getElementById('scoreValue').textContent = country.score;
  
  // Update license information dynamically
  licenseSection.innerHTML = `
    <div>${country.license}</div>
    <div>${country.capital}</div>
    <div>${country.authority}</div>
    <div>${country.restriction}</div>
  `;
  // ...
}
```

#### `updateReportView()` - 보고서 동적 업데이트 (신규)
```javascript
function updateReportView() {
  const countryCode = analysisState.countryCode;
  const country = countryData[countryCode] || countryData['india'];
  
  console.log(`[updateReportView] 보고서 업데이트: ${country.name}`);
  
  // Update report header
  reportTitle.innerHTML = `
    <span>${country.flag}</span>
    <span>${country.name} 진출 진단 보고서</span>
  `;
  
  // Update license section in report
  // ...
}
```

#### `viewReport()` - 보고서 열기 시 업데이트
```javascript
function viewReport() {
  closeAnalysisModal();
  hideAnalysisStatus();
  
  // Update S4 report with selected country data
  updateReportView(); // 추가
  
  navigate('s4');
}
```

## 🔄 데이터 흐름

```
1. 사용자 국가 선택
   ↓
   S1: <select id="targetCountry">
   value = "uk" (영국)

2. 진단 실행 버튼 클릭
   ↓
   runDiagnosis()
   → startMultiAgentAnalysis('영국', 'uk')
   → showAnalysisStatus('영국', 'uk')

3. 전역 상태 저장
   ↓
   analysisState.country = '영국'
   analysisState.countryCode = 'uk'
   analysisState.countryFlag = '🇬🇧'

4. 분석 완료
   ↓
   showDiagnosisResults('uk')
   → countryData['uk'] 조회
   → 영국 데이터로 UI 업데이트

5. 보고서 보기 클릭
   ↓
   viewReport()
   → updateReportView()
   → countryData[analysisState.countryCode] 조회
   → S4 보고서를 영국 데이터로 업데이트
```

## 🧪 테스트 시나리오

### 시나리오 1: 영국 선택
1. S1 화면 이동
2. 대상 국가: **영국** 선택
3. 진단 실행 클릭
4. **확인 사항:**
   - ✅ 상태 카드: "🇬🇧 영국 분석 중..."
   - ✅ 팝업 제목: "🇬🇧 영국 진출 진단 분석 중"
   - ✅ 결과 패널 제목: "영국"
   - ✅ 점수: 78점
   - ✅ 라이선스: "FCA 인가"
   - ✅ 자본금: "£1M"
   - ✅ 발급기관: "Financial Conduct Authority"
5. 보고서 보기 클릭
6. **확인 사항:**
   - ✅ 보고서 제목: "🇬🇧 영국 진출 진단 보고서"
   - ✅ 권역: "유럽"
   - ✅ 라이선스 정보: 영국 데이터

### 시나리오 2: 멕시코 선택
1. S1 화면에서 대상 국가: **멕시코** 선택
2. 진단 실행
3. **확인 사항:**
   - ✅ 상태 카드: "🇲🇽 멕시코 분석 중..."
   - ✅ 점수: 62점
   - ✅ 라이선스: "SOFOM ENR"
   - ✅ 자본금: "MXN 5,000만"
   - ✅ 권역: "미주"

### 시나리오 3: 스페인 선택
1. S1 화면에서 대상 국가: **스페인** 선택
2. 진단 실행
3. **확인 사항:**
   - ✅ 상태 카드: "🇪🇸 스페인 분석 중..."
   - ✅ 점수: 81점
   - ✅ 라이선스: "EFC 인가"
   - ✅ 자본금: "€5M"
   - ✅ 권역: "유럽"

## 🎯 해결된 문제

### Before (버그 상태)
```
선택: 영국 → 결과: 인도 ❌
선택: 멕시코 → 결과: 인도 ❌
선택: 스페인 → 결과: 인도 ❌
```

### After (수정 후)
```
선택: 영국 → 결과: 영국 ✅
선택: 멕시코 → 결과: 멕시코 ✅
선택: 스페인 → 결과: 스페인 ✅
```

## 📊 지원되는 국가

| 코드 | 국가명 | 플래그 | 권역 | 점수 |
|------|--------|--------|------|------|
| india | 인도 | 🇮🇳 | 아시아·태평양 | 74 |
| indonesia | 인도네시아 | 🇮🇩 | 아시아·태평양 | 68 |
| mexico | 멕시코 | 🇲🇽 | 미주 | 62 |
| spain | 스페인 | 🇪🇸 | 유럽 | 81 |
| uk | 영국 | 🇬🇧 | 유럽 | 78 |
| poland | 폴란드 | 🇵🇱 | 유럽 | 70 |

## 🔍 디버깅 로그

추가된 콘솔 로그로 데이터 흐름 추적 가능:

```javascript
[showAnalysisStatus] 국가 설정: 영국 (uk)
[showDiagnosisResults] 결과 표시: 영국 (uk)
[updateReportView] 보고서 업데이트: 영국 (uk)
```

## 📝 추가 개선 사항

### 향후 작업
- [ ] 백엔드 API 연동 시 countryData를 서버에서 가져오기
- [ ] 국가별 실제 데이터 수집 및 교체
- [ ] 국가 추가 시 자동 UI 업데이트 시스템
- [ ] 국가별 분석 히스토리 저장

### 확장 가능성
```javascript
// 백엔드 연동 예시
async function loadCountryData(countryCode) {
  const response = await fetch(`/api/countries/${countryCode}`);
  const data = await response.json();
  return data;
}

// 사용
const country = await loadCountryData(analysisState.countryCode);
showDiagnosisResults(country);
```

## 📁 수정된 파일

1. ✅ `04_화면설계흐름.md` - 데이터 동기화 원칙 추가
2. ✅ `dashboard.html` - 전역 상태 확장 및 함수 수정
3. ✅ `MULTI_AGENT_README.md` - 상태 관리 문서 업데이트
4. ✅ `BUGFIX_COUNTRY_SELECTION.md` - 본 문서 (수정 내역)

---

**Version**: v1.1
**Date**: 2026-06-16
**Status**: ✅ 수정 완료
**Impact**: 🔴 Critical Bug Fix
