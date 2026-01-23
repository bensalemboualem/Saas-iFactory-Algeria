/**
 * Credit costs per operation
 * Centralized configuration for Dzir IA credit usage
 */

export const OPERATION_COSTS = {
  // Search: cheapest - just embedding + vector search
  search: 1,

  // Ask (RAG): embedding + LLM generation
  ask: 5,

  // Capture: depends on source type
  capture: {
    text: 1,
    url: 2, // fetching + parsing
    pdf: 3, // parsing + more chunks
  },
} as const;

export type Operation = keyof typeof OPERATION_COSTS;
export type CaptureSourceType = keyof typeof OPERATION_COSTS.capture;

/**
 * Get the cost for an operation
 */
export function getOperationCost(operation: Operation, subType?: CaptureSourceType): number {
  if (operation === 'capture' && subType) {
    return OPERATION_COSTS.capture[subType] || OPERATION_COSTS.capture.text;
  }
  const cost = OPERATION_COSTS[operation];
  return typeof cost === 'number' ? cost : OPERATION_COSTS.capture.text;
}
