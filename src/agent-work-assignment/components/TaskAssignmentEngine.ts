/**
 * Task Assignment Engine Component
 * 
 * Monitors the Needs_Action folder for new tasks, maintains a priority queue,
 * and coordinates task assignment to agents based on configurable strategies.
 * 
 * Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 8.1, 8.2, 8.4, 8.5, 16.1, 16.2, 16.3, 16.4, 16.5
 */

import { promises as fs } from 'fs';
import * as fsSync from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import type { TaskMetadata, TaskPriority, AssignmentStrategy } from '../models';
import type { AgentRegistry } from './AgentRegistry';
import type { TaskRouter } from './TaskRouter';
import type { ClaimLockManager } from './ClaimLockManager';
import { TaskValidator, type TaskValidatorConfig } from './TaskValidator';
import { AuditLogger } from '../../components/AuditLogger';

export interface TaskAssignmentEngineConfig {
  needsActionFolder: string;
  malformedFolder?: string;
  defaultPriority?: TaskPriority;
  defaultTimeoutMinutes?: number;
  validatorConfig?: TaskValidatorConfig;
  logFolder?: string;
}

export class TaskAssignmentEngine {
  private config: TaskAssignmentEngineConfig;
  private agentRegistry: AgentRegistry;
  private taskRouter: TaskRouter;
  private claimLockManager: ClaimLockManager;
  private validator: TaskValidator;
  private logger: AuditLogger;
  
  private taskQueue: TaskMetadata[] = [];
  private watcher: fsSync.FSWatcher | null = null;
  private isWatching: boolean = false;
  private strategy: AssignmentStrategy = 'priority-first';
  private roundRobinIndex: number = 0; // Track round-robin position

  constructor(
    config: TaskAssignmentEngineConfig,
    agentRegistry: AgentRegistry,
    taskRouter: TaskRouter,
    claimLockManager: ClaimLockManager
  ) {
    this.config = config;
    this.agentRegistry = agentRegistry;
    this.taskRouter = taskRouter;
    this.claimLockManager = claimLockManager;
    // TaskId is not required in validation since we can extract it from filename
    const validatorConfig = {
      ...config.validatorConfig,
      requiredFields: config.validatorConfig?.requiredFields || []
    };
    this.validator = new TaskValidator(validatorConfig);
    this.logger = new AuditLogger(
      config.logFolder || '.logs',
      'task-assignment-engine.log'
    );
  }

  /**
   * Start watching the Needs_Action folder for new tasks
   * Requirements: 2.1
   */
  async startWatching(): Promise<void> {
    if (this.isWatching) {
      return;
    }

    // Ensure the Needs_Action folder exists
    await fs.mkdir(this.config.needsActionFolder, { recursive: true });

    // Ensure the Malformed folder exists if configured
    if (this.config.malformedFolder) {
      await fs.mkdir(this.config.malformedFolder, { recursive: true });
    }

    // Load existing tasks from the folder
    await this.loadExistingTasks();

    // Start watching for file system changes
    this.watcher = fsSync.watch(
      this.config.needsActionFolder,
      { persistent: true },
      async (eventType, filename) => {
        if (!filename || !filename.endsWith('.md')) {
          return;
        }

        try {
          if (eventType === 'rename' || eventType === 'change') {
            // Check if file exists (rename can mean add or delete)
            const filePath = path.join(this.config.needsActionFolder, filename);
            try {
              await fs.access(filePath);
              // File exists - it was added or modified
              await this.handleTaskAdded(filename);
            } catch {
              // File doesn't exist - it was removed
              await this.handleTaskRemoved(filename);
            }
          }
        } catch (error) {
          this.logger.error('Error handling file system event', error as Error, { filename });
        }
      }
    );

    this.isWatching = true;
  }

  /**
   * Stop watching the Needs_Action folder
   * Requirements: 2.1
   */
  async stopWatching(): Promise<void> {
    if (this.watcher) {
      this.watcher.close();
      this.watcher = null;
    }
    this.isWatching = false;
  }

