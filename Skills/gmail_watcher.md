---
skill_name: gmail_watcher
category: perception
version: 1.0.0
status: draft
inputs: [polling_interval, importance_criteria, priority_rules]
outputs: [markdown_files, processed_count, error_log]
mcp_tools: [gmail.authenticate, gmail.list, gmail.get, gmail.markRead]
risk_level: medium
requires_approval: true
spec_reference: ".kiro/specs/gmail-watcher-skill/"
---

# Gmail Watcher Agent Skill

## Purpose

Monitor Gmail inbox for unread important emails and automatically create actionable markdown files in the Obsidian vault's `Needs_Action` folder. This skill operates as part of the Ralph Loop (Perception → Reasoning → Action) architecture, providing automated email triage and task creation.

## Overview

The Gmail Watcher skill continuously polls Gmail via MCP (Model Context Protocol), filters emails based on importance criteria, assigns priority levels, and generates structured markdown files with complete metadata. It includes robust error handling, rate limiting, duplicate prevention, and comprehensive audit logging.

## Preconditions

**Required**:
- Gmail API access configured via MCP
- OAuth 2.0 credentials (credentials.json and token.json)
- MCP server `gmail-watcher` installed and enabled
- Obsidian vault with `Needs_Action` folder
- Configuration file at `Skills/config/gmail_watcher_config.yaml`

**Optional**:
- Git repository for version control
- Dataview plugin for querying email tasks

## Inputs

### Configuration Parameters

```yaml
# Skills/config/gmail_watcher_config.yaml

pollingIntervalMs: 300000  # 5 minutes

importanceCriteria:
  senderWhitelist:
    - "boss@company.com"
    - "client@important.com"
  keywordPatterns:
    - "urgent"
    - "important"
    - "action required"
    - "deadline"
  requiredLabels:
    - "IMPORTANT"
    - "STARRED"
  logicMode: "OR"  # Match any criterion

priorityRules:
  highPriorityKeywords:
    - "urgent"
    - "asap"
    - "critical"
    - "emergency"
    - "immediately"
  vipSenders:
    - "ceo@company.com"
    - "boss@company.com"
  highPriorityLabels:
    - "IMPORTANT"
    - "STARRED"
  mediumPriorityKeywords:
    - "follow up"
    - "reminder"
    - "deadline"
    - "review"

rateLimitConfig:
  maxRequestsPerMinute: 60
  maxRequestsPerDay: 10000
  initialBackoffMs: 1000
  maxBackoffMs: 60000
  backoffMultiplier: 2

needsActionFolder: "Needs_Action"
logFolder: "Logs/gmail_watcher"
```

## Execution Flow

### Ralph Loop Integration

```
┌─────────────────────────────────────────────────────────┐
│                    PERCEPTION PHASE                      │
├─────────────────────────────────────────────────────────┤
│ 1. Poll Gmail API via MCP (every 5 minutes)            │
│ 2. Fetch unread emails from inbox                       │
│ 3. Extract metadata: sender, subject, date, labels      │
│ 4. Parse email body (HTML → text)                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    REASONING PHASE                       │
├─────────────────────────────────────────────────────────┤
│ 5. Filter: Is email important? (criteria matching)      │
│ 6. Detect priority: high/medium/low (rule evaluation)   │
│ 7. Check duplicates: Already processed? (index lookup)  │
│ 8. Determine action: Create markdown or skip            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                     ACTION PHASE                         │
├─────────────────────────────────────────────────────────┤
│ 9. Generate markdown with frontmatter                    │
│ 10. Write file to Needs_Action folder                   │
│ 11. Update processed email index                        │
│ 12. Log operation to audit trail                        │
│ 13. Mark email as read in Gmail (optional)              │
└─────────────────────────────────────────────────────────┘
```

### Detailed Workflow

**Step 1: Authentication**
- Authenticate with Gmail API using OAuth 2.0
- Refresh token if expired
- Handle authentication errors gracefully

**Step 2: Email Retrieval**
- Query Gmail for unread emails: `is:unread in:inbox`
- Fetch up to 50 emails per poll
- Extract full email content including HTML body

**Step 3: Importance Filtering**
- Check sender against whitelist
- Search subject/body for keyword patterns (case-insensitive)
- Check for required Gmail labels
- Use OR logic: match any criterion

