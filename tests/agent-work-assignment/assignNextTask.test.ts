/**
 * Integration tests for TaskAssignmentEngine.assignNextTask() method
 * 
 * Verifies that assignNextTask() correctly:
 * - Coordinates with TaskRouter to get eligible agents
 * - Applies assignment strategy to select agent
 * - Coordinates with ClaimLockManager to claim task
 * 
 * Requirements: 7.2, 9.1, 16.1
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { promises as fs } from 'fs';
import * as path from 'path';
import { TaskAssignmentEngine, TaskAssignmentEngineConfig } from '../../src/agent-work-assignment/components/TaskAssignmentEngine';
import { AgentRegistry, AgentRegistryConfig } from '../../src/agent-work-assignment/components/AgentRegistry';
import { TaskRouter } from '../../src/agent-work-assignment/components/TaskRouter';
import { ClaimLockManager, ClaimLockManagerConfig } from '../../src/agent-work-assignment/components/ClaimLockManager';
import type { AgentMetadata } from '../../src/agent-work-assignment/models';

describe('TaskAssignmentEngine.assignNextTask()', () => {
  const testDir = path.join(process.cwd(), 'test-temp-assign-next-task');
  const needsActionFolder = path.join(testDir, 'Needs_Action');
  const inProgressFolder = path.join(testDir, 'In_Progress');
  const lockDirectory = path.join(testDir, 'locks');
  const registryFilePath = path.join(testDir, 'agents.yaml');

  let engine: TaskAssignmentEngine;
  let agentRegistry: AgentRegistry;
  let taskRouter: TaskRouter;
  let claimLockManager: ClaimLockManager;

  beforeEach(async () => {
    // Create test directories
    await fs.mkdir(needsActionFolder, { recursive: true });
    await fs.mkdir(inProgressFolder, { recursive: true });
    await fs.mkdir(lockDirectory, { recursive: true });

    // Initialize components
    const registryConfig: AgentRegistryConfig = {
      registryFilePath,
      inProgressBasePath: inProgressFolder
    };
    agentRegistry = new AgentRegistry(registryConfig);
    await agentRegistry.initialize();

    taskRouter = new TaskRouter(agentRegistry);

    const lockConfig: ClaimLockManagerConfig = {
      lockDirectory,
      maxLockDurationSeconds: 10,
      needsActionFolder,
      inProgressFolder
    };
    claimLockManager = new ClaimLockManager(lockConfig);
    await claimLockManager.initialize();

    const engineConfig: TaskAssignmentEngineConfig = {
      needsActionFolder,
      defaultPriority: 'medium',
      defaultTimeoutMinutes: 30
    };
    engine = new TaskAssignmentEngine(engineConfig, agentRegistry, taskRouter, claimLockManager);
  });

  afterEach(async () => {
    await engine.stopWatching();
    try {
      await fs.rm(testDir, { recursive: true, force: true });
    } catch (error) {
      // Ignore cleanup errors
    }
  });

  describe('Capacity checking (Requirement 7.2)', () => {
    it('should return null when agent has no capacity', async () => {
      // Register agent with 0 capacity
      const agent: AgentMetadata = {
        agentId: 'agent_no_capacity',
        capabilities: ['test'],
        maxConcurrentTasks: 0,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      await agentRegistry.registerAgent(agent);

      // Create a task
      const taskContent = `---
taskId: task_001
priority: high
taskType: test
---

# Task 001
`;
      await fs.writeFile(path.join(needsActionFolder, 'task_001.md'), taskContent);
      await engine.startWatching();
      await new Promise(resolve => setTimeout(resolve, 100));

      const result = await engine.assignNextTask('agent_no_capacity');
      expect(result).toBeNull();
    });

    it('should return null when agent is at max capacity', async () => {
      // Register agent with capacity of 1
      const agent: AgentMetadata = {
        agentId: 'agent_limited',
        capabilities: ['test'],
        maxConcurrentTasks: 1,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      await agentRegistry.registerAgent(agent);

      // Create two tasks
      await fs.writeFile(path.join(needsActionFolder, 'task_001.md'), `---
taskId: task_001
priority: high
taskType: test
---

# Task 001
`);
      await fs.writeFile(path.join(needsActionFolder, 'task_002.md'), `---
taskId: task_002
priority: high
taskType: test
---

# Task 002
`);
      
      await engine.startWatching();
      await new Promise(resolve => setTimeout(resolve, 100));

      // First assignment should succeed
      const firstTask = await engine.assignNextTask('agent_limited');
      expect(firstTask).not.toBeNull();
      expect(firstTask?.taskId).toBe('task_001');

      // Second assignment should fail (agent at capacity)
      const secondTask = await engine.assignNextTask('agent_limited');
      expect(secondTask).toBeNull();
    });
  });

  describe('Capability-based routing (Requirement 9.1)', () => {
    it('should only assign tasks matching agent capabilities', async () => {
      // Register agent with specific capabilities
      const agent: AgentMetadata = {
        agentId: 'agent_email',
        capabilities: ['email', 'nlp'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      await agentRegistry.registerAgent(agent);

      // Create task requiring different capabilities
      const taskContent = `---
taskId: task_social
priority: high
taskType: social_media
requiredCapabilities: [social_media, image_processing]
---

# Social Media Task
`;
      await fs.writeFile(path.join(needsActionFolder, 'task_social.md'), taskContent);
      await engine.startWatching();
      await new Promise(resolve => setTimeout(resolve, 100));

      const result = await engine.assignNextTask('agent_email');
      expect(result).toBeNull();
    });

    it('should assign tasks when agent has all required capabilities', async () => {
      // Register agent with matching capabilities
      const agent: AgentMetadata = {
        agentId: 'agent_email',
        capabilities: ['email', 'nlp', 'pdf'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      await agentRegistry.registerAgent(agent);

      // Create task requiring subset of agent capabilities
      const taskContent = `---
taskId: task_email
priority: high
taskType: email_processing
requiredCapabilities: [email, nlp]
---

# Email Task
`;
      await fs.writeFile(path.join(needsActionFolder, 'task_email.md'), taskContent);
      await engine.startWatching();
      await new Promise(resolve => setTimeout(resolve, 100));

      const result = await engine.assignNextTask('agent_email');
      expect(result).not.toBeNull();
      expect(result?.taskId).toBe('task_email');
    });

    it('should assign tasks with no capability requirements to any agent', async () => {
      // Register agent with any capabilities
      const agent: AgentMetadata = {
        agentId: 'agent_generic',
        capabilities: ['basic'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      await agentRegistry.registerAgent(agent);

      // Create task with no capability requirements
      const taskContent = `---
taskId: task_generic
priority: high
taskType: generic_task
---

# Generic Task
`;
      await fs.writeFile(path.join(needsActionFolder, 'task_generic.md'), taskContent);
      await engine.startWatching();
      await new Promise(resolve => setTimeout(resolve, 100));

      const result = await engine.assignNextTask('agent_generic');
      expect(result).not.toBeNull();
      expect(result?.taskId).toBe('task_generic');
    });
  });

  describe('Per-type capacity limits', () => {
    it('should respect per-type capacity limits', async () => {
      // Register agent with per-type limits
      const agent: AgentMetadata = {
        agentId: 'agent_typed',
        capabilities: ['email'],
        maxConcurrentTasks: 10,
        maxTasksByType: new Map([['email_processing', 1]]),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      await agentRegistry.registerAgent(agent);

      // Create two email tasks
      await fs.writeFile(path.join(needsActionFolder, 'task_email_1.md'), `---
taskId: task_email_1
priority: high
taskType: email_processing
requiredCapabilities: [email]
---

# Email Task 1
`);
      await fs.writeFile(path.join(needsActionFolder, 'task_email_2.md'), `---
taskId: task_email_2
priority: high
taskType: email_processing
requiredCapabilities: [email]
---

# Email Task 2
`);
      
      await engine.startWatching();
      await new Promise(resolve => setTimeout(resolve, 100));

      // First email task should succeed
      const firstTask = await engine.assignNextTask('agent_typed');
      expect(firstTask).not.toBeNull();
      expect(firstTask?.taskType).toBe('email_processing');

      // Second email task should fail (per-type limit reached)
      const secondTask = await engine.assignNextTask('agent_typed');
      expect(secondTask).toBeNull();
    });
  });

  describe('Task claiming coordination (Requirement 16.1)', () => {
    it('should successfully claim task and move it to In_Progress', async () => {
      // Register agent
      const agent: AgentMetadata = {
        agentId: 'agent_claimer',
        capabilities: ['test'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      await agentRegistry.registerAgent(agent);

      // Create task
      const taskContent = `---
taskId: task_claim
priority: high
taskType: test
---

# Task to Claim
`;
      await fs.writeFile(path.join(needsActionFolder, 'task_claim.md'), taskContent);
      await engine.startWatching();
      await new Promise(resolve => setTimeout(resolve, 100));

      const result = await engine.assignNextTask('agent_claimer');
      expect(result).not.toBeNull();
      expect(result?.taskId).toBe('task_claim');

      // Verify task was moved to In_Progress
      const inProgressPath = path.join(inProgressFolder, 'agent_claimer', 'task_claim.md');
      const needsActionPath = path.join(needsActionFolder, 'task_claim.md');

      const inProgressExists = await fs.access(inProgressPath).then(() => true).catch(() => false);
      const needsActionExists = await fs.access(needsActionPath).then(() => true).catch(() => false);

      expect(inProgressExists).toBe(true);
      expect(needsActionExists).toBe(false);

      // Verify frontmatter was updated
      const claimedContent = await fs.readFile(inProgressPath, 'utf-8');
      expect(claimedContent).toContain('claimedBy: agent_claimer');
      expect(claimedContent).toContain('status: in_progress');
    });

    it('should remove task from queue after successful claim', async () => {
      // Register agent
      const agent: AgentMetadata = {
        agentId: 'agent_queue',
        capabilities: ['test'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      await agentRegistry.registerAgent(agent);

      // Create task
      await fs.writeFile(path.join(needsActionFolder, 'task_queue.md'), `---
taskId: task_queue
priority: high
taskType: test
---

# Task
`);
      
      await engine.startWatching();
      await new Promise(resolve => setTimeout(resolve, 100));

      // Verify task is in queue
      let tasks = await engine.getAvailableTasks();
      expect(tasks.length).toBe(1);

      // Assign task
      await engine.assignNextTask('agent_queue');

      // Verify task is removed from queue
      tasks = await engine.getAvailableTasks();
      expect(tasks.length).toBe(0);
    });
  });

  describe('Priority-based assignment (Requirement 16.1)', () => {
    it('should assign highest priority task first', async () => {
      // Register agent
      const agent: AgentMetadata = {
        agentId: 'agent_priority',
        capabilities: ['test'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      await agentRegistry.registerAgent(agent);

      // Create tasks with different priorities
      await fs.writeFile(path.join(needsActionFolder, 'task_low.md'), `---
taskId: task_low
priority: low
taskType: test
---

# Low Priority Task
`);
      await fs.writeFile(path.join(needsActionFolder, 'task_critical.md'), `---
taskId: task_critical
priority: critical
taskType: test
---

# Critical Priority Task
`);
      await fs.writeFile(path.join(needsActionFolder, 'task_medium.md'), `---
taskId: task_medium
priority: medium
taskType: test
---

# Medium Priority Task
`);
      
      await engine.startWatching();
      await new Promise(resolve => setTimeout(resolve, 200));

      // Should assign critical task first
      const result = await engine.assignNextTask('agent_priority');
      expect(result).not.toBeNull();
      expect(result?.taskId).toBe('task_critical');
      expect(result?.priority).toBe('critical');
    });
  });

  describe('Error handling', () => {
    it('should return null when no tasks are available', async () => {
      // Register agent
      const agent: AgentMetadata = {
        agentId: 'agent_empty',
        capabilities: ['test'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      await agentRegistry.registerAgent(agent);

      await engine.startWatching();
      await new Promise(resolve => setTimeout(resolve, 100));

      const result = await engine.assignNextTask('agent_empty');
      expect(result).toBeNull();
    });

    it('should handle non-existent agent gracefully', async () => {
      // Create task
      await fs.writeFile(path.join(needsActionFolder, 'task_orphan.md'), `---
taskId: task_orphan
priority: high
taskType: test
---

# Task
`);
      
      await engine.startWatching();
      await new Promise(resolve => setTimeout(resolve, 100));

      // Try to assign to non-existent agent - should throw error
      await expect(engine.assignNextTask('non_existent_agent')).rejects.toThrow('Agent with ID \'non_existent_agent\' is not registered');
    });
  });

  describe('Multiple agents coordination', () => {
    it('should assign different tasks to different agents', async () => {
      // Register two agents
      const agent1: AgentMetadata = {
        agentId: 'agent_1',
        capabilities: ['test'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      const agent2: AgentMetadata = {
        agentId: 'agent_2',
        capabilities: ['test'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      await agentRegistry.registerAgent(agent1);
      await agentRegistry.registerAgent(agent2);

      // Create two tasks
      await fs.writeFile(path.join(needsActionFolder, 'task_a.md'), `---
taskId: task_a
priority: high
taskType: test
---

# Task A
`);
      await fs.writeFile(path.join(needsActionFolder, 'task_b.md'), `---
taskId: task_b
priority: high
taskType: test
---

# Task B
`);
      
      await engine.startWatching();
      await new Promise(resolve => setTimeout(resolve, 100));

      // Assign tasks to both agents
      const result1 = await engine.assignNextTask('agent_1');
      const result2 = await engine.assignNextTask('agent_2');

      expect(result1).not.toBeNull();
      expect(result2).not.toBeNull();
      expect(result1?.taskId).not.toBe(result2?.taskId);
    });
  });
});
