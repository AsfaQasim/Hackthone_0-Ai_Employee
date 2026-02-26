/**
 * Central export for all data models
 */

// Email models
export type { Email, EmailAddress } from './Email';
export { isValidEmail, isValidEmailAddress } from './Email';

// Configuration models
export type {
  WatcherConfig,
  ImportanceCriteria,
  PriorityRules,
  RateLimitConfig
} from './Config';
export {
  isValidWatcherConfig,
  isValidImportanceCriteria,
  isValidPriorityRules,
  isValidRateLimitConfig
} from './Config';

// Processed email index models
export type {
  ProcessedEmailIndex,
  ProcessedEmailEntry,
  PriorityLevel
} from './ProcessedEmailIndex';
export {
  isValidProcessedEmailIndex,
  isValidProcessedEmailEntry,
  isValidPriorityLevel
} from './ProcessedEmailIndex';

// Log entry models
export type { LogEntry, LogLevel } from './LogEntry';
export { isValidLogEntry, isValidLogLevel } from './LogEntry';

// Error types
export {
  AuthenticationError,
  NetworkError,
  RateLimitError,
  APIError,
  ConfigurationError
} from './Errors';
