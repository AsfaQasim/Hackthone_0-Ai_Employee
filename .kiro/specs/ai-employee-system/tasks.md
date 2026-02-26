# Implementation Plan: AI Employee System

## Overview

This implementation plan breaks down the AI Employee System into progressive tiers, with each tier building on the previous one. The plan follows a bottom-up approach, starting with foundational components (vault, watchers) and progressively adding reasoning, actions, and orchestration. Each tier represents a working system with increasing sophistication.

The implementation uses Python for all components, with the following key libraries:
- `watchdog` for file system monitoring
- `hypothesis` for property-based testing
- `mcp` (Model Context Protocol SDK) for MCP servers
- `odoorpc` for Odoo integration
- `python-dotenv` for credential management
- Gmail API, LinkedIn API, and social media SDKs for external integrations

## Tasks

### Bronze Tier: Foundation (8-12 hours)

- [x] 1. Set up project structure and dependencies
  - Create Python project with virtual environment
  - Install core dependencies: watchdog, python-dotenv, pytest, hypothesis
  - Create directory structure: src/, tests/, config/
  - Set up .env.example file for credential templates
  - Create .gitignore to exclude credentials and vault data
  - _Requirements: 12.1, 12.2_

- [x] 2. Implement Obsidian vault initialization
  - [x] 2.1 Create VaultManager class for vault operations
    - Implement vault directory creation
    - Implement folder structure creation (/Inbox, /Needs_Action, /Done, /Plans, /Pending_Approval)
    - Implement template file creation (Dashboard.md, Company_Handbook.md)
    - _Requirements: 1.1, 1.4, 1.5, 1.6, 1.7_
  
  - [ ]* 2.2 Write property test for vault initialization
    - **Property 1: Vault Initialization Completeness**
    - **Validates: Requirements 1.1, 1.4, 1.5, 1.6, 1.7**
  
  - [ ]* 2.3 Write unit tests for VaultManager
    - Test folder creation
    - Test template file generation
    - Test Dashboard.md structure
    - _Requirements: 1.2, 1.8_

- [x] 3. Implement Gmail Watcher
  - [x] 3.1 Create base Watcher class with common interface
    - Define start(), stop(), check_for_new_items() methods
    - Implement inbox file creation logic
    - Add structured metadata formatting
    - _Requirements: 2.1, 2.8_
  
  - [x] 3.2 Implement GmailWatcher with Gmail API integration
    - Set up OAuth2 authentication
    - Implement email polling (60-second interval)
    - Filter for unread emails
    - Mark emails as read after processing
    - _Requirements: 2.1, 2.8_
  
  - [ ]* 3.3 Write property test for watcher detection
    - **Property 3: Watcher Detection Creates Inbox Files**
    - **Validates: Requirements 2.8**
  
  - [ ]* 3.4 Write unit tests for GmailWatcher
    - Test email detection
    - Test inbox file creation
    - Test metadata formatting
    - _Requirements: 2.8_

- [x] 4. Implement basic Claude Code integration
  - [x] 4.1 Create ClaudeCodeAgent class
    - Implement vault file reading
    - Implement vault file writing
    - Implement inbox processing loop
    - Add Dashboard.md update functionality
    - _Requirements: 3.1, 3.2, 3.4_
  
  - [ ]* 4.2 Write property tests for vault access
    - **Property 4: Vault File Access**
    - **Validates: Requirements 3.1, 3.2**
  
  - [ ]* 4.3 Write unit tests for ClaudeCodeAgent
    - Test file reading
    - Test file writing
    - Test Dashboard updates
    - _Requirements: 3.1, 3.2, 3.4_

- [x] 5. Implement basic Agent Skills framework
  - Create AgentSkill base class
  - Implement email_triage skill
  - Add skill registration and execution
  - _Requirements: 3.5_

