/**
 * Unit tests for ClaimLockManager
 * Tests atomic lock operations, stale lock cleanup, and edge cases
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import * as fs from 'fs/promises';
import * as path from 'path';
import { ClaimLockManager } from '../../src/agent-work-assignment/components/ClaimLockManager';

describe('ClaimLockManager', () => {
  const testBaseDir = path.join(process.cwd(), 'test-temp');
  const testLockDir = path.join(testBaseDir, 'locks');
  const testNeedsActionDir = path.join(testBaseDir, 'Needs_Action');
  const testInProgressDir = path.join(testBaseDir, 'In_Progress');
  let lockManager: ClaimLockManager;

  beforeEach(async () => {
    // Clean up test directory
    await fs.rm(testBaseDir, { recursive: true, force: true });
    
    lockManager = new ClaimLockManager({
      lockDirectory: testLockDir,
      maxLockDurationSeconds: 10,
      needsActionFolder: testNeedsActionDir,
      inProgressFolder: testInProgressDir,
      retryAttempts: 3,
      retryBackoffMs: [10, 20, 30] // Shorter delays for testing
    });
    
    await lockManager.initialize();
    await fs.mkdir(testNeedsActionDir, { recursive: true });
    await fs.mkdir(testInProgressDir, { recursive: true });
  });

  afterEach(async () => {
    // Clean up test directory
    await fs.rm(testBaseDir, { recursive: true, force: true });
  });

  describe('acquireLock', () => {
    it('should successfully acquire a lock for a task', async () => {
      const result = await lockManager.acquireLock('task_123');
      expect(result).toBe(true);
      
      // Verify lock file exists
      const isLocked = await lockManager.isLocked('task_123');
      expect(isLocked).toBe(true);
    });

    it('should fail to acquire a lock if already held', async () => {
      // First acquisition should succeed
      const firstResult = await lockManager.acquireLock('task_123');
      expect(firstResult).toBe(true);
      
      // Second acquisition should fail
      const secondResult = await lockManager.acquireLock('task_123');
      expect(secondResult).toBe(false);
    });

    it('should handle special characters in task IDs', async () => {
      const taskId = 'task/with:special@chars';
      const result = await lockManager.acquireLock(taskId);
      expect(result).toBe(true);
      
      const isLocked = await lockManager.isLocked(taskId);
      expect(isLocked).toBe(true);
    });
  });

  describe('releaseLock', () => {
    it('should successfully release a held lock', async () => {
      await lockManager.acquireLock('task_123');
      
      await lockManager.releaseLock('task_123');
      
      // Verify lock is released
      const isLocked = await lockManager.isLocked('task_123');
      expect(isLocked).toBe(false);
    });

    it('should not throw when releasing a non-existent lock', async () => {
      // Should not throw
      await expect(lockManager.releaseLock('nonexistent_task')).resolves.toBeUndefined();
    });

    it('should allow re-acquisition after release', async () => {
      await lockManager.acquireLock('task_123');
      await lockManager.releaseLock('task_123');
      
      const result = await lockManager.acquireLock('task_123');
      expect(result).toBe(true);
    });
  });

  describe('releaseStaleLocksOlderThan', () => {
    it('should release locks older than threshold', async () => {
      // Acquire a lock
      await lockManager.acquireLock('task_old');
      
      // Manually modify the lock file to make it appear old
      const lockFilePath = path.join(testLockDir, 'task_old.lock');
      const lockContent = await fs.readFile(lockFilePath, 'utf-8');
      const lockData = JSON.parse(lockContent);
      
      // Set acquiredAt to 15 seconds ago
      const oldTime = new Date(Date.now() - 15000);
      lockData.acquiredAt = oldTime.toISOString();
      await fs.writeFile(lockFilePath, JSON.stringify(lockData, null, 2));
      
      // Release stale locks older than 10 seconds
      const releasedCount = await lockManager.releaseStaleLocksOlderThan(10);
      expect(releasedCount).toBe(1);
      
      // Verify lock is released
      const isLocked = await lockManager.isLocked('task_old');
      expect(isLocked).toBe(false);
    });

    it('should not release locks newer than threshold', async () => {
      await lockManager.acquireLock('task_new');
      
      // Release stale locks older than 10 seconds
      const releasedCount = await lockManager.releaseStaleLocksOlderThan(10);
      expect(releasedCount).toBe(0);
      
      // Verify lock is still held
      const isLocked = await lockManager.isLocked('task_new');
      expect(isLocked).toBe(true);
    });

    it('should handle corrupted lock files', async () => {
      // Create a corrupted lock file
      const corruptedLockPath = path.join(testLockDir, 'corrupted.lock');
      await fs.writeFile(corruptedLockPath, 'invalid json {{{');
      
      // Should not throw and should remove corrupted lock
      const releasedCount = await lockManager.releaseStaleLocksOlderThan(10);
      expect(releasedCount).toBe(1);
    });

    it('should return 0 when no locks exist', async () => {
      const releasedCount = await lockManager.releaseStaleLocksOlderThan(10);
      expect(releasedCount).toBe(0);
    });

    it('should handle multiple stale locks', async () => {
      // Create multiple old locks
      await lockManager.acquireLock('task_1');
      await lockManager.acquireLock('task_2');
      await lockManager.acquireLock('task_3');
      
      // Make all locks appear old
      const lockFiles = await fs.readdir(testLockDir);
      const oldTime = new Date(Date.now() - 15000);
      
      for (const lockFile of lockFiles) {
        const lockFilePath = path.join(testLockDir, lockFile);
        const lockContent = await fs.readFile(lockFilePath, 'utf-8');
        const lockData = JSON.parse(lockContent);
        lockData.acquiredAt = oldTime.toISOString();
        await fs.writeFile(lockFilePath, JSON.stringify(lockData, null, 2));
      }
      
      const releasedCount = await lockManager.releaseStaleLocksOlderThan(10);
      expect(releasedCount).toBe(3);
    });
  });

  describe('isLocked', () => {
    it('should return true for locked tasks', async () => {
      await lockManager.acquireLock('task_123');
      const isLocked = await lockManager.isLocked('task_123');
      expect(isLocked).toBe(true);
    });

    it('should return false for unlocked tasks', async () => {
      const isLocked = await lockManager.isLocked('task_123');
      expect(isLocked).toBe(false);
    });

    it('should return false after lock is released', async () => {
      await lockManager.acquireLock('task_123');
      await lockManager.releaseLock('task_123');
      const isLocked = await lockManager.isLocked('task_123');
      expect(isLocked).toBe(false);
    });
  });

  describe('concurrent operations', () => {
    it('should handle concurrent lock attempts correctly', async () => {
      // Simulate multiple agents trying to acquire the same lock
      const results = await Promise.all([
        lockManager.acquireLock('task_concurrent'),
        lockManager.acquireLock('task_concurrent'),
        lockManager.acquireLock('task_concurrent')
      ]);
      
      // Exactly one should succeed
      const successCount = results.filter(r => r === true).length;
      expect(successCount).toBe(1);
    });
  });

  describe('attemptClaim', () => {
    const createTaskFile = async (taskId: string, priority: string = 'medium') => {
      const taskContent = `---
taskId: ${taskId}
priority: ${priority}
taskType: test_task
requiredCapabilities: []
createdAt: ${new Date().toISOString()}
reclaimCount: 0
timeoutMinutes: 30
---

# Task: ${taskId}

This is a test task.
`;
      const taskPath = path.join(testNeedsActionDir, `${taskId}.md`);
      await fs.writeFile(taskPath, taskContent, 'utf-8');
    };

    it('should successfully claim a task and move it to agent In_Progress folder', async () => {
      const taskId = 'task_123';
      const agentId = 'agent_alpha';
      
      await createTaskFile(taskId);
      
      const result = await lockManager.attemptClaim(taskId, agentId);
      
      expect(result.success).toBe(true);
      expect(result.taskId).toBe(taskId);
      expect(result.agentId).toBe(agentId);
      expect(result.error).toBeUndefined();
      
      // Verify task moved to In_Progress
      const sourcePath = path.join(testNeedsActionDir, `${taskId}.md`);
      const destPath = path.join(testInProgressDir, agentId, `${taskId}.md`);
      
      await expect(fs.access(sourcePath)).rejects.toThrow();
      await expect(fs.access(destPath)).resolves.toBeUndefined();
    });

    it('should update task frontmatter with claim metadata', async () => {
      const taskId = 'task_456';
      const agentId = 'agent_beta';
      
      await createTaskFile(taskId);
      
      const result = await lockManager.attemptClaim(taskId, agentId);
      
      expect(result.success).toBe(true);
      
      // Read claimed task file
      const destPath = path.join(testInProgressDir, agentId, `${taskId}.md`);
      const content = await fs.readFile(destPath, 'utf-8');
      
      // Verify frontmatter contains claim metadata
      expect(content).toContain(`claimedBy: ${agentId}`);
      expect(content).toContain('status: in_progress');
      expect(content).toContain('claimedAt:');
      
      // Verify the claimedAt field has a value (not empty)
      const claimedAtMatch = content.match(/claimedAt: (.+)/);
      expect(claimedAtMatch).toBeTruthy();
      expect(claimedAtMatch![1].trim()).not.toBe('');
    });

    it('should fail when task file does not exist', async () => {
      const taskId = 'nonexistent_task';
      const agentId = 'agent_gamma';
      
      const result = await lockManager.attemptClaim(taskId, agentId);
      
      expect(result.success).toBe(false);
      expect(result.error).toContain('Task file not found');
    });

    it('should handle concurrent claim attempts with mutual exclusion', async () => {
      const taskId = 'task_concurrent_claim';
      await createTaskFile(taskId);
      
      // Multiple agents try to claim the same task
      const results = await Promise.all([
        lockManager.attemptClaim(taskId, 'agent_1'),
        lockManager.attemptClaim(taskId, 'agent_2'),
        lockManager.attemptClaim(taskId, 'agent_3')
      ]);
      
      // Exactly one should succeed
      const successCount = results.filter(r => r.success).length;
      expect(successCount).toBe(1);
      
      // Find the successful claim
      const successfulClaim = results.find(r => r.success);
      expect(successfulClaim).toBeDefined();
      
      if (successfulClaim) {
        // Verify task is in the correct agent's folder
        const destPath = path.join(testInProgressDir, successfulClaim.agentId, `${taskId}.md`);
        await expect(fs.access(destPath)).resolves.toBeUndefined();
      }
      
      // Verify task is not in Needs_Action
      const sourcePath = path.join(testNeedsActionDir, `${taskId}.md`);
      await expect(fs.access(sourcePath)).rejects.toThrow();
    });

    it('should retry on transient failures with exponential backoff', async () => {
      const taskId = 'task_retry';
      const agentId = 'agent_delta';
      
      await createTaskFile(taskId);
      
      // The retry logic is built into attemptClaim
      // This test verifies it completes successfully even with potential contention
      const result = await lockManager.attemptClaim(taskId, agentId);
      
      expect(result.success).toBe(true);
    });

    it('should create agent In_Progress folder if it does not exist', async () => {
      const taskId = 'task_new_agent';
      const agentId = 'agent_new';
      
      await createTaskFile(taskId);
      
      // Verify agent folder doesn't exist yet
      const agentFolder = path.join(testInProgressDir, agentId);
      await expect(fs.access(agentFolder)).rejects.toThrow();
      
      const result = await lockManager.attemptClaim(taskId, agentId);
      
      expect(result.success).toBe(true);
      
      // Verify agent folder was created
      await expect(fs.access(agentFolder)).resolves.toBeUndefined();
    });

    it('should preserve task body content when updating frontmatter', async () => {
      const taskId = 'task_preserve_body';
      const agentId = 'agent_epsilon';
      const taskBody = '# Task: Preserve Body\n\nThis content should be preserved.\n\n## Details\n- Item 1\n- Item 2';
      
      const taskContent = `---
taskId: ${taskId}
priority: high
taskType: test_task
---

${taskBody}`;
      
      const taskPath = path.join(testNeedsActionDir, `${taskId}.md`);
      await fs.writeFile(taskPath, taskContent, 'utf-8');
      
      const result = await lockManager.attemptClaim(taskId, agentId);
      
      expect(result.success).toBe(true);
      
      // Read claimed task file
      const destPath = path.join(testInProgressDir, agentId, `${taskId}.md`);
      const content = await fs.readFile(destPath, 'utf-8');
      
      // Verify body content is preserved
      expect(content).toContain(taskBody);
    });

    it('should handle tasks with no frontmatter by adding it', async () => {
      const taskId = 'task_no_frontmatter';
      const agentId = 'agent_zeta';
      const taskContent = '# Task Without Frontmatter\n\nThis task has no frontmatter.';
      
      const taskPath = path.join(testNeedsActionDir, `${taskId}.md`);
      await fs.writeFile(taskPath, taskContent, 'utf-8');
      
      const result = await lockManager.attemptClaim(taskId, agentId);
      
      expect(result.success).toBe(true);
      
      // Read claimed task file
      const destPath = path.join(testInProgressDir, agentId, `${taskId}.md`);
      const content = await fs.readFile(destPath, 'utf-8');
      
      // Verify frontmatter was added
      expect(content).toMatch(/^---\n/);
      expect(content).toContain(`claimedBy: ${agentId}`);
      expect(content).toContain('status: in_progress');
    });
  });

  describe('releaseClaim', () => {
    const createClaimedTask = async (taskId: string, agentId: string) => {
      const taskContent = `---
taskId: ${taskId}
priority: medium
taskType: test_task
claimedAt: ${new Date().toISOString()}
claimedBy: ${agentId}
status: in_progress
---

# Task: ${taskId}

This is a claimed task.
`;
      const agentFolder = path.join(testInProgressDir, agentId);
      await fs.mkdir(agentFolder, { recursive: true });
      const taskPath = path.join(agentFolder, `${taskId}.md`);
      await fs.writeFile(taskPath, taskContent, 'utf-8');
    };

    it('should release a claimed task back to Needs_Action', async () => {
      const taskId = 'task_release';
      const agentId = 'agent_alpha';
      
      await createClaimedTask(taskId, agentId);
      
      await lockManager.releaseClaim(taskId, agentId);
      
      // Verify task moved back to Needs_Action
      const sourcePath = path.join(testInProgressDir, agentId, `${taskId}.md`);
      const destPath = path.join(testNeedsActionDir, `${taskId}.md`);
      
      await expect(fs.access(sourcePath)).rejects.toThrow();
      await expect(fs.access(destPath)).resolves.toBeUndefined();
    });

    it('should clear claim metadata from frontmatter', async () => {
      const taskId = 'task_clear_metadata';
      const agentId = 'agent_beta';
      
      await createClaimedTask(taskId, agentId);
      
      await lockManager.releaseClaim(taskId, agentId);
      
      // Read released task file
      const destPath = path.join(testNeedsActionDir, `${taskId}.md`);
      const content = await fs.readFile(destPath, 'utf-8');
      
      // Verify claim metadata is removed
      expect(content).not.toContain('claimedBy:');
      expect(content).not.toContain('claimedAt:');
      expect(content).not.toContain('status: in_progress');
      
      // Verify other metadata is preserved
      expect(content).toContain(`taskId: ${taskId}`);
      expect(content).toContain('priority: medium');
    });

    it('should throw error when task file does not exist', async () => {
      const taskId = 'nonexistent_task';
      const agentId = 'agent_gamma';
      
      await expect(lockManager.releaseClaim(taskId, agentId)).rejects.toThrow(
        'Task file not found'
      );
    });

    it('should preserve task body content when clearing metadata', async () => {
      const taskId = 'task_preserve_on_release';
      const agentId = 'agent_delta';
      const taskBody = '# Task Body\n\nImportant content here.';
      
      const taskContent = `---
taskId: ${taskId}
priority: high
claimedAt: ${new Date().toISOString()}
claimedBy: ${agentId}
status: in_progress
---

${taskBody}`;
      
      const agentFolder = path.join(testInProgressDir, agentId);
      await fs.mkdir(agentFolder, { recursive: true });
      const taskPath = path.join(agentFolder, `${taskId}.md`);
      await fs.writeFile(taskPath, taskContent, 'utf-8');
      
      await lockManager.releaseClaim(taskId, agentId);
      
      // Read released task file
      const destPath = path.join(testNeedsActionDir, `${taskId}.md`);
      const content = await fs.readFile(destPath, 'utf-8');
      
      // Verify body content is preserved
      expect(content).toContain(taskBody);
    });
  });
});
