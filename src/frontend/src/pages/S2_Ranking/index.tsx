import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { VerdictBadge } from '@/components/results/VerdictBadge'
import type { ReportSummary } from '@/types/report'

const REGIONS = ['아시아 & 태평양', '유럽', '미주', '중동 & 아프리카']

export default function S2Ranking() {
  const navigate = useNavigate()
  const [selectedRegion, setSelectedRegion] = useState<string>(REGIONS[0])
  const [results] = useState<ReportSummary[]>([])
  const [running, setRunning] = useState(false)

  const handleRun = async () => {
    setRunning(true)
    // TODO: 권역 분석 API 연동 (Phase 4)
    setTimeout(() => setRunning(false), 1000)
  }

  return (
    <div className="p-8 max-w-4xl">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-ink">권역 순위</h2>
        <p className="text-sm text-ink-soft mt-1">권역 내 국가들을 일괄 분석하고 진출 우선순위를 산출합니다</p>
      </div>

      {/* 권역 선택 */}
      <div className="bg-panel border border-line rounded-xl p-6 mb-6">
        <label className="text-xs text-ink-soft font-medium block mb-3">권역 선택</label>
        <div className="flex gap-2 flex-wrap mb-4">
          {REGIONS.map(r => (
            <button
              key={r}
              onClick={() => setSelectedRegion(r)}
              className={`px-4 py-2 rounded-full text-sm transition-colors ${
                selectedRegion === r
                  ? 'bg-accent text-white'
                  : 'bg-paper border border-line text-ink-soft hover:border-accent'
              }`}
            >
              {r}
            </button>
          ))}
        </div>
        <button
          onClick={handleRun}
          disabled={running}
          className="w-full py-3 bg-accent text-white rounded-lg font-medium text-sm disabled:opacity-40 hover:bg-accent/90 transition-colors"
        >
          {running ? '분석 중...' : `📊 ${selectedRegion} 권역 분석 실행`}
        </button>
      </div>

      {/* 결과 테이블 */}
      {results.length > 0 ? (
        <div className="bg-panel border border-line rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-line-soft">
              <tr>
                <th className="px-4 py-3 text-left text-xs text-ink-soft font-medium">순위</th>
                <th className="px-4 py-3 text-left text-xs text-ink-soft font-medium">국가</th>
                <th className="px-4 py-3 text-right text-xs text-ink-soft font-medium">점수</th>
                <th className="px-4 py-3 text-center text-xs text-ink-soft font-medium">판정</th>
                <th className="px-4 py-3 text-center text-xs text-ink-soft font-medium">보고서</th>
              </tr>
            </thead>
            <tbody>
              {results.map((r, i) => (
                <tr key={r.id} className="border-t border-line hover:bg-line-soft/50 transition-colors">
                  <td className="px-4 py-3 text-ink-soft font-mono">{i + 1}</td>
                  <td className="px-4 py-3 font-medium text-ink">{r.target_country}</td>
                  <td className="px-4 py-3 text-right font-mono text-ink">
                    {r.total_score?.toFixed(1) ?? '-'}
                  </td>
                  <td className="px-4 py-3 text-center">
                    <VerdictBadge verdict={r.verdict} />
                  </td>
                  <td className="px-4 py-3 text-center">
                    <button
                      onClick={() => navigate(`/reports/${r.id}`)}
                      className="text-xs text-accent underline"
                    >
                      보기
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="bg-panel border border-line rounded-xl p-12 text-center text-ink-soft text-sm">
          권역을 선택하고 분석을 실행하세요
        </div>
      )}
    </div>
  )
}
