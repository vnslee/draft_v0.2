import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCountries } from '@/hooks/useCountries'
import { fetchReports } from '@/api/reports'
import { VerdictBadge } from '@/components/results/VerdictBadge'
import { useAnalysisStore } from '@/store/analysisStore'
import type { ReportSummary } from '@/types/report'

const STATUS_COLOR: Record<string, string> = {
  '진출': '#1a1a1a',
  '진출예정': '#6b7280',
  '미진출': '#9ca3af',
}

export default function S0Main() {
  const navigate = useNavigate()
  const { countries, loading } = useCountries()
  const [reports, setReports] = useState<ReportSummary[]>([])
  const [selectedCountry, setSelectedCountry] = useState<string | null>(null)
  useAnalysisStore()

  useEffect(() => {
    fetchReports(5).then(setReports).catch(() => {})
  }, [])

  const enteredCount = countries.filter(c => c.entry_status === '진출').length
  const candidateCount = countries.filter(c => c.entry_status === '진출예정').length

  return (
    <div className="p-8 max-w-5xl">
      {/* 헤더 */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-ink">대시보드</h2>
        <p className="text-sm text-ink-soft mt-1">오토금융 해외진출 의사결정 지원 시스템</p>
      </div>

      {/* 요약 카드 */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-panel border border-line rounded-xl p-5">
          <p className="text-xs text-ink-soft uppercase tracking-wide mb-1">진출 완료국</p>
          <p className="text-3xl font-bold text-ink">{enteredCount}</p>
        </div>
        <div className="bg-panel border border-line rounded-xl p-5">
          <p className="text-xs text-ink-soft uppercase tracking-wide mb-1">진출 예정국</p>
          <p className="text-3xl font-bold text-ink">{candidateCount}</p>
        </div>
        <div className="bg-panel border border-line rounded-xl p-5">
          <p className="text-xs text-ink-soft uppercase tracking-wide mb-1">최근 분석</p>
          <p className="text-3xl font-bold text-ink">{reports.length}</p>
        </div>
      </div>

      {/* 국가 목록 + 진단 진입 */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div className="bg-panel border border-line rounded-xl p-5">
          <h3 className="text-sm font-semibold text-ink mb-3">국가 현황</h3>
          {loading ? (
            <p className="text-xs text-ink-soft">로딩 중...</p>
          ) : (
            <div className="space-y-1 max-h-64 overflow-y-auto">
              {countries.map(c => (
                <button
                  key={c.name}
                  onClick={() => setSelectedCountry(c.name === selectedCountry ? null : c.name)}
                  className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs transition-colors ${
                    selectedCountry === c.name ? 'bg-accent-soft' : 'hover:bg-line-soft'
                  }`}
                >
                  <span className="text-ink">{c.name}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-ink-soft">{c.region}</span>
                    <span
                      className="px-2 py-0.5 rounded-full text-[10px] font-medium"
                      style={{
                        background: `${STATUS_COLOR[c.entry_status ?? ''] ?? '#9ca3af'}20`,
                        color: STATUS_COLOR[c.entry_status ?? ''] ?? '#9ca3af',
                      }}
                    >
                      {c.entry_status ?? '미확인'}
                    </span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="space-y-4">
          {/* 선택된 국가 카드 */}
          {selectedCountry && (
            <div className="bg-accent-soft border border-accent rounded-xl p-5">
              <p className="text-xs text-accent font-semibold uppercase tracking-wide mb-1">선택된 국가</p>
              <p className="text-xl font-bold text-ink mb-3">{selectedCountry}</p>
              <button
                onClick={() => navigate('/diagnosis', {
                  state: { country: countries.find(c => c.name === selectedCountry)?.country_id ?? selectedCountry },
                })}
                className="w-full py-2 bg-accent text-white rounded-lg text-sm font-medium hover:bg-accent/90 transition-colors"
              >
                🔍 국가 진단 시작
              </button>
            </div>
          )}

          {/* 빠른 진입 */}
          <div className="bg-panel border border-line rounded-xl p-5 space-y-2">
            <h3 className="text-sm font-semibold text-ink mb-3">바로 시작</h3>
            <button
              onClick={() => navigate('/diagnosis')}
              className="w-full py-2.5 bg-ink text-white rounded-lg text-sm font-medium hover:bg-ink/90 transition-colors"
            >
              🔍 단일 국가 진단
            </button>
            <button
              onClick={() => navigate('/ranking')}
              className="w-full py-2.5 bg-panel border border-line text-ink rounded-lg text-sm font-medium hover:bg-line-soft transition-colors"
            >
              📊 권역 순위 분석
            </button>
          </div>
        </div>
      </div>

      {/* 최근 보고서 */}
      {reports.length > 0 && (
        <div className="bg-panel border border-line rounded-xl p-5">
          <h3 className="text-sm font-semibold text-ink mb-3">최근 분석 보고서</h3>
          <div className="space-y-2">
            {reports.map(r => (
              <button
                key={r.id}
                onClick={() => navigate(`/reports/${r.id}`)}
                className="w-full flex items-center justify-between px-3 py-2.5 rounded-lg hover:bg-line-soft transition-colors text-xs"
              >
                <div className="flex items-center gap-3">
                  <span className="font-medium text-ink">{r.target_country}</span>
                  <span className="text-ink-soft">vs {r.compared_country}</span>
                </div>
                <div className="flex items-center gap-3">
                  {r.total_score !== null && (
                    <span className="text-ink-soft">{r.total_score.toFixed(1)}점</span>
                  )}
                  <VerdictBadge verdict={r.verdict} />
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