- [x] 6. Bronze Tier Checkpoint
  - Run all tests and ensure they pass
  - Test end-to-end: Gmail detection → Inbox file → Claude processing
  - Verify vault structure is correct
  - Ask user if questions arise


### Silver Tier: Functional Assistant (20-30 hours)

- [x] 7. Implement additional watchers
  - [x] 7.1 Implement WhatsAppWatcher
    - Set up WhatsApp Web API integration
    - Implement message polling (30-second interval)
    - Handle QR code authentication
    - Capture messages, media, and group chats
    - _Requirements: 2.2, 2.8_
  
  - [x] 7.2 Implement LinkedInWatcher
    - Set up LinkedIn API OAuth2
    - Monitor messages, connection requests, post engagement
    - Implement 300-second polling interval for rate limit compliance
    - _Requirements: 2.4, 2.8_
  
  - [ ]* 7.3 Write property test for watcher isolation
    - **Property 33: Watcher Isolation**
    - **Validates: Requirements 2.9, 14.1**

- [x] 8. Implement Email MCP Server
  - [x] 8.1 Create BaseMCPServer class
    - Set up MCP server framework using mcp SDK
    - Implement tool registration
    - Implement tool call handling
    - Add parameter validation
    - _Requirements: 4.1, 4.4_
  
  - [x] 8.2 Implement EmailMCPServer
    - Register send_email tool
    - Implement email sending via Gmail API
    - Add error handling and descriptive error messages
    - _Requirements: 4.1, 4.5_
  
  - [ ]* 8.3 Write property tests for MCP server
    - **Property 7: MCP Parameter Validation**
    - **Property 8: MCP Error Messages**
    - **Validates: Requirements 4.4, 4.5**
  
  - [ ]* 8.4 Write unit tests for EmailMCPServer
    - Test tool registration
    - Test parameter validation
    - Test email sending
    - Test error handling
    - _Requirements: 4.1, 4.4, 4.5_

- [x] 9. Implement approval workflow
  - [x] 9.1 Create ApprovalWorkflow class
    - Implement approval request file creation
    - Add risk level assessment
    - Create approval file format with action details
    - _Requirements: 5.1, 5.6_
  
  - [x] 9.2 Implement approval processing
    - Monitor /Pending_Approval folder
    - Handle approval (move to /Needs_Action)
    - Handle rejection (move to /Done with metadata)
    - _Requirements: 5.2, 5.3_
  
  - [x] 9.3 Implement approval threshold enforcement
    - Define risk levels (low, medium, high)
    - Block sensitive actions without approval
    - _Requirements: 5.4, 5.5_
  
  - [ ]* 9.4 Write property tests for approval workflow
    - **Property 9: Sensitive Action Approval Creation**
    - **Property 10: Approval State Transitions**
    - **Property 11: Sensitive Action Blocking**
    - **Property 12: Approval File Completeness**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.5, 5.6**
  
  - [ ]* 9.5 Write unit tests for approval workflow
    - Test approval request creation
    - Test approval processing
    - Test rejection processing
    - Test threshold enforcement
    - _Requirements: 5.1, 5.2, 5.3, 5.5_

- [x] 10. Implement Plan.md creation and basic execution
  - [x] 10.1 Create PlanManager class
    - Implement Plan.md file creation
    - Add step-by-step breakdown formatting
    - Store plans in /Plans folder
    - _Requirements: 6.2, 3.6_
  
  - [x] 10.2 Implement basic plan execution
    - Read Plan.md files
    - Execute steps sequentially
    - Update plan file with progress
    - _Requirements: 6.3_
  
  - [ ]* 10.3 Write property tests for plan management
    - **Property 6: Plan Storage Location**
    - **Property 13: Multi-Step Plan Creation**
    - **Property 14: Plan Progress Updates**
    - **Validates: Requirements 3.6, 6.2, 6.3**

