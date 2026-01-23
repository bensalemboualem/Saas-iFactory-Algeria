/**
 * Credits System - PR-003
 *
 * Production-ready implementation replacing the Phase 1 mock.
 * Uses atomic transactions to prevent TOCTOU and double-spend.
 */

// Export the new production service
export { CreditsService } from './credits.service.js';

// Legacy mock API - DEPRECATED, kept for backwards compatibility during transition
// Remove after all consumers migrate to CreditsService
/** @deprecated Use CreditsService instead */
export const creditsSystem = {
  async check(userId: string, required: number): Promise<boolean> {
    console.warn('[CREDITS] DEPRECATED: creditsSystem.check() - Use CreditsService.reserve() instead');
    console.log(`[CREDITS] Check user ${userId} has ${required} credits? (Mock: YES)`);
    return true;
  },

  async deduct(userId: string, amount: number, toolId: string): Promise<void> {
    console.warn('[CREDITS] DEPRECATED: creditsSystem.deduct() - Use CreditsService.finalize() instead');
    console.log(`[CREDITS] Deducting ${amount} credits from ${userId} for tool ${toolId}`);
  },

  async addCredits(userId: string, amount: number, source: string): Promise<void> {
    console.warn('[CREDITS] DEPRECATED: creditsSystem.addCredits() - Use CreditsService.credit() instead');
    console.log(`[CREDITS] Adding ${amount} credits to ${userId} from ${source}`);
  },
};
