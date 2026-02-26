/**
 * ClaimLockManager - Manages atomic file operations for task claiming
 * 
 * Provides lock mechanisms to prevent race conditions when multiple agents
 * attempt to claim the same task simultaneously.
 * 
 * Requirements: 3.1, 3.2, 4.1, 4.3, 4.4, 4.5
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { ClaimResult } from '../models';

export interface ClaimLockManagerConfig {
  lockDirectory: string;
  maxLockDurationSeconds: number;
  needsActionFolder: string;
  inProgressFolder: string;
  retryAttempts?: number;
  retryBackoffMs?: number[];
}

export class ClaimLockManager {
  private lockDirectory: string;
  private needsActionFolder: string;
  private inProgressFolder: string;
  private retryAttempts: number;
  private retryBackoffMs: number[];

  constructor(config: ClaimLockManagerConfig) {
    this.lockDirectory = config.lockDirectory;
    this.needsActionFolder = config.needsActionFolder;
    this.inProgressFolder = config.inProgressFolder;
    this.retryAttempts = config.retryAttempts ?? 3;
    this.retryBackoffMs = config.retryBackoffMs ?? [100, 500, 1000];
  }

  /**
   * Initialize the lock manager by ensuring the lock directory exists
   */
  async initialize(): Promise<void> {
    await fs.mkdir(this.lockDirectory, { recursive: true });
  }

  /**
   * Acquire a lock for a specific task
   * Uses file system atomic operations to prevent race conditions
   * 
   * @param taskId - The ID of the task to lock
   * @returns true if lock was acquired, false if already locked
   */
  async acquireLock(taskId: string): Promise<boolean> {
    const lockFilePath = this.getLockFilePath(taskId);
    
    try {
      // Use 'wx' flag for atomic create-if-not-exists operation
      // This will fail if the file already exists
      const lockData = {
        taskId,
        acquiredAt: new Date().toISOString(),
        pid: process.pid
      };
      
      await fs.writeFile(
        lockFilePath,
        JSON.stringify(lockData, null, 2),
        { flag: 'wx' }
      );
      
      return true;
    } catch (error: any) {
      // EEXIST means the lock file already exists (lock is held)
      if (error.code === 'EEXIST') {
        return false;
      }
      // Other errors should be thrown
      throw error;
    }
  }

  /**
   * Release a lock for a specific task
   * 
   * @param taskId - The ID of the task to unlock
   */
  async releaseLock(taskId: string): Promise<void> {
    const lockFilePath = this.getLockFilePath(taskId);
    
    try {
      await fs.unlink(lockFilePath);
    } catch (error: any) {
      // Ignore ENOENT errors (lock file doesn't exist)
      if (error.code !== 'ENOENT') {
        throw error;
      }
    }
  }

  /**
   * Release all stale locks older than the specified duration
   * This prevents locks from being held indefinitely if a process crashes
   * 
   * @param seconds - Age threshold in seconds
   * @returns Number of stale locks released
   */
  async releaseStaleLocksOlderThan(seconds: number): Promise<number> {
    const thresholdMs = seconds * 1000;
    const now = Date.now();
    let releasedCount = 0;

    try {
      const lockFiles = await fs.readdir(this.lockDirectory);
      
      for (const lockFile of lockFiles) {
        if (!lockFile.endsWith('.lock')) {
          continue;
        }
        
        const lockFilePath = path.join(this.lockDirectory, lockFile);
        
        try {
          const lockContent = await fs.readFile(lockFilePath, 'utf-8');
          const lockData = JSON.parse(lockContent);
          
          const acquiredAt = new Date(lockData.acquiredAt).getTime();
          const age = now - acquiredAt;
          
          if (age > thresholdMs) {
            await fs.unlink(lockFilePath);
            releasedCount++;
          }
        } catch (error: any) {
          // If we can't read or parse the lock file, it's corrupted
          // Remove it to prevent it from blocking forever
          if (error.code !== 'ENOENT') {
            await fs.unlink(lockFilePath).catch(() => {});
            releasedCount++;
          }
        }
      }
    } catch (error: any) {
      // If the lock directory doesn't exist, no locks to release
      if (error.code !== 'ENOENT') {
        throw error;
      }
    }

    return releasedCount;
  }

  /**
   * Get the file path for a task's lock file
   */
  private getLockFilePath(taskId: string): string {
    // Sanitize taskId to prevent path traversal
    const sanitizedTaskId = taskId.replace(/[^a-zA-Z0-9_-]/g, '_');
    return path.join(this.lockDirectory, `${sanitizedTaskId}.lock`);
  }

  /**
   * Check if a task is currently locked
   * 
   * @param taskId - The ID of the task to check
   * @returns true if the task is locked
   */
  async isLocked(taskId: string): Promise<boolean> {
    const lockFilePath = this.getLockFilePath(taskId);
    
    try {
      await fs.access(lockFilePath);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Attempt to claim a task atomically with retry logic
   * Moves task from Needs_Action to In_Progress/<agentId> and updates frontmatter
   * 
   * Requirements: 3.1, 3.2, 4.1, 4.5
   * 
   * @param taskId - The ID of the task to claim (filename without extension)
   * @param agentId - The ID of the agent claiming the task
   * @returns ClaimResult indicating success or failure
   */
  async attemptClaim(taskId: string, agentId: string): Promise<ClaimResult> {
    let lastError: string | undefined;

    // Retry logic with exponential backoff
    for (let attempt = 0; attempt < this.retryAttempts; attempt++) {
      try {
        // Try to acquire lock
        const lockAcquired = await this.acquireLock(taskId);
        
        if (!lockAcquired) {
          lastError = 'Failed to acquire lock - task may be claimed by another agent';
          
          // Wait before retrying (exponential backoff)
          if (attempt < this.retryAttempts - 1) {
            const backoffMs = this.retryBackoffMs[attempt] ?? this.retryBackoffMs[this.retryBackoffMs.length - 1];
            await this.sleep(backoffMs);
            continue;
          }
          break;
        }

        try {
          // Perform atomic claim operation
          const result = await this.performAtomicClaim(taskId, agentId);
          
          // Release lock after successful claim
          await this.releaseLock(taskId);
          
          return result;
        } catch (error: any) {
          // Release lock on error
          await this.releaseLock(taskId);
          throw error;
        }
      } catch (error: any) {
        lastError = error.message || 'Unknown error during claim operation';
        
        // Wait before retrying (exponential backoff)
        if (attempt < this.retryAttempts - 1) {
          const backoffMs = this.retryBackoffMs[attempt] ?? this.retryBackoffMs[this.retryBackoffMs.length - 1];
          await this.sleep(backoffMs);
        }
      }
    }

    // All retry attempts failed
    return {
      success: false,
      taskId,
      agentId,
      error: lastError || 'Failed to claim task after all retry attempts'
    };
  }

  /**
   * Perform the atomic claim operation
   * Moves task file and updates frontmatter
   * 
   * @param taskId - The ID of the task to claim
   * @param agentId - The ID of the agent claiming the task
   * @returns ClaimResult indicating success or failure
   */
  private async performAtomicClaim(taskId: string, agentId: string): Promise<ClaimResult> {
    const taskFileName = `${taskId}.md`;
    const sourcePath = path.join(this.needsActionFolder, taskFileName);
    const agentInProgressFolder = path.join(this.inProgressFolder, agentId);
    const destinationPath = path.join(agentInProgressFolder, taskFileName);

    // Check if source file exists
    try {
      await fs.access(sourcePath);
    } catch {
      return {
        success: false,
        taskId,
        agentId,
        error: 'Task file not found in Needs_Action folder'
      };
    }

    // Ensure agent's In_Progress folder exists
    await fs.mkdir(agentInProgressFolder, { recursive: true });

    // Read task file content
    let fileContent: string;
    try {
      fileContent = await fs.readFile(sourcePath, 'utf-8');
    } catch (error: any) {
      return {
        success: false,
        taskId,
        agentId,
        error: `Failed to read task file: ${error.message}`
      };
    }

    // Update frontmatter with claim metadata
    const updatedContent = this.updateFrontmatter(fileContent, {
      claimedAt: new Date().toISOString(),
      claimedBy: agentId,
      status: 'in_progress'
    });

    // Write updated content to destination
    try {
      await fs.writeFile(destinationPath, updatedContent, 'utf-8');
    } catch (error: any) {
      return {
        success: false,
        taskId,
        agentId,
        error: `Failed to write task file to destination: ${error.message}`
      };
    }

    // Atomically remove source file (this completes the "move")
    try {
      await fs.unlink(sourcePath);
    } catch (error: any) {
      // If we can't remove the source, we need to clean up the destination
      await fs.unlink(destinationPath).catch(() => {});
      return {
        success: false,
        taskId,
        agentId,
        error: `Failed to remove source file: ${error.message}`
      };
    }

    return {
      success: true,
      taskId,
      agentId
    };
  }

  /**
   * Update YAML frontmatter in a markdown file
   * 
   * @param content - The original file content
   * @param updates - Key-value pairs to update in frontmatter
   * @returns Updated file content with modified frontmatter
   */
  private updateFrontmatter(content: string, updates: Record<string, any>): string {
    const frontmatterRegex = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/;
    const match = content.match(frontmatterRegex);

    if (!match) {
      // No frontmatter exists, create it
      const frontmatterLines = Object.entries(updates).map(
        ([key, value]) => `${key}: ${this.formatYamlValue(value)}`
      );
      return `---\n${frontmatterLines.join('\n')}\n---\n${content}`;
    }

    const [, frontmatterContent, bodyContent] = match;
    const frontmatterLines = frontmatterContent.split('\n');
    
    // Parse existing frontmatter into a map
    const frontmatterMap = new Map<string, string>();
    for (const line of frontmatterLines) {
      const colonIndex = line.indexOf(':');
      if (colonIndex > 0) {
        const key = line.substring(0, colonIndex).trim();
        const value = line.substring(colonIndex + 1).trim();
        frontmatterMap.set(key, value);
      }
    }

    // Apply updates
    for (const [key, value] of Object.entries(updates)) {
      frontmatterMap.set(key, this.formatYamlValue(value));
    }

    // Reconstruct frontmatter
    const updatedFrontmatterLines = Array.from(frontmatterMap.entries()).map(
      ([key, value]) => `${key}: ${value}`
    );

    return `---\n${updatedFrontmatterLines.join('\n')}\n---\n${bodyContent}`;
  }

  /**
   * Format a value for YAML frontmatter
   * 
   * @param value - The value to format
   * @returns Formatted string for YAML
   */
  private formatYamlValue(value: any): string {
    if (typeof value === 'string') {
      // Quote strings if they contain special characters
      if (value.includes(':') || value.includes('#') || value.includes('\n')) {
        return `"${value.replace(/"/g, '\\"')}"`;
      }
      return value;
    }
    if (typeof value === 'number' || typeof value === 'boolean') {
      return String(value);
    }
    if (Array.isArray(value)) {
      return `[${value.map(v => this.formatYamlValue(v)).join(', ')}]`;
    }
    return JSON.stringify(value);
  }

  /**
   * Sleep for a specified duration
   * 
   * @param ms - Duration in milliseconds
   */
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Release a claimed task back to Needs_Action
   * Moves task from In_Progress/<agentId> to Needs_Action and clears claim metadata
   * 
   * Requirements: 13.1, 13.2, 15.3
   * 
   * @param taskId - The ID of the task to release
   * @param agentId - The ID of the agent releasing the task
   */
  async releaseClaim(taskId: string, agentId: string): Promise<void> {
    const taskFileName = `${taskId}.md`;
    const sourcePath = path.join(this.inProgressFolder, agentId, taskFileName);
    const destinationPath = path.join(this.needsActionFolder, taskFileName);

    // Check if source file exists
    try {
      await fs.access(sourcePath);
    } catch {
      throw new Error(`Task file not found in agent's In_Progress folder: ${sourcePath}`);
    }

    // Read task file content
    const fileContent = await fs.readFile(sourcePath, 'utf-8');

    // Clear claim metadata from frontmatter
    const updatedContent = this.clearClaimMetadata(fileContent);

    // Write updated content to destination
    await fs.writeFile(destinationPath, updatedContent, 'utf-8');

    // Remove source file
    await fs.unlink(sourcePath);
  }

  /**
   * Clear claim metadata from frontmatter
   * 
   * @param content - The original file content
   * @returns Updated file content with claim metadata removed
   */
  private clearClaimMetadata(content: string): string {
    const frontmatterRegex = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/;
    const match = content.match(frontmatterRegex);

    if (!match) {
      return content;
    }

    const [, frontmatterContent, bodyContent] = match;
    const frontmatterLines = frontmatterContent.split('\n');
    
    // Parse existing frontmatter and remove claim-related fields
    const frontmatterMap = new Map<string, string>();
    for (const line of frontmatterLines) {
      const colonIndex = line.indexOf(':');
      if (colonIndex > 0) {
        const key = line.substring(0, colonIndex).trim();
        const value = line.substring(colonIndex + 1).trim();
        
        // Skip claim-related fields
        if (key !== 'claimedAt' && key !== 'claimedBy' && key !== 'status') {
          frontmatterMap.set(key, value);
        }
      }
    }

    // Reconstruct frontmatter
    const updatedFrontmatterLines = Array.from(frontmatterMap.entries()).map(
      ([key, value]) => `${key}: ${value}`
    );

    return `---\n${updatedFrontmatterLines.join('\n')}\n---\n${bodyContent}`;
  }
}