**Step 4: Priority Detection**
- **High Priority**: Contains urgent keywords OR from VIP sender OR has high-priority labels
- **Medium Priority**: Contains medium-priority keywords OR doesn't match high criteria
- **Low Priority**: Default when no other criteria match

**Step 5: Duplicate Prevention**
- Check email ID against processed index (`.index/gmail-watcher-processed.json`)
- Skip if already processed
- Log skip event

**Step 6: Markdown Generation**
- Convert HTML body to markdown
- Generate frontmatter with all metadata
- Create unique filename: `YYYYMMDD_HHMMSS_sanitized-subject.md`
- Write to `Needs_Action` folder

**Step 7: Index Update**
- Add email ID to processed index
- Record filename and timestamp
- Persist index to disk

**Step 8: Audit Logging**
- Log polling initiation
- Log important email detection
- Log markdown file creation
- Log any errors encountered

## Outputs

### Markdown File Format

```markdown
---
email_id: "18d4f2a3b5c6e7f8"
sender: "John Doe <john@example.com>"
sender_email: "john@example.com"
sender_name: "John Doe"
subject: "Q1 Report Review Needed"
date: "2026-02-14T09:30:00Z"
priority: "high"
labels: ["INBOX", "IMPORTANT"]
processed_at: "2026-02-14T09:35:00Z"
source: "gmail"
type: "email_task"
status: "pending"
---

# Email: Q1 Report Review Needed

**From**: John Doe <john@example.com>  
**Date**: February 14, 2026 9:30 AM  
**Priority**: 🔴 High  
**Labels**: INBOX, IMPORTANT

## Email Content

Hi there,

Could you please review the Q1 report by end of week? 
Let me know if you have any questions.

Thanks,
John

---

## Action Items

- [ ] Review Q1 report
- [ ] Provide feedback to John
- [ ] Reply by end of week

## Links

- [View in Gmail](https://mail.google.com/mail/u/0/#inbox/18d4f2a3b5c6e7f8)

---

*Processed by Gmail Watcher Skill v1.0.0*
```

### Processed Email Index

```json
{
  "18d4f2a3b5c6e7f8": {
    "filename": "20260214_093500_q1-report-review-needed.md",
    "processedAt": "2026-02-14T09:35:00Z",
    "priority": "high"
  },
  "19e5g3b4c6d7e8f9": {
    "filename": "20260214_100000_meeting-tomorrow.md",
    "processedAt": "2026-02-14T10:00:00Z",
    "priority": "medium"
  }
}
```

### Audit Log

```json
{"timestamp":"2026-02-14T09:35:00Z","level":"INFO","message":"Polling cycle initiated","context":{"interval":300000}}
{"timestamp":"2026-02-14T09:35:01Z","level":"INFO","message":"Retrieved 3 unread emails","context":{"count":3}}
{"timestamp":"2026-02-14T09:35:02Z","level":"INFO","message":"Important email detected","context":{"emailId":"18d4f2a3b5c6e7f8","sender":"john@example.com","subject":"Q1 Report Review Needed","priority":"high"}}
{"timestamp":"2026-02-14T09:35:03Z","level":"INFO","message":"Markdown file created","context":{"emailId":"18d4f2a3b5c6e7f8","filename":"20260214_093500_q1-report-review-needed.md","path":"Needs_Action/20260214_093500_q1-report-review-needed.md"}}
{"timestamp":"2026-02-14T09:35:04Z","level":"INFO","message":"Polling cycle completed","context":{"processed":1,"filtered":2,"created":1,"errors":0}}
```

## Postconditions

**Guaranteed**:
- All unread important emails are detected within polling interval
- Each important email creates exactly one markdown file
- All markdown files contain complete metadata and content
- Processed email index is updated
- All operations are logged to audit trail
- No duplicate files are created

**Side Effects**:
- Emails may be marked as read in Gmail (if configured)
- Disk space used for markdown files and logs
- Gmail API quota consumed

## Error Handling

### Error Categories

**1. Authentication Errors**
- **Symptom**: OAuth token expired or invalid
- **Response**: Log error, notify user, halt polling
- **Recovery**: User must re-authenticate manually
- **Log Level**: ERROR

