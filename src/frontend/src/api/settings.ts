import client from './client'
import type { Ruleset } from '@/types/settings'

export const fetchRulesets = () =>
  client.get<{ rulesets: Ruleset[] }>('/settings/rulesets').then(r => r.data.rulesets)

export const fetchRuleset = (id: string) =>
  client.get<Ruleset>(`/settings/rulesets/${id}`).then(r => r.data)

export const createRuleset = (body: Partial<Ruleset>) =>
  client.post<Ruleset>('/settings/rulesets', body).then(r => r.data)

export const updateRuleset = (id: string, body: Partial<Ruleset>) =>
  client.put<Ruleset>(`/settings/rulesets/${id}`, body).then(r => r.data)

export const lockRuleset = (id: string) =>
  client.post(`/settings/rulesets/${id}/lock`).then(r => r.data)
