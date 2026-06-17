import client from './client'
import type { Country } from '@/types/country'

export const fetchCountries = () =>
  client.get<{ countries: Country[] }>('/countries').then(r => r.data.countries)

export const fetchCountry = (name: string) =>
  client.get<Country>(`/countries/${encodeURIComponent(name)}`).then(r => r.data)
