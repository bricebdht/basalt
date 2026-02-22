import { apiFetch } from './client'
import type {
  LayoutValidationRequest,
  LayoutValidationResponse,
  LayoutSuggestionRequest,
  LayoutSuggestionResponse,
} from '../types'

export function validateLayout(req: LayoutValidationRequest): Promise<LayoutValidationResponse> {
  return apiFetch<LayoutValidationResponse>('/layout/validate', {
    method: 'POST',
    body: JSON.stringify(req),
  })
}

export function suggestLayout(req: LayoutSuggestionRequest): Promise<LayoutSuggestionResponse> {
  return apiFetch<LayoutSuggestionResponse>('/layout/suggest', {
    method: 'POST',
    body: JSON.stringify(req),
  })
}
