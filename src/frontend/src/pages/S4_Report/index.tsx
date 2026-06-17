import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { fetchReport } from '@/api/reports'
import { VerdictBadge } from '@/components/results/VerdictBadge'
import { ScoreBreakdown } from '@/components/results/ScoreBreakdown'
import { KillswitchWarning } from '@/components/results/KillswitchWarning'
import { CostEstimate } from '@/components/results/CostEstimate'
import type { Report } from '@/types/report'

const TIER_COLOR: Record<string, string> = {
  TIER1: 'text-verdict-ok',
  TIER2: 'text-amber',
  TIER3: 'text-ink-soft',
  BLOCKED: 'text-signal',
}

export default function S4Report() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [report, setReport] = useState<Report | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    fetchReport(id)
      .then(setReport)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <div className="p-8 text-ink-soft text-sm">보고서 로딩 중...</div>
  if (error) return <div className="p-8 text-signal text-sm">오류: {error}</div>
  if (!report) return null

  const allKillswitches = report.category_results.flatMap(c => c.killswitch_results)

  return (
    <div className="p-8 max-w-3xl space-y-6">
      {/* 헤더 */}
      <div className="flex items-start justify-between">
        <div>
          <button onClick={() => navigate(-1)} className="text-xs text-ink-soft mb-2 hover:text-ink">
            ← 뒤로
          </button>
          <h2 className="text-2xl font-bold text-ink">{report.target_country} 진출 분석 보고서</h2>
          <p className="text-sm text-ink-soft mt-1">
            기준국: {report.compared_country} · {new Date(report.created_at).toLocaleDateString('ko-KR')}
          </p>
        </div>
        <VerdictBadge verdict={report.verdict} />
      </div>

      {/* 킬스위치 경고 */}
      {allKillswitches.length > 0 && <KillswitchWarning hits={allKillswitches} />}

      {/* 종합 점수 */}
      <div className="bg-panel border border-line rounded-xl p-6 flex items-center justify-between">
        <div>
          <p className="text-xs text-ink-soft mb-1">종합 유사도 점수</p>
          <p className="text-4xl font-bold text-ink">{report.total_score?.toFixed(1) ?? '-'}</p>
        </div>
        {report.cost_estimate && <CostEstimate data={report.cost_estimate} />}
      </div>

      {/* 카테고리 점수 */}
      <div className="bg-panel border border-line rounded-xl p-6">
        <h3 className="text-sm font-semibold text-ink mb-4">카테고리별 분석</h3>
        <ScoreBreakdown categories={report.category_results} totalScore={null} />
      </div>

      {/* AI 요약 */}
      {report.summary && (
        <div className="bg-panel border border-line rounded-xl p-6">
          <h3 className="text-sm font-semibold text-ink mb-3">요약</h3>
          <p className="text-sm text-ink leading-relaxed whitespace-pre-wrap">{report.summary}</p>
        </div>
      )}

      {/* AI 인사이트 */}
      {report.ai_insight && (
        <div className="bg-accent-soft border border-accent rounded-xl p-6">
          <h3 className="text-sm font-semibold text-accent mb-3">AI 인사이트</h3>
          <p className="text-sm text-ink leading-relaxed whitespace-pre-wrap">{report.ai_insight}</p>
        </div>
      )}

      {/* 항목별 상세 */}
      {report.category_results.map(cat => (
        <div key={cat.category} className="bg-panel border border-line rounded-xl overflow-hidden">
          <div className="px-5 py-3 bg-line-soft border-b border-line">
            <h3 className="text-sm font-semibold text-ink">{cat.category} 상세</h3>
          </div>
          <div className="divide-y divide-line">
            {cat.items.map(item => (
              <div key={item.catalog_item_id} className="px-5 py-3 flex gap-4 text-xs">
                <div className="w-40 shrink-0">
                  <p className="font-medium text-ink">{item.catalog_item_id}</p>
                  <p className={`${TIER_COLOR[item.source_tier] ?? 'text-ink-soft'}`}>
                    {item.source_tier}
                  </p>
                </div>
                <div className="flex-1">
                  {item.is_missing ? (
                    <span className="text-amber">비교 불가 — 데이터 미확보</span>
                  ) : (
                    <p className="text-ink-soft">{item.evidence || '근거 없음'}</p>
                  )}
                </div>
                <div className="w-16 text-right shrink-0">
                  {item.similarity !== null
                    ? <span className="font-mono text-ink">{(item.similarity * 100).toFixed(1)}</span>
                    : <span className="text-ink-soft">-</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}

      {/* 사람 검토 필요 항목 */}
      {report.human_review_flags.length > 0 && (
        <div className="bg-amber-soft border border-amber rounded-xl p-5">
          <h3 className="text-sm font-semibold text-amber mb-2">사람 검토 필요</h3>
          <ul className="space-y-1">
            {report.human_review_flags.map((flag, i) => (
              <li key={i} className="text-xs text-amber">• {flag}</li>
            ))}
          </ul>
        </div>
      )}

      {/* 액션 */}
      <div className="flex gap-3">
        <button
          onClick={() => navigate('/diagnosis')}
          className="flex-1 py-2.5 bg-ink text-white rounded-lg text-sm font-medium hover:bg-ink/90"
        >
          새 분석 실행
        </button>
        <button
          onClick={() => navigate('/settings')}
          className="flex-1 py-2.5 bg-panel border border-line text-ink rounded-lg text-sm font-medium hover:bg-line-soft"
        >
          이 보고서 가중치로 재실행
        </button>
      </div>
    </div>
  )
}