- [x] 11. Implement LinkedIn posting capability
  - [x] 11.1 Create SocialMediaMCPServer
    - Register post_to_linkedin tool
    - Implement LinkedIn posting via API
    - Add visibility options (public, connections)
    - _Requirements: 8.1, 8.2_
  
  - [x] 11.2 Integrate LinkedIn posting with approval workflow
    - Generate LinkedIn post drafts
    - Create approval requests for posts
    - Publish approved posts
    - Track posted content with timestamps
    - _Requirements: 8.2, 8.3, 8.4_
  
  - [ ]* 11.3 Write property tests for social media operations
    - **Property 20: Approved Post Publishing**
    - **Property 21: Content Tracking**
    - **Validates: Requirements 8.3, 8.4**

- [x] 12. Implement scheduling
  - [x] 12.1 Create Scheduler class
    - Support cron (Linux/Mac) and Task Scheduler (Windows)
    - Schedule reasoning loop execution
    - Schedule health checks
    - _Requirements: 7.7_
  
  - [ ]* 12.2 Write unit tests for scheduler
    - Test cron configuration
    - Test Task Scheduler configuration
    - Test scheduled execution
    - _Requirements: 7.7_

- [x] 13. Silver Tier Checkpoint
  - Run all tests and ensure they pass
  - Test end-to-end approval workflow
  - Test LinkedIn posting workflow
  - Verify multiple watchers work independently
  - Ask user if questions arise


### Gold Tier: Autonomous Employee (40+ hours)

- [ ] 14. Set up Odoo Community Edition
  - Install Odoo Community Edition locally
  - Configure database and basic settings
  - Create test accounts and sample data
  - Set up JSON-RPC API access
  - _Requirements: 9.1_

- [ ] 15. Implement Odoo MCP Server
  - [ ] 15.1 Create OdooMCPServer class
    - Set up OdooRPC connection
    - Implement authentication
    - Register create_invoice_draft tool
    - Register create_payment_draft tool
    - Register query_financial_reports tool
    - _Requirements: 9.2, 9.3, 9.4_
  
  - [ ] 15.2 Integrate Odoo operations with approval workflow
    - Require approval for all financial transactions
    - Create approval requests for invoices and payments
    - Post to Odoo only after approval
    - _Requirements: 9.5_
  
  - [ ]* 15.3 Write property test for financial transaction approval
    - **Property 22: Financial Transaction Approval Requirement**
    - **Validates: Requirements 9.5**
  
  - [ ]* 15.4 Write unit tests for OdooMCPServer
    - Test connection and authentication
    - Test invoice draft creation
    - Test payment draft creation
    - Test financial report queries
    - _Requirements: 9.2, 9.3, 9.4_

- [ ] 16. Implement additional social media watchers and posting
  - [ ] 16.1 Implement FacebookWatcher
    - Set up Facebook API OAuth2
    - Monitor messages, mentions, comments
    - Implement rate limit compliance
    - _Requirements: 2.5, 2.8_
  
  - [ ] 16.2 Implement InstagramWatcher
    - Set up Instagram API OAuth2
    - Monitor messages, mentions, comments
    - Implement rate limit compliance
    - _Requirements: 2.6, 2.8_
  
  - [ ] 16.3 Implement TwitterWatcher
    - Set up Twitter (X) API OAuth2
    - Monitor messages, mentions, comments
    - Implement rate limit compliance
    - _Requirements: 2.7, 2.8_
  
  - [ ] 16.4 Extend SocialMediaMCPServer for all platforms
    - Add post_to_facebook tool
    - Add post_to_instagram tool
    - Add post_to_twitter tool
    - Implement engagement metrics tracking
    - _Requirements: 10.1, 10.2, 10.3, 10.6_
  
  - [ ]* 16.5 Write property test for engagement tracking
    - **Property 21: Content Tracking** (extended for all platforms)
    - **Validates: Requirements 10.6**

