// Returns the axis-aligned bounding box of a polygon
export function polygonBBox(vertices: [number, number][]): {
  minX: number
  minY: number
  maxX: number
  maxY: number
  width: number
  height: number
} {
  const xs = vertices.map(([x]) => x)
  const ys = vertices.map(([, y]) => y)
  const minX = Math.min(...xs)
  const minY = Math.min(...ys)
  const maxX = Math.max(...xs)
  const maxY = Math.max(...ys)
  return { minX, minY, maxX, maxY, width: maxX - minX, height: maxY - minY }
}
