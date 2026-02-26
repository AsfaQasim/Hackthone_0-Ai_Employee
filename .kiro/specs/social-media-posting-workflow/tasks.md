# Implementation Plan: Social Media Posting Workflow

## Overview

This implementation plan breaks down the social media posting workflow into incremental coding tasks. The workflow integrates with Claude AI for content generation and MCP servers for multi-platform publishing, following the Ralph Loop architecture within an Obsidian vault structure.

The implementation follows a bottom-up approach: core data models and utilities first, then individual components, then integration and workflow orchestration.

## Tasks

- [ ] 1. Set up project structure and core types
  - Create directory structure for components, models, and tests
  - Define TypeScript interfaces for GoalData, PostDraft, Platform, and error types
  - Set up fast-check for property-based testing
  - Configure test framework with 100 iterations for property tests
  - _Requirements: All requirements (foundation)_

- [ ] 2. Implement GoalParser component
  - [ ] 2.1 Implement markdown parsing and frontmatter extraction
    - Write parse() method to read markdown files and extract YAML frontmatter
    - Write validate() method to check required fields
    - Handle file reading errors and malformed YAML
    - _Requirements: 1.1, 1.2, 1.5_
  
  - [ ]* 2.2 Write property test for Business Goal parsing completeness
    - **Property 1: Business Goal Parsing Completeness**
    - **Validates: Requirements 1.1, 1.5**
  
  - [ ]* 2.3 Write property test for Business Goal validation enforcement
    - **Property 2: Business Goal Validation Enforcement**
    - **Validates: Requirements 1.2, 1.3**
  
  - [ ]* 2.4 Write property test for Business Goal serialization round-trip
    - **Property 39: Business Goal Serialization Round-Trip**
    - **Validates: Requirements 1.1, 1.5**
  
  - [ ]* 2.5 Write unit tests for GoalParser edge cases
    - Test empty files, missing frontmatter, invalid YAML
    - Test special characters in content
    - _Requirements: 1.1, 1.2, 1.3_

- [ ] 3. Implement platform constraints and validation
  - [ ] 3.1 Create PLATFORM_CONSTRAINTS configuration
    - Define character limits, hashtag rules, and formatting requirements for each platform
    - Implement getPlatformConstraints() utility function
    - _Requirements: 2.2, 7.1, 7.2, 7.3_
  
  - [ ] 3.2 Implement character count validation
    - Write validateCharacterCount() function
    - Handle platform-specific limits
    - _Requirements: 7.4, 7.5_
  
  - [ ]* 3.3 Write property test for character count validation
    - **Property 17: Character Count Validation**
    - **Validates: Requirements 7.4, 7.5**

- [ ] 4. Implement ContentGenerator component
  - [ ] 4.1 Create Claude API client wrapper
    - Implement API request formatting with platform constraints
    - Handle authentication using ConfigurationManager
    - Implement timeout handling (30 seconds)
    - _Requirements: 2.1, 2.2_
  
  - [ ] 4.2 Implement retry logic with exponential backoff
    - Write retry wrapper with 1s, 2s, 4s backoff intervals
    - Limit to 3 retry attempts
    - Log each retry attempt
    - _Requirements: 2.5, 2.6, 9.2_
  
  - [ ]* 4.3 Write property test for exponential backoff retry pattern
    - **Property 6: Exponential Backoff Retry Pattern**
    - **Validates: Requirements 2.5, 2.6, 9.2**
  
  - [ ] 4.4 Implement template loading and variable substitution
    - Load templates from templates directory
    - Implement applyTemplate() with variable replacement
    - Handle missing templates with fallback
    - _Requirements: 8.1, 8.2, 8.3, 8.4_
  
  - [ ]* 4.5 Write property test for template variable substitution
    - **Property 18: Template Variable Substitution**
    - **Validates: Requirements 8.2, 8.3**
  
  - [ ]* 4.6 Write property test for platform constraints application
    - **Property 4: Platform Constraints Application**
    - **Validates: Requirements 2.2**
  
  - [ ]* 4.7 Write unit tests for ContentGenerator
    - Test specific platform examples (Twitter, LinkedIn)
    - Test template application with real templates
    - Test API error scenarios
    - _Requirements: 2.1, 2.2, 2.3, 8.2_

