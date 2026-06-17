import type { Verdict } from './analysis'

export interface ItemScore {
  catalog_item_id: string
  similarity: number | null
  confidence_grade: string
  source_tier: string
  evidence: string
  is_missing: boolean
}

export interface CategoryResult {
  category: string
  items: ItemScore[]
  category_score: number | null
  coverage: number
  gate_passed: boolean | null
  killswitch_results: { item_id: string; blocked: boolean; reason: string }[]
  warnings: string[]
}

export interface CostEstimate {
  estimated: boolean
  base_cost_usd_million?: number
  multiplier?: number
  estimated_cost_usd_million?: number
  similarity_ratio?: number
  reason?: string
}

export interface Report {
  id: string
  analysis_id: string
  target_country: string
  compared_country: string
  ruleset_id: string
  verdict: Verdict
  total_score: number | null
  category_results: CategoryResult[]
  cost_estimate: CostEstimate | null
  summary: string
  ai_insight: string
  human_review_flags: string[]
  created_at: string
}

export interface ReportSummary {
  id: string
  target_country: string
  compared_country: string
  verdict: Verdict
  total_score: number | null
  created_at: string
}
