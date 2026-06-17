import type { CategoryResult } from '@/types/report'

const CATEGORY_LABELS: Record<string, string> = {
  MARKET: '시장',
  REGULATORY: '규제',
  FINANCIAL: '금융환경',
  SYSTEM: '시스템',
}

const CATEGORY_WEIGHTS: Record<string, number> = {
  MARKET: 25,
  REGULATORY: 25,
  FINANCIAL: 20,
  SYSTEM: 30,
}

interface Props {
  categories: CategoryResult[]
  totalScore: number | null
}

export function ScoreBreakdown({ categories, totalScore }: Props) {
  return (
    <div className="space-y-3">
      {totalScore !== null && (
        <div className="flex items-center justify-between mb-4">
          <span className="text-sm text-ink-soft">종합 유사도 점수</span>
          <span className="text-3xl font-bold text-ink">{totalScore.toFixed(1)}</span>
        </div>
      )}
      {categories.map(cat => {
        const score = cat.category_score ?? null
        const width = score !== null ? Math.min(100, Math.max(0, score)) : 0
        const barColor = score === null ? 'bg-line' :
          score >= 60 ? 'bg-verdict-ok' :
          score >= 40 ? 'bg-verdict-deep' : 'bg-verdict-blocked'

        return (
          <div key={cat.category}>
            <div className="flex items-center justify-between text-xs mb-1">
              <span className="text-ink-soft">
                {CATEGORY_LABELS[cat.category] ?? cat.category}
                <span className="ml-1 text-[10px] text-ink-soft/60">
                  (가중치 {CATEGORY_WEIGHTS[cat.category] ?? '-'}%)
                </span>
              </span>
              <div className="flex items-center gap-2">
                {cat.coverage < 0.5 && (
                  <span className="text-amber text-[10px]">데이터 부족</span>
                )}
                <span className="font-medium text-ink">
                  {score !== null ? score.toFixed(1) : '비교 불가'}
                </span>
              </div>
            </div>
            <div className="h-2 bg-line rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-500 ${barColor}`}
                style={{ width: `${width}%` }}
              />
            </div>
            {cat.warnings.length > 0 && (
              <ul className="mt-1 space-y-0.5">
                {cat.warnings.map((w, i) => (
                  <li key={i} className="text-[11px] text-amber">⚠ {w}</li>
                ))}
              </ul>
            )}
          </div>
        )
      })}
    </div>
  )
}
