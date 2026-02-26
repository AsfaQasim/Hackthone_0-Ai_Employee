---
type: feature_spec
status: draft
category: perception
risk_level: medium
created: 2026-02-14
mcp_servers: [gmail-watcher]
requires_approval: true
---

# Gmail Watcher Specification

## Overview

A perception layer component that monitors Gmail inbox for new emails and triggers the Ralph Loop to process, categorize, and take action on incoming messages within the Obsidian vault.

## Purpose

Enable the Personal AI Employee to:
- Monitor Gmail inbox for new messages
- Extract and parse email content
- Categorize emails by type and priority
- Create actionable items in the vault
- Trigger appropriate workflows based on email content

## User Stories

### US-1: Email Monitoring
**As a** user  
**I want** the AI Employee to monitor my Gmail inbox  
**So that** I don't miss important emails and can process them systematically

**Acceptance Criteria**:
- System checks Gmail every 5 minutes for new emails
- Only unread emails are processed
- Emails are marked as read after processing
- System handles Gmail API rate limits gracefully

### US-2: Email Categorization
**As a** user  
**I want** emails automatically categorized by type  
**So that** I can prioritize and respond appropriately

**Acceptance Criteria**:
- Emails categorized as: Action Required, FYI, Newsletter, Spam, Personal
- Category is determined by sender, subject, and content analysis
- Categories are stored in email metadata
- User can override automatic categorization

### US-3: Action Item Creation
**As a** user  
**I want** action-required emails to create tasks in my vault  
**So that** I can track and complete email-driven work

**Acceptance Criteria**:
- Emails marked "Action Required" create tasks in `/Needs_Action/`
- Task includes: sender, subject, summary, due date (if mentioned)
- Link to original email is preserved
- Task status syncs with email status

### US-4: Email Archiving
**As a** user  
**I want** processed emails archived in my vault  
**So that** I have a searchable local record

**Acceptance Criteria**:
- Email content saved as markdown in `/Logs/emails/`
- Frontmatter includes: sender, date, category, labels
- Attachments are downloaded and linked (if enabled)
- Original email ID preserved for reference

### US-5: Smart Filtering
**As a** user  
**I want** to define rules for email handling  
**So that** routine emails are processed automatically

**Acceptance Criteria**:
- User can define filters in `/Skills/email_filters.md`
- Filters support: sender, subject patterns, keywords
- Actions include: archive, create task, forward, ignore
- Filters are applied before manual review

## Architecture

### Ralph Loop Integration

```
PERCEPTION (Gmail Watcher)
    ↓
  [Poll Gmail API]
    ↓
  [Fetch new emails]
    ↓
  [Parse content]
    ↓
REASONING (Email Processor)
    ↓
  [Categorize email]
    ↓
  [Apply filters]
    ↓
  [Determine action]
    ↓
ACTION (Vault Operations)
    ↓
  [Create task/archive]
    ↓
  [Mark email as read]
    ↓
  [Log activity]
```

### Components

#### 1. Gmail Watcher (Perception)
- **Polling Service**: Check Gmail every N minutes
- **Email Fetcher**: Retrieve unread emails via Gmail API
- **Content Parser**: Extract sender, subject, body, attachments
- **Event Emitter**: Trigger Ralph Loop with email data

#### 2. Email Processor (Reasoning)
- **Categorizer**: Classify email by type and priority
- **Filter Engine**: Apply user-defined rules
- **Action Planner**: Decide what to do with email
- **Risk Assessor**: Determine if approval needed

#### 3. Vault Integrator (Action)
- **Task Creator**: Generate action items in vault
- **Email Archiver**: Save email as markdown
- **Status Updater**: Mark emails as processed
- **Logger**: Record all operations

## MCP Server: gmail-watcher

### Configuration

