# Implementation Plan: Gmail Watcher Agent Skill

## Overview

This implementation plan breaks down the Gmail Watcher Agent Skill into discrete, incremental coding tasks. The approach follows a bottom-up strategy: building core components first, then integrating them into the orchestrator. Each task builds on previous work, with property-based tests placed close to implementation to catch errors early.

The implementation uses TypeScript with the fast-check library for property-based testing.

## Current Status

No implementation exists yet. Starting from scratch with project setup.

## Tasks

- [x] 1. Set up project structure and dependencies
  - [x] 1.1 Initialize Node.js project with package.json
    - Run npm init
    - Set project name, version, description
    - _Requirements: All_
  
  - [x] 1.2 Create TypeScript configuration
    - Create tsconfig.json with strict mode
    - Configure output directory (dist/)
    - Configure source directory (src/)
    - Enable ES modules
    - _Requirements: All_
  
  - [x] 1.3 Install core dependencies
    - Install typescript, @types/node
    - Install js-yaml and @types/js-yaml (config parsing)
    - Install turndown (HTML to markdown)
    - _Requirements: 4.5, 8.1_
  
  - [x] 1.4 Install testing dependencies
    - Install vitest (test framework)
    - Install fast-check (property-based testing)
    - Install @types/turndown
    - _Requirements: All (for testing)_
  
  - [x] 1.5 Create directory structure
    - Create src/ directory
    - Create src/models/ directory
    - Create src/components/ directory
    - Create src/utils/ directory
    - Create tests/ directory
    - Create tests/arbitraries/ directory
    - _Requirements: All_
  
  - [x] 1.6 Configure test scripts
    - Add test scripts to package.json
    - Configure vitest.config.ts
    - _Requirements: All (for testing)_

- [x] 2. Implement core data models and types
  - [x] 2.1 Create TypeScript interfaces for core data models
    - Create src/models/Email.ts with Email and EmailAddress interfaces
    - Create src/models/Config.ts with WatcherConfig, ImportanceCriteria, PriorityRules, RateLimitConfig interfaces
    - Create src/models/ProcessedEmailIndex.ts with index types
    - Create src/models/LogEntry.ts with LogEntry and LogLevel types
    - Include validation type guards where needed
    - _Requirements: 1.3, 8.1_
  
  - [x] 2.2 Create custom error types
    - Create src/models/Errors.ts
    - Implement AuthenticationError class
    - Implement NetworkError class
    - Implement RateLimitError class
    - Implement APIError class
    - Implement ConfigurationError class
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
  
  - [ ]* 2.3 Write property test for email model validation
    - **Property 2: Complete Metadata Extraction**
    - **Validates: Requirements 1.3**
    - _Requirements: 1.3_

- [x] 3. Implement Configuration Manager
  - [x] 3.1 Create ConfigurationManager class
    - Create src/components/ConfigurationManager.ts
    - Implement loadConfig method (YAML/JSON parsing)
    - Implement validateConfig method
    - Implement getDefaultConfig method
    - Return default config on missing/malformed files
    - _Requirements: 8.1, 8.6, 8.7_
  
  - [ ]* 3.2 Write unit tests for configuration loading
    - Create tests/ConfigurationManager.test.ts
    - Test valid config file loading
    - Test missing config file (should use defaults)
    - Test malformed config file (should use defaults)
    - _Requirements: 8.1, 8.6, 8.7_
  
  - [ ]* 3.3 Write property test for configuration application
    - **Property 19: Configuration Application**
    - **Validates: Requirements 8.3, 8.4, 8.5**
    - _Requirements: 8.3, 8.4, 8.5_

- [x] 4. Implement Audit Logger
  - [x] 4.1 Create AuditLogger class
    - Create src/components/AuditLogger.ts
    - Implement info, warn, and error methods
    - Implement JSON Lines log format
    - Write to persistent log file
    - Include timestamp, level, message, context, and stack trace
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7_
  
  - [ ]* 4.2 Write unit tests for log file writing
    - Create tests/AuditLogger.test.ts
    - Test log file creation
    - Test log entry format
    - _Requirements: 7.6_
  
  - [ ]* 4.3 Write property test for log entry structure
    - **Property 18: Log Entry Structure**
    - **Validates: Requirements 7.7**
    - _Requirements: 7.7_
  
  - [ ]* 4.4 Write property test for comprehensive error logging
    - **Property 15: Comprehensive Error Logging**
    - **Validates: Requirements 5.6, 7.4**
    - _Requirements: 5.6, 7.4_

