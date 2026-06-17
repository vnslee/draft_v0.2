export type AgentName = 'market' | 'regulation' | 'environment' | 'system' | 'summary'
export type AgentStatusType = 'waiting' | 'running' | 'completed' | 'error'
export type Verdict = 'TRANSPLANTABLE' | 'DEEP_RESEARCH' | 'BLOCKED' | 'FAILED'

export interface AgentStatus {
  progress: number
  status: AgentStatusType
  message: string
}

export interface AnalysisJob {
  id: string
  target_country: string
  compared_country: string
  ruleset_id: string
  status: string
  agents: Record<AgentName, AgentStatus>
  result_id: string | null
  created_at: string
  updated_at: string
}

export interface WSMessage {
  type: 'progress' | 'completed' | 'error'
  agent?: AgentName
  progress?: number
  status?: AgentStatusType
  message?: string
  result_id?: string
  verdict?: Verdict
  total_score?: number
  recoverable?: boolean
}
