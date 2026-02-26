/**
 * Unit tests for agent work assignment models
 */

import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import {
  type TaskMetadata,
  type AgentMetadata,
  type ClaimResult,
  type AssignmentStrategy,
  isValidTaskMetadata,
  isValidAgentMetadata,
  isValidClaimResult,
  isValidTaskPriority,
  isValidAgentStatus,
  isValidAssignmentStrategy
} from '../../src/agent-work-assignment/models/index';

describe('TaskMetadata', () => {
  it('should validate valid task metadata', () => {
    const validTask: TaskMetadata = {
      taskId: 'task_001',
      priority: 'high',
      taskType: 'email_processing',
      requiredCapabilities: ['email', 'nlp'],
      createdAt: new Date(),
      reclaimCount: 0,
      timeoutMinutes: 30
    };
    
    expect(isValidTaskMetadata(validTask)).toBe(true);
  });

  it('should reject invalid task metadata', () => {
    expect(isValidTaskMetadata(null)).toBe(false);
    expect(isValidTaskMetadata({})).toBe(false);
    expect(isValidTaskMetadata({ taskId: 'test' })).toBe(false);
  });

  it('should validate task priority values', () => {
    expect(isValidTaskPriority('critical')).toBe(true);
    expect(isValidTaskPriority('high')).toBe(true);
    expect(isValidTaskPriority('medium')).toBe(true);
    expect(isValidTaskPriority('low')).toBe(true);
    expect(isValidTaskPriority('invalid')).toBe(false);
  });
});

describe('AgentMetadata', () => {
  it('should validate valid agent metadata', () => {
    const validAgent: AgentMetadata = {
      agentId: 'agent_001',
      capabilities: ['email', 'social_media'],
      maxConcurrentTasks: 5,
      maxTasksByType: new Map([['email', 3]]),
      status: 'active',
      lastHeartbeat: new Date(),
      registeredAt: new Date()
    };
    
    expect(isValidAgentMetadata(validAgent)).toBe(true);
  });

  it('should reject invalid agent metadata', () => {
    expect(isValidAgentMetadata(null)).toBe(false);
    expect(isValidAgentMetadata({})).toBe(false);
  });

  it('should validate agent status values', () => {
    expect(isValidAgentStatus('active')).toBe(true);
    expect(isValidAgentStatus('inactive')).toBe(true);
    expect(isValidAgentStatus('unresponsive')).toBe(true);
    expect(isValidAgentStatus('invalid')).toBe(false);
  });
});

describe('ClaimResult', () => {
  it('should validate valid claim result', () => {
    const validResult: ClaimResult = {
      success: true,
      taskId: 'task_001',
      agentId: 'agent_001'
    };
    
    expect(isValidClaimResult(validResult)).toBe(true);
  });

  it('should validate claim result with error', () => {
    const resultWithError: ClaimResult = {
      success: false,
      taskId: 'task_001',
      agentId: 'agent_001',
      error: 'Task already claimed'
    };
    
    expect(isValidClaimResult(resultWithError)).toBe(true);
  });
});

describe('AssignmentStrategy', () => {
  it('should validate assignment strategy values', () => {
    expect(isValidAssignmentStrategy('round-robin')).toBe(true);
    expect(isValidAssignmentStrategy('priority-first')).toBe(true);
    expect(isValidAssignmentStrategy('least-loaded')).toBe(true);
    expect(isValidAssignmentStrategy('capability-match')).toBe(true);
    expect(isValidAssignmentStrategy('invalid')).toBe(false);
  });
});
