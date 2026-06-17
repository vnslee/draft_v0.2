import { useEffect, useState } from 'react'
import { useSettingsStore } from '@/store/settingsStore'
import { fetchRulesets, createRuleset, lockRuleset } from '@/api/settings'
import type { CategoryWeight, Thresholds, Ruleset } from '@/types/settings'

export default function S3Settings() {
  const { currentRuleset, rulesets, setCurrentRuleset, setRulesets } = useSettingsStore()
  const [weights, setWeights] = useState<CategoryWeight>({ market: 25, regulation: 25, environment: 20, system: 30 })
  const [thresholds, setThresholds] = useState<Thresholds>({ entry: 60, system_gate: 50 })
  const [killswitchEnabled, setKillswitchEnabled] = useState(true)
  const [name, setName] = useState('')
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetchRulesets().then(rs => {
      setRulesets(rs)
      if (!currentRuleset && rs.length > 0) setCurrentRuleset(rs[0])
    }).catch(() => {})
  }, [])

  useEffect(() => {
    if (currentRuleset) {
      setWeights({
        market: currentRuleset.weights.market * 100,
        regulation: currentRuleset.weights.regulation * 100,
        environment: currentRuleset.weights.environment * 100,
        system: currentRuleset.weights.system * 100,
      })
      setThresholds(currentRuleset.thresholds)
      setKillswitchEnabled(currentRuleset.killswitch_enabled)
      setName(`${currentRuleset.name} (사본)`)
    }
  }, [currentRuleset])

  const weightTotal = weights.market + weights.regulation + weights.environment + weights.system

  const handleSave = async () => {
    setSaving(true)
    setMessage('')
    try {
      const created = await createRuleset({
        name: name || '새 룰셋',
        weights: {
          market: weights.market / 100,
          regulation: weights.regulation / 100,
          environment: weights.environment / 100,
          system: weights.system / 100,
        },
        thresholds,
        killswitch_enabled: killswitchEnabled,
      } as Partial<Ruleset>)
      setCurrentRuleset(created)
      setRulesets([...rulesets, created])
      setMessage('새 룰셋이 저장되었습니다.')
    } catch (e: any) {
      setMessage(`오류: ${e.message}`)
    } finally {
      setSaving(false)
    }
  }

  const handleLock = async () => {
    if (!currentRuleset) return
    await lockRuleset(currentRuleset.id)
    setMessage('룰셋이 잠겼습니다.')
  }

  const WEIGHT_ITEMS: { key: keyof CategoryWeight; label: string }[] = [
    { key: 'market', label: '시장' },
    { key: 'regulation', label: '규제' },
    { key: 'environment', label: '금융환경' },
    { key: 'system', label: '시스템' },
  ]

  return (
    <div className="p-8 max-w-2xl">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-ink">설정</h2>
        <p className="text-sm text-ink-soft mt-1">가중치·임계값·킬스위치를 변경하면 항상 새 룰셋으로 저장됩니다</p>
      </div>

      {/* 현재 룰셋 */}
      {currentRuleset && (
        <div className="bg-accent-soft border border-accent rounded-xl px-4 py-3 mb-6 flex items-center justify-between">
          <div>
            <p className="text-xs text-accent font-semibold">현재 룰셋</p>
            <p className="text-sm font-medium text-ink">
              {currentRuleset.name}
              {currentRuleset.locked && <span className="ml-2 text-amber text-xs">🔒 잠김</span>}
            </p>
          </div>
          <div className="flex gap-2">
            <select
              value={currentRuleset.id}
              onChange={e => {
                const r = rulesets.find(r => r.id === e.target.value)
                if (r) setCurrentRuleset(r)
              }}
              className="text-xs px-2 py-1 border border-line rounded bg-paper text-ink"
            >
              {rulesets.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
            </select>
            {!currentRuleset.locked && (
              <button onClick={handleLock} className="text-xs text-amber underline">잠금</button>
            )}
          </div>
        </div>
      )}

      {/* 카테고리 가중치 */}
      <div className="bg-panel border border-line rounded-xl p-6 mb-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-ink">카테고리 가중치</h3>
          <span className={`text-xs font-mono ${weightTotal !== 100 ? 'text-signal' : 'text-verdict-ok'}`}>
            합계: {weightTotal}%
          </span>
        </div>
        <div className="space-y-4">
          {WEIGHT_ITEMS.map(({ key, label }) => (
            <div key={key}>
              <div className="flex justify-between text-xs text-ink-soft mb-1">
                <span>{label}</span>
                <span className="font-mono">{weights[key]}%</span>
              </div>
              <input
                type="range" min={0} max={100} step={5}
                value={weights[key]}
                onChange={e => setWeights(w => ({ ...w, [key]: +e.target.value }))}
                className="w-full accent-accent"
              />
            </div>
          ))}
        </div>
      </div>

      {/* 임계값 */}
      <div className="bg-panel border border-line rounded-xl p-6 mb-4">
        <h3 className="text-sm font-semibold text-ink mb-4">임계값</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-xs text-ink-soft block mb-1">진입 임계값 (TRANSPLANTABLE)</label>
            <input
              type="number" min={0} max={100}
              value={thresholds.entry}
              onChange={e => setThresholds(t => ({ ...t, entry: +e.target.value }))}
              className="w-full px-3 py-2 border border-line rounded-lg text-sm text-ink bg-paper"
            />
          </div>
          <div>
            <label className="text-xs text-ink-soft block mb-1">시스템 게이트</label>
            <input
              type="number" min={0} max={100}
              value={thresholds.system_gate}
              onChange={e => setThresholds(t => ({ ...t, system_gate: +e.target.value }))}
              className="w-full px-3 py-2 border border-line rounded-lg text-sm text-ink bg-paper"
            />
          </div>
        </div>
      </div>

      {/* 킬스위치 */}
      <div className="bg-panel border border-line rounded-xl p-6 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold text-ink">킬스위치</h3>
            <p className="text-xs text-ink-soft mt-0.5">비활성화 시 차단 항목이 있어도 BLOCKED 판정 생략</p>
          </div>
          <button
            onClick={() => setKillswitchEnabled(v => !v)}
            className={`relative w-12 h-6 rounded-full transition-colors ${
              killswitchEnabled ? 'bg-verdict-ok' : 'bg-line'
            }`}
          >
            <span className={`absolute top-1 w-4 h-4 rounded-full bg-white shadow transition-transform ${
              killswitchEnabled ? 'translate-x-7' : 'translate-x-1'
            }`} />
          </button>
        </div>
      </div>

      {/* 룰셋 이름 + 저장 */}
      <div className="space-y-3">
        <input
          type="text"
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="새 룰셋 이름"
          className="w-full px-3 py-2 border border-line rounded-lg text-sm text-ink bg-paper focus:outline-none focus:border-accent"
        />
        <button
          onClick={handleSave}
          disabled={saving || weightTotal !== 100}
          className="w-full py-3 bg-accent text-white rounded-lg font-medium text-sm disabled:opacity-40 hover:bg-accent/90 transition-colors"
        >
          {saving ? '저장 중...' : '새 룰셋으로 저장'}
        </button>
        {message && (
          <p className={`text-xs text-center ${message.startsWith('오류') ? 'text-signal' : 'text-verdict-ok'}`}>
            {message}
          </p>
        )}
      </div>
    </div>
  )
}
