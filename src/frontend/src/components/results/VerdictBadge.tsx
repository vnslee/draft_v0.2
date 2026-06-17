import type { Verdict } from '@/types/analysis'

const CONFIG: Record<string, { label: string; className: string }> = {
  TRANSPLANTABLE: { label: '이식 가능',  className: 'bg-green-soft text-verdict-ok border-verdict-ok' },
  DEEP_RESEARCH:  { label: '심층 조사',  className: 'bg-amber-soft text-verdict-deep border-verdict-deep' },
  BLOCKED:        { label: '진출 차단',  className: 'bg-signal-soft text-verdict-blocked border-verdict-blocked' },
  FAILED:         { label: '분석 실패',  className: 'bg-line text-ink-soft border-line' },
}

export function VerdictBadge({ verdict }: { verdict: Verdict | string }) {
  const cfg = CONFIG[verdict] ?? { label: verdict, className: 'bg-line text-ink-soft border-line' }
  return (
    <span className={`inline-flex items-center px-3 py-1 rounded-full border text-xs font-semibold ${cfg.className}`}>
      {cfg.label}
    </span>
  )
}
