/**
 * Unit tests for AgentRegistry component
 * 
 * Tests registration, deregistration, heartbeat tracking, capacity management,
 * and capability-based queries.
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { promises as fs } from 'fs';
import * as path from 'path';
import { AgentRegistry } from '../../src/agent-work-assignment/components/AgentRegistry';
import type { AgentMetadata } from '../../src/agent-work-assignment/models/AgentMetadata';

describe('AgentRegistry', () => {
  const testDir = path.join(process.cwd(), 'test-temp', 'agent-registry');
  const registryFile = path.join(testDir, 'registry.yaml');
  const inProgressBase = path.join(testDir, 'In_Progress');
  
  let registry: AgentRegistry;

  beforeEach(async () => {
    // Clean up test directory
    await fs.rm(testDir, { recursive: true, force: true });
    await fs.mkdir(testDir, { recursive: true });

    registry = new AgentRegistry({
      registryFilePath: registryFile,
      inProgressBasePath: inProgressBase,
    });
    await registry.initialize();
  });

  afterEach(async () => {
    // Clean up test directory
    await fs.rm(testDir, { recursive: true, force: true });
  });

  describe('registerAgent', () => {
    it('should register a new agent with valid metadata', async () => {
      const metadata: AgentMetadata = {
        agentId: 'agent_test',
        capabilities: ['email', 'nlp'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map([['email_processing', 3]]),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(metadata);

      const retrieved = await registry.getAgentStatus('agent_test');
      expect(retrieved.agentId).toBe('agent_test');
      expect(retrieved.capabilities).toEqual(['email', 'nlp']);
      expect(retrieved.maxConcurrentTasks).toBe(5);
    });

    it('should create In_Progress folder for registered agent', async () => {
      const metadata: AgentMetadata = {
        agentId: 'agent_folder_test',
        capabilities: [],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(metadata);

      const agentFolder = path.join(inProgressBase, 'agent_folder_test');
      const stats = await fs.stat(agentFolder);
      expect(stats.isDirectory()).toBe(true);
    });

    it('should reject duplicate agent registration', async () => {
      const metadata: AgentMetadata = {
        agentId: 'agent_duplicate',
        capabilities: [],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(metadata);

      await expect(registry.registerAgent(metadata)).rejects.toThrow(
        "Agent with ID 'agent_duplicate' is already registered"
      );
    });

    it('should persist agent to registry file', async () => {
      const metadata: AgentMetadata = {
        agentId: 'agent_persist',
        capabilities: ['social_media'],
        maxConcurrentTasks: 2,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(metadata);

      // Create new registry instance and load from file
      const newRegistry = new AgentRegistry({
        registryFilePath: registryFile,
        inProgressBasePath: inProgressBase,
      });
      await newRegistry.initialize();

      const retrieved = await newRegistry.getAgentStatus('agent_persist');
      expect(retrieved.agentId).toBe('agent_persist');
      expect(retrieved.capabilities).toEqual(['social_media']);
    });
  });

  describe('deregisterAgent', () => {
    it('should remove agent from registry', async () => {
      const metadata: AgentMetadata = {
        agentId: 'agent_remove',
        capabilities: [],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(metadata);
      await registry.deregisterAgent('agent_remove');

      await expect(registry.getAgentStatus('agent_remove')).rejects.toThrow(
        "Agent with ID 'agent_remove' is not registered"
      );
    });

    it('should throw error when deregistering non-existent agent', async () => {
      await expect(registry.deregisterAgent('non_existent')).rejects.toThrow(
        "Agent with ID 'non_existent' is not registered"
      );
    });

    it('should persist deregistration to file', async () => {
      const metadata: AgentMetadata = {
        agentId: 'agent_persist_remove',
        capabilities: [],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(metadata);
      await registry.deregisterAgent('agent_persist_remove');

      // Create new registry instance and load from file
      const newRegistry = new AgentRegistry({
        registryFilePath: registryFile,
        inProgressBasePath: inProgressBase,
      });
      await newRegistry.initialize();

      await expect(newRegistry.getAgentStatus('agent_persist_remove')).rejects.toThrow();
    });
  });

  describe('recordHeartbeat', () => {
    it('should update lastHeartbeat timestamp', async () => {
      const metadata: AgentMetadata = {
        agentId: 'agent_heartbeat',
        capabilities: [],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date('2024-01-01T00:00:00Z'),
        registeredAt: new Date(),
      };

      await registry.registerAgent(metadata);

      const beforeHeartbeat = new Date();
      await registry.recordHeartbeat('agent_heartbeat');
      const afterHeartbeat = new Date();

      const agent = await registry.getAgentStatus('agent_heartbeat');
      expect(agent.lastHeartbeat.getTime()).toBeGreaterThanOrEqual(beforeHeartbeat.getTime());
      expect(agent.lastHeartbeat.getTime()).toBeLessThanOrEqual(afterHeartbeat.getTime());
    });

    it('should mark unresponsive agent as active on heartbeat', async () => {
      const metadata: AgentMetadata = {
        agentId: 'agent_unresponsive',
        capabilities: [],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'unresponsive',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(metadata);
      await registry.recordHeartbeat('agent_unresponsive');

      const agent = await registry.getAgentStatus('agent_unresponsive');
      expect(agent.status).toBe('active');
    });

    it('should throw error for non-existent agent', async () => {
      await expect(registry.recordHeartbeat('non_existent')).rejects.toThrow(
        "Agent with ID 'non_existent' is not registered"
      );
    });
  });

  describe('listActiveAgents', () => {
    it('should return only active agents', async () => {
      const activeAgent: AgentMetadata = {
        agentId: 'agent_active',
        capabilities: [],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      const inactiveAgent: AgentMetadata = {
        agentId: 'agent_inactive',
        capabilities: [],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'inactive',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(activeAgent);
      await registry.registerAgent(inactiveAgent);

      const activeAgents = await registry.listActiveAgents();
      expect(activeAgents).toHaveLength(1);
      expect(activeAgents[0].agentId).toBe('agent_active');
    });

    it('should return empty array when no active agents', async () => {
      const activeAgents = await registry.listActiveAgents();
      expect(activeAgents).toHaveLength(0);
    });
  });

  describe('getAgentsByCapability', () => {
    it('should return agents with specified capability', async () => {
      const agent1: AgentMetadata = {
        agentId: 'agent_email',
        capabilities: ['email', 'nlp'],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      const agent2: AgentMetadata = {
        agentId: 'agent_social',
        capabilities: ['social_media'],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(agent1);
      await registry.registerAgent(agent2);

      const emailAgents = await registry.getAgentsByCapability('email');
      expect(emailAgents).toHaveLength(1);
      expect(emailAgents[0].agentId).toBe('agent_email');
    });

    it('should return empty array when no agents have capability', async () => {
      const agents = await registry.getAgentsByCapability('non_existent_capability');
      expect(agents).toHaveLength(0);
    });
  });

  describe('getAgentWorkload', () => {
    it('should return 0 for agent with no tasks', async () => {
      const metadata: AgentMetadata = {
        agentId: 'agent_empty',
        capabilities: [],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(metadata);

      const workload = await registry.getAgentWorkload('agent_empty');
      expect(workload).toBe(0);
    });

    it('should count task files in agent folder', async () => {
      const metadata: AgentMetadata = {
        agentId: 'agent_workload',
        capabilities: [],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(metadata);

      // Create some task files
      const agentFolder = path.join(inProgressBase, 'agent_workload');
      await fs.writeFile(path.join(agentFolder, 'task1.md'), '# Task 1');
      await fs.writeFile(path.join(agentFolder, 'task2.md'), '# Task 2');
      await fs.writeFile(path.join(agentFolder, 'readme.txt'), 'Not a task');

      const workload = await registry.getAgentWorkload('agent_workload');
      expect(workload).toBe(2);
    });
  });

  describe('hasCapacity', () => {
    it('should return true when agent has capacity', async () => {
      const metadata: AgentMetadata = {
        agentId: 'agent_capacity',
        capabilities: [],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(metadata);

      const hasCapacity = await registry.hasCapacity('agent_capacity');
      expect(hasCapacity).toBe(true);
    });

    it('should return false when agent is at max capacity', async () => {
      const metadata: AgentMetadata = {
        agentId: 'agent_full',
        capabilities: [],
        maxConcurrentTasks: 2,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(metadata);

      // Fill agent to capacity
      const agentFolder = path.join(inProgressBase, 'agent_full');
      await fs.writeFile(path.join(agentFolder, 'task1.md'), '# Task 1');
      await fs.writeFile(path.join(agentFolder, 'task2.md'), '# Task 2');

      const hasCapacity = await registry.hasCapacity('agent_full');
      expect(hasCapacity).toBe(false);
    });
  });

  describe('hasCapacityForType', () => {
    it('should return true when no type limit is configured', async () => {
      const metadata: AgentMetadata = {
        agentId: 'agent_no_limit',
        capabilities: [],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(metadata);

      const hasCapacity = await registry.hasCapacityForType('agent_no_limit', 'email_processing');
      expect(hasCapacity).toBe(true);
    });

    it('should return false when overall capacity is exceeded', async () => {
      const metadata: AgentMetadata = {
        agentId: 'agent_overall_full',
        capabilities: [],
        maxConcurrentTasks: 1,
        maxTasksByType: new Map([['email_processing', 5]]),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(metadata);

      // Fill overall capacity
      const agentFolder = path.join(inProgressBase, 'agent_overall_full');
      await fs.writeFile(path.join(agentFolder, 'task1.md'), '# Task 1');

      const hasCapacity = await registry.hasCapacityForType('agent_overall_full', 'email_processing');
      expect(hasCapacity).toBe(false);
    });

    it('should check per-type capacity when configured', async () => {
      const metadata: AgentMetadata = {
        agentId: 'agent_type_limit',
        capabilities: [],
        maxConcurrentTasks: 10,
        maxTasksByType: new Map([['email_processing', 2]]),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(metadata);

      // Add tasks of specific type
      const agentFolder = path.join(inProgressBase, 'agent_type_limit');
      await fs.writeFile(
        path.join(agentFolder, 'task1.md'),
        '---\ntaskType: email_processing\n---\n# Task 1'
      );
      await fs.writeFile(
        path.join(agentFolder, 'task2.md'),
        '---\ntaskType: email_processing\n---\n# Task 2'
      );

      const hasCapacity = await registry.hasCapacityForType('agent_type_limit', 'email_processing');
      expect(hasCapacity).toBe(false);
    });
  });
});