- [ ] 5. Checkpoint - Ensure parsing and generation tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Implement PostDraftCreator component
  - [ ] 6.1 Implement unique post ID generation
    - Generate UUIDs for post_id
    - Ensure uniqueness across system
    - _Requirements: 3.1_
  
  - [ ]* 6.2 Write property test for post ID uniqueness
    - **Property 7: Post ID Uniqueness**
    - **Validates: Requirements 3.1**
  
  - [ ] 6.3 Implement Post_Draft creation and serialization
    - Create PostDraft objects with all required frontmatter fields
    - Serialize to markdown format with YAML frontmatter
    - Generate filenames following {platform}_{timestamp}_{post_id}.md pattern
    - _Requirements: 3.2, 3.3, 3.4_
  
  - [ ]* 6.4 Write property test for Post Draft creation from generated content
    - **Property 5: Post Draft Creation from Generated Content**
    - **Validates: Requirements 2.3, 3.2, 3.4**
  
  - [ ]* 6.5 Write property test for Post Draft file naming convention
    - **Property 8: Post Draft File Naming Convention**
    - **Validates: Requirements 3.3**
  
  - [ ]* 6.6 Write property test for Post Draft serialization round-trip
    - **Property 40: Post Draft Serialization Round-Trip**
    - **Validates: Requirements 3.2, 3.4**
  
  - [ ] 6.7 Integrate with DuplicateTracker for duplicate detection
    - Implement checkDuplicate() using content hash comparison
    - Check last 30 days of posts
    - Add duplicate_warning flag when detected
    - _Requirements: 14.1, 14.2, 14.3_
  
  - [ ]* 6.8 Write property test for content hash duplicate detection
    - **Property 35: Content Hash Duplicate Detection**
    - **Validates: Requirements 14.2**
  
  - [ ]* 6.9 Write property test for duplicate warning flagging
    - **Property 36: Duplicate Warning Flagging**
    - **Validates: Requirements 14.1, 14.3**

- [ ] 7. Implement SchedulerQueue component
  - [ ] 7.1 Create priority queue data structure
    - Implement enqueue() to add posts sorted by scheduled_time
    - Implement getNextDue() to retrieve posts where scheduled_time <= now
    - Implement remove() to remove posts by post_id
    - _Requirements: 5.1, 5.4, 5.5_
  
  - [ ]* 7.2 Write property test for scheduler queue ordering invariant
    - **Property 10: Scheduler Queue Ordering Invariant**
    - **Validates: Requirements 5.4**
  
  - [ ] 7.3 Implement scheduled time validation
    - Validate ISO 8601 format
    - Verify future timestamps
    - _Requirements: 5.2_
  
  - [ ]* 7.4 Write property test for scheduled time validation
    - **Property 12: Scheduled Time Validation**
    - **Validates: Requirements 5.2**
  
  - [ ]* 7.5 Write property test for immediate vs scheduled posting
    - **Property 11: Immediate vs Scheduled Posting**
    - **Validates: Requirements 5.1, 5.3, 5.5**

- [ ] 8. Implement MCPClient component
  - [ ] 8.1 Create MCP Server HTTP client
    - Implement post() method to send HTTP requests to MCP endpoints
    - Implement authenticate() using ConfigurationManager credentials
    - Implement getEndpoint() for platform-specific URLs
    - _Requirements: 6.1, 6.2, 6.6_
  
  - [ ]* 8.2 Write property test for MCP authentication consistency
    - **Property 13: MCP Authentication Consistency**
    - **Validates: Requirements 6.2**
  
  - [ ]* 8.3 Write property test for platform endpoint routing
    - **Property 16: Platform Endpoint Routing**
    - **Validates: Requirements 6.6**
  
  - [ ]* 8.4 Write unit tests for MCPClient
    - Test authentication with mock credentials
    - Test endpoint routing for each platform
    - Test error responses from MCP Server
    - _Requirements: 6.1, 6.2, 6.6_

