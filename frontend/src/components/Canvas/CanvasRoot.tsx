import { useRef, useEffect, useState, useCallback } from 'react'
import { Stage, Layer } from 'react-konva'
import Konva from 'konva'
import { GridLayer } from './GridLayer'
import { useZoomPan } from '../../hooks/useZoomPan'

export function CanvasRoot() {
  const stageRef = useRef<Konva.Stage | null>(null)
  const containerRef = useRef<HTMLDivElement | null>(null)
  const [size, setSize] = useState({ width: 800, height: 600 })

  const {
    handleWheel,
    handleMouseDown,
    handleMouseMove,
    handleMouseUp,
    resetView,
  } = useZoomPan(stageRef)

  const updateSize = useCallback(() => {
    if (containerRef.current) {
      setSize({
        width: containerRef.current.offsetWidth,
        height: containerRef.current.offsetHeight,
      })
    }
  }, [])

  useEffect(() => {
    updateSize()
    window.addEventListener('resize', updateSize)
    return () => window.removeEventListener('resize', updateSize)
  }, [updateSize])

  return (
    <div
      ref={containerRef}
      style={{ flex: 1, overflow: 'hidden', position: 'relative', background: '#fafafa' }}
    >
      <button
        onClick={resetView}
        style={{
          position: 'absolute',
          top: 8,
          right: 8,
          zIndex: 10,
          padding: '4px 8px',
          fontSize: '12px',
          cursor: 'pointer',
        }}
      >
        Reset view
      </button>
      <Stage
        ref={stageRef}
        width={size.width}
        height={size.height}
        x={40}
        y={40}
        onWheel={handleWheel}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
      >
        {/* Grid layer */}
        <Layer>
          <GridLayer width={size.width} height={size.height} />
        </Layer>

        {/* Terrain layer — will be added in issue #10 */}
        <Layer />

        {/* Rooms layer — will be added in issue #11 */}
        <Layer />

        {/* Dimensions layer — will be added later */}
        <Layer />
      </Stage>
    </div>
  )
}
