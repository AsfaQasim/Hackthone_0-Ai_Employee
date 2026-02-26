/**
 * Unit tests for TaskRouter component
 * 
 * Tests capability matching, routing rules, and agent eligibility.
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { promises as fs } from 'fs';
import * as path from 'path';
import { TaskRouter } from '../../src/agent-work-assignment/components/TaskRouter';
import { AgentRegistry } from '../../src/agent-work-assignment/components/AgentRegistry';
import type { AgentMetadata } from '../../src/agent-work-assignment/models/AgentMetadata';
import type { TaskMetadata } from '../../src/agent-work-assignment/models/TaskMetadata';
import type { RoutingRule } from '../../src/agent-work-assignment/components/TaskRouter';

describe('TaskRouter', () => {
  const testDir = path.join(process.cwd(), 'test-temp', 'task-router');
  const registryFile = path.join(testDir, 'registry.yaml');
  const inProgressBase = path.join(testDir, 'In_Progress');
  
  let registry: AgentRegistry;
  let router: TaskRouter;

  beforeEach(async () => {
    // Clean up test directory
    await fs.rm(testDir, { recursive: true, force: true });
    await fs.mkdir(testDir, { recursive: true });

    registry = new AgentRegistry({
      registryFilePath: registryFile,
      inProgressBasePath: inProgressBase,
    });
    await registry.initialize();

    router = new TaskRouter(registry);
  });

  afterEach(async () => {
    // Clean up test directory
    await fs.rm(testDir, { recursive: true, force: true });
  });

  describe('getEligibleAgents', () => {
    it('should return all active agents for task with no capability requirements', async () => {
      // Register multiple agents
      const agent1: AgentMetadata = {
        agentId: 'agent_1',
        capabilities: ['email'],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      const agent2: AgentMetadata = {
        agentId: 'agent_2',
        capabilities: ['social_media'],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(agent1);
      await registry.registerAgent(agent2);

      // Task with no capability requirements
      const task: TaskMetadata = {
        taskId: 'task_1',
        priority: 'medium',
        taskType: 'general',
        requiredCapabilities: [],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const eligibleAgents = await router.getEligibleAgents(task);
      expect(eligibleAgents).toHaveLength(2);
      expect(eligibleAgents).toContain('agent_1');
      expect(eligibleAgents).toContain('agent_2');
    });

    it('should return only agents with matching capabilities', async () => {
      // Register agents with different capabilities
      const emailAgent: AgentMetadata = {
        agentId: 'agent_email',
        capabilities: ['email', 'nlp'],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      const socialAgent: AgentMetadata = {
        agentId: 'agent_social',
        capabilities: ['social_media', 'image_processing'],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(emailAgent);
      await registry.registerAgent(socialAgent);

      // Task requiring email capability
      const task: TaskMetadata = {
        taskId: 'task_email',
        priority: 'high',
        taskType: 'email_processing',
        requiredCapabilities: ['email'],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const eligibleAgents = await router.getEligibleAgents(task);
      expect(eligibleAgents).toHaveLength(1);
      expect(eligibleAgents).toContain('agent_email');
    });

    it('should return agents with all required capabilities for multi-capability task', async () => {
      // Register agents with various capabilities
      const fullAgent: AgentMetadata = {
        agentId: 'agent_full',
        capabilities: ['email', 'nlp', 'pdf_generation'],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      const partialAgent: AgentMetadata = {
        agentId: 'agent_partial',
        capabilities: ['email'],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(fullAgent);
      await registry.registerAgent(partialAgent);

      // Task requiring multiple capabilities
      const task: TaskMetadata = {
        taskId: 'task_multi',
        priority: 'high',
        taskType: 'complex_processing',
        requiredCapabilities: ['email', 'nlp'],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const eligibleAgents = await router.getEligibleAgents(task);
      expect(eligibleAgents).toHaveLength(1);
      expect(eligibleAgents).toContain('agent_full');
    });

    it('should return empty array when no agents have required capabilities', async () => {
      const agent: AgentMetadata = {
        agentId: 'agent_basic',
        capabilities: ['email'],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(agent);

      // Task requiring capability no agent has
      const task: TaskMetadata = {
        taskId: 'task_special',
        priority: 'high',
        taskType: 'special_processing',
        requiredCapabilities: ['quantum_computing'],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const eligibleAgents = await router.getEligibleAgents(task);
      expect(eligibleAgents).toHaveLength(0);
    });

    it('should not return inactive agents', async () => {
      const activeAgent: AgentMetadata = {
        agentId: 'agent_active',
        capabilities: ['email'],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      const inactiveAgent: AgentMetadata = {
        agentId: 'agent_inactive',
        capabilities: ['email'],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'inactive',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(activeAgent);
      await registry.registerAgent(inactiveAgent);

      const task: TaskMetadata = {
        taskId: 'task_email',
        priority: 'medium',
        taskType: 'email_processing',
        requiredCapabilities: ['email'],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const eligibleAgents = await router.getEligibleAgents(task);
      expect(eligibleAgents).toHaveLength(1);
      expect(eligibleAgents).toContain('agent_active');
    });
  });

  describe('canAgentHandleTask', () => {
    it('should return true when agent has all required capabilities', async () => {
      const agent: AgentMetadata = {
        agentId: 'agent_capable',
        capabilities: ['email', 'nlp', 'pdf_generation'],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(agent);

      const task: TaskMetadata = {
        taskId: 'task_1',
        priority: 'medium',
        taskType: 'email_processing',
        requiredCapabilities: ['email', 'nlp'],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const canHandle = await router.canAgentHandleTask('agent_capable', task);
      expect(canHandle).toBe(true);
    });

    it('should return false when agent lacks required capabilities', async () => {
      const agent: AgentMetadata = {
        agentId: 'agent_limited',
        capabilities: ['email'],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(agent);

      const task: TaskMetadata = {
        taskId: 'task_1',
        priority: 'medium',
        taskType: 'complex_processing',
        requiredCapabilities: ['email', 'nlp'],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const canHandle = await router.canAgentHandleTask('agent_limited', task);
      expect(canHandle).toBe(false);
    });

    it('should return true for task with no capability requirements', async () => {
      const agent: AgentMetadata = {
        agentId: 'agent_any',
        capabilities: ['email'],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(agent);

      const task: TaskMetadata = {
        taskId: 'task_simple',
        priority: 'low',
        taskType: 'general',
        requiredCapabilities: [],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const canHandle = await router.canAgentHandleTask('agent_any', task);
      expect(canHandle).toBe(true);
    });

    it('should return false for non-existent agent', async () => {
      const task: TaskMetadata = {
        taskId: 'task_1',
        priority: 'medium',
        taskType: 'email_processing',
        requiredCapabilities: ['email'],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const canHandle = await router.canAgentHandleTask('non_existent_agent', task);
      expect(canHandle).toBe(false);
    });

    it('should handle empty capability requirements', async () => {
      const agent: AgentMetadata = {
        agentId: 'agent_test',
        capabilities: [],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(agent);

      const task: TaskMetadata = {
        taskId: 'task_no_req',
        priority: 'medium',
        taskType: 'simple',
        requiredCapabilities: [],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const canHandle = await router.canAgentHandleTask('agent_test', task);
      expect(canHandle).toBe(true);
    });
  });

  describe('routing rules', () => {
    it('should add and evaluate routing rules', async () => {
      const rule: RoutingRule = {
        ruleId: 'rule_1',
        condition: (task) => task.priority === 'critical',
        targetAgents: ['agent_priority'],
        priority: 10,
      };

      router.addRoutingRule(rule);

      const task: TaskMetadata = {
        taskId: 'task_critical',
        priority: 'critical',
        taskType: 'urgent',
        requiredCapabilities: [],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 15,
      };

      const targetAgents = await router.evaluateRoutingRules(task);
      expect(targetAgents).toEqual(['agent_priority']);
    });

    it('should apply highest priority rule when multiple rules match', async () => {
      const rule1: RoutingRule = {
        ruleId: 'rule_low',
        condition: (task) => task.taskType === 'email_processing',
        targetAgents: ['agent_general'],
        priority: 5,
      };

      const rule2: RoutingRule = {
        ruleId: 'rule_high',
        condition: (task) => task.taskType === 'email_processing',
        targetAgents: ['agent_specialist'],
        priority: 10,
      };

      router.addRoutingRule(rule1);
      router.addRoutingRule(rule2);

      const task: TaskMetadata = {
        taskId: 'task_email',
        priority: 'medium',
        taskType: 'email_processing',
        requiredCapabilities: [],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const targetAgents = await router.evaluateRoutingRules(task);
      expect(targetAgents).toEqual(['agent_specialist']);
    });

    it('should return empty array when no rules match', async () => {
      const rule: RoutingRule = {
        ruleId: 'rule_specific',
        condition: (task) => task.priority === 'critical',
        targetAgents: ['agent_priority'],
        priority: 10,
      };

      router.addRoutingRule(rule);

      const task: TaskMetadata = {
        taskId: 'task_normal',
        priority: 'medium',
        taskType: 'general',
        requiredCapabilities: [],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const targetAgents = await router.evaluateRoutingRules(task);
      expect(targetAgents).toEqual([]);
    });

    it('should remove routing rules', async () => {
      const rule: RoutingRule = {
        ruleId: 'rule_temp',
        condition: (task) => task.priority === 'high',
        targetAgents: ['agent_temp'],
        priority: 10,
      };

      router.addRoutingRule(rule);
      router.removeRoutingRule('rule_temp');

      const task: TaskMetadata = {
        taskId: 'task_high',
        priority: 'high',
        taskType: 'general',
        requiredCapabilities: [],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const targetAgents = await router.evaluateRoutingRules(task);
      expect(targetAgents).toEqual([]);
    });

    it('should handle complex routing conditions', async () => {
      const rule: RoutingRule = {
        ruleId: 'rule_complex',
        condition: (task) => 
          task.priority === 'critical' && 
          task.taskType === 'email_processing' &&
          task.requiredCapabilities.includes('nlp'),
        targetAgents: ['agent_specialist'],
        priority: 10,
      };

      router.addRoutingRule(rule);

      const matchingTask: TaskMetadata = {
        taskId: 'task_match',
        priority: 'critical',
        taskType: 'email_processing',
        requiredCapabilities: ['nlp', 'email'],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 15,
      };

      const nonMatchingTask: TaskMetadata = {
        taskId: 'task_no_match',
        priority: 'high',
        taskType: 'email_processing',
        requiredCapabilities: ['nlp', 'email'],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const matchingResult = await router.evaluateRoutingRules(matchingTask);
      expect(matchingResult).toEqual(['agent_specialist']);

      const nonMatchingResult = await router.evaluateRoutingRules(nonMatchingTask);
      expect(nonMatchingResult).toEqual([]);
    });
  });

  describe('edge cases', () => {
    it('should handle agent with no capabilities matching task with no requirements', async () => {
      const agent: AgentMetadata = {
        agentId: 'agent_empty',
        capabilities: [],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(agent);

      const task: TaskMetadata = {
        taskId: 'task_empty',
        priority: 'medium',
        taskType: 'simple',
        requiredCapabilities: [],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const eligibleAgents = await router.getEligibleAgents(task);
      expect(eligibleAgents).toContain('agent_empty');
    });

    it('should handle task with duplicate capability requirements', async () => {
      const agent: AgentMetadata = {
        agentId: 'agent_test',
        capabilities: ['email'],
        maxConcurrentTasks: 3,
        maxTasksByType: new Map(),
        status: 'active',
        lastHeartbeat: new Date(),
        registeredAt: new Date(),
      };

      await registry.registerAgent(agent);

      const task: TaskMetadata = {
        taskId: 'task_dup',
        priority: 'medium',
        taskType: 'email_processing',
        requiredCapabilities: ['email', 'email'],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const canHandle = await router.canAgentHandleTask('agent_test', task);
      expect(canHandle).toBe(true);
    });

    it('should return empty array when no agents are registered', async () => {
      const task: TaskMetadata = {
        taskId: 'task_1',
        priority: 'medium',
        taskType: 'general',
        requiredCapabilities: [],
        createdAt: new Date(),
        reclaimCount: 0,
        timeoutMinutes: 30,
      };

      const eligibleAgents = await router.getEligibleAgents(task);
      expect(eligibleAgents).toHaveLength(0);
    });
  });
});
