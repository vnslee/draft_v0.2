import { create } from 'zustand'

interface UIState {
  detailModalOpen: boolean
  selectedCountryName: string | null
  setDetailModalOpen: (v: boolean) => void
  setSelectedCountry: (name: string | null) => void
}

export const useUIStore = create<UIState>(set => ({
  detailModalOpen: false,
  selectedCountryName: null,
  setDetailModalOpen: v => set({ detailModalOpen: v }),
  setSelectedCountry: name => set({ selectedCountryName: name }),
}))
