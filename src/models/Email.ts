/**
 * Email data models for Gmail Watcher Agent Skill
 * Represents emails retrieved from Gmail via MCP
 */

/**
 * Email address with display name and email
 */
export interface EmailAddress {
  name: string;
  email: string;
}

/**
 * Email retrieved from Gmail
 */
export interface Email {
  id: string;                    // Gmail message ID (unique)
  threadId: string;              // Gmail thread ID
  sender: EmailAddress;          // Sender information
  subject: string;               // Email subject line
  date: Date;                    // Email sent date
  labels: string[];              // Gmail labels (e.g., "INBOX", "IMPORTANT")
  bodyHtml: string;              // HTML body content
  bodyText: string;              // Plain text body content
  snippet: string;               // Email preview snippet
}

/**
 * Type guard to validate Email object has all required fields
 */
export function isValidEmail(obj: any): obj is Email {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.id === 'string' &&
    typeof obj.threadId === 'string' &&
    isValidEmailAddress(obj.sender) &&
    typeof obj.subject === 'string' &&
    obj.date instanceof Date &&
    Array.isArray(obj.labels) &&
    obj.labels.every((label: any) => typeof label === 'string') &&
    typeof obj.bodyHtml === 'string' &&
    typeof obj.bodyText === 'string' &&
    typeof obj.snippet === 'string'
  );
}

/**
 * Type guard to validate EmailAddress object
 */
export function isValidEmailAddress(obj: any): obj is EmailAddress {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.name === 'string' &&
    typeof obj.email === 'string'
  );
}