- [ ] 17. Implement Ralph Wiggum Loop
  - [ ] 17.1 Create RalphWiggumLoop class
    - Implement multi-step task execution
    - Add context preservation across iterations
    - Implement step retry logic with exponential backoff
    - Create approval requests for blocked plans
    - _Requirements: 6.1, 6.4, 6.5, 6.6_
  
  - [ ]* 17.2 Write property tests for Ralph Wiggum Loop
    - **Property 15: Step Failure Retry Logic**
    - **Property 16: Blocked Plan Escalation**
    - **Property 17: Context Preservation Across Iterations**
    - **Validates: Requirements 6.4, 6.5, 6.6**
  
  - [ ]* 17.3 Write unit tests for RalphWiggumLoop
    - Test multi-step execution
    - Test context preservation
    - Test retry logic
    - Test escalation to approval
    - _Requirements: 6.4, 6.5, 6.6_

- [ ] 18. Implement comprehensive error recovery
  - [ ] 18.1 Implement CircuitBreaker class
    - Add failure threshold tracking
    - Implement open/closed/half-open states
    - Add timeout and recovery logic
    - _Requirements: 14.5_
  
  - [ ] 18.2 Implement error handling patterns
    - Add transient error retry with exponential backoff
    - Implement MCP action queueing for unavailable servers
    - Create error reports for reasoning failures
    - Add vault unavailability buffering
    - _Requirements: 14.2, 14.3, 14.4, 14.6_
  
  - [ ]* 18.3 Write property tests for error handling
    - **Property 34: MCP Action Queueing**
    - **Property 35: Reasoning Failure Error Reports**
    - **Property 36: Exponential Backoff for Transient Failures**
    - **Property 37: Circuit Breaker Activation**
    - **Property 38: Vault Unavailability Buffering**
    - **Validates: Requirements 14.2, 14.3, 14.4, 14.5, 14.6**

- [ ] 19. Implement Master Orchestrator
  - [ ] 19.1 Create MasterOrchestrator class
    - Implement component startup (watchers, MCP servers, Claude agent)
    - Add health monitoring for all components
    - Implement component restart logic
    - Add reasoning loop scheduling
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.6_
  
  - [ ] 19.2 Implement WatchdogProcess
    - Monitor orchestrator heartbeat
    - Detect orchestrator failures
    - Restart orchestrator automatically
    - _Requirements: 7.5, 14.7_
  
  - [ ]* 19.3 Write property tests for orchestrator
    - **Property 18: Failed Component Restart**
    - **Property 19: Health Status Reporting**
    - **Validates: Requirements 7.4, 7.6, 7.8, 14.7**
  
  - [ ]* 19.4 Write unit tests for orchestrator
    - Test component startup
    - Test health monitoring
    - Test component restart
    - Test watchdog process
    - _Requirements: 7.4, 7.6, 14.7_

- [ ] 20. Implement audit logging
  - [ ] 20.1 Create AuditLogger class
    - Implement structured log format (JSON)
    - Log watcher detections
    - Log Claude Code reasoning decisions
    - Log MCP server actions
    - Log approval workflow events
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_
  
  - [ ] 20.2 Implement log rotation and management
    - Add daily log rotation
    - Compress logs older than 7 days
    - Implement 90-day retention policy
    - _Requirements: 13.6_
  
  - [ ]* 20.3 Write property tests for audit logging
    - **Property 31: Comprehensive Event Logging**
    - **Property 32: Structured Log Format**
    - **Validates: Requirements 13.1, 13.2, 13.3, 13.4, 13.5**

- [ ] 21. Implement weekly audit reports
  - [ ] 21.1 Create AuditReportGenerator class
    - Generate Business and Accounting Audit reports
    - Generate CEO Briefing documents
    - Summarize financial status from Odoo
    - Include social media activity summaries
    - _Requirements: 9.6, 9.7_
  
  - [ ]* 21.2 Write unit tests for audit reports
    - Test Business Audit generation
    - Test CEO Briefing generation
    - Test financial summary extraction
    - _Requirements: 9.6, 9.7_