- [ ] 9. Implement PostPublisher component
  - [ ] 9.1 Implement publish() method
    - Send post to MCPClient
    - Handle successful responses
    - Update post status and move to Done folder
    - _Requirements: 6.1, 6.3_
  
  - [ ]* 9.2 Write property test for successful post status update
    - **Property 14: Successful Post Status Update**
    - **Validates: Requirements 6.3**
  
  - [ ] 9.3 Implement retry logic with fixed intervals
    - Retry failed posts with 60-second intervals
    - Limit to 3 retry attempts
    - Move to posting_failed after exhausting retries
    - _Requirements: 6.4, 6.5, 9.3_
  
  - [ ]* 9.4 Write property test for fixed interval retry pattern
    - **Property 15: Fixed Interval Retry Pattern**
    - **Validates: Requirements 6.4, 6.5, 9.3**
  
  - [ ]* 9.5 Write unit tests for PostPublisher
    - Test successful publishing flow
    - Test retry scenarios with mock failures
    - Test file movement to Done and posting_failed
    - _Requirements: 6.3, 6.4, 6.5_

- [ ] 10. Checkpoint - Ensure core components tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Implement FileWatcher component
  - [ ] 11.1 Set up file system watching
    - Use chokidar or similar library to watch folders
    - Monitor Needs_Action, Pending_Approval, and Approved folders
    - Implement debouncing for rapid changes (5 second window)
    - _Requirements: 15.1, 15.2_
  
  - [ ] 11.2 Implement event handlers
    - Handle file added events
    - Handle file moved events
    - Handle file deleted events
    - Emit FileEvent objects with type, path, and timestamp
    - _Requirements: 15.2, 15.3, 15.4_
  
  - [ ]* 11.3 Write property test for file watcher event triggering
    - **Property 37: File Watcher Event Triggering**
    - **Validates: Requirements 15.3**
  
  - [ ]* 11.4 Write property test for file deletion tracking
    - **Property 38: File Deletion Tracking**
    - **Validates: Requirements 15.4**
  
  - [ ]* 11.5 Write unit tests for FileWatcher
    - Test detection timing with real file operations
    - Test debouncing with rapid changes
    - Test concurrent file changes
    - _Requirements: 15.1, 15.2, 15.5_

- [ ] 12. Implement tracking and metrics
  - [ ] 12.1 Create tracking data structure
    - Define tracking JSON schema
    - Implement functions to create and update tracking data
    - Link Business_Goals to all generated posts
    - _Requirements: 11.1, 11.2_
  
  - [ ]* 12.2 Write property test for post tracking data completeness
    - **Property 26: Post Tracking Data Completeness**
    - **Validates: Requirements 11.1, 11.2**
  
  - [ ] 12.3 Implement workflow metrics calculation
    - Calculate time from goal to draft
    - Calculate time from draft to approval
    - Calculate time from approval to publish
    - _Requirements: 11.3_
  
  - [ ]* 12.4 Write property test for workflow metrics calculation
    - **Property 27: Workflow Metrics Calculation**
    - **Validates: Requirements 11.3**
  
  - [ ] 12.5 Implement post history query with filtering
    - Support filtering by platform, date range, and Business_Goal
    - Return matching posts from tracking data
    - _Requirements: 11.4_
  
  - [ ]* 12.6 Write property test for post history query filtering
    - **Property 28: Post History Query Filtering**
    - **Validates: Requirements 11.4**
  
  - [ ]* 12.7 Write property test for tracking data format validity
    - **Property 29: Tracking Data Format Validity**
    - **Validates: Requirements 11.5**
  
  - [ ]* 12.8 Write property test for tracking data serialization round-trip
    - **Property 41: Tracking Data Serialization Round-Trip**
    - **Validates: Requirements 11.5**

