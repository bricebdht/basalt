export const DEFAULT_SCALE = 40 // pixels per meter

export const mToPx = (m: number, scale = DEFAULT_SCALE): number => m * scale
export const pxToM = (px: number, scale = DEFAULT_SCALE): number => px / scale
