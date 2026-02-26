/**
 * Configuration data models for Gmail Watcher Agent Skill
 * Defines all configuration structures for the skill
 */

/**
 * Importance criteria for filtering emails
 */
export interface ImportanceCriteria {
  senderWhitelist: string[];     // Email addresses to always include
  keywordPatterns: string[];     // Keywords to match in subject/body
  requiredLabels: string[];      // Gmail labels to match
  logicMode: 'OR' | 'AND';       // How to combine criteria
}

/**
 * Priority detection rules
 */
export interface PriorityRules {
  highPriorityKeywords: string[];    // Keywords indicating high priority
  vipSenders: string[];              // VIP email addresses
  highPriorityLabels: string[];      // Labels indicating high priority
  mediumPriorityKeywords: string[];  // Keywords indicating medium priority
}

/**
 * Rate limiting configuration
 */
export interface RateLimitConfig {
  maxRequestsPerMinute: number;      // Per-minute request limit
  maxRequestsPerDay: number;         // Per-day request limit
  initialBackoffMs: number;          // Initial backoff delay
  maxBackoffMs: number;              // Maximum backoff delay
  backoffMultiplier: number;         // Backoff multiplier
}

/**
 * Complete watcher configuration
 */
export interface WatcherConfig {
  pollingIntervalMs: number;                 // Polling frequency in milliseconds
  importanceCriteria: ImportanceCriteria;    // Email filtering rules
  priorityRules: PriorityRules;              // Priority detection rules
  rateLimitConfig: RateLimitConfig;          // Rate limiting settings
  needsActionFolder: string;                 // Target folder for markdown files
  logFolder: string;                         // Log file location
}

/**
 * Type guard to validate ImportanceCriteria
 */
export function isValidImportanceCriteria(obj: any): obj is ImportanceCriteria {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    Array.isArray(obj.senderWhitelist) &&
    obj.senderWhitelist.every((s: any) => typeof s === 'string') &&
    Array.isArray(obj.keywordPatterns) &&
    obj.keywordPatterns.every((k: any) => typeof k === 'string') &&
    Array.isArray(obj.requiredLabels) &&
    obj.requiredLabels.every((l: any) => typeof l === 'string') &&
    (obj.logicMode === 'OR' || obj.logicMode === 'AND')
  );
}

/**
 * Type guard to validate PriorityRules
 */
export function isValidPriorityRules(obj: any): obj is PriorityRules {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    Array.isArray(obj.highPriorityKeywords) &&
    obj.highPriorityKeywords.every((k: any) => typeof k === 'string') &&
    Array.isArray(obj.vipSenders) &&
    obj.vipSenders.every((s: any) => typeof s === 'string') &&
    Array.isArray(obj.highPriorityLabels) &&
    obj.highPriorityLabels.every((l: any) => typeof l === 'string') &&
    Array.isArray(obj.mediumPriorityKeywords) &&
    obj.mediumPriorityKeywords.every((k: any) => typeof k === 'string')
  );
}

/**
 * Type guard to validate RateLimitConfig
 */
export function isValidRateLimitConfig(obj: any): obj is RateLimitConfig {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.maxRequestsPerMinute === 'number' &&
    obj.maxRequestsPerMinute > 0 &&
    typeof obj.maxRequestsPerDay === 'number' &&
    obj.maxRequestsPerDay > 0 &&
    typeof obj.initialBackoffMs === 'number' &&
    obj.initialBackoffMs > 0 &&
    typeof obj.maxBackoffMs === 'number' &&
    obj.maxBackoffMs > 0 &&
    typeof obj.backoffMultiplier === 'number' &&
    obj.backoffMultiplier > 1
  );
}

/**
 * Type guard to validate WatcherConfig
 */
export function isValidWatcherConfig(obj: any): obj is WatcherConfig {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.pollingIntervalMs === 'number' &&
    obj.pollingIntervalMs > 0 &&
    isValidImportanceCriteria(obj.importanceCriteria) &&
    isValidPriorityRules(obj.priorityRules) &&
    isValidRateLimitConfig(obj.rateLimitConfig) &&
    typeof obj.needsActionFolder === 'string' &&
    typeof obj.logFolder === 'string'
  );
}
