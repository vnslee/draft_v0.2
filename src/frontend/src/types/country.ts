export interface Country {
  name: string
  country_id: string | null    // ISO 3166-1 alpha-2 (KR, US, DE ...)
  region: string | null
  entry_status: string | null  // 진출 | 진출예정 | 미진출
  country_code: string | null
}
