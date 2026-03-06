import { create } from 'zustand'
import type { TerrainInput, TerrainResponse } from '../types'
import { computeTerrain } from '../api/terrain'

interface TerrainState {
  terrain: TerrainResponse | null
  isLoading: boolean
  error: string | null

  compute: (input: TerrainInput) => Promise<void>
  clear: () => void
}

export const useTerrainStore = create<TerrainState>((set) => ({
  terrain: null,
  isLoading: false,
  error: null,

  compute: async (input) => {
    set({ isLoading: true, error: null })
    try {
      const terrain = await computeTerrain(input)
      set({ terrain, isLoading: false })
    } catch (e) {
      set({ error: e instanceof Error ? e.message : 'Unknown error', isLoading: false })
    }
  },

  clear: () => set({ terrain: null, error: null }),
}))
