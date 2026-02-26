/**
 * Integration tests for task validation in TaskAssignmentEngine
 * Tests that malformed tasks are moved to Malformed folder and logged
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { promises as fs } from 'fs';
import * as path from 'path';
import { TaskAssignmentEngine } from '../../src/agent-work-assignment/components/TaskAssignmentEngine';
import { AgentRegistry } from '../../src/agent-work-assignment/components/AgentRegistry';
import { TaskRouter } from '../../src/agent-work-assignment/components/TaskRouter';
import { ClaimLockManager } from '../../src/agent-work-assignment/components/ClaimLockManager';

describe('TaskAssignmentEngine - Validation Integration', () => {
  const testDir = path.join(process.cwd(), 'test-temp-validation');
  const needsActionFolder = path.join(testDir, 'Needs_Action');
  const malformedFolder = path.join(testDir, 'Malformed');
  const inProgressFolder = path.join(testDir, 'In_Progress');
  const logFolder = path.join(testDir, '.logs');

  let engine: TaskAssignmentEngine;
  let agentRegistry: AgentRegistry;
  let taskRouter: TaskRouter;
  let claimLockManager: ClaimLockManager;

  beforeEach(async () => {
    // Create test directories
    await fs.mkdir(needsActionFolder, { recursive: true });
    await fs.mkdir(malformedFolder, { recursive: true });
    await fs.mkdir(inProgressFolder, { recursive: true });
    await fs.mkdir(logFolder, { recursive: true });

    // Initialize components
    agentRegistry = new AgentRegistry({
      registryFolder: testDir,
      inProgressFolder
    });

    taskRouter = new TaskRouter(agentRegistry);

    claimLockManager = new ClaimLockManager({
      needsActionFolder,
      inProgressFolder,
      lockFolder: path.join(testDir, '.locks')
    });

    engine = new TaskAssignmentEngine(
      {
        needsActionFolder,
        malformedFolder,
        defaultPriority: 'medium',
        defaultTimeoutMinutes: 30,
        logFolder,
        validatorConfig: {
          requiredFields: ['taskId', 'priority'],
          registeredTaskTypes: ['email_processing', 'invoice_generation'],
          allowUnregisteredTypes: false
        }
      },
      agentRegistry,
      taskRouter,
      claimLockManager
    );

    await engine.startWatching();
  });

  afterEach(async () => {
    await engine.stopWatching();
    
    // Clean up test directory
    try {
      await fs.rm(testDir, { recursive: true, force: true });
    } catch (error) {
      // Ignore cleanup errors
    }
  });

  it('should accept valid task files', async () => {
    const taskContent = `---
taskId: task_valid_001
priority: high
taskType: email_processing
requiredCapabilities: [email]
---

# Valid Task
`;

    await fs.writeFile(
      path.join(needsActionFolder, 'task_valid_001.md'),
      taskContent
    );

    // Wait for file watcher to process
    await new Promise(resolve => setTimeout(resolve, 100));

    // Task should be in queue
    const tasks = await engine.getAvailableTasks();
    expect(tasks.length).toBe(1);
    expect(tasks[0].taskId).toBe('task_valid_001');

    // Task should NOT be in Malformed folder
    const malformedFiles = await fs.readdir(malformedFolder);
    expect(malformedFiles.length).toBe(0);
  });

  it('should move task with missing required fields to Malformed folder', async () => {
    const taskContent = `---
priority: high
taskType: email_processing
---

# Task Missing ID
`;

    await fs.writeFile(
      path.join(needsActionFolder, 'task_missing_id.md'),
      taskContent
    );

    // Wait for file watcher to process
    await new Promise(resolve => setTimeout(resolve, 100));

    // Task should NOT be in queue
    const tasks = await engine.getAvailableTasks();
    expect(tasks.length).toBe(0);

    // Task should be in Malformed folder
    const malformedFiles = await fs.readdir(malformedFolder);
    expect(malformedFiles).toContain('task_missing_id.md');
  });

  it('should move task with invalid priority to Malformed folder', async () => {
    const taskContent = `---
taskId: task_invalid_priority
priority: super_urgent
taskType: email_processing
---

# Task with Invalid Priority
`;

    await fs.writeFile(
      path.join(needsActionFolder, 'task_invalid_priority.md'),
      taskContent
    );

    // Wait for file watcher to process
    await new Promise(resolve => setTimeout(resolve, 100));

    // Task should NOT be in queue
    const tasks = await engine.getAvailableTasks();
    expect(tasks.length).toBe(0);

    // Task should be in Malformed folder
    const malformedFiles = await fs.readdir(malformedFolder);
    expect(malformedFiles).toContain('task_invalid_priority.md');
  });

  it('should move task with unregistered task type to Malformed folder', async () => {
    const taskContent = `---
taskId: task_unregistered_type
priority: high
taskType: unknown_type
---

# Task with Unregistered Type
`;

    await fs.writeFile(
      path.join(needsActionFolder, 'task_unregistered_type.md'),
      taskContent
    );

    // Wait for file watcher to process
    await new Promise(resolve => setTimeout(resolve, 100));

    // Task should NOT be in queue
    const tasks = await engine.getAvailableTasks();
    expect(tasks.length).toBe(0);

    // Task should be in Malformed folder
    const malformedFiles = await fs.readdir(malformedFolder);
    expect(malformedFiles).toContain('task_unregistered_type.md');
  });

  it('should move task with invalid YAML to Malformed folder', async () => {
    const taskContent = `---
taskId: task_invalid_yaml
priority: high
  invalid: indentation
taskType: email_processing
---

# Task with Invalid YAML
`;

    await fs.writeFile(
      path.join(needsActionFolder, 'task_invalid_yaml.md'),
      taskContent
    );

    // Wait for file watcher to process
    await new Promise(resolve => setTimeout(resolve, 100));

    // Task should NOT be in queue
    const tasks = await engine.getAvailableTasks();
    expect(tasks.length).toBe(0);

    // Task should be in Malformed folder
    const malformedFiles = await fs.readdir(malformedFolder);
    expect(malformedFiles).toContain('task_invalid_yaml.md');
  });

  it('should move task with missing frontmatter to Malformed folder', async () => {
    const taskContent = `# Task without Frontmatter

This task has no frontmatter at all.
`;

    await fs.writeFile(
      path.join(needsActionFolder, 'task_no_frontmatter.md'),
      taskContent
    );

    // Wait for file watcher to process
    await new Promise(resolve => setTimeout(resolve, 100));

    // Task should NOT be in queue
    const tasks = await engine.getAvailableTasks();
    expect(tasks.length).toBe(0);

    // Task should be in Malformed folder
    const malformedFiles = await fs.readdir(malformedFolder);
    expect(malformedFiles).toContain('task_no_frontmatter.md');
  });

  it('should handle multiple validation errors', async () => {
    const taskContent = `---
priority: invalid_priority
taskType: unregistered_type
---

# Task with Multiple Errors
`;

    await fs.writeFile(
      path.join(needsActionFolder, 'task_multiple_errors.md'),
      taskContent
    );

    // Wait for file watcher to process
    await new Promise(resolve => setTimeout(resolve, 100));

    // Task should NOT be in queue
    const tasks = await engine.getAvailableTasks();
    expect(tasks.length).toBe(0);

    // Task should be in Malformed folder
    const malformedFiles = await fs.readdir(malformedFolder);
    expect(malformedFiles).toContain('task_multiple_errors.md');
  });

  it('should accept valid tasks and reject invalid ones simultaneously', async () => {
    const validTask = `---
taskId: task_valid
priority: high
taskType: email_processing
---

# Valid Task
`;

    const invalidTask = `---
taskId: task_invalid
priority: invalid_priority
taskType: email_processing
---

# Invalid Task
`;

    await fs.writeFile(
      path.join(needsActionFolder, 'task_valid.md'),
      validTask
    );

    await fs.writeFile(
      path.join(needsActionFolder, 'task_invalid.md'),
      invalidTask
    );

    // Wait for file watcher to process
    await new Promise(resolve => setTimeout(resolve, 150));

    // Only valid task should be in queue
    const tasks = await engine.getAvailableTasks();
    expect(tasks.length).toBe(1);
    expect(tasks[0].taskId).toBe('task_valid');

    // Invalid task should be in Malformed folder
    const malformedFiles = await fs.readdir(malformedFolder);
    expect(malformedFiles).toContain('task_invalid.md');
    expect(malformedFiles).not.toContain('task_valid.md');
  });
});
