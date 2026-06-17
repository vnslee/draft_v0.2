interface KillswitchHit {
  item_id: string
  blocked: boolean
  reason?: string
}

interface Props {
  hits: KillswitchHit[]
}

const ITEM_LABELS: Record<string, string> = {
  foreign_ownership_limit: '외국인 지분 한도',
  fx_remittance: '외환 송금 규제',
  dividend_remittance: '배당 송금 제한',
  data_localization: '데이터 현지화 의무',
  interest_rate_cap: '금리 상한',
}

export function KillswitchWarning({ hits }: Props) {
  const blocked = hits.filter(h => h.blocked)
  const reviews = hits.filter(h => !h.blocked && h.reason?.includes('검토'))

  if (blocked.length === 0 && reviews.length === 0) return null

  return (
    <div className="space-y-2">
      {blocked.length > 0 && (
        <div className="bg-signal-soft border border-signal rounded-lg px-4 py-3">
          <p className="text-sm font-semibold text-signal mb-1">🚫 진출 차단 — 킬스위치 발동</p>
          <ul className="space-y-1">
            {blocked.map(h => (
              <li key={h.item_id} className="text-xs text-signal">
                • {ITEM_LABELS[h.item_id] ?? h.item_id}
                {h.reason && <span className="text-ink-soft ml-1">({h.reason})</span>}
              </li>
            ))}
          </ul>
        </div>
      )}
      {reviews.length > 0 && (
        <div className="bg-amber-soft border border-amber rounded-lg px-4 py-3">
          <p className="text-sm font-semibold text-amber mb-1">⚠️ 사람 검토 필요 항목</p>
          <ul className="space-y-1">
            {reviews.map(h => (
              <li key={h.item_id} className="text-xs text-amber">
                • {ITEM_LABELS[h.item_id] ?? h.item_id}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
