import { Line } from 'react-konva'
import { useTerrainStore } from '../../store/terrainStore'
import { useUIStore } from '../../store/uiStore'

export function TerrainLayer() {
  const terrain = useTerrainStore((s) => s.terrain)
  const scale = useUIStore((s) => s.scale)
  const showSetbacks = useUIStore((s) => s.showSetbacks)

  if (!terrain) return null

  const terrainPoints = terrain.vertices.flatMap(([x, y]) => [x * scale, y * scale])
  const buildablePoints = terrain.buildable_polygon.flatMap(([x, y]) => [x * scale, y * scale])

  return (
    <>
      {/* Terrain boundary */}
      <Line
        points={terrainPoints}
        closed
        stroke="#333"
        strokeWidth={2}
        fill="rgba(200, 220, 200, 0.15)"
        listening={false}
      />

      {/* Setback zone (buildable area) */}
      {showSetbacks && buildablePoints.length > 0 && (
        <>
          {/* Setback area = terrain minus buildable, shown as red overlay */}
          <Line
            points={terrainPoints}
            closed
            fill="rgba(255, 100, 100, 0.12)"
            listening={false}
          />
          {/* Buildable area overlay to "punch out" the setback */}
          <Line
            points={buildablePoints}
            closed
            fill="#fafafa"
            listening={false}
          />
          {/* Buildable boundary dashed line */}
          <Line
            points={buildablePoints}
            closed
            stroke="#e53e3e"
            strokeWidth={1}
            dash={[6, 4]}
            listening={false}
          />
        </>
      )}
    </>
  )
}