- [ ] 13. Implement WorkflowManager orchestration
  - [ ] 13.1 Implement processNewGoal() workflow
    - Parse Business_Goal using GoalParser
    - Generate content for each platform using ContentGenerator
    - Create Post_Drafts using PostDraftCreator
    - Save drafts to Pending_Approval folder
    - Log workflow state changes
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.3, 3.1, 3.2, 3.3_
  
  - [ ]* 13.2 Write property test for multi-platform generation completeness
    - **Property 3: Multi-Platform Generation Completeness**
    - **Validates: Requirements 1.4, 2.4, 3.5, 12.1, 12.3**
  
  - [ ] 13.3 Implement processApproval() workflow
    - Validate approved Post_Draft
    - Check for scheduled_time
    - Queue scheduled posts or publish immediately
    - Update tracking data
    - Log workflow state changes
    - _Requirements: 4.3, 5.1, 5.3, 5.5, 6.1_
  
  - [ ]* 13.4 Write property test for approval workflow file validation
    - **Property 9: Approval Workflow File Validation**
    - **Validates: Requirements 4.3**
  
  - [ ] 13.5 Implement error handling and recovery
    - Handle validation errors with file movement
    - Handle API errors with retry logic
    - Handle file operation errors with retry
    - Maintain operation state for idempotent recovery
    - _Requirements: 9.1, 9.4, 9.5_
  
  - [ ]* 13.6 Write property test for idempotent failure recovery
    - **Property 22: Idempotent Failure Recovery**
    - **Validates: Requirements 9.5**
  
  - [ ]* 13.7 Write property test for file operation retry resilience
    - **Property 21: File Operation Retry Resilience**
    - **Validates: Requirements 9.4**

- [ ] 14. Implement logging and audit trail
  - [ ] 14.1 Integrate with AuditLogger component
    - Log all workflow state changes
    - Log all API calls and responses
    - Log all errors with full context
    - _Requirements: 10.1, 10.2, 10.3_
  
  - [ ]* 14.2 Write property test for comprehensive error logging
    - **Property 23: Comprehensive Error Logging**
    - **Validates: Requirements 9.1, 10.1**
  
  - [ ]* 14.3 Write property test for workflow state change logging
    - **Property 24: Workflow State Change Logging**
    - **Validates: Requirements 10.2, 10.3**
  
  - [ ] 14.4 Implement summary logging for published posts
    - Create summary log entries with all workflow stages
    - Include timestamps for each stage
    - _Requirements: 10.5_
  
  - [ ]* 14.5 Write property test for published post summary logging
    - **Property 25: Published Post Summary Logging**
    - **Validates: Requirements 10.5**
  
  - [ ]* 14.6 Write unit tests for logging
    - Test log entry format
    - Test daily log rotation
    - Test log file creation
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [ ] 15. Checkpoint - Ensure workflow orchestration tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 16. Implement multi-platform coordination
  - [ ] 16.1 Implement cross-platform scheduling synchronization
    - Ensure all platform variations have same scheduled_time when no overrides
    - Handle platform-specific overrides
    - _Requirements: 12.2, 12.5_
  
  - [ ]* 16.2 Write property test for cross-platform scheduling synchronization
    - **Property 30: Cross-Platform Scheduling Synchronization**
    - **Validates: Requirements 12.2**
  
  - [ ]* 16.3 Write property test for platform override application
    - **Property 32: Platform Override Application**
    - **Validates: Requirements 12.5**
  
  - [ ] 16.4 Implement partial failure isolation
    - Continue posting to remaining platforms when one fails
    - Log partial failures
    - Update tracking data for successful and failed posts
    - _Requirements: 12.4_
  
  - [ ]* 16.5 Write property test for partial failure isolation
    - **Property 31: Partial Failure Isolation**
    - **Validates: Requirements 12.4**
  
  - [ ]* 16.6 Write unit tests for multi-platform coordination
    - Test synchronized posting across platforms
    - Test partial failure scenarios
    - Test platform-specific overrides
    - _Requirements: 12.2, 12.4, 12.5_

