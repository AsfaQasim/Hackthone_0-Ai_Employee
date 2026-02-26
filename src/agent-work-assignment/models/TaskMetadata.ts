/**
 * Task metadata model for agent work assignment system
 */

export type TaskPriority = 'critical' | 'high' | 'medium' | 'low';

export interface TaskMetadata {
  taskId: string;
  priority: TaskPriority;
  taskType: string;
  requiredCapabilities: string[];
  createdAt: Date;
  claimedAt?: Date;
  claimedBy?: string;
  completedAt?: Date;
  reclaimCount: number;
  timeoutMinutes: number;
}

export function isValidTaskPriority(priority: string): priority is TaskPriority {
  return ['critical', 'high', 'medium', 'low'].includes(priority);
}

export function isValidTaskMetadata(obj: unknown): obj is TaskMetadata {
  if (typeof obj !== 'object' || obj === null) return false;
  
  const task = obj as Partial<TaskMetadata>;
  
  return (
    typeof task.taskId === 'string' &&
    typeof task.priority === 'string' &&
    isValidTaskPriority(task.priority) &&
    typeof task.taskType === 'string' &&
    Array.isArray(task.requiredCapabilities) &&
    task.requiredCapabilities.every(cap => typeof cap === 'string') &&
    task.createdAt instanceof Date &&
    (task.claimedAt === undefined || task.claimedAt instanceof Date) &&
    (task.claimedBy === undefined || typeof task.claimedBy === 'string') &&
    (task.completedAt === undefined || task.completedAt instanceof Date) &&
    typeof task.reclaimCount === 'number' &&
    typeof task.timeoutMinutes === 'number'
  );
}
