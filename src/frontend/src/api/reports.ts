import client from './client'
import type { Report, ReportSummary } from '@/types/report'

export const fetchReport = (id: string) =>
  client.get<Report>(`/reports/${id}`).then(r => r.data)

export const fetchReports = (limit = 20) =>
  client.get<{ reports: ReportSummary[] }>(`/reports?limit=${limit}`).then(r => r.data.reports)
