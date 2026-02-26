/**
 * Custom error types for Gmail Watcher Agent Skill
 * Defines specific error classes for different failure scenarios
 */

/**
 * Authentication error - OAuth token issues, expired credentials, insufficient permissions
 * Requires manual user intervention to resolve
 */
export class AuthenticationError extends Error {
  public readonly originalError?: Error;

  constructor(message: string, originalError?: Error) {
    super(message);
    this.name = 'AuthenticationError';
    this.originalError = originalError;
    
    // Maintains proper stack trace for where error was thrown (V8 only)
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, AuthenticationError);
    }
  }
}

/**
 * Network error - Connection timeouts, DNS failures, network unavailability
 * Should be retried with exponential backoff
 */
export class NetworkError extends Error {
  public readonly originalError?: Error;

  constructor(message: string, originalError?: Error) {
    super(message);
    this.name = 'NetworkError';
    this.originalError = originalError;
    
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, NetworkError);
    }
  }
}

/**
 * Rate limit error - Exceeding Gmail API quota limits
 * Should pause requests and resume after specified delay
 */
export class RateLimitError extends Error {
  public readonly retryAfter: number;
  public readonly originalError?: Error;

  constructor(message: string, retryAfter: number, originalError?: Error) {
    super(message);
    this.name = 'RateLimitError';
    this.retryAfter = retryAfter;
    this.originalError = originalError;
    
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, RateLimitError);
    }
  }
}

/**
 * API error - Invalid requests, server errors, service unavailability
 * 4xx errors should be skipped, 5xx errors should be retried
 */
export class APIError extends Error {
  public readonly statusCode: number;
  public readonly originalError?: Error;

  constructor(message: string, statusCode: number, originalError?: Error) {
    super(message);
    this.name = 'APIError';
    this.statusCode = statusCode;
    this.originalError = originalError;
    
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, APIError);
    }
  }
}

/**
 * Configuration error - Missing config file, invalid YAML/JSON, invalid values
 * Should fall back to default configuration
 */
export class ConfigurationError extends Error {
  public readonly validationErrors?: string[];

  constructor(message: string, validationErrors?: string[]) {
    super(message);
    this.name = 'ConfigurationError';
    this.validationErrors = validationErrors;
    
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, ConfigurationError);
    }
  }
}
