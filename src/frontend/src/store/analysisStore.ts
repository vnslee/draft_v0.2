import { create } from 'zustand'
import type { AgentName, AgentStatus, Verdict } from '@/types/analysis'
import type { Country } from '@/types/country'

const defaultAgents = (): Record<AgentName, AgentStatus> => ({
  market:      { progress: 0, status: 'waiting', message: '' },
  regulation:  { progress: 0, status: 'waiting', message: '' },
  environment: { progress: 0, status: 'waiting', message: '' },
  system:      { progress: 0, status: 'waiting', message: '' },
  summary:     { progress: 0, status: 'waiting', message: '' },
})

interface AnalysisState {
  isRunning: boolean
  analysisId: string | null
  mode: 'single' | 'region' | null
  targetCountry: Country | null
  comparedCountry: string
  overallProgress: number
  agents: Record<AgentName, AgentStatus>
  startedAt: Date | null
  resultId: string | null
  verdict: Verdict | null
  totalScore: number | null

  startAnalysis: (target: Country, compared: string, mode?: 'single' | 'region') => void
  setAnalysisId: (id: string) => void
  updateAgentProgress: (agent: AgentName, update: Partial<AgentStatus>) => void
  completeAnalysis: (resultId: string, verdict?: Verdict, totalScore?: number) => void
  failAnalysis: () => void
  resetAnalysis: () => void
}

export const useAnalysisStore = create<AnalysisState>((set, get) => ({
  isRunning: false,
  analysisId: null,
  mode: null,
  targetCountry: null,
  comparedCountry: '한국',
  overallProgress: 0,
  agents: defaultAgents(),
  startedAt: null,
  resultId: null,
  verdict: null,
  totalScore: null,

  startAnalysis: (target, compared, mode = 'single') =>
    set({
      isRunning: true,
      analysisId: null,
      mode,
      targetCountry: target,
      comparedCountry: compared,
      overallProgress: 0,
      agents: defaultAgents(),
      startedAt: new Date(),
      resultId: null,
      verdict: null,
      totalScore: null,
    }),

  setAnalysisId: id => set({ analysisId: id }),

  updateAgentProgress: (agent, update) => {
    const agents = { ...get().agents, [agent]: { ...get().agents[agent], ...update } }
    // 전체 진행률: Phase1 에이전트 4개 평균 * 0.8 + summary * 0.2
    const phase1 = (['market', 'regulation', 'environment', 'system'] as AgentName[])
      .map(a => agents[a].progress)
      .reduce((s, v) => s + v, 0) / 4
    const overallProgress = Math.round(phase1 * 0.8 + agents.summary.progress * 0.2)
    set({ agents, overallProgress })
  },

  completeAnalysis: (resultId, verdict, totalScore) =>
    set({ isRunning: false, resultId, verdict: verdict ?? null, totalScore: totalScore ?? null, overallProgress: 100 }),

  failAnalysis: () => set({ isRunning: false, overallProgress: 0 }),

  resetAnalysis: () =>
    set({
      isRunning: false,
      analysisId: null,
      mode: null,
      targetCountry: null,
      overallProgress: 0,
      agents: defaultAgents(),
      startedAt: null,
      resultId: null,
      verdict: null,
      totalScore: null,
    }),
}))
