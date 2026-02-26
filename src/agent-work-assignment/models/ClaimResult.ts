/**
 * Claim result model for task claiming operations
 */

export interface ClaimResult {
  success: boolean;
  taskId: string;
  agentId: string;
  error?: string;
}

export function isValidClaimResult(obj: unknown): obj is ClaimResult {
  if (typeof obj !== 'object' || obj === null) return false;
  
  const result = obj as Partial<ClaimResult>;
  
  return (
    typeof result.success === 'boolean' &&
    typeof result.taskId === 'string' &&
    typeof result.agentId === 'string' &&
    (result.error === undefined || typeof result.error === 'string')
  );
}
