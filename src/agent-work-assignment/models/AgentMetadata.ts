/**
 * Agent metadata model for agent work assignment system
 */

export type AgentStatus = 'active' | 'inactive' | 'unresponsive';

export interface AgentMetadata {
  agentId: string;
  capabilities: string[];
  maxConcurrentTasks: number;
  maxTasksByType: Map<string, number>;
  status: AgentStatus;
  lastHeartbeat: Date;
  registeredAt: Date;
}

export function isValidAgentStatus(status: string): status is AgentStatus {
  return ['active', 'inactive', 'unresponsive'].includes(status);
}

export function isValidAgentMetadata(obj: unknown): obj is AgentMetadata {
  if (typeof obj !== 'object' || obj === null) return false;
  
  const agent = obj as Partial<AgentMetadata>;
  
  return (
    typeof agent.agentId === 'string' &&
    Array.isArray(agent.capabilities) &&
    agent.capabilities.every(cap => typeof cap === 'string') &&
    typeof agent.maxConcurrentTasks === 'number' &&
    agent.maxTasksByType instanceof Map &&
    typeof agent.status === 'string' &&
    isValidAgentStatus(agent.status) &&
    agent.lastHeartbeat instanceof Date &&
    agent.registeredAt instanceof Date
  );
}
