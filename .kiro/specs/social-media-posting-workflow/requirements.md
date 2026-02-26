# Requirements Document: Social Media Posting Workflow

## Introduction

This document specifies the requirements for an automated social media posting workflow that integrates with the AI Employee system. The workflow enables business goal-driven content generation using Claude AI, human-in-the-loop approval, and automated posting to social media platforms via MCP (Model Context Protocol) servers.

The system follows the Ralph Loop architecture (Perception → Reasoning → Action) and operates within an Obsidian vault structure with designated folders for workflow stages.

## Glossary

- **System**: The social media posting workflow automation system
- **Claude_API**: The Claude AI service used for content generation
- **MCP_Server**: Model Context Protocol server that handles social media platform integrations
- **Business_Goal**: A markdown file containing content requirements, target audience, and posting objectives
- **Post_Draft**: Generated social media content stored in a markdown file with frontmatter metadata
- **Approval_File**: A Post_Draft located in the Pending_Approval folder awaiting human review
- **Approved_Post**: A Post_Draft that has been moved to the Approved folder by a human reviewer
- **Platform**: A social media service (Twitter, LinkedIn, Facebook, Instagram, etc.)
- **Vault**: The Obsidian vault directory structure containing all workflow folders
- **Frontmatter**: YAML metadata at the top of markdown files containing post configuration
- **Post_Template**: A predefined structure for specific post types (announcement, promotion, thought leadership, etc.)
- **Audit_Logger**: Component that records all system actions and state changes
- **File_Watcher**: Component that monitors folder changes to detect approvals

## Requirements

### Requirement 1: Business Goal Ingestion

**User Story:** As a content manager, I want to define business goals and content requirements in a structured format, so that the system can generate appropriate social media posts.

#### Acceptance Criteria

1. WHEN a Business_Goal file is created in the Needs_Action folder, THE System SHALL parse the file and extract content requirements
2. THE System SHALL validate that Business_Goal files contain required fields: objective, target_audience, key_messages, and platforms
3. WHEN a Business_Goal file is missing required fields, THE System SHALL log an error and move the file to a validation_failed subfolder
4. THE System SHALL support multiple platforms specified in a single Business_Goal file
5. WHEN parsing Business_Goal frontmatter, THE System SHALL extract scheduling preferences, tone guidelines, and character limits

### Requirement 2: AI Content Generation

**User Story:** As a content manager, I want Claude AI to generate social media posts based on business goals, so that I can save time while maintaining quality content.

#### Acceptance Criteria

1. WHEN a valid Business_Goal is processed, THE System SHALL send a generation request to Claude_API with the extracted requirements
2. THE System SHALL include platform-specific constraints (character limits, hashtag conventions, formatting rules) in the Claude_API request
3. WHEN Claude_API returns generated content, THE System SHALL create a Post_Draft file with the content and metadata
4. THE System SHALL generate platform-specific variations when multiple platforms are specified in the Business_Goal
5. WHEN Claude_API fails to respond within 30 seconds, THE System SHALL retry up to 3 times with exponential backoff
6. WHEN all retry attempts fail, THE System SHALL log the error and move the Business_Goal to a generation_failed subfolder

### Requirement 3: Post Draft Creation

**User Story:** As a content manager, I want generated posts to be saved in a structured format with metadata, so that I can review and track them effectively.

#### Acceptance Criteria

1. WHEN creating a Post_Draft, THE System SHALL generate a unique identifier for the post
2. THE System SHALL populate frontmatter with: post_id, created_date, target_platform, status, business_goal_reference, and scheduled_time
3. THE System SHALL save Post_Draft files to the Pending_Approval folder with naming format: `{platform}_{timestamp}_{post_id}.md`
4. THE System SHALL preserve the original Business_Goal reference in the Post_Draft metadata
5. WHEN generating multiple platform variations, THE System SHALL create separate Post_Draft files linked to the same Business_Goal

### Requirement 4: Human Approval Workflow

