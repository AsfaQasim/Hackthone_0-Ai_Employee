/**
 * Assignment strategy enum for task assignment engine
 */

export type AssignmentStrategy = 
  | 'round-robin' 
  | 'priority-first' 
  | 'least-loaded' 
  | 'capability-match';

export function isValidAssignmentStrategy(strategy: string): strategy is AssignmentStrategy {
  return ['round-robin', 'priority-first', 'least-loaded', 'capability-match'].includes(strategy);
}