- [ ] 22. Create architecture documentation
  - Document system architecture with diagrams
  - Document component interfaces
  - Document data flows
  - Document deployment procedures
  - _Requirements: 15.5_

- [ ] 23. Gold Tier Checkpoint
  - Run all tests and ensure they pass
  - Test end-to-end financial workflow
  - Test multi-platform social media posting
  - Test Ralph Wiggum Loop with complex plans
  - Test error recovery scenarios
  - Ask user if questions arise


### Platinum Tier: Cloud + Local Executive (60+ hours)

- [ ] 24. Set up cloud infrastructure
  - [ ] 24.1 Provision cloud VM
    - Set up Linux VM on cloud provider (AWS, GCP, or Azure)
    - Configure networking and firewall rules
    - Set up SSH access and security hardening
    - _Requirements: 11.8_
  
  - [ ] 24.2 Deploy Odoo to cloud
    - Install Odoo Community Edition on cloud VM
    - Configure HTTPS with SSL certificates
    - Set up automated backups
    - Implement health monitoring
    - _Requirements: 11.9_
  
  - [ ]* 24.3 Write unit tests for cloud deployment
    - Test HTTPS connectivity
    - Test backup procedures
    - Test health monitoring
    - _Requirements: 11.9_

- [ ] 25. Implement vault synchronization
  - [ ] 25.1 Set up Git-based vault sync
    - Initialize Git repository for vault
    - Configure .gitignore to exclude secrets
    - Set up automatic commit and push
    - Implement pull and merge logic
    - _Requirements: 11.4, 11.7_
  
  - [ ] 25.2 Alternative: Set up Syncthing-based vault sync
    - Install and configure Syncthing on both cloud and local
    - Set up selective sync (markdown only)
    - Exclude secrets and credentials
    - _Requirements: 11.4, 11.7_
  
  - [ ]* 25.3 Write property test for vault sync security
    - **Property 25: Vault Sync Excludes Secrets**
    - **Validates: Requirements 11.7**

- [ ] 26. Implement work-zone specialization
  - [ ] 26.1 Create WorkZone class
    - Define Cloud and Local work zone types
    - Implement work zone responsibilities
    - Add claim-by-move rule enforcement
    - Implement single-writer rule for Dashboard.md
    - _Requirements: 11.2, 11.3, 11.5, 11.6_
  
  - [ ] 26.2 Configure cloud work zone
    - Deploy watchers for email triage
    - Deploy Claude agent for draft generation
    - Deploy MCP servers for draft-only actions
    - Configure Odoo MCP for draft-only accounting
    - _Requirements: 11.2, 11.10_
  
  - [ ] 26.3 Configure local work zone
    - Deploy WhatsApp watcher (local only for security)
    - Deploy approval processing
    - Deploy MCP servers for final actions (send, post, pay)
    - Configure Dashboard.md as single-writer
    - _Requirements: 11.3, 11.6_
  
  - [ ]* 26.4 Write property tests for work-zone coordination
    - **Property 23: Work Zone Claim-by-Move**
    - **Property 24: Dashboard Single-Writer Rule**
    - **Validates: Requirements 11.5, 11.6**
  
  - [ ]* 26.5 Write integration tests for work-zone coordination
    - Test cloud draft creation → local approval → local execution
    - Test claim-by-move prevents duplicate work
    - Test Dashboard.md single-writer enforcement
    - _Requirements: 11.5, 11.6_

- [ ] 27. Deploy cloud components
  - [ ] 27.1 Deploy cloud orchestrator
    - Package application for cloud deployment
    - Set up systemd service for orchestrator
    - Configure environment variables
    - Deploy watchers (Gmail, LinkedIn, Facebook, Instagram, Twitter)
    - _Requirements: 11.8_
  
  - [ ] 27.2 Set up cloud health monitoring
    - Implement health check endpoints
    - Set up monitoring dashboard
    - Configure alerting for failures
    - _Requirements: 11.8_
  
  - [ ]* 27.3 Write unit tests for cloud deployment
    - Test systemd service configuration
    - Test health check endpoints
    - Test alerting logic
    - _Requirements: 11.8_

