import type { AgentStatus } from '@/types/analysis'

const AGENT_LABELS: Record<string, string> = {
  market: '시장',
  regulation: '규제',
  environment: '금융환경',
  system: '시스템',
  summary: 'Summary',
}

const STATUS_ICON: Record<string, string> = {
  waiting: '⏸',
  running: '⏳',
  completed: '✓',
  error: '⚠️',
}

interface Props {
  agent: string
  status: AgentStatus
}

export function AgentProgressBar({ agent, status }: Props) {
  const color =
    status.status === 'completed' ? 'bg-verdict-ok' :
    status.status === 'error'     ? 'bg-verdict-blocked' :
    status.status === 'running'   ? 'bg-status-running' :
    'bg-status-waiting'

  return (
    <div className="flex items-center gap-2 text-xs">
      <span className="w-4 text-center">{STATUS_ICON[status.status] ?? '⏸'}</span>
      <span className="w-16 text-ink-soft shrink-0">{AGENT_LABELS[agent] ?? agent}</span>
      <div className="flex-1 h-1.5 bg-line rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-300 ${color}`}
          style={{ width: `${status.progress}%` }}
        />
      </div>
      <span className="w-8 text-right text-ink-soft">{status.progress}%</span>
    </div>
  )
}
