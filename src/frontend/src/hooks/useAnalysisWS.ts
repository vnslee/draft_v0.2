import { useEffect, useRef } from 'react'
import { useAnalysisStore } from '@/store/analysisStore'
import { pollAnalysisStatus } from '@/api/analysis'
import { BASE_PATH } from '@/config/runtime'
import type { WSMessage, AgentName } from '@/types/analysis'

export function useAnalysisWS(analysisId: string | null) {
  const updateAgentProgress = useAnalysisStore(s => s.updateAgentProgress)
  const completeAnalysis = useAnalysisStore(s => s.completeAnalysis)
  const failAnalysis = useAnalysisStore(s => s.failAnalysis)
  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const startPolling = (id: string) => {
    if (pollingRef.current) return
    pollingRef.current = setInterval(async () => {
      try {
        const data = await pollAnalysisStatus(id)
        Object.entries(data.agents ?? {}).forEach(([agent, status]: [string, any]) => {
          updateAgentProgress(agent as AgentName, {
            progress: status.progress,
            status: status.status,
            message: status.message,
          })
        })
        if (data.status === 'COMPLETED' && data.result_id) {
          completeAnalysis(data.result_id)
          clearInterval(pollingRef.current!)
          pollingRef.current = null
        } else if (data.status === 'FAILED') {
          failAnalysis()
          clearInterval(pollingRef.current!)
          pollingRef.current = null
        }
      } catch {
        // 폴링 실패 시 계속 재시도
      }
    }, 5000)
  }

  useEffect(() => {
    if (!analysisId) return

    const wsProto = location.protocol === 'https:' ? 'wss:' : 'ws:'
    const ws = new WebSocket(`${wsProto}//${location.host}${BASE_PATH}/ws/analysis/${analysisId}`)

    ws.onmessage = e => {
      const msg: WSMessage = JSON.parse(e.data)
      if (msg.type === 'progress' && msg.agent) {
        updateAgentProgress(msg.agent, {
          progress: Math.round(msg.progress ?? 0),
          status: msg.status ?? 'running',
          message: msg.message ?? '',
        })
      } else if (msg.type === 'completed' && msg.result_id) {
        completeAnalysis(msg.result_id, msg.verdict, msg.total_score)
      } else if (msg.type === 'error') {
        if (!msg.recoverable) failAnalysis()
      }
    }

    ws.onerror = () => startPolling(analysisId)
    ws.onclose = () => {
      // 정상 완료가 아닌 경우 폴링 폴백
      const state = useAnalysisStore.getState()
      if (state.isRunning) startPolling(analysisId)
    }

    return () => {
      ws.close()
      if (pollingRef.current) {
        clearInterval(pollingRef.current)
        pollingRef.current = null
      }
    }
  }, [analysisId])
}