- [x] 5. Implement Duplicate Tracker
  - [x] 5.1 Create DuplicateTracker class
    - Create src/components/DuplicateTracker.ts
    - Implement isProcessed method
    - Implement markProcessed method
    - Implement rebuildIndex method
    - Implement JSON index file management
    - Implement index persistence
    - Implement index rebuild from markdown files
    - _Requirements: 10.1, 10.2, 10.4, 10.5_
  
  - [ ]* 5.2 Write unit tests for duplicate tracking
    - Create tests/DuplicateTracker.test.ts
    - Test index file creation
    - Test index rebuild from markdown files
    - _Requirements: 10.4, 10.5_
  
  - [ ]* 5.3 Write property test for duplicate detection
    - **Property 23: Duplicate Detection by Gmail ID**
    - **Validates: Requirements 10.1, 10.2**
    - _Requirements: 10.1, 10.2_

- [x] 6. Implement Email Filter
  - [x] 6.1 Create EmailFilter class
    - Create src/components/EmailFilter.ts
    - Implement isImportant method
    - Implement sender whitelist matching
    - Implement keyword pattern matching (case-insensitive)
    - Implement label matching
    - Implement OR logic for criteria combination
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_
  
  - [ ]* 6.2 Write property test for email filter criteria evaluation
    - Create tests/EmailFilter.test.ts
    - **Property 3: Email Filter Criteria Evaluation**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.6**
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.6_
  
  - [ ]* 6.3 Write property test for non-important email exclusion
    - **Property 4: Non-Important Email Exclusion**
    - **Validates: Requirements 2.5**
    - _Requirements: 2.5_

- [x] 7. Implement Priority Detector
  - [x] 7.1 Create PriorityDetector class
    - Create src/components/PriorityDetector.ts
    - Implement detectPriority method
    - Implement high-priority keyword detection
    - Implement VIP sender detection
    - Implement high-priority label detection
    - Implement medium/low priority fallback logic
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_
  
  - [ ]* 7.2 Write property test for priority level assignment
    - Create tests/PriorityDetector.test.ts
    - **Property 5: Priority Level Assignment**
    - **Validates: Requirements 3.1**
    - _Requirements: 3.1_
  
  - [ ]* 7.3 Write property test for high priority detection
    - **Property 6: High Priority Detection**
    - **Validates: Requirements 3.2, 3.3, 3.4**
    - _Requirements: 3.2, 3.3, 3.4_
  
  - [ ]* 7.4 Write property test for default priority assignment
    - **Property 7: Default Priority Assignment**
    - **Validates: Requirements 3.5**
    - _Requirements: 3.5_

- [-] 8. Implement Markdown Generator
  - [x] 8.1 Create MarkdownGenerator class
    - Create src/components/MarkdownGenerator.ts
    - Implement generateMarkdown method
    - Implement createFile method
    - Implement htmlToMarkdown method
    - Implement frontmatter generation with all required fields
    - Implement HTML to markdown conversion using turndown library
    - Implement filename generation with timestamp and sanitized subject
    - Implement file writing to Needs_Action folder
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_
  
  - [ ]* 8.2 Write unit tests for filename generation edge cases
    - Create tests/MarkdownGenerator.test.ts
    - Test special characters in subject
    - Test very long subjects
    - Test empty subjects
    - _Requirements: 4.4_
  
  - [ ]* 8.3 Write property test for markdown file creation
    - **Property 8: Markdown File Creation**
    - **Validates: Requirements 4.1**
    - _Requirements: 4.1_
  
  - [ ]* 8.4 Write property test for complete markdown content
    - **Property 9: Complete Markdown Content**
    - **Validates: Requirements 4.2, 4.3**
    - _Requirements: 4.2, 4.3_
  
  - [ ]* 8.5 Write property test for unique filename generation
    - **Property 10: Unique Filename Generation**
    - **Validates: Requirements 4.4**
    - _Requirements: 4.4_
  
  - [ ]* 8.6 Write property test for HTML to markdown conversion
    - **Property 11: HTML to Markdown Conversion Preservation**
    - **Validates: Requirements 4.5**
    - _Requirements: 4.5_

