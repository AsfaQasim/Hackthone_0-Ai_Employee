/**
 * Agent Registry Component
 * 
 * Manages agent registration, deregistration, and metadata storage.
 * Provides agent lookup, capacity tracking, and capability-based queries.
 * 
 * Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 7.1, 7.2, 7.5, 9.2, 10.1, 10.4, 17.1, 17.2, 17.5
 */

import { promises as fs } from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import type { AgentMetadata } from '../models/AgentMetadata';

export interface AgentRegistryConfig {
  registryFilePath: string;
  inProgressBasePath: string;
}

export class AgentRegistry {
  private agents: Map<string, AgentMetadata> = new Map();
  private config: AgentRegistryConfig;

  constructor(config: AgentRegistryConfig) {
    this.config = config;
  }

  /**
   * Initialize the registry by loading existing agent data from file
   */
  async initialize(): Promise<void> {
    try {
      await this.loadFromFile();
    } catch (error) {
      // If file doesn't exist, start with empty registry
      if ((error as NodeJS.ErrnoException).code !== 'ENOENT') {
        throw error;
      }
    }
  }

  /**
   * Register an agent with the system
   * Requirements: 1.1, 1.2, 1.5
   */
  async registerAgent(metadata: AgentMetadata): Promise<void> {
    // Requirement 1.5: Reject duplicate agent IDs
    if (this.agents.has(metadata.agentId)) {
      throw new Error(`Agent with ID '${metadata.agentId}' is already registered`);
    }

    // Requirement 1.1: Record agent metadata
    this.agents.set(metadata.agentId, metadata);

    // Requirement 1.2: Create In_Progress folder for the agent
    const agentFolder = path.join(this.config.inProgressBasePath, metadata.agentId);
    await fs.mkdir(agentFolder, { recursive: true });

    // Requirement 1.4: Persist to configuration file
    await this.saveToFile();
  }

  /**
   * Deregister an agent from the system
   * Requirements: 1.3
   */
  async deregisterAgent(agentId: string): Promise<void> {
    if (!this.agents.has(agentId)) {
      throw new Error(`Agent with ID '${agentId}' is not registered`);
    }

    // Remove agent from registry
    this.agents.delete(agentId);

    // Persist changes to file
    await this.saveToFile();
  }

  /**
   * Record a heartbeat from an agent
   * Requirements: 10.1, 10.4
   */
  async recordHeartbeat(agentId: string): Promise<void> {
    const agent = this.agents.get(agentId);
    if (!agent) {
      throw new Error(`Agent with ID '${agentId}' is not registered`);
    }

    // Update lastHeartbeat timestamp
    agent.lastHeartbeat = new Date();
    
    // If agent was unresponsive, mark it as active again
    if (agent.status === 'unresponsive') {
      agent.status = 'active';
    }

    await this.saveToFile();
  }

  /**
   * Get agent status and metadata
   * Requirements: 10.4
   */
  async getAgentStatus(agentId: string): Promise<AgentMetadata> {
    const agent = this.agents.get(agentId);
    if (!agent) {
      throw new Error(`Agent with ID '${agentId}' is not registered`);
    }

    return { ...agent };
  }

  /**
   * List all active agents
   * Requirements: 10.1
   */
  async listActiveAgents(): Promise<AgentMetadata[]> {
    return Array.from(this.agents.values())
      .filter(agent => agent.status === 'active')
      .map(agent => ({ ...agent }));
  }

  /**
   * Get agents by capability
   * Requirements: 9.2
   */
  async getAgentsByCapability(capability: string): Promise<AgentMetadata[]> {
    return Array.from(this.agents.values())
      .filter(agent => agent.capabilities.includes(capability))
      .map(agent => ({ ...agent }));
  }

