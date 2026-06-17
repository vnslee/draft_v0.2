import type { CostEstimate as CostEstimateType } from '@/types/report'

export function CostEstimate({ data }: { data: CostEstimateType }) {
  if (!data.estimated) {
    return (
      <div className="bg-line-soft rounded-lg px-4 py-3 text-sm text-ink-soft">
        비용 추정 불가 — {data.reason ?? '기준국 비용 데이터 미확보'}
      </div>
    )
  }

  return (
    <div className="bg-panel border border-line rounded-lg px-4 py-3 space-y-1.5">
      <p className="text-xs text-ink-soft font-medium uppercase tracking-wide">비용 추정</p>
      <div className="flex items-baseline gap-2">
        <span className="text-2xl font-bold text-ink">
          ${data.estimated_cost_usd_million?.toFixed(1)}M
        </span>
        <span className="text-xs text-ink-soft">USD</span>
      </div>
      <div className="text-xs text-ink-soft space-y-0.5">
        <p>기준 비용: ${data.base_cost_usd_million?.toFixed(1)}M × 배수 {data.multiplier?.toFixed(1)}x</p>
        <p className="text-amber">※ 목업 기준값 — 실측 데이터로 교체 필요</p>
      </div>
    </div>
  )
}