- [ ] 9. Checkpoint - Verify core components work independently
  - Run all tests to ensure components function correctly
  - Verify no compilation errors
  - Ask user if questions arise
  - _Requirements: All_

- [ ] 10. Implement Rate Limiter
  - [ ] 10.1 Create RateLimiter class
    - Create src/components/RateLimiter.ts
    - Implement checkLimit method
    - Implement recordRequest method
    - Implement handleRateLimitError method
    - Implement request counting per time window
    - Implement exponential backoff logic
    - Implement backoff ceiling (max 60 seconds)
    - Implement window reset logic
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  
  - [ ]* 10.2 Write unit tests for rate limit scenarios
    - Create tests/RateLimiter.test.ts
    - Test request delay when approaching limit
    - Test counter reset at window boundary
    - _Requirements: 6.2, 6.5_
  
  - [ ]* 10.3 Write property test for request count tracking
    - **Property 16: Request Count Tracking**
    - **Validates: Requirements 6.1**
    - _Requirements: 6.1_
  
  - [ ]* 10.4 Write property test for exponential backoff
    - **Property 13: Network Error Retry with Backoff**
    - **Validates: Requirements 5.2, 6.3, 6.4**
    - _Requirements: 5.2, 6.3, 6.4_

- [ ] 11. Implement MCP Client
  - [ ] 11.1 Create MCPClient class
    - Create src/components/MCPClient.ts
    - Implement authenticate method
    - Implement fetchUnreadEmails method
    - Implement refreshToken method
    - Implement OAuth 2.0 authentication flow
    - Implement MCP protocol request formatting
    - Implement MCP protocol response parsing
    - Implement automatic token refresh
    - Implement error code translation to internal error types
    - _Requirements: 1.1, 1.2, 9.1, 9.2, 9.3, 9.4, 9.5_
  
  - [ ]* 11.2 Write unit tests for authentication and token refresh
    - Create tests/MCPClient.test.ts
    - Test authentication flow
    - Test token refresh on expiration
    - _Requirements: 9.1, 9.4_
  
  - [ ]* 11.3 Write property test for MCP protocol request format
    - **Property 20: MCP Protocol Request Format**
    - **Validates: Requirements 9.2**
    - _Requirements: 9.2_
  
  - [ ]* 11.4 Write property test for MCP protocol response parsing
    - **Property 21: MCP Protocol Response Parsing**
    - **Validates: Requirements 9.3**
    - _Requirements: 9.3_
  
  - [ ]* 11.5 Write property test for MCP error code translation
    - **Property 22: MCP Error Code Translation**
    - **Validates: Requirements 9.5**
    - _Requirements: 9.5_

- [ ] 12. Implement error handling utilities
  - [ ] 12.1 Create error handling utility functions
    - Create src/utils/errorHandlers.ts
    - Implement authentication error handler (log and notify)
    - Implement network error handler (retry with backoff)
    - Implement rate limit error handler (pause and resume)
    - Implement API error handler (retry 5xx, skip 4xx)
    - Implement data validation error handler (log and skip)
    - Implement file system error handler (try fallback)
    - Implement configuration error handler (use defaults)
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
  
  - [ ]* 12.2 Write unit tests for specific error scenarios
    - Create tests/errorHandlers.test.ts
    - Test authentication error handling
    - Test rate limit error handling with retry-after
    - Test server error retry (exactly 3 attempts)
    - _Requirements: 5.1, 5.3, 5.4_
  
  - [ ]* 12.3 Write property test for malformed data handling
    - **Property 14: Malformed Data Handling**
    - **Validates: Requirements 5.5**
    - _Requirements: 5.5_

- [ ] 13. Checkpoint - Verify error handling works correctly
  - Run all tests to ensure error handling functions properly
  - Verify retry logic and backoff strategies
  - Ask user if questions arise
  - _Requirements: All_

