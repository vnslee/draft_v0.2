import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useCountries } from '@/hooks/useCountries'
import { useAnalysisStore } from '@/store/analysisStore'
import { useSettingsStore } from '@/store/settingsStore'
import { runAnalysis } from '@/api/analysis'
import { fetchRuleset } from '@/api/settings'
import { VerdictBadge } from '@/components/results/VerdictBadge'
import { ScoreBreakdown } from '@/components/results/ScoreBreakdown'
import { KillswitchWarning } from '@/components/results/KillswitchWarning'
import { CostEstimate } from '@/components/results/CostEstimate'
import { fetchReport } from '@/api/reports'
import type { Report } from '@/types/report'
import type { Country } from '@/types/country'

export default function S1Diagnosis() {
  const location = useLocation()
  const navigate = useNavigate()
  const { countries, loading } = useCountries()
  const { isRunning, startAnalysis, setAnalysisId, resultId } = useAnalysisStore()
  const { currentRuleset, setCurrentRuleset } = useSettingsStore()

  const [target, setTarget] = useState<string>(location.state?.country ?? '')
  const [compared, setCompared] = useState<string>('KR')
  const [report, setReport] = useState<Report | null>(null)
  const [error, setError] = useState<string | null>(null)

  // 룰셋 로드
  useEffect(() => {
    if (!currentRuleset) {
      fetchRuleset('default').then(setCurrentRuleset).catch(() => {})
    }
  }, [])

  // 분석 완료 후 보고서 로드
  useEffect(() => {
    if (resultId && !isRunning) {
      fetchReport(resultId).then(setReport).catch(() => {})
    }
  }, [resultId, isRunning])

  const handleRun = async () => {
    if (!target || !compared) return
    setError(null)
    setReport(null)

    const targetCountry = countries.find(c => c.country_id === target) ?? { name: target } as Country
    startAnalysis(targetCountry, compared)

    try {
      const { analysis_id } = await runAnalysis(target, compared, currentRuleset?.id ?? 'default')
      setAnalysisId(analysis_id)
    } catch (e: any) {
      setError(e.message)
    }
  }

  const enteredCountries = countries.filter(c => c.entry_status === '진출')

  const allKillswitchHits = report?.category_results
    .flatMap(c => c.killswitch_results) ?? []

  return (
    <div className="p-8 max-w-3xl">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-ink">단일 국가 진단</h2>
        <p className="text-sm text-ink-soft mt-1">진출 대상국과 기준국을 선택하고 분석을 실행하세요</p>
      </div>

      {/* 설정 패널 */}
      <div className="bg-panel border border-line rounded-xl p-6 mb-6 space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-xs text-ink-soft font-medium block mb-1.5">진단 대상국</label>
            <select
              value={target}
              onChange={e => setTarget(e.target.value)}
              className="w-full px-3 py-2 bg-paper border border-line rounded-lg text-sm text-ink focus:outline-none focus:border-accent"
              disabled={isRunning}
            >
              <option value="">국가 선택...</option>
              {loading ? (
                <option disabled>로딩 중...</option>
              ) : (
                countries.map(c => (
                  <option key={c.country_id ?? c.name} value={c.country_id ?? c.name}>
                    {c.name} ({c.entry_status ?? '-'})
                  </option>
                ))
              )}
            </select>
          </div>
          <div>
            <label className="text-xs text-ink-soft font-medium block mb-1.5">기준국 (진출 완료)</label>
            <select
              value={compared}
              onChange={e => setCompared(e.target.value)}
              className="w-full px-3 py-2 bg-paper border border-line rounded-lg text-sm text-ink focus:outline-none focus:border-accent"
              disabled={isRunning}
            >
              {enteredCountries.map(c => (
                <option key={c.country_id ?? c.name} value={c.country_id ?? c.name}>{c.name}</option>
              ))}
            </select>
          </div>
        </div>

        {/* 룰셋 표시 */}
        <div className="flex items-center justify-between text-xs">
          <span className="text-ink-soft">
            룰셋: <span className="text-ink font-medium">{currentRuleset?.name ?? '기본 룰셋'}</span>
            {currentRuleset?.locked && <span className="ml-1 text-amber">🔒 잠김</span>}
          </span>
          <button onClick={() => navigate('/settings')} className="text-accent underline">
            변경
          </button>
        </div>

        {error && (
          <p className="text-xs text-signal bg-signal-soft px-3 py-2 rounded-lg">{error}</p>
        )}

        <button
          onClick={handleRun}
          disabled={!target || !compared || isRunning}
          className="w-full py-3 bg-accent text-white rounded-lg font-medium text-sm disabled:opacity-40 disabled:cursor-not-allowed hover:bg-accent/90 transition-colors"
        >
          {isRunning ? '분석 중...' : '🔍 분석 실행'}
        </button>
      </div>

      {/* 분석 결과 */}
      {report && (
        <div className="space-y-4">
          {/* 킬스위치 경고 — 최상단 */}
          {allKillswitchHits.length > 0 && (
            <KillswitchWarning hits={allKillswitchHits} />
          )}

          {/* 판정 헤더 */}
          <div className="bg-panel border border-line rounded-xl p-5 flex items-center justify-between">
            <div>
              <p className="text-xs text-ink-soft mb-1">{report.target_country} vs {report.compared_country}</p>
              <VerdictBadge verdict={report.verdict} />
            </div>
            <div className="text-right">
              <p className="text-3xl font-bold text-ink">
                {report.total_score?.toFixed(1) ?? '-'}
              </p>
              <p className="text-xs text-ink-soft">종합 점수</p>
            </div>
          </div>

          {/* 카테고리 점수 */}
          <div className="bg-panel border border-line rounded-xl p-5">
            <h3 className="text-sm font-semibold text-ink mb-4">카테고리별 점수</h3>
            <ScoreBreakdown categories={report.category_results} totalScore={report.total_score} />
          </div>

          {/* 비용 추정 */}
          {report.cost_estimate && (
            <CostEstimate data={report.cost_estimate} />
          )}

          {/* 보고서 보기 버튼 */}
          <button
            onClick={() => navigate(`/reports/${report.id}`)}
            className="w-full py-3 bg-ink text-white rounded-xl font-medium text-sm hover:bg-ink/90 transition-colors"
          >
            📄 상세 보고서 보기
          </button>
        </div>
      )}
    </div>
  )
}
