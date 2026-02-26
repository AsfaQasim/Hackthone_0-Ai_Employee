# Requirements Document: AI Employee System

## Introduction

The AI Employee System is a progressive, tier-based autonomous assistant platform that monitors multiple communication channels, processes information through an Obsidian knowledge base, and executes actions through MCP servers with human-in-the-loop approval workflows. The system is designed to be built incrementally across four tiers (Bronze, Silver, Gold, Platinum), each adding more sophisticated capabilities while maintaining security, auditability, and reliability.

## Glossary

- **System**: The AI Employee System as a whole
- **Watcher**: A monitoring script that observes external data sources (Gmail, WhatsApp, file system, social media)
- **Vault**: The Obsidian knowledge base containing markdown files organized in structured folders
- **MCP_Server**: Model Context Protocol server that enables external actions (email sending, accounting, social media posting)
- **Claude_Code**: The AI reasoning engine that reads from and writes to the Vault
- **Orchestrator**: The master Python process that coordinates Watchers, reasoning loops, and MCP servers
- **Ralph_Wiggum_Loop**: The autonomous multi-step task completion reasoning pattern
- **Approval_Workflow**: File-based human-in-the-loop process for sensitive actions
- **Agent_Skill**: A discrete capability or function that the AI can perform
- **Work_Zone**: Cloud or Local execution environment with specific responsibilities
- **Odoo**: Open-source accounting and business management system (Community Edition)

## Requirements

### Requirement 1: Obsidian Vault Knowledge Base

**User Story:** As a system architect, I want a structured Obsidian vault as the central knowledge repository, so that all system components can share state and information through markdown files.

#### Acceptance Criteria

1. THE System SHALL create an Obsidian vault with a root directory structure
2. THE System SHALL maintain a Dashboard.md file in the vault root
3. THE System SHALL maintain a Company_Handbook.md file in the vault root
4. THE System SHALL create an /Inbox folder for incoming items requiring processing
5. THE System SHALL create a /Needs_Action folder for items requiring action
6. THE System SHALL create a /Done folder for completed items
7. WHEN the vault is initialized, THE System SHALL create all required folders and template files
8. THE Dashboard.md file SHALL contain current system status, pending actions, and recent activity summaries

### Requirement 2: Watcher Scripts for External Monitoring

**User Story:** As a user, I want automated monitoring of my communication channels, so that incoming messages and events are captured without manual intervention.

#### Acceptance Criteria

1. THE System SHALL implement a Gmail Watcher that monitors email accounts
2. THE System SHALL implement a WhatsApp Watcher that monitors WhatsApp messages
3. THE System SHALL implement a File_System Watcher that monitors designated directories
4. THE System SHALL implement a LinkedIn Watcher that monitors LinkedIn activity
5. THE System SHALL implement a Facebook Watcher that monitors Facebook activity
6. THE System SHALL implement an Instagram Watcher that monitors Instagram activity
7. THE System SHALL implement a Twitter Watcher that monitors Twitter (X) activity
8. WHEN a Watcher detects new content, THE System SHALL create a markdown file in /Inbox with structured metadata
9. WHEN a Watcher encounters an error, THE System SHALL log the error and continue monitoring
10. THE System SHALL implement each Watcher as an independent process with restart capability

### Requirement 3: Claude Code Integration

**User Story:** As a system architect, I want Claude Code to read from and write to the Vault, so that AI reasoning can process information and update system state.

#### Acceptance Criteria

1. THE Claude_Code SHALL have read access to all markdown files in the Vault
2. THE Claude_Code SHALL have write access to create and modify markdown files in the Vault
3. WHEN Claude_Code processes an item, THE System SHALL move it from /Inbox to /Needs_Action or /Done as appropriate
4. THE Claude_Code SHALL update Dashboard.md with processing results
5. THE Claude_Code SHALL implement all AI functionality as discrete Agent_Skills
6. WHEN Claude_Code creates a Plan.md file, THE System SHALL store it in the /Plans folder

### Requirement 4: MCP Server Integration for External Actions

**User Story:** As a user, I want the system to perform external actions through MCP servers, so that the AI can send emails, post to social media, and interact with business systems.

#### Acceptance Criteria

1. THE System SHALL implement an Email_MCP_Server for sending emails
2. THE System SHALL implement a Social_Media_MCP_Server for posting to LinkedIn, Facebook, Instagram, and Twitter
3. THE System SHALL implement an Odoo_MCP_Server for accounting system integration via JSON-RPC APIs
4. WHEN an MCP_Server is called, THE System SHALL validate the request parameters
5. WHEN an MCP_Server encounters an error, THE System SHALL return a descriptive error message
6. THE System SHALL implement each MCP_Server as an independent service with health monitoring
7. THE Odoo_MCP_Server SHALL connect to Odoo Community Edition via JSON-RPC APIs

