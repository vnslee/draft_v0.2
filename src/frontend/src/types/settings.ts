export interface CategoryWeight {
  market: number
  regulation: number
  environment: number
  system: number
}

export interface Thresholds {
  entry: number
  system_gate: number
}

export interface Ruleset {
  id: string
  name: string
  version: number
  locked: boolean
  weights: CategoryWeight
  thresholds: Thresholds
  killswitch_enabled: boolean
  created_at: string
}
