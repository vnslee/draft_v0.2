import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAnalysisStore } from '@/store/analysisStore'
import { useAnalysisWS } from '@/hooks/useAnalysisWS'
import { AgentProgressBar } from './AgentProgressBar'
import type { AgentName } from '@/types/analysis'

const AGENT_ORDER: AgentName[] = ['market', 'regulation', 'environment', 'system', 'summary']

export function AnalysisStatusCard() {
  const navigate = useNavigate()
  const { isRunning, analysisId, targetCountry, overallProgress, agents, resultId } = useAnalysisStore()
  const [expanded, setExpanded] = useState(false)

  useAnalysisWS(analysisId)

  // 완료 10초 후 자동 축소
  useEffect(() => {
    if (!isRunning && resultId) {
      const t = setTimeout(() => setExpanded(false), 10000)
      return () => clearTimeout(t)
    }
  }, [isRunning, resultId])

  if (!isRunning && !resultId) return null

  return (
    <div className="fixed top-4 right-4 z-50 w-72 bg-panel border border-line rounded-xl shadow-lg text-sm">
      {/* 헤더 */}
      <div
        className="flex items-center justify-between px-4 py-3 cursor-pointer"
        onClick={() => setExpanded(v => !v)}
      >
        <div className="flex items-center gap-2">
          {isRunning
            ? <span className="animate-spin text-base">🔄</span>
            : <span className="text-base">✓</span>}
          <span className="font-medium text-ink">
            {targetCountry?.name ?? ''} {isRunning ? '분석 중' : '분석 완료'}
          </span>
        </div>
        <div className="flex items-center gap-2">
          {resultId && !isRunning && (
            <button
              className="text-xs text-accent underline"
              onClick={e => { e.stopPropagation(); navigate(`/reports/${resultId}`) }}
            >
              보고서
            </button>
          )}
          <span className="text-ink-soft text-xs">{overallProgress}%</span>
          <span className="text-ink-soft">{expanded ? '▲' : '▼'}</span>
        </div>
      </div>

      {/* 전체 진행 바 */}
      <div className="px-4 pb-2">
        <div className="h-1.5 bg-line rounded-full overflow-hidden">
          <div
            className="h-full bg-accent rounded-full transition-all duration-500"
            style={{ width: `${overallProgress}%` }}
          />
        </div>
      </div>

      {/* 확장 패널 */}
      {expanded && (
        <div className="px-4 pb-4 flex flex-col gap-2 border-t border-line-soft pt-3 mt-1">
          {AGENT_ORDER.map(agent => (
            <AgentProgressBar key={agent} agent={agent} status={agents[agent]} />
          ))}
          {agents[AGENT_ORDER[0]]?.message && (
            <p className="text-xs text-ink-soft mt-1 truncate">{agents.market.message}</p>
          )}
        </div>
      )}
    </div>
  )
}