```json
{
  "mcpServers": {
    "gmail-watcher": {
      "command": "node",
      "args": ["./mcp-servers/gmail-server.js"],
      "env": {
        "GMAIL_CREDENTIALS_PATH": "./config/gmail-credentials.json",
        "GMAIL_TOKEN_PATH": "./config/gmail-token.json",
        "POLL_INTERVAL_MINUTES": "5",
        "MAX_EMAILS_PER_POLL": "50"
      },
      "disabled": false,
      "autoApprove": [
        "gmail.list",
        "gmail.get",
        "gmail.markRead"
      ]
    }
  }
}
```

### MCP Tools

#### gmail.authenticate()
- **Purpose**: Authenticate with Gmail API using OAuth2
- **Inputs**: None (uses credentials file)
- **Outputs**: Authentication token
- **Risk**: Low (read-only initially)

#### gmail.list(query, maxResults)
- **Purpose**: List emails matching query
- **Inputs**: 
  - `query`: Gmail search query (e.g., "is:unread")
  - `maxResults`: Max emails to return (default: 50)
- **Outputs**: Array of email metadata
- **Risk**: Low (read-only)

#### gmail.get(emailId)
- **Purpose**: Fetch full email content
- **Inputs**: `emailId`: Gmail message ID
- **Outputs**: Email object with headers, body, attachments
- **Risk**: Low (read-only)

#### gmail.markRead(emailId)
- **Purpose**: Mark email as read
- **Inputs**: `emailId`: Gmail message ID
- **Outputs**: Success boolean
- **Risk**: Medium (modifies Gmail state)

#### gmail.archive(emailId)
- **Purpose**: Archive email (remove from inbox)
- **Inputs**: `emailId`: Gmail message ID
- **Outputs**: Success boolean
- **Risk**: Medium (modifies Gmail state)

#### gmail.label(emailId, labelName)
- **Purpose**: Add label to email
- **Inputs**: 
  - `emailId`: Gmail message ID
  - `labelName`: Label to apply
- **Outputs**: Success boolean
- **Risk**: Medium (modifies Gmail state)

## Data Models

### Email Object

```markdown
---
type: email
email_id: "18d4f2a3b5c6e7f8"
sender: "john@example.com"
sender_name: "John Doe"
subject: "Q1 Report Review Needed"
received_at: 2026-02-14T09:30:00Z
category: action_required
priority: high
labels: [work, reports]
processed_at: 2026-02-14T09:35:00Z
status: archived
---

# Email: Q1 Report Review Needed

**From**: John Doe <john@example.com>  
**Date**: February 14, 2026 9:30 AM  
**Category**: Action Required  
**Priority**: High

## Content

Hi there,

Could you please review the Q1 report by end of week? 
Let me know if you have any questions.

Thanks,
John

## Actions Taken

- [x] Created task in /Needs_Action/
- [x] Marked as read in Gmail
- [x] Archived to /Logs/emails/2026-02/

## Links

- Gmail: [View Original](https://mail.google.com/mail/u/0/#inbox/18d4f2a3b5c6e7f8)
- Task: [[Needs_Action/review_q1_report]]
```

### Task from Email

```markdown
---
type: task
source: email
email_id: "18d4f2a3b5c6e7f8"
created_from: "john@example.com"
due_date: 2026-02-18
priority: high
status: pending
---

# Review Q1 Report

**Requested by**: John Doe (john@example.com)  
**Due**: February 18, 2026  
**Priority**: High

## Description

Review the Q1 report and provide feedback.

## Context

From email received on February 14, 2026:
> Could you please review the Q1 report by end of week?

## Actions

- [ ] Download Q1 report
- [ ] Review content
- [ ] Provide feedback
- [ ] Reply to John

## Links

- Original Email: [[Logs/emails/2026-02/email_18d4f2a3b5c6e7f8]]
- Gmail: [View](https://mail.google.com/mail/u/0/#inbox/18d4f2a3b5c6e7f8)
```

## Email Filters

### Filter Configuration

