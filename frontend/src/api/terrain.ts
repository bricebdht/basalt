import { apiFetch } from './client'
import type { TerrainInput, TerrainResponse } from '../types'

export function computeTerrain(input: TerrainInput): Promise<TerrainResponse> {
  return apiFetch<TerrainResponse>('/terrain/compute', {
    method: 'POST',
    body: JSON.stringify(input),
  })
}

export function getTerrain(id: string): Promise<TerrainResponse> {
  return apiFetch<TerrainResponse>(`/terrain/${id}`)
}
