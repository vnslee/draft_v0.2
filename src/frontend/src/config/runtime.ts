/**
 * runtime.ts — 앱이 서빙되는 경로 접두어(base path)를 런타임에 자동 감지.
 *
 * 배포 환경에 따라 앱이 루트(`/`)가 아닌 하위 경로에서 서빙될 수 있다.
 *  - 코드 에디터 포트 프록시: `/ports/5173/` 하위 (프록시가 이 접두어를 떼고 vite로 전달)
 *  - 정식 nginx 배포: 루트 `/`
 *
 * 접두어는 빌드 산출물 JS의 자체 URL(import.meta.url)에서 추출한다.
 * 예) https://host/ports/5173/assets/index-abc.js → BASE_PATH = "/ports/5173"
 *     https://host/assets/index-abc.js           → BASE_PATH = ""
 * 라우트 경로와 무관하게 항상 자산 경로 기준이므로 딥링크 새로고침에도 안전하다.
 */
function detectBasePath(): string {
  try {
    const pathname = new URL(import.meta.url).pathname
    const idx = pathname.indexOf('/assets/')
    return idx > 0 ? pathname.slice(0, idx) : ''
  } catch {
    return ''
  }
}

/** 앱 경로 접두어. 예: "/ports/5173" 또는 "" (루트 배포). */
export const BASE_PATH = detectBasePath()