Stored in `/Skills/email_filters.md`:

```markdown
---
type: skill
skill_name: email_filters
category: reasoning
version: 1.0
---

# Email Filters

## Filter Rules

### Rule 1: Newsletter Auto-Archive
- **Condition**: sender contains "newsletter" OR subject contains "unsubscribe"
- **Action**: categorize as "newsletter", archive to /Logs/emails/newsletters/
- **Approval**: Not required

### Rule 2: Boss Emails High Priority
- **Condition**: sender is "boss@company.com"
- **Action**: categorize as "action_required", priority "high", create task
- **Approval**: Not required

### Rule 3: Meeting Invites
- **Condition**: subject contains "meeting" OR "calendar invite"
- **Action**: categorize as "calendar", extract date/time, create calendar entry
- **Approval**: Required (calendar modification)

### Rule 4: Receipts and Confirmations
- **Condition**: subject contains "receipt" OR "confirmation" OR "order"
- **Action**: categorize as "fyi", archive to /Logs/emails/receipts/
- **Approval**: Not required

### Rule 5: Spam Detection
- **Condition**: sender not in contacts AND subject contains "urgent" OR "act now"
- **Action**: categorize as "spam", archive to /Logs/emails/spam/
- **Approval**: Not required

## Custom Actions

### Action: Create Task
- Create markdown file in /Needs_Action/
- Extract due date from email body
- Set priority based on keywords
- Link to original email

### Action: Archive
- Save email as markdown
- Organize by date: /Logs/emails/YYYY-MM/
- Preserve all metadata
- Mark as read in Gmail

### Action: Forward
- Create approval request
- Include forwarding address
- Wait for human approval
- Execute via Gmail API
```

## Correctness Properties

### P-1: Email Detection Completeness
**Property**: All new emails in Gmail inbox are detected within poll interval  
**Validation**: Compare Gmail unread count with processed count  
**Test**: Send test emails, verify all are detected

### P-2: No Duplicate Processing
**Property**: Each email is processed exactly once  
**Validation**: Check email_id uniqueness in logs  
**Test**: Run watcher multiple times, verify no duplicates

### P-3: Content Preservation
**Property**: Email content is accurately preserved in vault  
**Validation**: Compare original email with archived markdown  
**Test**: Archive emails, verify content matches

### P-4: Filter Consistency
**Property**: Filters are applied consistently to all emails  
**Validation**: Same email always produces same categorization  
**Test**: Process same email multiple times, verify consistent results

### P-5: Approval Enforcement
**Property**: High-risk actions require approval before execution  
**Validation**: Check approval log for all medium/high risk actions  
**Test**: Trigger high-risk action, verify approval request created

## Security and Privacy

### Gmail API Permissions

**Required Scopes**:
- `gmail.readonly` - Read email content
- `gmail.modify` - Mark as read, add labels
- `gmail.send` - Send emails (optional, for replies)

**Security Measures**:
- OAuth2 authentication (no password storage)
- Credentials stored locally, never transmitted
- Token refresh handled automatically
- Rate limiting to prevent API abuse

### Data Privacy

**Local Storage**:
- All email content stays in local Obsidian vault
- No cloud storage or external services
- User controls data retention
- Easy to delete or export

**Sensitive Content**:
- Passwords and tokens redacted from logs
- Email addresses can be anonymized
- Attachments downloaded only if enabled
- User can exclude specific senders

## Error Handling

### Gmail API Errors

**Rate Limit Exceeded**:
- Back off exponentially (1min, 2min, 4min, etc.)
- Log warning in /Logs/errors/
- Resume when rate limit resets

**Authentication Failed**:
- Create approval request for re-authentication
- Pause watcher until resolved
- Log error with instructions

**Network Timeout**:
- Retry up to 3 times
- Log transient errors
- Continue with next poll cycle

### Vault Errors