  /**
   * Get agent workload (count of tasks in In_Progress folder)
   * Requirements: 7.5, 17.5
   */
  async getAgentWorkload(agentId: string): Promise<number> {
    const agent = this.agents.get(agentId);
    if (!agent) {
      throw new Error(`Agent with ID '${agentId}' is not registered`);
    }

    const agentFolder = path.join(this.config.inProgressBasePath, agentId);
    
    try {
      const files = await fs.readdir(agentFolder);
      // Count only .md files (task files)
      return files.filter(file => file.endsWith('.md')).length;
    } catch (error) {
      // If folder doesn't exist, workload is 0
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        return 0;
      }
      throw error;
    }
  }

  /**
   * Check if agent has capacity for new tasks
   * Requirements: 7.2
   */
  async hasCapacity(agentId: string): Promise<boolean> {
    const agent = this.agents.get(agentId);
    if (!agent) {
      throw new Error(`Agent with ID '${agentId}' is not registered`);
    }

    const currentWorkload = await this.getAgentWorkload(agentId);
    return currentWorkload < agent.maxConcurrentTasks;
  }

  /**
   * Check if agent has capacity for a specific task type
   * Requirements: 17.2, 17.5
   */
  async hasCapacityForType(agentId: string, taskType: string): Promise<boolean> {
    const agent = this.agents.get(agentId);
    if (!agent) {
      throw new Error(`Agent with ID '${agentId}' is not registered`);
    }

    // Check overall capacity first
    if (!(await this.hasCapacity(agentId))) {
      return false;
    }

    // Check per-type capacity if configured
    const typeLimit = agent.maxTasksByType.get(taskType);
    if (typeLimit === undefined) {
      // No specific limit for this type, overall capacity check is sufficient
      return true;
    }

    // Count tasks of this specific type in agent's folder
    const agentFolder = path.join(this.config.inProgressBasePath, agentId);
    
    try {
      const files = await fs.readdir(agentFolder);
      const taskFiles = files.filter(file => file.endsWith('.md'));
      
      // Count tasks of the specific type by reading frontmatter
      let typeCount = 0;
      for (const file of taskFiles) {
        const filePath = path.join(agentFolder, file);
        const content = await fs.readFile(filePath, 'utf-8');
        
        // Extract frontmatter
        const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
        if (frontmatterMatch) {
          const frontmatter = yaml.load(frontmatterMatch[1]) as { taskType?: string };
          if (frontmatter.taskType === taskType) {
            typeCount++;
          }
        }
      }
      
      return typeCount < typeLimit;
    } catch (error) {
      // If folder doesn't exist, agent has capacity
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        return true;
      }
      throw error;
    }
  }

  /**
   * Load agent registry from file
   * Requirements: 1.4
   */
  private async loadFromFile(): Promise<void> {
    const content = await fs.readFile(this.config.registryFilePath, 'utf-8');
    const data = yaml.load(content) as { agents: Array<{
      agentId: string;
      capabilities: string[];
      maxConcurrentTasks: number;
      maxTasksByType: Record<string, number>;
      status: 'active' | 'inactive' | 'unresponsive';
      lastHeartbeat: string;
      registeredAt: string;
    }> };

    this.agents.clear();
    
    if (data.agents) {
      for (const agentData of data.agents) {
        const metadata: AgentMetadata = {
          agentId: agentData.agentId,
          capabilities: agentData.capabilities,
          maxConcurrentTasks: agentData.maxConcurrentTasks,
          maxTasksByType: new Map(Object.entries(agentData.maxTasksByType || {})),
          status: agentData.status,
          lastHeartbeat: new Date(agentData.lastHeartbeat),
          registeredAt: new Date(agentData.registeredAt),
        };
        this.agents.set(metadata.agentId, metadata);
      }
    }
  }

  /**
   * Save agent registry to file
   * Requirements: 1.4
   */
  private async saveToFile(): Promise<void> {
    const agents = Array.from(this.agents.values()).map(agent => ({
      agentId: agent.agentId,
      capabilities: agent.capabilities,
      maxConcurrentTasks: agent.maxConcurrentTasks,
      maxTasksByType: Object.fromEntries(agent.maxTasksByType),
      status: agent.status,
      lastHeartbeat: agent.lastHeartbeat.toISOString(),
      registeredAt: agent.registeredAt.toISOString(),
    }));

    const data = { agents };
    const yamlContent = yaml.dump(data);

    // Ensure directory exists
    const dir = path.dirname(this.config.registryFilePath);
    await fs.mkdir(dir, { recursive: true });

    await fs.writeFile(this.config.registryFilePath, yamlContent, 'utf-8');
  }
}
