import { create } from 'zustand'
import type { Ruleset } from '@/types/settings'

interface SettingsState {
  currentRuleset: Ruleset | null
  rulesets: Ruleset[]
  setCurrentRuleset: (r: Ruleset) => void
  setRulesets: (rs: Ruleset[]) => void
}

export const useSettingsStore = create<SettingsState>(set => ({
  currentRuleset: null,
  rulesets: [],
  setCurrentRuleset: r => set({ currentRuleset: r }),
  setRulesets: rs => set({ rulesets: rs }),
}))