- [ ] 28. Implement security hardening
  - [ ] 28.1 Implement credential management
    - Store all credentials in environment variables
    - Verify no credentials in version control
    - Implement credential rotation procedures
    - _Requirements: 12.1, 12.2_
  
  - [ ] 28.2 Implement sandboxing and permission boundaries
    - Enforce approval thresholds
    - Sandbox external API calls
    - Implement rate limiting
    - _Requirements: 12.5, 12.6_
  
  - [ ] 28.3 Implement data encryption
    - Encrypt sensitive data at rest in vault
    - Use HTTPS for all external communications
    - _Requirements: 12.7_
  
  - [ ]* 28.4 Write property tests for security
    - **Property 26: Credential Storage in Environment**
    - **Property 27: Version Control Excludes Credentials**
    - **Property 28: Permission Boundary Enforcement**
    - **Property 29: API Call Sandboxing**
    - **Property 30: Sensitive Data Encryption**
    - **Validates: Requirements 12.1, 12.2, 12.5, 12.6, 12.7**

- [ ] 29. Implement comprehensive testing
  - [ ]* 29.1 Write integration tests for end-to-end workflows
    - Test email processing: Detection → Triage → Reply → Send
    - Test social posting: Generation → Approval → Publish → Track
    - Test financial workflow: Invoice → Approval → Post to Odoo
    - Test multi-step plan: Creation → Execution → Completion
    - Test error recovery: Failure → Restart → Resume
    - Test cloud/local coordination: Sync → Distribution → Approval
    - _Requirements: 16.4_
  
  - [ ]* 29.2 Run all property-based tests
    - Execute all 38 property tests with 100 iterations each
    - Verify all properties pass
    - _Requirements: 16.3_
  
  - [ ]* 29.3 Run all unit tests
    - Execute complete unit test suite
    - Verify code coverage meets requirements
    - _Requirements: 16.1, 16.2_

- [ ] 30. Performance optimization and load testing
  - [ ] 30.1 Implement performance optimizations
    - Optimize vault file operations
    - Add caching for frequently accessed data
    - Optimize MCP server response times
    - _Requirements: 15.5_
  
  - [ ]* 30.2 Conduct load testing
    - Test system under high watcher detection volume
    - Test concurrent MCP server requests
    - Test vault sync under load
    - _Requirements: 15.5_

- [ ] 31. Implement backup and disaster recovery
  - [ ] 31.1 Set up automated backups
    - Backup vault daily
    - Backup Odoo database daily
    - Backup audit logs weekly
    - Store backups in separate location
    - _Requirements: 11.9_
  
  - [ ] 31.2 Create disaster recovery procedures
    - Document recovery steps
    - Test recovery from backups
    - Create runbooks for common failures
    - _Requirements: 11.9_

- [ ] 32. Final security audit
  - Review all credential storage
  - Verify no secrets in version control
  - Test permission boundaries
  - Review audit logs for anomalies
  - Conduct penetration testing
  - _Requirements: 12.1, 12.2, 12.5, 12.6, 12.7_

- [ ] 33. Platinum Tier Checkpoint
  - Run all tests (unit, property, integration) and ensure they pass
  - Test 24/7 cloud operation for 48 hours
  - Test cloud/local coordination end-to-end
  - Test disaster recovery procedures
  - Verify all security requirements met
  - Ask user if questions arise

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at tier boundaries
- Property tests validate universal correctness properties (38 total)
- Unit tests validate specific examples and edge cases
- Integration tests validate end-to-end workflows
- The system is designed for progressive implementation: Bronze → Silver → Gold → Platinum
- Each tier represents a working system with increasing sophistication