- [ ] 14. Implement Gmail Watcher Orchestrator
  - [ ] 14.1 Create GmailWatcherOrchestrator class
    - Create src/components/GmailWatcherOrchestrator.ts
    - Implement start method
    - Implement stop method
    - Implement pollOnce method
    - Implement polling cycle coordination
    - Integrate all components (MCP Client, Email Filter, Priority Detector, Markdown Generator, etc.)
    - Implement workflow: retrieve → filter → prioritize → check duplicates → generate markdown → log
    - Implement polling interval management
    - Implement graceful shutdown
    - _Requirements: 1.1, 1.5, 2.1, 3.1, 4.1, 10.1_
  
  - [ ]* 14.2 Write property test for complete email retrieval
    - Create tests/GmailWatcherOrchestrator.test.ts
    - **Property 1: Complete Email Retrieval**
    - **Validates: Requirements 1.1**
    - _Requirements: 1.1_
  
  - [ ]* 14.3 Write property test for idempotent email processing
    - **Property 12: Idempotent Email Processing**
    - **Validates: Requirements 4.6, 10.3**
    - _Requirements: 4.6, 10.3_
  
  - [ ]* 14.4 Write property test for operation logging completeness
    - **Property 17: Operation Logging Completeness**
    - **Validates: Requirements 7.2, 7.3**
    - _Requirements: 7.2, 7.3_

- [ ] 15. Implement edge case handling
  - [ ] 15.1 Add empty inbox handling to orchestrator
    - Update GmailWatcherOrchestrator to handle empty inbox
    - Verify graceful handling when no emails returned
    - Log empty inbox event
    - _Requirements: 1.4_
  
  - [ ]* 15.2 Write unit test for empty inbox handling
    - Update tests/GmailWatcherOrchestrator.test.ts
    - Test empty inbox response
    - _Requirements: 1.4_

- [ ] 16. Create main entry point and CLI
  - [ ] 16.1 Create main entry point with CLI
    - Create src/main.ts
    - Implement CLI argument parsing
    - Support start/stop commands
    - Support one-time poll command
    - Load configuration from specified path
    - Initialize all components
    - Start orchestrator
    - _Requirements: All_
  
  - [ ]* 16.2 Write integration tests for end-to-end workflows
    - Create tests/integration.test.ts
    - Test full polling cycle with mocked Gmail API
    - Test error recovery scenarios
    - Test duplicate prevention
    - _Requirements: All_

- [ ] 17. Add comprehensive logging throughout all components
  - [ ] 17.1 Integrate AuditLogger throughout all components
    - Update all components to use AuditLogger
    - Add polling initiation logging
    - Add important email detection logging
    - Add markdown file creation logging
    - Add rate limit event logging
    - _Requirements: 7.1, 7.2, 7.3, 7.5_

- [ ] 18. Create test data generators (arbitraries)
  - [ ] 18.1 Create fast-check arbitraries for all data models
    - Create tests/arbitraries/emailArbitrary.ts
    - Create tests/arbitraries/importanceCriteriaArbitrary.ts
    - Create tests/arbitraries/priorityRulesArbitrary.ts
    - Create tests/arbitraries/configArbitrary.ts
    - Create tests/arbitraries/index.ts to export all arbitraries
    - _Requirements: All (for testing)_

- [ ] 19. Final checkpoint - Run all tests and verify integration
  - Run complete test suite
  - Verify all property tests pass with 100+ iterations
  - Verify all unit tests pass
  - Check code compiles without errors
  - Ask user if questions arise
  - _Requirements: All_

- [ ] 20. Create documentation
  - [ ] 20.1 Create README.md with setup and usage instructions
    - Create README.md in project root
    - Document installation steps
    - Document configuration file format
    - Document CLI commands
    - Document troubleshooting common issues
    - _Requirements: All_
  
  - [ ] 20.2 Create example configuration file
    - Create config.example.yaml
    - Include all configuration options documented
    - Include sensible example values
    - _Requirements: 8.1_
  
  - [ ] 20.3 Add build scripts to package.json
    - Add build script (tsc)
    - Add start script
    - Add dev script with watch mode
    - _Requirements: All_

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties (minimum 100 iterations each)
- Unit tests validate specific examples and edge cases
- The implementation follows TypeScript best practices with strong typing
- All property tests must include the tag format: `Feature: gmail-watcher-skill, Property {number}: {property_text}`
- Current status: No implementation exists yet - starting from project setup
