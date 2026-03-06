import { useCallback, useRef } from 'react'
import Konva from 'konva'
import { useUIStore } from '../store/uiStore'

const MIN_SCALE = 8   // 8 px/m
const MAX_SCALE = 200  // 200 px/m
const ZOOM_FACTOR = 1.1

export function useZoomPan(stageRef: React.RefObject<Konva.Stage | null>) {
  const isPanning = useRef(false)
  const lastPointer = useRef({ x: 0, y: 0 })

  const handleWheel = useCallback((e: Konva.KonvaEventObject<WheelEvent>) => {
    e.evt.preventDefault()
    const stage = stageRef.current
    if (!stage) return

    const pointer = stage.getPointerPosition()
    if (!pointer) return

    const oldScale = useUIStore.getState().scale
    const direction = e.evt.deltaY < 0 ? 1 : -1
    const newScale = direction > 0
      ? Math.min(oldScale * ZOOM_FACTOR, MAX_SCALE)
      : Math.max(oldScale / ZOOM_FACTOR, MIN_SCALE)

    // Zoom toward pointer position
    const oldPos = stage.position()
    const mousePointTo = {
      x: (pointer.x - oldPos.x) / oldScale,
      y: (pointer.y - oldPos.y) / oldScale,
    }

    const newPos = {
      x: pointer.x - mousePointTo.x * newScale,
      y: pointer.y - mousePointTo.y * newScale,
    }

    stage.position(newPos)
    useUIStore.getState().setScale(newScale)
  }, [stageRef])

  const handleMouseDown = useCallback((e: Konva.KonvaEventObject<MouseEvent>) => {
    // Middle mouse button or space+click for pan
    if (e.evt.button === 1 || useUIStore.getState().activeTool === 'pan') {
      isPanning.current = true
      const pos = stageRef.current?.getPointerPosition()
      if (pos) {
        lastPointer.current = pos
      }
      e.evt.preventDefault()
    }
  }, [stageRef])

  const handleMouseMove = useCallback((_e: Konva.KonvaEventObject<MouseEvent>) => {
    if (!isPanning.current) return
    const stage = stageRef.current
    if (!stage) return

    const pos = stage.getPointerPosition()
    if (!pos) return

    const dx = pos.x - lastPointer.current.x
    const dy = pos.y - lastPointer.current.y
    const oldPos = stage.position()

    stage.position({ x: oldPos.x + dx, y: oldPos.y + dy })
    lastPointer.current = pos
  }, [stageRef])

  const handleMouseUp = useCallback(() => {
    isPanning.current = false
  }, [])

  const resetView = useCallback(() => {
    const stage = stageRef.current
    if (!stage) return
    stage.position({ x: 40, y: 40 })
    useUIStore.getState().setScale(40)
  }, [stageRef])

  return {
    handleWheel,
    handleMouseDown,
    handleMouseMove,
    handleMouseUp,
    resetView,
  }
}
