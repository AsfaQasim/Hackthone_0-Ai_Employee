/**
 * Unit tests for TaskAssignmentEngine
 * 
 * Tests file watching, task parsing, queue management, and assignment logic
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { promises as fs } from 'fs';
import * as path from 'path';
import { TaskAssignmentEngine, TaskAssignmentEngineConfig } from '../../src/agent-work-assignment/components/TaskAssignmentEngine';
import { AgentRegistry, AgentRegistryConfig } from '../../src/agent-work-assignment/components/AgentRegistry';
import { TaskRouter } from '../../src/agent-work-assignment/components/TaskRouter';
import { ClaimLockManager, ClaimLockManagerConfig } from '../../src/agent-work-assignment/components/ClaimLockManager';
import type { AgentMetadata, TaskMetadata } from '../../src/agent-work-assignment/models';

describe('TaskAssignmentEngine', () => {
  const testDir = path.join(process.cwd(), 'test-temp-assignment-engine');
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
    // Stop watching
    await engine.stopWatching();

    // Clean up test directories
    try {
      await fs.rm(testDir, { recursive: true, force: true });
    } catch (error) {
      // Ignore cleanup errors
    }
  });

  describe('startWatching and stopWatching', () => {
    it('should start watching the Needs_Action folder', async () => {
      await engine.startWatching();
      
      // Verify the folder exists
      const stats = await fs.stat(needsActionFolder);
      expect(stats.isDirectory()).toBe(true);
    });

    it('should stop watching when stopWatching is called', async () => {
      await engine.startWatching();
      await engine.stopWatching();
      
      // No error should occur
      expect(true).toBe(true);
    });

    it('should not throw when startWatching is called multiple times', async () => {
      await engine.startWatching();
      await engine.startWatching();
      
      expect(true).toBe(true);
    });
  });

  describe('task file parsing', () => {
    it('should parse task file with complete frontmatter', async () => {
      const taskContent = `---
taskId: task_001
priority: high
taskType: email_processing
requiredCapabilities: [email, nlp]
createdAt: 2024-01-15T12:00:00Z
reclaimCount: 0
timeoutMinutes: 30
---

# Task: Process Email

This is a test task.
`;

      await fs.writeFile(path.join(needsActionFolder, 'task_001.md'), taskContent);
      await engine.startWatching();

      // Wait for file watcher to detect the file
      await new Promise(resolve => setTimeout(resolve, 100));

      const tasks = await engine.getAvailableTasks();
      expect(tasks.length).toBe(1);
      expect(tasks[0].taskId).toBe('task_001');
      expect(tasks[0].priority).toBe('high');
      expect(tasks[0].taskType).toBe('email_processing');
      expect(tasks[0].requiredCapabilities).toEqual(['email', 'nlp']);
    });

    it('should apply default priority when not specified', async () => {
      const taskContent = `---
taskId: task_002
taskType: default_task
---

# Task: Default Priority

This task has no priority specified.
`;

      await fs.writeFile(path.join(needsActionFolder, 'task_002.md'), taskContent);
      await engine.startWatching();

      // Wait for file watcher to detect the file
      await new Promise(resolve => setTimeout(resolve, 100));

      const tasks = await engine.getAvailableTasks();
      expect(tasks.length).toBe(1);
      expect(tasks[0].priority).toBe('medium'); // default priority
    });

    it('should extract taskId from filename if not in frontmatter', async () => {
      const taskContent = `---
priority: low
taskType: test_task
---

# Task: No ID

This task has no taskId in frontmatter.
`;

      await fs.writeFile(path.join(needsActionFolder, 'task_003.md'), taskContent);
      await engine.startWatching();

      // Wait for file watcher to detect the file
      await new Promise(resolve => setTimeout(resolve, 100));

      const tasks = await engine.getAvailableTasks();
      expect(tasks.length).toBe(1);
      expect(tasks[0].taskId).toBe('task_003');
    });
  });

  describe('task queue management', () => {
    it('should maintain tasks in priority order', async () => {
      const tasks = [
        { id: 'task_low', priority: 'low' },
        { id: 'task_critical', priority: 'critical' },
        { id: 'task_medium', priority: 'medium' },
        { id: 'task_high', priority: 'high' }
      ];

      await engine.startWatching();

      for (const task of tasks) {
        const content = `---
taskId: ${task.id}
priority: ${task.priority}
taskType: test
---

# Task
`;
        await fs.writeFile(path.join(needsActionFolder, `${task.id}.md`), content);
      }

      // Wait for file watcher to detect all files
      await new Promise(resolve => setTimeout(resolve, 200));

      const availableTasks = await engine.getAvailableTasks();
      expect(availableTasks.length).toBe(4);
      
      // Verify priority order: critical, high, medium, low
      expect(availableTasks[0].priority).toBe('critical');
      expect(availableTasks[1].priority).toBe('high');
      expect(availableTasks[2].priority).toBe('medium');
      expect(availableTasks[3].priority).toBe('low');
    });

    it('should remove task from queue when file is deleted', async () => {
      const taskContent = `---
taskId: task_delete
priority: high
taskType: test
---

# Task
`;

      const filePath = path.join(needsActionFolder, 'task_delete.md');
      await fs.writeFile(filePath, taskContent);
      await engine.startWatching();

      // Wait for file watcher to detect the file
      await new Promise(resolve => setTimeout(resolve, 100));

      let tasks = await engine.getAvailableTasks();
      expect(tasks.length).toBe(1);

      // Delete the file
      await fs.unlink(filePath);

      // Wait for file watcher to detect the deletion
      await new Promise(resolve => setTimeout(resolve, 100));

      tasks = await engine.getAvailableTasks();
      expect(tasks.length).toBe(0);
    });

    it('should filter tasks by priority', async () => {
      const tasks = [
        { id: 'task_high_1', priority: 'high' },
        { id: 'task_high_2', priority: 'high' },
        { id: 'task_low_1', priority: 'low' }
      ];

      await engine.startWatching();

      for (const task of tasks) {
        const content = `---
taskId: ${task.id}
priority: ${task.priority}
taskType: test
---

# Task
`;
        await fs.writeFile(path.join(needsActionFolder, `${task.id}.md`), content);
      }

      // Wait for file watcher to detect all files
      await new Promise(resolve => setTimeout(resolve, 200));

      const highPriorityTasks = await engine.getTasksByPriority('high');
      expect(highPriorityTasks.length).toBe(2);
      expect(highPriorityTasks.every(t => t.priority === 'high')).toBe(true);
    });
  });

  describe('assignment strategy', () => {
    it('should set and get assignment strategy', () => {
      expect(engine.getStrategy()).toBe('priority-first'); // default

      engine.setStrategy('round-robin');
      expect(engine.getStrategy()).toBe('round-robin');

      engine.setStrategy('least-loaded');
      expect(engine.getStrategy()).toBe('least-loaded');
    });

    it('should apply round-robin strategy correctly', async () => {
      // Register three agents
      const agents: AgentMetadata[] = [
        {
          agentId: 'agent_rr_1',
          capabilities: ['test'],
          maxConcurrentTasks: 5,
          maxTasksByType: new Map(),
          status: 'active',
          lastHeartbeat: new Date(),
          registeredAt: new Date()
        },
        {
          agentId: 'agent_rr_2',
          capabilities: ['test'],
          maxConcurrentTasks: 5,
          maxTasksByType: new Map(),
          status: 'active',
          lastHeartbeat: new Date(),
          registeredAt: new Date()
        },
        {
          agentId: 'agent_rr_3',
          capabilities: ['test'],
          maxConcurrentTasks: 5,
          maxTasksByType: new Map(),
          status: 'active',
          lastHeartbeat: new Date(),
          registeredAt: new Date()
        }
      ];

      for (const agent of agents) {
        await agentRegistry.registerAgent(agent);
      }

      // Set round-robin strategy
      engine.setStrategy('round-robin');

      // Create three tasks
      await engine.startWatching();
      for (let i = 1; i <= 3; i++) {
        const taskContent = `---
taskId: task_rr_${i}
priority: medium
taskType: test
requiredCapabilities: [test]
---

# Task ${i}
`;
        await fs.writeFile(path.join(needsActionFolder, `task_rr_${i}.md`), taskContent);
      }

      await new Promise(resolve => setTimeout(resolve, 200));

      // Assign tasks and track which agents get them
      const assignments: string[] = [];
      const tasks = await engine.getAvailableTasks();
      
      for (const task of tasks) {
        const assignedAgent = await engine.assignTaskToAgent(task);
        if (assignedAgent) {
          assignments.push(assignedAgent);
        }
      }

      // Verify round-robin distribution (each agent should get one task)
      expect(assignments.length).toBe(3);
      expect(assignments).toContain('agent_rr_1');
      expect(assignments).toContain('agent_rr_2');
      expect(assignments).toContain('agent_rr_3');
    });

    it('should apply least-loaded strategy correctly', async () => {
      // Register two agents
      const agent1: AgentMetadata = {
        agentId: 'agent_ll_1',
        capabilities: ['test'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      const agent2: AgentMetadata = {
        agentId: 'agent_ll_2',
        capabilities: ['test'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };

      await agentRegistry.registerAgent(agent1);
      await agentRegistry.registerAgent(agent2);

      // Give agent1 an existing task (simulate workload)
      const agent1Folder = path.join(inProgressFolder, 'agent_ll_1');
      await fs.mkdir(agent1Folder, { recursive: true });
      const existingTaskContent = `---
taskId: existing_task
priority: medium
taskType: test
---

# Existing Task
`;
      await fs.writeFile(path.join(agent1Folder, 'existing_task.md'), existingTaskContent);

      // Set least-loaded strategy
      engine.setStrategy('least-loaded');

      // Create a new task
      await engine.startWatching();
      const taskContent = `---
taskId: task_ll_1
priority: medium
taskType: test
requiredCapabilities: [test]
---

# Task
`;
      await fs.writeFile(path.join(needsActionFolder, 'task_ll_1.md'), taskContent);
      await new Promise(resolve => setTimeout(resolve, 100));

      const tasks = await engine.getAvailableTasks();
      expect(tasks.length).toBe(1);

      // Assign task - should go to agent_ll_2 (least loaded)
      const assignedAgent = await engine.assignTaskToAgent(tasks[0]);
      expect(assignedAgent).toBe('agent_ll_2');
    });

    it('should apply capability-match strategy correctly', async () => {
      // Register agents with different capability sets
      const agent1: AgentMetadata = {
        agentId: 'agent_cm_1',
        capabilities: ['test', 'email', 'nlp', 'social_media'], // 4 capabilities
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      const agent2: AgentMetadata = {
        agentId: 'agent_cm_2',
        capabilities: ['test', 'email'], // 2 capabilities (most specialized)
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      const agent3: AgentMetadata = {
        agentId: 'agent_cm_3',
        capabilities: ['test', 'email', 'nlp'], // 3 capabilities
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };

      await agentRegistry.registerAgent(agent1);
      await agentRegistry.registerAgent(agent2);
      await agentRegistry.registerAgent(agent3);

      // Set capability-match strategy
      engine.setStrategy('capability-match');

      // Create a task requiring test and email capabilities
      await engine.startWatching();
      const taskContent = `---
taskId: task_cm_1
priority: medium
taskType: test
requiredCapabilities: [test, email]
---

# Task
`;
      await fs.writeFile(path.join(needsActionFolder, 'task_cm_1.md'), taskContent);
      await new Promise(resolve => setTimeout(resolve, 100));

      const tasks = await engine.getAvailableTasks();
      expect(tasks.length).toBe(1);

      // Assign task - should go to agent_cm_2 (most specialized with fewest capabilities)
      const assignedAgent = await engine.assignTaskToAgent(tasks[0]);
      expect(assignedAgent).toBe('agent_cm_2');
    });

    it('should apply priority-first strategy correctly', async () => {
      // Register an agent
      const agent: AgentMetadata = {
        agentId: 'agent_pf_1',
        capabilities: ['test'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      await agentRegistry.registerAgent(agent);

      // Set priority-first strategy
      engine.setStrategy('priority-first');

      // Create tasks with different priorities
      await engine.startWatching();
      const tasks = [
        { id: 'task_pf_low', priority: 'low' },
        { id: 'task_pf_high', priority: 'high' },
        { id: 'task_pf_medium', priority: 'medium' }
      ];

      for (const task of tasks) {
        const content = `---
taskId: ${task.id}
priority: ${task.priority}
taskType: test
requiredCapabilities: [test]
---

# Task
`;
        await fs.writeFile(path.join(needsActionFolder, `${task.id}.md`), content);
      }

      await new Promise(resolve => setTimeout(resolve, 200));

      const availableTasks = await engine.getAvailableTasks();
      expect(availableTasks.length).toBe(3);

      // Assign first task - should be high priority
      const assignedAgent1 = await engine.assignTaskToAgent(availableTasks[0]);
      expect(assignedAgent1).toBe('agent_pf_1');
      expect(availableTasks[0].priority).toBe('high');
    });
  });

  describe('task assignment', () => {
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
taskId: task_assign_1
priority: high
taskType: test
---

# Task
`;
      await fs.writeFile(path.join(needsActionFolder, 'task_assign_1.md'), taskContent);
      await engine.startWatching();
      await new Promise(resolve => setTimeout(resolve, 100));

      const assignedTask = await engine.assignNextTask('agent_no_capacity');
      expect(assignedTask).toBeNull();
    });

    it('should return null when no tasks match agent capabilities', async () => {
      // Register agent with specific capabilities
      const agent: AgentMetadata = {
        agentId: 'agent_specific',
        capabilities: ['email'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      await agentRegistry.registerAgent(agent);

      // Create a task requiring different capabilities
      const taskContent = `---
taskId: task_assign_2
priority: high
taskType: test
requiredCapabilities: [social_media]
---

# Task
`;
      await fs.writeFile(path.join(needsActionFolder, 'task_assign_2.md'), taskContent);
      await engine.startWatching();
      await new Promise(resolve => setTimeout(resolve, 100));

      const assignedTask = await engine.assignNextTask('agent_specific');
      expect(assignedTask).toBeNull();
    });
  });

  describe('notifyAgentsOfTask', () => {
    it('should notify eligible agents for critical priority tasks', async () => {
      // Register multiple agents with different capabilities
      const agent1: AgentMetadata = {
        agentId: 'agent_email',
        capabilities: ['email', 'nlp'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      const agent2: AgentMetadata = {
        agentId: 'agent_social',
        capabilities: ['social_media'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      const agent3: AgentMetadata = {
        agentId: 'agent_multi',
        capabilities: ['email', 'social_media', 'nlp'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };

      await agentRegistry.registerAgent(agent1);
      await agentRegistry.registerAgent(agent2);
      await agentRegistry.registerAgent(agent3);

      // Create a critical task requiring email capability
      const criticalTask: TaskMetadata = {
        taskId: 'task_critical_001',
        priority: 'critical',
        taskType: 'email_processing',
        requiredCapabilities: ['email'],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30
      };

      // Spy on console.log to verify notification
      const consoleSpy = vi.spyOn(console, 'log');

      await engine.notifyAgentsOfTask(criticalTask);

      // Verify notification was logged
      expect(consoleSpy).toHaveBeenCalled();
      const logCall = consoleSpy.mock.calls.find(call => 
        call[0].includes('Critical task task_critical_001')
      );
      expect(logCall).toBeDefined();
      
      // Verify eligible agents are included (agent_email and agent_multi have email capability)
      expect(logCall![0]).toContain('agent_email');
      expect(logCall![0]).toContain('agent_multi');
      
      // Verify ineligible agent is not included (agent_social doesn't have email capability)
      expect(logCall![0]).not.toContain('agent_social');

      consoleSpy.mockRestore();
    });

    it('should not notify agents for non-critical priority tasks', async () => {
      // Register an agent
      const agent: AgentMetadata = {
        agentId: 'agent_test',
        capabilities: ['test'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      await agentRegistry.registerAgent(agent);

      // Create a high priority task (not critical)
      const highTask: TaskMetadata = {
        taskId: 'task_high_001',
        priority: 'high',
        taskType: 'test_task',
        requiredCapabilities: ['test'],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30
      };

      // Spy on console.log to verify no notification
      const consoleSpy = vi.spyOn(console, 'log');

      await engine.notifyAgentsOfTask(highTask);

      // Verify no critical task notification was logged
      const criticalLogCall = consoleSpy.mock.calls.find(call => 
        call[0].includes('Critical task')
      );
      expect(criticalLogCall).toBeUndefined();

      consoleSpy.mockRestore();
    });

    it('should handle critical tasks with no required capabilities', async () => {
      // Register multiple agents
      const agent1: AgentMetadata = {
        agentId: 'agent_1',
        capabilities: ['capability_a'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      const agent2: AgentMetadata = {
        agentId: 'agent_2',
        capabilities: ['capability_b'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };

      await agentRegistry.registerAgent(agent1);
      await agentRegistry.registerAgent(agent2);

      // Create a critical task with no required capabilities (available to all agents)
      const criticalTask: TaskMetadata = {
        taskId: 'task_critical_all',
        priority: 'critical',
        taskType: 'general_task',
        requiredCapabilities: [],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30
      };

      // Spy on console.log to verify notification
      const consoleSpy = vi.spyOn(console, 'log');

      await engine.notifyAgentsOfTask(criticalTask);

      // Verify notification was logged
      expect(consoleSpy).toHaveBeenCalled();
      const logCall = consoleSpy.mock.calls.find(call => 
        call[0].includes('Critical task task_critical_all')
      );
      expect(logCall).toBeDefined();
      
      // Verify all agents are included
      expect(logCall![0]).toContain('agent_1');
      expect(logCall![0]).toContain('agent_2');

      consoleSpy.mockRestore();
    });

    it('should handle critical tasks when no agents are eligible', async () => {
      // Register an agent with specific capabilities
      const agent: AgentMetadata = {
        agentId: 'agent_limited',
        capabilities: ['capability_x'],
        maxConcurrentTasks: 5,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date()
      };
      await agentRegistry.registerAgent(agent);

      // Create a critical task requiring different capabilities
      const criticalTask: TaskMetadata = {
        taskId: 'task_critical_no_match',
        priority: 'critical',
        taskType: 'special_task',
        requiredCapabilities: ['capability_y', 'capability_z'],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30
      };

      // Spy on console.log to verify notification
      const consoleSpy = vi.spyOn(console, 'log');

      await engine.notifyAgentsOfTask(criticalTask);

      // Verify notification was logged (even with empty agent list)
      expect(consoleSpy).toHaveBeenCalled();
      const logCall = consoleSpy.mock.calls.find(call => 
        call[0].includes('Critical task task_critical_no_match')
      );
      expect(logCall).toBeDefined();
      
      // Verify no agents are listed (empty list or no agent names)
      expect(logCall![0]).not.toContain('agent_limited');

      consoleSpy.mockRestore();
    });
  });
});