- [ ] 17. Implement configuration management
  - [ ] 17.1 Define configuration schema
    - Claude_API credentials
    - MCP_Server endpoints for all platforms
    - Retry limits and timeout values
    - Folder paths
    - _Requirements: 13.2_
  
  - [ ] 17.2 Implement configuration validation
    - Validate required fields on startup
    - Validate MCP_Server endpoints for all platforms
    - Refuse to start with invalid configuration
    - _Requirements: 13.3, 13.5_
  
  - [ ]* 17.3 Write property test for configuration validation on startup
    - **Property 33: Configuration Validation on Startup**
    - **Validates: Requirements 13.3, 13.5**
  
  - [ ]* 17.4 Write property test for configuration completeness
    - **Property 34: Configuration Completeness**
    - **Validates: Requirements 13.2**
  
  - [ ]* 17.5 Write unit tests for configuration management
    - Test loading valid configuration
    - Test invalid configuration scenarios
    - Test hot-reloading for non-critical settings
    - _Requirements: 13.1, 13.2, 13.3, 13.4_

- [ ] 18. Implement template system
  - [ ] 18.1 Create template loader
    - Load templates from templates directory on startup
    - Parse template structure and variables
    - _Requirements: 8.1_
  
  - [ ] 18.2 Implement template validation
    - Validate templates contain required sections for target platform
    - Handle missing templates with warnings
    - _Requirements: 8.4, 8.5_
  
  - [ ]* 18.3 Write property test for missing template fallback
    - **Property 19: Missing Template Fallback**
    - **Validates: Requirements 8.4**
  
  - [ ]* 18.4 Write property test for template platform validation
    - **Property 20: Template Platform Validation**
    - **Validates: Requirements 8.5**
  
  - [ ]* 18.5 Write unit tests for template system
    - Test template loading on startup
    - Test template validation
    - Test variable substitution with real templates
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 19. Integration and system startup
  - [ ] 19.1 Implement WorkflowManager start() and stop()
    - Initialize all components
    - Load configuration
    - Load templates
    - Start FileWatcher
    - Set up graceful shutdown
    - _Requirements: All requirements (system initialization)_
  
  - [ ] 19.2 Wire FileWatcher events to WorkflowManager
    - Connect file added events to processNewGoal()
    - Connect file moved events to processApproval()
    - Connect file deleted events to tracking updates
    - _Requirements: 15.3, 15.4_
  
  - [ ] 19.3 Wire SchedulerQueue to PostPublisher
    - Poll queue for due posts
    - Trigger publishing for due posts
    - Handle immediate posting for posts without scheduled_time
    - _Requirements: 5.1, 5.3, 5.5_
  
  - [ ]* 19.4 Write integration tests for end-to-end workflow
    - Test Business_Goal → Draft → Approval → Publishing (happy path)
    - Test multi-platform coordination with partial failures
    - Test retry and recovery scenarios
    - Test duplicate detection and override workflow
    - Test template application workflow
    - Test scheduled posting workflow
    - _Requirements: All requirements (integration)_

- [ ] 20. Final checkpoint - Ensure all tests pass
  - Run all unit tests
  - Run all property-based tests (100 iterations each)
  - Run all integration tests
  - Verify test coverage meets 80%+ target
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- Property tests validate universal correctness properties with 100 iterations
- Unit tests validate specific examples, edge cases, and integration points
- The implementation follows a bottom-up approach: data models → components → orchestration → integration