  /**
   * Load existing tasks from the Needs_Action folder
   * Requirements: 2.1, 2.2
   */
  private async loadExistingTasks(): Promise<void> {
    try {
      const files = await fs.readdir(this.config.needsActionFolder);
      const taskFiles = files.filter(file => file.endsWith('.md'));

      for (const file of taskFiles) {
        await this.handleTaskAdded(file);
      }
    } catch (error) {
      console.error('Error loading existing tasks:', error);
    }
  }

  /**
   * Handle a task file being added to Needs_Action
   * Requirements: 2.1, 2.2, 18.2, 18.5
   */
  private async handleTaskAdded(filename: string): Promise<void> {
    const filePath = path.join(this.config.needsActionFolder, filename);
    
    try {
      // Read file content for validation
      const fileContent = await fs.readFile(filePath, 'utf-8');
      
      // Validate the task file
      const validationResult = this.validator.validateTaskFile(fileContent);
      
      if (!validationResult.valid) {
        // Task is malformed - move to Malformed folder and log errors
        await this.handleMalformedTask(filename, filePath, validationResult.errors);
        return;
      }
      
      // Parse task metadata
      const taskMetadata = await this.parseTaskFile(filePath);
      
      // Remove existing entry if present (in case of modification)
      this.taskQueue = this.taskQueue.filter(t => t.taskId !== taskMetadata.taskId);
      
      // Add to queue
      this.taskQueue.push(taskMetadata);
      
      // Re-sort queue by priority and timestamp
      this.sortTaskQueue();
      
      this.logger.info('Task added to queue', {
        taskId: taskMetadata.taskId,
        priority: taskMetadata.priority,
        taskType: taskMetadata.taskType
      });
    } catch (error) {
      this.logger.error('Error processing task file', error as Error, { filename });
      
      // If we have a malformed folder configured, move the file there
      if (this.config.malformedFolder) {
        try {
          await this.moveToMalformed(filename, filePath, `Parse error: ${(error as Error).message}`);
        } catch (moveError) {
          this.logger.error('Failed to move malformed task', moveError as Error, { filename });
        }
      }
    }
  }

  /**
   * Handle a malformed task by moving it to the Malformed folder
   * Requirements: 18.2, 18.5
   */
  private async handleMalformedTask(
    filename: string,
    filePath: string,
    errors: Array<{ field: string; message: string }>
  ): Promise<void> {
    const errorMessages = errors.map(e => `${e.field}: ${e.message}`).join('; ');
    
    this.logger.error('Task validation failed', new Error(errorMessages), {
      filename,
      validationErrors: errors
    });
    
    if (this.config.malformedFolder) {
      await this.moveToMalformed(filename, filePath, errorMessages);
    }
  }

  /**
   * Move a task file to the Malformed folder
   * Requirements: 18.2
   */
  private async moveToMalformed(filename: string, sourcePath: string, reason: string): Promise<void> {
    if (!this.config.malformedFolder) {
      return;
    }

    const destPath = path.join(this.config.malformedFolder, filename);
    
    try {
      // Ensure malformed folder exists
      await fs.mkdir(this.config.malformedFolder, { recursive: true });
      
      // Move the file
      await fs.rename(sourcePath, destPath);
      
      this.logger.warn('Task moved to Malformed folder', {
        filename,
        reason,
        destination: destPath
      });
    } catch (error) {
      this.logger.error('Failed to move task to Malformed folder', error as Error, {
        filename,
        sourcePath,
        destPath
      });
      throw error;
    }
  }

  /**
   * Handle a task file being removed from Needs_Action
   * Requirements: 2.4
   */
  private async handleTaskRemoved(filename: string): Promise<void> {
    // Extract taskId from filename (remove .md extension)
    const taskId = filename.replace(/\.md$/, '');
    
    // Remove from queue
    this.taskQueue = this.taskQueue.filter(t => t.taskId !== taskId);
  }