**2. Network Errors**
- **Symptom**: Connection timeout, DNS failure
- **Response**: Retry with exponential backoff (1s, 2s, 4s, 8s, 16s, 32s, 60s max)
- **Recovery**: Automatic retry up to 7 attempts
- **Log Level**: WARN (transient), ERROR (persistent)

**3. Rate Limit Errors**
- **Symptom**: Gmail API quota exceeded
- **Response**: Pause requests, wait for retry-after duration
- **Recovery**: Automatic resume after delay
- **Log Level**: WARN

**4. API Errors (4xx/5xx)**
- **Symptom**: Invalid request or server error
- **Response**: 
  - 4xx: Log and skip
  - 5xx: Retry up to 3 times
- **Recovery**: Automatic for 5xx, skip for 4xx
- **Log Level**: ERROR

**5. Data Validation Errors**
- **Symptom**: Malformed API response, missing fields
- **Response**: Log error, skip problematic email
- **Recovery**: Automatic - continue with remaining emails
- **Log Level**: WARN

**6. File System Errors**
- **Symptom**: Permission denied, disk full
- **Response**: Log error, attempt fallback location
- **Recovery**: Manual intervention if critical
- **Log Level**: ERROR

**7. Configuration Errors**
- **Symptom**: Missing or invalid config file
- **Response**: Log warning, use default values
- **Recovery**: Automatic - fall back to defaults
- **Log Level**: WARN

### Error Handling Example

```json
{
  "timestamp": "2026-02-14T09:35:05Z",
  "level": "ERROR",
  "message": "Network timeout while fetching emails",
  "context": {
    "error": "NetworkError",
    "attempt": 1,
    "maxAttempts": 7,
    "nextRetryIn": "1000ms"
  },
  "stackTrace": "NetworkError: Connection timeout after 30 seconds\n    at MCPClient.fetchUnreadEmails..."
}
```

## Correctness Properties

This skill implements 23 correctness properties validated through property-based testing:

### Core Properties

1. **Complete Email Retrieval**: All unread emails are retrieved
2. **Complete Metadata Extraction**: All required fields are extracted
3. **Email Filter Criteria Evaluation**: Filters work correctly with OR logic
4. **Non-Important Email Exclusion**: Non-important emails are skipped
5. **Priority Level Assignment**: Exactly one priority assigned per email
6. **High Priority Detection**: Urgent emails get high priority
7. **Default Priority Assignment**: All emails get a priority
8. **Markdown File Creation**: One file per important email
9. **Complete Markdown Content**: All metadata included in frontmatter
10. **Unique Filename Generation**: No filename collisions
11. **HTML to Markdown Conversion**: Content structure preserved
12. **Idempotent Email Processing**: No duplicate files created

### Error Handling Properties

13. **Network Error Retry with Backoff**: Exponential backoff implemented
14. **Malformed Data Handling**: Bad data doesn't crash system
15. **Comprehensive Error Logging**: All errors logged with context

### System Properties

16. **Request Count Tracking**: Rate limits respected
17. **Operation Logging Completeness**: All operations logged
18. **Log Entry Structure**: Logs have consistent format
19. **Configuration Application**: Config settings applied correctly
20. **MCP Protocol Request Format**: Requests follow MCP spec
21. **MCP Protocol Response Parsing**: Responses parsed correctly
22. **MCP Error Code Translation**: MCP errors mapped to internal types
23. **Duplicate Detection by Gmail ID**: Duplicates detected by ID

## MCP Integration

