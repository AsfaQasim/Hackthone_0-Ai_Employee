/**
 * Processed email index data models
 * Tracks processed emails to prevent duplicates
 */

/**
 * Priority level for emails
 */
export type PriorityLevel = 'high' | 'medium' | 'low';

/**
 * Entry for a processed email
 */
export interface ProcessedEmailEntry {
  filename: string;              // Generated markdown filename
  processedAt: Date;             // When email was processed
  priority: PriorityLevel;       // Assigned priority level
}

/**
 * Index of processed emails
 * Maps email ID to processed email entry
 */
export interface ProcessedEmailIndex {
  [emailId: string]: ProcessedEmailEntry;
}

/**
 * Type guard to validate PriorityLevel
 */
export function isValidPriorityLevel(value: any): value is PriorityLevel {
  return value === 'high' || value === 'medium' || value === 'low';
}

/**
 * Type guard to validate ProcessedEmailEntry
 */
export function isValidProcessedEmailEntry(obj: any): obj is ProcessedEmailEntry {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.filename === 'string' &&
    obj.processedAt instanceof Date &&
    isValidPriorityLevel(obj.priority)
  );
}

/**
 * Type guard to validate ProcessedEmailIndex
 */
export function isValidProcessedEmailIndex(obj: any): obj is ProcessedEmailIndex {
  if (typeof obj !== 'object' || obj === null) {
    return false;
  }
  
  for (const key in obj) {
    if (!isValidProcessedEmailEntry(obj[key])) {
      return false;
    }
  }
  
  return true;
}