**User Story:** As a content manager, I want to review and approve generated posts before they are published, so that I can ensure quality and brand alignment.

#### Acceptance Criteria

1. WHEN a Post_Draft is created in Pending_Approval, THE System SHALL notify the user via log entry
2. WHEN a human moves a Post_Draft from Pending_Approval to Approved, THE File_Watcher SHALL detect the change within 5 seconds
3. WHEN a Post_Draft is moved to Approved, THE System SHALL validate that the file structure and required metadata are intact
4. THE System SHALL support rejection by moving files to a Rejected subfolder
5. WHEN a Post_Draft is in Pending_Approval for more than 24 hours, THE System SHALL log a reminder notification

### Requirement 5: Post Scheduling

**User Story:** As a content manager, I want to schedule posts for optimal posting times, so that I can maximize engagement.

#### Acceptance Criteria

1. WHEN an Approved_Post contains a scheduled_time in frontmatter, THE System SHALL queue the post for publishing at that time
2. THE System SHALL validate that scheduled_time is in the future and in ISO 8601 format
3. WHEN scheduled_time is not specified, THE System SHALL post immediately after approval
4. THE System SHALL maintain a queue of scheduled posts sorted by scheduled_time
5. WHEN the current time matches or exceeds a post's scheduled_time, THE System SHALL trigger the posting process

### Requirement 6: MCP Social Media Integration

**User Story:** As a content manager, I want the system to automatically post approved content to social media platforms, so that I don't have to manually publish each post.

#### Acceptance Criteria

1. WHEN an Approved_Post is ready for publishing, THE System SHALL send the post content and metadata to the appropriate MCP_Server endpoint
2. THE System SHALL authenticate with MCP_Server using credentials from the ConfigurationManager
3. WHEN MCP_Server successfully posts content, THE System SHALL update the Post_Draft status to "published" and move it to the Done folder
4. WHEN MCP_Server returns an error, THE System SHALL log the error and retry up to 3 times with 60-second intervals
5. WHEN all posting attempts fail, THE System SHALL move the post to a posting_failed subfolder and log the failure
6. THE System SHALL support multiple MCP_Server endpoints for different platforms (Twitter, LinkedIn, Facebook, Instagram)

### Requirement 7: Platform-Specific Formatting

**User Story:** As a content manager, I want posts to be formatted correctly for each platform, so that they display properly and meet platform requirements.

#### Acceptance Criteria

1. WHEN generating content for Twitter, THE System SHALL enforce a 280-character limit
2. WHEN generating content for LinkedIn, THE System SHALL support up to 3000 characters and professional formatting
3. WHEN generating content for Instagram, THE System SHALL include hashtag recommendations and support caption formatting
4. THE System SHALL validate character counts before sending to MCP_Server
5. WHEN a post exceeds platform limits, THE System SHALL log an error and move the post to a validation_failed subfolder

### Requirement 8: Post Template Support

**User Story:** As a content manager, I want to use predefined templates for common post types, so that I can maintain consistency and speed up content creation.

#### Acceptance Criteria

1. THE System SHALL load Post_Template files from a templates directory on startup
2. WHEN a Business_Goal specifies a template name, THE System SHALL apply that template structure to the generated content
3. THE System SHALL support template variables that are replaced with Business_Goal values
4. WHEN a specified template does not exist, THE System SHALL log a warning and proceed with default generation
5. THE System SHALL validate that templates contain required sections for the target platform

### Requirement 9: Error Handling and Retry Logic

**User Story:** As a system administrator, I want robust error handling and retry mechanisms, so that temporary failures don't result in lost posts.

#### Acceptance Criteria

1. WHEN any API call fails, THE System SHALL log the error with full context (timestamp, operation, error message, request details)
2. THE System SHALL implement exponential backoff for Claude_API retries: 1s, 2s, 4s
3. THE System SHALL implement fixed interval retries for MCP_Server posting: 60s between attempts
4. WHEN a file operation fails, THE System SHALL retry up to 3 times before logging a fatal error
5. THE System SHALL maintain operation state to prevent duplicate posts after recovery from failures