### Requirement 5: Human-in-the-Loop Approval Workflow

**User Story:** As a user, I want to approve sensitive actions before they execute, so that I maintain control over important decisions.

#### Acceptance Criteria

1. THE System SHALL create approval request files in /Pending_Approval when sensitive actions are proposed
2. WHEN a user approves an action, THE System SHALL move the approval file to /Needs_Action
3. WHEN a user rejects an action, THE System SHALL move the approval file to /Done with rejection metadata
4. THE System SHALL define approval thresholds for different action types (email sending, social posting, payments)
5. THE System SHALL NOT execute sensitive actions without explicit approval
6. THE Approval_Workflow SHALL include action details, reasoning, and risk assessment in approval files

### Requirement 6: Autonomous Reasoning with Ralph Wiggum Loop

**User Story:** As a user, I want the system to autonomously complete multi-step tasks, so that complex workflows execute without constant supervision.

#### Acceptance Criteria

1. THE Claude_Code SHALL implement the Ralph_Wiggum_Loop for autonomous task completion
2. WHEN a task requires multiple steps, THE System SHALL create a Plan.md file with step-by-step breakdown
3. WHEN executing a plan, THE System SHALL update the plan file with progress after each step
4. WHEN a step fails, THE System SHALL implement retry logic with exponential backoff
5. WHEN a plan cannot proceed, THE System SHALL create an approval request for human intervention
6. THE Ralph_Wiggum_Loop SHALL maintain context across multiple reasoning iterations

### Requirement 7: Orchestration and Scheduling

**User Story:** As a system architect, I want a master orchestrator to coordinate all system components, so that Watchers, reasoning loops, and MCP servers work together reliably.

#### Acceptance Criteria

1. THE System SHALL implement a Python Orchestrator as the master coordination process
2. THE Orchestrator SHALL start and monitor all Watcher processes
3. THE Orchestrator SHALL trigger Claude_Code reasoning loops on a schedule
4. THE Orchestrator SHALL monitor MCP_Server health and restart failed services
5. THE Orchestrator SHALL implement a watchdog process for self-recovery
6. WHEN a component fails, THE Orchestrator SHALL log the failure and attempt restart
7. THE System SHALL support scheduling via cron (Linux/Mac) or Task Scheduler (Windows)
8. THE Orchestrator SHALL generate health status reports in Dashboard.md

### Requirement 8: LinkedIn Business Automation

**User Story:** As a business owner, I want automated LinkedIn posting for my business, so that I maintain consistent social media presence without manual effort.

#### Acceptance Criteria

1. THE System SHALL generate LinkedIn post drafts based on business content
2. WHEN a LinkedIn post is ready, THE System SHALL create an approval request
3. WHEN a LinkedIn post is approved, THE Social_Media_MCP_Server SHALL publish it
4. THE System SHALL track posted content in the Vault with timestamps and engagement metrics
5. THE System SHALL generate weekly summaries of LinkedIn activity

### Requirement 9: Odoo Accounting Integration

**User Story:** As a business owner, I want integration with Odoo Community accounting system, so that financial transactions are tracked and managed automatically.

#### Acceptance Criteria

1. THE System SHALL connect to a self-hosted Odoo Community Edition instance
2. THE Odoo_MCP_Server SHALL support creating draft invoices via JSON-RPC
3. THE Odoo_MCP_Server SHALL support creating draft payments via JSON-RPC
4. THE Odoo_MCP_Server SHALL support querying financial reports via JSON-RPC
5. WHEN creating financial transactions, THE System SHALL require approval before posting
6. THE System SHALL generate weekly Business and Accounting Audit reports
7. THE System SHALL generate CEO Briefing documents summarizing financial status

### Requirement 10: Multi-Platform Social Media Integration

**User Story:** As a content creator, I want integration with Facebook, Instagram, and Twitter, so that I can manage all social media from one system.

#### Acceptance Criteria

1. THE Social_Media_MCP_Server SHALL support posting to Facebook
2. THE Social_Media_MCP_Server SHALL support posting to Instagram
3. THE Social_Media_MCP_Server SHALL support posting to Twitter (X)
4. THE System SHALL generate daily summaries of social media activity across all platforms
5. WHEN social media content is ready, THE System SHALL create approval requests
6. THE System SHALL track engagement metrics (likes, comments, shares) for all posts

### Requirement 11: Cloud and Local Work-Zone Specialization

**User Story:** As a user, I want 24/7 cloud deployment with local approval capabilities, so that the system runs continuously while I maintain control over sensitive actions.

