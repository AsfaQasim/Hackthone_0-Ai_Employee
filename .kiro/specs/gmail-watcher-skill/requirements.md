# Requirements Document: Gmail Watcher Agent Skill

## Introduction

The Gmail Watcher Agent Skill is a component of a Personal AI Employee system that monitors Gmail inboxes for important unread emails and creates actionable markdown files in an Obsidian vault. The skill operates within the Ralph Loop architecture (Perception → Reasoning → Action) and integrates with Gmail via the Model Context Protocol (MCP). It provides automatic priority detection, robust error handling, and maintains an audit trail of all operations.

## Glossary

- **Gmail_Watcher**: The skill component that monitors Gmail for important emails
- **MCP_Client**: The Model Context Protocol client that interfaces with Gmail API
- **Email_Filter**: The component that determines if an email is "important" based on criteria
- **Priority_Detector**: The component that assigns priority levels to emails
- **Markdown_Generator**: The component that creates markdown files from email data
- **Needs_Action_Folder**: The Obsidian vault folder where email markdown files are created
- **Rate_Limiter**: The component that manages API request rates and implements backoff
- **Audit_Logger**: The component that logs all operations for traceability
- **Important_Email**: An email that matches configured importance criteria
- **Priority_Level**: A classification of email urgency (high, medium, low)
- **Frontmatter**: YAML metadata at the top of markdown files
- **Backoff_Strategy**: A retry mechanism with increasing delays between attempts

## Requirements

### Requirement 1: Email Detection and Polling

**User Story:** As a user, I want the system to automatically detect unread important emails from my Gmail inbox, so that I can stay informed about critical communications without manually checking email.

#### Acceptance Criteria

1. WHEN the Gmail_Watcher polls the Gmail API, THE Gmail_Watcher SHALL retrieve all unread emails from the inbox
2. WHEN polling occurs, THE Gmail_Watcher SHALL use the MCP_Client to communicate with Gmail API
3. WHEN the Gmail API returns emails, THE Gmail_Watcher SHALL extract email metadata including sender, subject, date, labels, and content
4. WHEN polling is initiated, THE Gmail_Watcher SHALL handle empty inbox responses gracefully
5. THE Gmail_Watcher SHALL poll the Gmail API at configurable intervals

### Requirement 2: Email Importance Filtering

**User Story:** As a user, I want the system to filter emails based on importance criteria, so that only relevant emails create action items in my vault.

#### Acceptance Criteria

1. WHEN an email is retrieved, THE Email_Filter SHALL evaluate it against configured importance criteria
2. WHERE importance criteria include sender whitelist, THE Email_Filter SHALL mark emails from whitelisted senders as important
3. WHERE importance criteria include keyword matching, THE Email_Filter SHALL mark emails containing specified keywords as important
4. WHERE importance criteria include label matching, THE Email_Filter SHALL mark emails with specified Gmail labels as important
5. WHEN an email does not match any importance criteria, THE Email_Filter SHALL exclude it from processing
6. THE Email_Filter SHALL support multiple criteria types evaluated with OR logic

### Requirement 3: Priority Level Detection

**User Story:** As a user, I want emails to be automatically assigned priority levels, so that I can focus on the most urgent items first.

#### Acceptance Criteria

1. WHEN an Important_Email is identified, THE Priority_Detector SHALL assign a Priority_Level of high, medium, or low
2. WHERE an email contains urgent keywords (e.g., "urgent", "asap", "critical"), THE Priority_Detector SHALL assign high priority
3. WHERE an email is from a VIP sender, THE Priority_Detector SHALL assign high priority
4. WHERE an email has specific Gmail labels indicating importance, THE Priority_Detector SHALL assign high priority
5. WHEN no high-priority indicators are present, THE Priority_Detector SHALL assign medium or low priority based on secondary criteria
6. THE Priority_Detector SHALL use configurable rules for priority assignment

### Requirement 4: Markdown File Generation

**User Story:** As a user, I want important emails to be converted into markdown files with comprehensive metadata, so that I can review and act on them within my Obsidian vault.

#### Acceptance Criteria

1. WHEN an Important_Email is processed, THE Markdown_Generator SHALL create a markdown file in the Needs_Action_Folder
2. WHEN creating a markdown file, THE Markdown_Generator SHALL include Frontmatter with sender, subject, date, priority, and labels
3. WHEN creating a markdown file, THE Markdown_Generator SHALL include the email body content in markdown format
4. WHEN creating a markdown file, THE Markdown_Generator SHALL generate a unique filename based on timestamp and subject
5. WHEN an email contains HTML content, THE Markdown_Generator SHALL convert it to markdown format
6. WHEN a markdown file already exists for an email, THE Markdown_Generator SHALL not create a duplicate

### Requirement 5: Gmail API Error Handling

