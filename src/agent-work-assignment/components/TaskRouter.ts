/**
 * Task Router Component
 * 
 * Routes tasks to appropriate agents based on capability matching.
 * Implements capability-based filtering and routing rules.
 * 
 * Requirements: 9.1, 9.4, 9.5
 */

import type { TaskMetadata } from '../models/TaskMetadata';
import type { AgentRegistry } from './AgentRegistry';

export interface RoutingRule {
  ruleId: string;
  condition: (task: TaskMetadata) => boolean;
  targetAgents: string[];
  priority: number;
}

export class TaskRouter {
  private agentRegistry: AgentRegistry;
  private routingRules: Map<string, RoutingRule> = new Map();

  constructor(agentRegistry: AgentRegistry) {
    this.agentRegistry = agentRegistry;
  }

  /**
   * Get list of agents eligible to handle a task based on capability matching
   * Requirements: 9.1, 9.4, 9.5
   */
  async getEligibleAgents(task: TaskMetadata): Promise<string[]> {
    // Requirement 9.5: If task has no capability requirements, make it available to all agents
    if (!task.requiredCapabilities || task.requiredCapabilities.length === 0) {
      const activeAgents = await this.agentRegistry.listActiveAgents();
      return activeAgents.map(agent => agent.agentId);
    }

    // Requirement 9.1, 9.4: Match task capabilities to agent capabilities
    const activeAgents = await this.agentRegistry.listActiveAgents();
    const eligibleAgents: string[] = [];

    for (const agent of activeAgents) {
      if (await this.canAgentHandleTask(agent.agentId, task)) {
        eligibleAgents.push(agent.agentId);
      }
    }

    return eligibleAgents;
  }

  /**
   * Check if a single agent can handle a task based on capability matching
   * Requirements: 9.1, 9.4
   */
  async canAgentHandleTask(agentId: string, task: TaskMetadata): Promise<boolean> {
    try {
      const agentMetadata = await this.agentRegistry.getAgentStatus(agentId);

      // Requirement 9.5: Tasks with no capability requirements can be handled by any agent
      if (!task.requiredCapabilities || task.requiredCapabilities.length === 0) {
        return true;
      }

      // Requirement 9.1, 9.4: Agent must have all required capabilities
      // Check if agent's capability set includes all required capabilities
      const agentCapabilities = new Set(agentMetadata.capabilities);
      return task.requiredCapabilities.every(requiredCap => 
        agentCapabilities.has(requiredCap)
      );
    } catch (error) {
      // If agent doesn't exist or is not registered, it cannot handle the task
      return false;
    }
  }

  /**
   * Add a routing rule
   * Requirements: 9.1
   */
  addRoutingRule(rule: RoutingRule): void {
    this.routingRules.set(rule.ruleId, rule);
  }

  /**
   * Remove a routing rule
   * Requirements: 9.1
   */
  removeRoutingRule(ruleId: string): void {
    this.routingRules.delete(ruleId);
  }

  /**
   * Evaluate routing rules for a task and return target agents
   * Requirements: 9.1
   */
  async evaluateRoutingRules(task: TaskMetadata): Promise<string[]> {
    // Get all rules sorted by priority (higher priority first)
    const sortedRules = Array.from(this.routingRules.values())
      .sort((a, b) => b.priority - a.priority);

    // Find the first matching rule
    for (const rule of sortedRules) {
      if (rule.condition(task)) {
        return rule.targetAgents;
      }
    }

    // If no rules match, return empty array (fall back to capability matching)
    return [];
  }
}
