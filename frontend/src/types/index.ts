// ── Terrain ──────────────────────────────────────────────────────────────────

export type TerrainInputMode = 'sides_angles' | 'sides_diagonals' | 'coordinates'

export interface TerrainInput {
  input_mode: TerrainInputMode
  sides?: { a: number; b: number }
  angles_deg?: { alpha: number }
  diagonals?: { e?: number; f?: number }
  heights?: { ha?: number; hb?: number }
  vertices?: [number, number][]
  setback_distance_m?: number
}

export interface TerrainResponse {
  id: string
  vertices: [number, number][]
  area_m2: number
  perimeter_m: number
  setback_distance_m: number
  buildable_polygon: [number, number][]
  buildable_area_m2: number
}

// ── Rooms ─────────────────────────────────────────────────────────────────────

export interface Room {
  id: string
  label: string
  x_m: number
  y_m: number
  width_m: number
  height_m: number
  wall_thickness_m: number
  phase: 1 | 2
  color?: string
}

// ── Layout validation ─────────────────────────────────────────────────────────

export type ViolationType = 'setback_violation' | 'overlap' | 'out_of_bounds'

export interface Violation {
  room_id: string
  type: ViolationType
  message: string
}

export interface LayoutValidationRequest {
  terrain_id: string
  rooms: Room[]
}

export interface LayoutValidationResponse {
  valid: boolean
  violations: Violation[]
}

// ── Layout suggestion ─────────────────────────────────────────────────────────

export interface RoomProgram {
  label: string
  min_width_m: number
  min_height_m: number
  max_width_m?: number
  max_height_m?: number
}

export interface LayoutSuggestionRequest {
  terrain_id: string
  program: RoomProgram[]
  phase?: 1 | 2
}

export interface LayoutVariant {
  topology: string
  rooms: Room[]
  score: number
}

export interface LayoutSuggestionResponse {
  variants: LayoutVariant[]
}
