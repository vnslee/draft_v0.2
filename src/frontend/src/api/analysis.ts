import client from './client'
import type { AnalysisJob } from '@/types/analysis'

export const runAnalysis = (target: string, compared: string, rulesetId = 'default') =>
  client.post<{ analysis_id: string; status: string }>('/analysis/run', {
    target_country: target,
    compared_country: compared,
    ruleset_id: rulesetId,
  }).then(r => r.data)

export const getAnalysis = (id: string) =>
  client.get<AnalysisJob>(`/analysis/${id}`).then(r => r.data)

export const pollAnalysisStatus = (id: string) =>
  client.get(`/analysis/${id}/status`).then(r => r.data)
