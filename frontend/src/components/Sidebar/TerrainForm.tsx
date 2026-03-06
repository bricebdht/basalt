import { useState } from 'react'
import { useTerrainStore } from '../../store/terrainStore'
import type { TerrainInput, TerrainInputMode } from '../../types'

export function TerrainForm() {
  const { terrain, isLoading, error, compute } = useTerrainStore()

  const [mode, setMode] = useState<TerrainInputMode>('sides_angles')
  const [a, setA] = useState('19.93')
  const [b, setB] = useState('12.2')
  const [alpha, setAlpha] = useState('101.085')
  const [diagE, setDiagE] = useState('21.273')
  const [setback, setSetback] = useState('3')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const input: TerrainInput = {
      input_mode: mode,
      setback_distance_m: parseFloat(setback) || 3,
    }
    if (mode === 'sides_angles') {
      input.sides = { a: parseFloat(a), b: parseFloat(b) }
      input.angles_deg = { alpha: parseFloat(alpha) }
    } else if (mode === 'sides_diagonals') {
      input.sides = { a: parseFloat(a), b: parseFloat(b) }
      input.diagonals = { e: parseFloat(diagE) }
    }
    compute(input)
  }

  return (
    <div style={{ padding: 16 }}>
      <h3 style={{ margin: '0 0 12px' }}>Terrain</h3>

      <form onSubmit={handleSubmit}>
        <label style={labelStyle}>
          Mode
          <select value={mode} onChange={(e) => setMode(e.target.value as TerrainInputMode)} style={inputStyle}>
            <option value="sides_angles">Côtés + angle</option>
            <option value="sides_diagonals">Côtés + diagonale</option>
          </select>
        </label>

        <label style={labelStyle}>
          Côté a (m)
          <input type="number" step="0.01" value={a} onChange={(e) => setA(e.target.value)} style={inputStyle} />
        </label>

        <label style={labelStyle}>
          Côté b (m)
          <input type="number" step="0.01" value={b} onChange={(e) => setB(e.target.value)} style={inputStyle} />
        </label>

        {mode === 'sides_angles' && (
          <label style={labelStyle}>
            Angle α (°)
            <input type="number" step="0.001" value={alpha} onChange={(e) => setAlpha(e.target.value)} style={inputStyle} />
          </label>
        )}

        {mode === 'sides_diagonals' && (
          <label style={labelStyle}>
            Diagonale e (m)
            <input type="number" step="0.001" value={diagE} onChange={(e) => setDiagE(e.target.value)} style={inputStyle} />
          </label>
        )}

        <label style={labelStyle}>
          Recul légal (m)
          <input type="number" step="0.5" value={setback} onChange={(e) => setSetback(e.target.value)} style={inputStyle} />
        </label>

        <button type="submit" disabled={isLoading} style={{ width: '100%', padding: '8px', marginTop: 8 }}>
          {isLoading ? 'Calcul...' : 'Calculer le terrain'}
        </button>
      </form>

      {error && <p style={{ color: 'red', fontSize: 12, marginTop: 8 }}>{error}</p>}

      {terrain && (
        <div style={{ marginTop: 16, fontSize: 13, lineHeight: 1.6 }}>
          <div><strong>Aire :</strong> {terrain.area_m2} m²</div>
          <div><strong>Périmètre :</strong> {terrain.perimeter_m} m</div>
          <div><strong>Zone constructible :</strong> {terrain.buildable_area_m2} m²</div>
          <div style={{ color: '#888', fontSize: 11 }}>
            ({Math.round(terrain.buildable_area_m2 / terrain.area_m2 * 100)}% du terrain)
          </div>
        </div>
      )}
    </div>
  )
}

const labelStyle: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  fontSize: 13,
  marginBottom: 8,
  gap: 2,
}

const inputStyle: React.CSSProperties = {
  padding: '4px 6px',
  fontSize: 13,
  border: '1px solid #ccc',
  borderRadius: 4,
}
