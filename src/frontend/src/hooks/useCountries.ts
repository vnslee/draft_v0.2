import { useEffect, useState } from 'react'
import { fetchCountries } from '@/api/countries'
import type { Country } from '@/types/country'

export function useCountries() {
  const [countries, setCountries] = useState<Country[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchCountries()
      .then(setCountries)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  return { countries, loading, error }
}