  /**
   * Parse a task file and extract metadata
   * Requirements: 2.2, 8.2
   */
  private async parseTaskFile(filePath: string): Promise<TaskMetadata> {
    const content = await fs.readFile(filePath, 'utf-8');
    
    // Extract frontmatter
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (!frontmatterMatch) {
      throw new Error('Task file missing frontmatter');
    }

    const frontmatter = yaml.load(frontmatterMatch[1]) as any;
    
    // Extract taskId from filename if not in frontmatter
    const filename = path.basename(filePath);
    const taskId = frontmatter.taskId || filename.replace(/\.md$/, '');
    
    // Requirement 8.2: Apply default priority if not specified
    const priority: TaskPriority = frontmatter.priority || this.config.defaultPriority || 'medium';
    
    // Parse dates
    const createdAt = frontmatter.createdAt ? new Date(frontmatter.createdAt) : new Date();
    const claimedAt = frontmatter.claimedAt ? new Date(frontmatter.claimedAt) : undefined;
    const completedAt = frontmatter.completedAt ? new Date(frontmatter.completedAt) : undefined;
    
    const taskMetadata: TaskMetadata = {
      taskId,
      priority,
      taskType: frontmatter.taskType || 'default',
      requiredCapabilities: frontmatter.requiredCapabilities || [],
      createdAt,
      claimedAt,
      claimedBy: frontmatter.claimedBy,
      completedAt,
      reclaimCount: frontmatter.reclaimCount || 0,
      timeoutMinutes: frontmatter.timeoutMinutes || this.config.defaultTimeoutMinutes || 30
    };

    return taskMetadata;
  }

  /**
   * Sort task queue by priority (critical > high > medium > low) then by timestamp (FIFO)
   * Requirements: 2.3, 8.1, 8.4
   */
  private sortTaskQueue(): void {
    const priorityOrder: Record<TaskPriority, number> = {
      critical: 4,
      high: 3,
      medium: 2,
      low: 1
    };

    this.taskQueue.sort((a, b) => {
      // First sort by priority (higher priority first)
      const priorityDiff = priorityOrder[b.priority] - priorityOrder[a.priority];
      if (priorityDiff !== 0) {
        return priorityDiff;
      }
      
      // Then sort by timestamp (earlier timestamp first - FIFO)
      return a.createdAt.getTime() - b.createdAt.getTime();
    });
  }

  /**
   * Get all available tasks in priority order
   * Requirements: 2.3
   */
  async getAvailableTasks(): Promise<TaskMetadata[]> {
    return [...this.taskQueue];
  }

  /**
   * Get tasks filtered by priority
   * Requirements: 8.1
   */
  async getTasksByPriority(priority: TaskPriority): Promise<TaskMetadata[]> {
    return this.taskQueue.filter(task => task.priority === priority);
  }

  /**
   * Set the assignment strategy
   * Requirements: 16.5
   */
  setStrategy(strategy: AssignmentStrategy): void {
    this.strategy = strategy;
  }

  /**
   * Get the current assignment strategy
   */
  getStrategy(): AssignmentStrategy {
    return this.strategy;
  }

  /**
   * Assign the next task to a specific agent
   * Requirements: 7.2, 9.1, 16.1
   */
  async assignNextTask(agentId: string): Promise<TaskMetadata | null> {
    // Check if agent has capacity
    if (!(await this.agentRegistry.hasCapacity(agentId))) {
      return null;
    }

    // Get eligible tasks for this agent
    const eligibleTasks: TaskMetadata[] = [];
    
    for (const task of this.taskQueue) {
      if (await this.taskRouter.canAgentHandleTask(agentId, task)) {
        // Check per-type capacity
        if (await this.agentRegistry.hasCapacityForType(agentId, task.taskType)) {
          eligibleTasks.push(task);
        }
      }
    }

    if (eligibleTasks.length === 0) {
      return null;
    }

    // Apply assignment strategy to select task
    const selectedTask = this.applyStrategy(eligibleTasks);
    if (!selectedTask) {
      return null;
    }

    // Attempt to claim the task
    const claimResult = await this.claimLockManager.attemptClaim(selectedTask.taskId, agentId);
    
    if (claimResult.success) {
      // Remove from queue since it's now claimed
      this.taskQueue = this.taskQueue.filter(t => t.taskId !== selectedTask.taskId);
      return selectedTask;
    }

    return null;
  }