#### Acceptance Criteria

1. THE System SHALL support deployment in Cloud and Local Work_Zones
2. THE Cloud Work_Zone SHALL handle email triage, draft replies, and social post drafts
3. THE Local Work_Zone SHALL handle approvals, WhatsApp monitoring, payments, and final send/post actions
4. THE System SHALL synchronize the Vault between Cloud and Local via Git or Syncthing
5. THE System SHALL implement a claim-by-move rule to prevent duplicate work across Work_Zones
6. THE System SHALL implement a single-writer rule for Dashboard.md (Local only)
7. THE Vault sync SHALL include only markdown and state files, excluding secrets and credentials
8. THE Cloud deployment SHALL include always-on Watchers, Orchestrator, and health monitoring
9. THE Odoo instance SHALL run on a Cloud VM with HTTPS, automated backups, and health monitoring
10. THE Cloud Agent SHALL create draft-only accounting actions requiring Local approval

### Requirement 12: Security and Credential Management

**User Story:** As a security-conscious user, I want secure credential management and permission boundaries, so that my sensitive information is protected.

#### Acceptance Criteria

1. THE System SHALL store all credentials in environment variables
2. THE System SHALL NOT commit credentials to version control
3. THE System SHALL implement a dry-run mode for development and testing
4. THE System SHALL maintain separate test and production accounts for external services
5. THE System SHALL implement permission boundaries with approval thresholds
6. THE System SHALL sandbox external API calls to prevent unauthorized actions
7. THE System SHALL encrypt sensitive data at rest in the Vault

### Requirement 13: Audit Logging and Observability

**User Story:** As a system administrator, I want comprehensive audit logging, so that I can track all system actions and troubleshoot issues.

#### Acceptance Criteria

1. THE System SHALL log all Watcher detections with timestamps and metadata
2. THE System SHALL log all Claude_Code reasoning decisions with input and output
3. THE System SHALL log all MCP_Server actions with request and response details
4. THE System SHALL log all approval workflow events (created, approved, rejected)
5. THE System SHALL maintain audit logs in a structured format (JSON or CSV)
6. THE System SHALL implement log rotation to prevent unbounded growth
7. THE System SHALL generate daily audit summaries in Dashboard.md

### Requirement 14: Error Handling and Graceful Degradation

**User Story:** As a user, I want the system to handle errors gracefully, so that temporary failures don't cause complete system breakdown.

#### Acceptance Criteria

1. WHEN a Watcher fails, THE System SHALL log the error and continue monitoring other sources
2. WHEN an MCP_Server is unavailable, THE System SHALL queue actions for retry
3. WHEN Claude_Code reasoning fails, THE System SHALL create an error report in /Needs_Action
4. THE System SHALL implement exponential backoff for transient failures
5. THE System SHALL implement circuit breakers for repeatedly failing components
6. WHEN the Vault is unavailable, THE System SHALL buffer updates in memory until reconnection
7. THE Orchestrator watchdog SHALL restart failed components automatically

### Requirement 15: Progressive Tier Implementation

**User Story:** As a developer, I want clear tier boundaries for progressive implementation, so that I can build the system incrementally with working functionality at each stage.

#### Acceptance Criteria

1. THE Bronze Tier SHALL include: Vault, one Watcher, Claude_Code integration, basic folder structure
2. THE Silver Tier SHALL include: Bronze plus two or more Watchers, LinkedIn posting, Plan.md creation, one MCP_Server, approval workflow, scheduling
3. THE Gold Tier SHALL include: Silver plus cross-domain integration, Odoo integration, Facebook/Instagram/Twitter integration, multiple MCP_Servers, weekly audits, Ralph_Wiggum_Loop, architecture documentation
4. THE Platinum Tier SHALL include: Gold plus 24/7 cloud deployment, Work_Zone specialization, vault sync, cloud Odoo with backups
5. WHEN implementing a tier, THE System SHALL maintain all functionality from previous tiers
6. THE System SHALL document tier boundaries and dependencies in architecture documentation

### Requirement 16: Testing and Validation

**User Story:** As a developer, I want comprehensive testing coverage, so that I can validate system correctness and catch bugs early.

#### Acceptance Criteria

1. THE System SHALL include unit tests for all Watcher components
2. THE System SHALL include unit tests for all MCP_Server components
3. THE System SHALL include property-based tests for core reasoning logic
4. THE System SHALL include integration tests for end-to-end workflows
5. THE System SHALL include tests for approval workflow state transitions
6. THE System SHALL include tests for error handling and retry logic
7. THE System SHALL validate that all tests pass before deployment