### Required MCP Server

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
        "gmail.get"
      ]
    }
  }
}
```

### MCP Tools Used

**gmail.authenticate()**
- Authenticate with Gmail API
- Returns: Authentication token
- Risk: Low (read-only)

**gmail.list(query, maxResults)**
- List emails matching query
- Query: `is:unread in:inbox`
- Returns: Array of email metadata
- Risk: Low (read-only)

**gmail.get(emailId)**
- Fetch full email content
- Returns: Email object with body
- Risk: Low (read-only)

**gmail.markRead(emailId)** (optional)
- Mark email as read
- Returns: Success boolean
- Risk: Medium (modifies Gmail)
- Requires: Explicit approval

## Performance

### Target Metrics

- **Polling Interval**: 5 minutes (configurable)
- **Processing Time**: < 10 seconds per email
- **API Calls**: < 100 per hour
- **Vault Writes**: < 50 per hour
- **Memory Usage**: < 100 MB
- **CPU Usage**: < 5% average

### Optimization Strategies

**Incremental Polling**:
- Track last processed timestamp
- Only fetch emails after last timestamp
- Reduces API calls

**Batch Processing**:
- Process multiple emails in single cycle
- Group similar operations
- Reduces overhead

**Caching**:
- Cache sender information
- Cache filter results
- Reduces redundant processing

## Testing

### Test Coverage

**Unit Tests** (20+ tests):
- Configuration loading (valid, missing, malformed)
- Authentication error handling
- Rate limit handling
- Server error retry logic
- Empty inbox handling
- Duplicate detection
- Filename generation edge cases
- Log file writing

**Property-Based Tests** (23 tests):
- One test per correctness property
- Minimum 100 iterations each
- Uses fast-check library
- Validates universal properties

**Integration Tests** (5+ tests):
- End-to-end polling cycle
- Error recovery scenarios
- Duplicate prevention
- Multi-email processing
- Configuration changes

## Usage

### Starting the Skill

```bash
# One-time poll (manual trigger)
node dist/main.js poll --config Skills/config/gmail_watcher_config.yaml

# Start continuous polling
node dist/main.js start --config Skills/config/gmail_watcher_config.yaml

# Stop polling
node dist/main.js stop
```

### Monitoring

**Check Logs**:
```bash
tail -f Logs/gmail_watcher/gmail-watcher.log
```

**View Processed Emails**:
```bash
ls -la Needs_Action/
```

**Check Index**:
```bash
cat .index/gmail-watcher-processed.json | jq
```

### Troubleshooting

**No emails detected**:
- Check importance criteria in config
- Verify Gmail API authentication
- Check audit log for errors

**Duplicate files created**:
- Check index file integrity
- Rebuild index: `node dist/main.js rebuild-index`

**Rate limit errors**:
- Increase polling interval
- Reduce max emails per poll
- Check rate limit config

## Dependencies

**Required**:
- Node.js 18+
- TypeScript 5+
- Gmail API access
- MCP server implementation

**NPM Packages**:
- `fast-check`: Property-based testing
- `js-yaml`: Configuration parsing
- `turndown`: HTML to markdown conversion
- `googleapis`: Gmail API client (for MCP server)

**Optional**:
- Git for version control
- Obsidian Dataview plugin
- Obsidian Tasks plugin

## Security and Privacy

### Data Privacy

**Local-First**:
- All email content stays in local vault
- No cloud storage or external services
- User controls data retention

**Sensitive Content**:
- Passwords and tokens redacted from logs
- Email addresses can be anonymized
- User can exclude specific senders

### Security Measures

**OAuth 2.0**:
- No password storage
- Credentials stored locally
- Token refresh automatic

**Rate Limiting**:
- Prevents API abuse
- Respects Gmail quotas
- Exponential backoff

**Audit Trail**:
- All operations logged
- Immutable log files
- Easy to review and debug

## Future Enhancements

### Planned Features

1. **Smart Replies**: Generate draft responses
2. **Thread Tracking**: Group related emails
3. **Attachment Processing**: Download and index attachments
4. **Calendar Integration**: Auto-create events from invites
5. **Contact Management**: Build contact database
6. **Email Search**: Full-text search across archived emails
7. **Mobile Notifications**: Push alerts for high-priority
8. **Multi-Account Support**: Monitor multiple Gmail accounts

### Research Areas

- Natural language understanding for categorization
- Predictive filtering based on past behavior
- Automated response generation
- Email sentiment analysis
- Priority prediction using ML

## Approval Required

This skill requires approval for:
- Gmail API access and OAuth permissions
- Automatic email processing
- File creation in vault
- Optional email marking as read

**Risk Assessment**: Medium
- Read access to Gmail (privacy concern)
- Automatic file creation (vault modification)
- API quota usage (cost concern)
- Potential for false positives (noise)

**Mitigation**:
- User controls importance criteria
- Duplicate prevention ensures no spam
- Comprehensive logging for audit
- Can be disabled at any time

---

**Status**: DRAFT  
**Spec Reference**: `.kiro/specs/gmail-watcher-skill/`  
**Implementation**: See tasks.md for implementation plan  
**Next Steps**: Review skill, approve, implement according to spec
