/**
 * Log entry data models for audit logging
 * Defines log entry structure and levels
 */

/**
 * Log severity levels
 */
export type LogLevel = 'INFO' | 'WARN' | 'ERROR';

/**
 * Log entry structure
 */
export interface LogEntry {
  timestamp: Date;               // When log entry was created
  level: LogLevel;               // Log severity level
  message: string;               // Log message
  context?: object;              // Additional context data
  stackTrace?: string;           // Error stack trace (for errors)
}

/**
 * Type guard to validate LogLevel
 */
export function isValidLogLevel(value: any): value is LogLevel {
  return value === 'INFO' || value === 'WARN' || value === 'ERROR';
}

/**
 * Type guard to validate LogEntry
 */
export function isValidLogEntry(obj: any): obj is LogEntry {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    obj.timestamp instanceof Date &&
    isValidLogLevel(obj.level) &&
    typeof obj.message === 'string' &&
    (obj.context === undefined || typeof obj.context === 'object') &&
    (obj.stackTrace === undefined || typeof obj.stackTrace === 'string')
  );
}