**File Write Failed**:
- Retry with different filename
- Log error with email details
- Create recovery file in /Needs_Action/

**Disk Space Full**:
- Pause watcher
- Create alert in /Needs_Action/
- Wait for human intervention

## Performance

### Optimization Strategies

**Incremental Polling**:
- Track last processed email timestamp
- Only fetch emails after last timestamp
- Reduces API calls and processing time

**Batch Processing**:
- Process multiple emails in single cycle
- Group similar operations (mark read, archive)
- Reduces API round trips

**Caching**:
- Cache sender information
- Cache filter results for similar emails
- Reduces redundant processing

### Metrics

**Target Performance**:
- Poll interval: 5 minutes
- Processing time: < 10 seconds per email
- API calls: < 100 per hour
- Vault writes: < 50 per hour

## Testing Strategy

### Unit Tests

- Email parsing (extract sender, subject, body)
- Filter matching (rules applied correctly)
- Categorization logic (correct categories assigned)
- Task creation (proper markdown format)

### Integration Tests

- Gmail API authentication
- Email fetching and marking read
- Vault file creation and organization
- End-to-end Ralph Loop cycle

### Property-Based Tests

- All emails are processed exactly once
- Filters are deterministic
- Content is preserved accurately
- Approval is enforced for high-risk actions

## Deployment

### Setup Steps

1. **Enable Gmail API**
   - Go to Google Cloud Console
   - Create project and enable Gmail API
   - Download credentials.json

2. **Configure MCP Server**
   - Add gmail-watcher to mcp.json
   - Set credentials path
   - Configure poll interval

3. **Authenticate**
   - Run initial authentication flow
   - Authorize required scopes
   - Save token for future use

4. **Create Filter Rules**
   - Copy template to /Skills/email_filters.md
   - Customize rules for your needs
   - Test with sample emails

5. **Start Watcher**
   - Enable gmail-watcher in mcp.json
   - Verify polling starts
   - Check logs for activity

### Monitoring

**Daily Checks**:
- Review /Dashboard/gmail_summary.md
- Check for authentication errors
- Verify emails are being processed

**Weekly Maintenance**:
- Review filter effectiveness
- Adjust categorization rules
- Clean up old archived emails

## Future Enhancements

### Planned Features

1. **Smart Replies**: Generate draft responses for common emails
2. **Thread Tracking**: Group related emails into conversations
3. **Attachment Processing**: Extract and index attachment content
4. **Calendar Integration**: Auto-create events from meeting invites
5. **Contact Management**: Build contact database from emails
6. **Email Search**: Full-text search across archived emails
7. **Mobile Notifications**: Push alerts for high-priority emails
8. **Multi-Account Support**: Monitor multiple Gmail accounts

### Research Areas

- Natural language understanding for better categorization
- Predictive filtering based on past behavior
- Automated response generation
- Email sentiment analysis
- Priority prediction using machine learning

## Dependencies

**Required**:
- Gmail API access
- OAuth2 credentials
- MCP server implementation
- Obsidian vault with folder structure

**Optional**:
- Git for version control
- Dataview plugin for email queries
- Calendar plugin for event creation
- Tasks plugin for task management

## Success Metrics

**Effectiveness**:
- 95%+ of emails correctly categorized
- 90%+ of action items captured
- < 5% false positives (spam detection)
- Zero emails lost or duplicated

**Efficiency**:
- Average processing time < 10s per email
- API usage within rate limits
- Minimal manual intervention required
- User satisfaction with automation

## Approval Required

This specification requires approval for:
- Gmail API access and permissions
- Automatic email marking as read
- Email archiving to vault
- Filter rules and actions

**Approval Decision**:
- [ ] Approve (move to /Approved/)
- [ ] Reject (move to /Needs_Action/ with feedback)
- [ ] Modify (edit this specification)

---

**Status**: DRAFT  
**Next Steps**: Review specification, approve, implement MCP server, test with sample emails