### Requirement 10: Audit Trail and Logging

**User Story:** As a system administrator, I want comprehensive logging of all workflow actions, so that I can troubleshoot issues and maintain accountability.

#### Acceptance Criteria

1. WHEN any workflow state change occurs, THE System SHALL log the event using Audit_Logger
2. THE System SHALL log: Business_Goal processing, content generation requests, approval actions, posting attempts, and errors
3. THE System SHALL include in each log entry: timestamp, operation type, file references, user actions, and outcome
4. THE System SHALL write logs to the Logs folder with daily rotation
5. WHEN a post is successfully published, THE System SHALL create a summary log entry with all workflow stages and timestamps

### Requirement 11: Post Tracking and Analytics

**User Story:** As a content manager, I want to track post performance and workflow metrics, so that I can optimize my content strategy.

#### Acceptance Criteria

1. WHEN a post is published, THE System SHALL record the post_id, platform, published_time, and Business_Goal reference
2. THE System SHALL maintain a tracking file that links Business_Goals to all generated and published posts
3. THE System SHALL calculate and log workflow metrics: time from goal to draft, time from draft to approval, time from approval to publish
4. WHEN querying post history, THE System SHALL support filtering by platform, date range, and Business_Goal
5. THE System SHALL store tracking data in a structured format (JSON or YAML) for easy analysis

### Requirement 12: Multi-Platform Coordination

**User Story:** As a content manager, I want to coordinate posts across multiple platforms, so that I can execute cohesive multi-channel campaigns.

#### Acceptance Criteria

1. WHEN a Business_Goal specifies multiple platforms, THE System SHALL generate coordinated content variations for each platform
2. THE System SHALL support cross-platform scheduling where all variations are posted at the same time
3. THE System SHALL link all platform variations to the same Business_Goal in tracking data
4. WHEN one platform posting fails, THE System SHALL continue posting to other platforms and log the partial failure
5. THE System SHALL support platform-specific overrides in Business_Goal files (different messages or timing per platform)

### Requirement 13: Configuration Management

**User Story:** As a system administrator, I want to configure system behavior and credentials centrally, so that I can manage the system efficiently.

#### Acceptance Criteria

1. THE System SHALL load configuration from ConfigurationManager on startup
2. THE System SHALL support configuration of: Claude_API credentials, MCP_Server endpoints, retry limits, timeout values, and folder paths
3. WHEN configuration is invalid or missing, THE System SHALL log an error and refuse to start
4. THE System SHALL support hot-reloading of configuration without system restart for non-critical settings
5. THE System SHALL validate that all required MCP_Server endpoints are configured before processing posts

### Requirement 14: Duplicate Detection

**User Story:** As a content manager, I want the system to prevent duplicate posts, so that I don't accidentally publish the same content multiple times.

#### Acceptance Criteria

1. WHEN creating a Post_Draft, THE System SHALL check if similar content has been posted within the last 30 days
2. THE System SHALL use content hash comparison to detect exact duplicates
3. WHEN a duplicate is detected, THE System SHALL log a warning and add a duplicate_warning flag to the Post_Draft frontmatter
4. THE System SHALL allow human override of duplicate warnings during the approval process
5. THE System SHALL integrate with DuplicateTracker component for duplicate detection logic

### Requirement 15: File Watcher Integration

**User Story:** As a system administrator, I want the system to automatically detect file changes, so that approvals are processed without manual intervention.

#### Acceptance Criteria

1. WHEN the System starts, THE File_Watcher SHALL monitor the Pending_Approval and Approved folders
2. THE File_Watcher SHALL detect file additions, moves, and deletions within 5 seconds
3. WHEN a file is moved to Approved, THE File_Watcher SHALL trigger the posting workflow
4. WHEN a file is deleted from Pending_Approval, THE File_Watcher SHALL log the deletion and update tracking data
5. THE File_Watcher SHALL handle multiple simultaneous file changes without race conditions
