import { create } from 'zustand'

export type ActiveTool = 'select' | 'pan'

interface UIState {
  activeTool: ActiveTool
  gridSizeM: number
  showGrid: boolean
  showSetbacks: boolean
  showDimensions: boolean
  scale: number // pixels per meter

  setActiveTool: (tool: ActiveTool) => void
  setGridSizeM: (size: number) => void
  toggleGrid: () => void
  toggleSetbacks: () => void
  toggleDimensions: () => void
  setScale: (scale: number) => void
}

export const useUIStore = create<UIState>((set) => ({
  activeTool: 'select',
  gridSizeM: 1,
  showGrid: true,
  showSetbacks: true,
  showDimensions: true,
  scale: 40,

  setActiveTool: (tool) => set({ activeTool: tool }),
  setGridSizeM: (size) => set({ gridSizeM: size }),
  toggleGrid: () => set((s) => ({ showGrid: !s.showGrid })),
  toggleSetbacks: () => set((s) => ({ showSetbacks: !s.showSetbacks })),
  toggleDimensions: () => set((s) => ({ showDimensions: !s.showDimensions })),
  setScale: (scale) => set({ scale }),
}))
