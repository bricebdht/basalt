import { Line } from 'react-konva'
import { useUIStore } from '../../store/uiStore'

interface GridLayerProps {
  width: number
  height: number
}

export function GridLayer({ width, height }: GridLayerProps) {
  const showGrid = useUIStore((s) => s.showGrid)
  const scale = useUIStore((s) => s.scale)
  const gridSizeM = useUIStore((s) => s.gridSizeM)

  if (!showGrid) return null

  const gridSizePx = gridSizeM * scale
  // Don't render grid if it would be too dense
  if (gridSizePx < 10) return null

  const lines = []
  // Extend grid beyond visible area to cover panning
  const extent = 2
  const startX = -width * extent
  const endX = width * (1 + extent)
  const startY = -height * extent
  const endY = height * (1 + extent)

  // Vertical lines
  const firstCol = Math.floor(startX / gridSizePx) * gridSizePx
  for (let x = firstCol; x <= endX; x += gridSizePx) {
    lines.push(
      <Line
        key={`v-${x}`}
        points={[x, startY, x, endY]}
        stroke="#e0e0e0"
        strokeWidth={0.5}
        listening={false}
      />
    )
  }

  // Horizontal lines
  const firstRow = Math.floor(startY / gridSizePx) * gridSizePx
  for (let y = firstRow; y <= endY; y += gridSizePx) {
    lines.push(
      <Line
        key={`h-${y}`}
        points={[startX, y, endX, y]}
        stroke="#e0e0e0"
        strokeWidth={0.5}
        listening={false}
      />
    )
  }

  return <>{lines}</>
}