  /**
   * Apply the current assignment strategy to select a task for a specific agent (pull model)
   * Requirements: 16.1, 16.2
   */
  private applyStrategy(eligibleTasks: TaskMetadata[]): TaskMetadata | null {
    if (eligibleTasks.length === 0) {
      return null;
    }

    switch (this.strategy) {
      case 'priority-first':
        // Tasks are already sorted by priority, return first
        return eligibleTasks[0];
      
      case 'round-robin':
        // For agent pull model, round-robin doesn't apply directly
        // Just return highest priority task
        return eligibleTasks[0];
      
      case 'least-loaded':
        // For agent pull model, the agent is already requesting
        // Just return highest priority task
        return eligibleTasks[0];
      
      case 'capability-match':
        // Return task that best matches agent capabilities
        // For now, return first eligible task
        return eligibleTasks[0];
      
      default:
        return eligibleTasks[0];
    }
  }

  /**
   * Assign a specific task to the best agent based on current strategy (push model)
   * Requirements: 16.1, 16.2, 16.3, 16.4
   */
  async assignTaskToAgent(task: TaskMetadata): Promise<string | null> {
    // Get eligible agents for this task
    const eligibleAgentIds = await this.taskRouter.getEligibleAgents(task);
    
    if (eligibleAgentIds.length === 0) {
      return null;
    }

    // Filter agents by capacity
    const availableAgents: string[] = [];
    for (const agentId of eligibleAgentIds) {
      if (await this.agentRegistry.hasCapacity(agentId) &&
          await this.agentRegistry.hasCapacityForType(agentId, task.taskType)) {
        availableAgents.push(agentId);
      }
    }

    if (availableAgents.length === 0) {
      return null;
    }

    // Apply strategy to select agent
    const selectedAgent = await this.selectAgentByStrategy(task, availableAgents);
    if (!selectedAgent) {
      return null;
    }

    // Attempt to claim the task for the selected agent
    const claimResult = await this.claimLockManager.attemptClaim(task.taskId, selectedAgent);
    
    if (claimResult.success) {
      // Remove from queue since it's now claimed
      this.taskQueue = this.taskQueue.filter(t => t.taskId !== task.taskId);
      return selectedAgent;
    }

    return null;
  }

  /**
   * Select an agent based on the current assignment strategy
   * Requirements: 16.1, 16.2, 16.3, 16.4
   */
  private async selectAgentByStrategy(_task: TaskMetadata, eligibleAgents: string[]): Promise<string | null> {
    if (eligibleAgents.length === 0) {
      return null;
    }

    switch (this.strategy) {
      case 'priority-first':
        // For push model, priority-first means we process high priority tasks first
        // Agent selection can use any method, we'll use first eligible
        return eligibleAgents[0];
      
      case 'round-robin':
        // Requirement 16.1: Distribute tasks evenly across agents
        const selectedAgent = eligibleAgents[this.roundRobinIndex % eligibleAgents.length];
        this.roundRobinIndex++;
        return selectedAgent;
      
      case 'least-loaded':
        // Requirement 16.4: Assign to agent with fewest current tasks
        let minWorkload = Infinity;
        let leastLoadedAgent: string | null = null;
        
        for (const agentId of eligibleAgents) {
          const workload = await this.agentRegistry.getAgentWorkload(agentId);
          if (workload < minWorkload) {
            minWorkload = workload;
            leastLoadedAgent = agentId;
          }
        }
        
        return leastLoadedAgent;
      
      case 'capability-match':
        // Requirement 16.3: Assign to most specialized agent
        // Most specialized = agent with fewest capabilities that still matches
        let minCapabilities = Infinity;
        let mostSpecializedAgent: string | null = null;
        
        for (const agentId of eligibleAgents) {
          const agentMetadata = await this.agentRegistry.getAgentStatus(agentId);
          if (agentMetadata.capabilities.length < minCapabilities) {
            minCapabilities = agentMetadata.capabilities.length;
            mostSpecializedAgent = agentId;
          }
        }
        
        return mostSpecializedAgent;
      
      default:
        return eligibleAgents[0];
    }
  }

  /**
   * Notify agents of a critical priority task
   * Requirements: 8.5
   */
  async notifyAgentsOfTask(task: TaskMetadata): Promise<void> {
    // This is a placeholder for notification logic
    // In a real implementation, this would send notifications to agents
    // For now, we just log the notification
    if (task.priority === 'critical') {
      const eligibleAgents = await this.taskRouter.getEligibleAgents(task);
      console.log(`Critical task ${task.taskId} available for agents: ${eligibleAgents.join(', ')}`);
    }
  }
}
