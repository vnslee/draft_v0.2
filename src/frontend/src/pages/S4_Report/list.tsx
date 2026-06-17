import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { fetchReports } from '@/api/reports'
import { VerdictBadge } from '@/components/results/VerdictBadge'
import type { ReportSummary } from '@/types/report'

export default function ReportList() {
  const navigate = useNavigate()
  const [reports, setReports] = useState<ReportSummary[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchReports(50).then(setReports).finally(() => setLoading(false))
  }, [])

  return (
    <div className="p-8 max-w-3xl">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-ink">보고서 목록</h2>
        <p className="text-sm text-ink-soft mt-1">완료된 분석 보고서</p>
      </div>

      {loading ? (
        <p className="text-ink-soft text-sm">로딩 중...</p>
      ) : reports.length === 0 ? (
        <div className="bg-panel border border-line rounded-xl p-12 text-center text-ink-soft text-sm">
          아직 분석 보고서가 없습니다
        </div>
      ) : (
        <div className="bg-panel border border-line rounded-xl divide-y divide-line">
          {reports.map(r => (
            <button
              key={r.id}
              onClick={() => navigate(`/reports/${r.id}`)}
              className="w-full flex items-center justify-between px-5 py-4 hover:bg-line-soft/50 transition-colors text-left"
            >
              <div>
                <p className="text-sm font-medium text-ink">{r.target_country}</p>
                <p className="text-xs text-ink-soft">vs {r.compared_country} · {new Date(r.created_at).toLocaleDateString('ko-KR')}</p>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-sm font-mono text-ink">
                  {r.total_score?.toFixed(1) ?? '-'}점
                </span>
                <VerdictBadge verdict={r.verdict} />
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