**User Story:** As a user, I want the system to handle Gmail API errors gracefully, so that temporary failures don't disrupt the monitoring process.

#### Acceptance Criteria

1. WHEN the Gmail API returns an authentication error, THE Gmail_Watcher SHALL log the error and notify the user
2. WHEN the Gmail API returns a network timeout error, THE Gmail_Watcher SHALL retry the request with exponential backoff
3. WHEN the Gmail API returns a rate limit error, THE Rate_Limiter SHALL pause requests and resume after the specified delay
4. WHEN the Gmail API returns a server error (5xx), THE Gmail_Watcher SHALL retry up to 3 times before logging failure
5. WHEN the Gmail API returns malformed data, THE Gmail_Watcher SHALL log the error and skip the problematic email
6. WHEN any error occurs, THE Audit_Logger SHALL record the error details with timestamp and context

### Requirement 6: Rate Limiting and Backoff

**User Story:** As a system administrator, I want the skill to respect Gmail API rate limits, so that the service remains available and doesn't get throttled.

#### Acceptance Criteria

1. THE Rate_Limiter SHALL track the number of API requests made within each time window
2. WHEN the request count approaches the rate limit, THE Rate_Limiter SHALL delay subsequent requests
3. WHEN a rate limit error is received, THE Rate_Limiter SHALL implement exponential backoff starting at 1 second
4. WHEN exponential backoff reaches maximum delay, THE Rate_Limiter SHALL maintain the maximum delay between retries
5. THE Rate_Limiter SHALL reset request counters when the rate limit window expires
6. THE Rate_Limiter SHALL use configurable rate limit thresholds

### Requirement 7: Audit Logging

**User Story:** As a user, I want all operations to be logged, so that I can audit the system's behavior and troubleshoot issues.

#### Acceptance Criteria

1. WHEN the Gmail_Watcher starts polling, THE Audit_Logger SHALL log the polling initiation with timestamp
2. WHEN an Important_Email is detected, THE Audit_Logger SHALL log the email metadata and assigned priority
3. WHEN a markdown file is created, THE Audit_Logger SHALL log the file path and email identifier
4. WHEN an error occurs, THE Audit_Logger SHALL log the error type, message, and stack trace
5. WHEN API rate limiting occurs, THE Audit_Logger SHALL log the rate limit event and backoff duration
6. THE Audit_Logger SHALL write logs to a persistent file in the vault
7. THE Audit_Logger SHALL include log levels (INFO, WARN, ERROR) for filtering

### Requirement 8: Configuration Management

**User Story:** As a user, I want to configure the skill's behavior through a configuration file, so that I can customize filtering and priority rules without modifying code.

#### Acceptance Criteria

1. THE Gmail_Watcher SHALL read configuration from a YAML or JSON file in the vault
2. WHERE configuration includes polling interval, THE Gmail_Watcher SHALL use the specified interval
3. WHERE configuration includes importance criteria, THE Email_Filter SHALL use the specified criteria
4. WHERE configuration includes priority rules, THE Priority_Detector SHALL use the specified rules
5. WHERE configuration includes rate limit thresholds, THE Rate_Limiter SHALL use the specified thresholds
6. WHEN the configuration file is missing, THE Gmail_Watcher SHALL use sensible default values
7. WHEN the configuration file is malformed, THE Gmail_Watcher SHALL log an error and use default values

### Requirement 9: MCP Integration

**User Story:** As a developer, I want the skill to integrate with Gmail via MCP, so that it follows the standard protocol for external service communication.

#### Acceptance Criteria

1. THE MCP_Client SHALL authenticate with Gmail API using OAuth 2.0 credentials
2. WHEN making API requests, THE MCP_Client SHALL use the MCP protocol format
3. WHEN receiving API responses, THE MCP_Client SHALL parse MCP protocol responses
4. WHEN authentication tokens expire, THE MCP_Client SHALL refresh tokens automatically
5. THE MCP_Client SHALL handle MCP-specific error codes and translate them to internal error types

### Requirement 10: Idempotency and Duplicate Prevention

**User Story:** As a user, I want the system to avoid creating duplicate markdown files for the same email, so that my vault remains organized and clutter-free.

#### Acceptance Criteria

1. WHEN processing an email, THE Gmail_Watcher SHALL check if a markdown file already exists for that email
2. WHEN checking for duplicates, THE Gmail_Watcher SHALL use the email's unique Gmail ID as the identifier
3. WHEN a duplicate is detected, THE Gmail_Watcher SHALL skip markdown file creation and log the skip event
4. THE Gmail_Watcher SHALL maintain a record of processed email IDs in a persistent index file
5. WHEN the index file is corrupted or missing, THE Gmail_Watcher SHALL rebuild it by scanning existing markdown files
