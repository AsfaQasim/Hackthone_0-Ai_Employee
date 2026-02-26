---
type: mcp_server_spec
status: draft
category: action
risk_level: high
created: 2026-02-15
requires_approval: true
mcp_server: gmail-action-server
---

# MCP Email Action Server Specification

## Overview

An MCP (Model Context Protocol) server that provides email capabilities with mandatory approval workflows, comprehensive audit logging, and dry-run testing mode.

## Purpose

Enable the Personal AI Employee to:
- Send emails via Gmail API
- Create draft emails for review
- Search emails and contacts
- Enforce approval requirements
- Log all email operations
- Test actions safely with dry-run mode

## Capabilities

### 1. Send Email
**Tool**: `email.send`  
**Risk**: HIGH  
**Approval**: Required for new contacts  
**Audit**: Full logging

### 2. Draft Email
**Tool**: `email.draft`  
**Risk**: LOW  
**Approval**: Not required  
**Audit**: Basic logging

### 3. Search Email
**Tool**: `email.search`  
**Risk**: LOW  
**Approval**: Not required  
**Audit**: Query logging

### 4. Approval Workflow
**Automatic**: Based on recipient status  
**Manual**: File-based approval system  
**Tracking**: Complete approval history

### 5. Audit Logging
**Level**: Comprehensive  
**Format**: JSON + Markdown  
**Retention**: Permanent  
**Compliance**: Export-ready

### 6. Dry Run Mode
**Purpose**: Test without sending  
**Scope**: All write operations  
**Output**: Simulated results  
**Safety**: No actual emails sent

## MCP Server Configuration

```json
{
  "mcpServers": {
    "gmail-action-server": {
      "command": "node",
      "args": ["./mcp-servers/gmail-action-server.js"],
      "env": {
        "GMAIL_CREDENTIALS_PATH": "./config/gmail-credentials.json",
        "GMAIL_TOKEN_PATH": "./config/gmail-token.json",
        "APPROVED_CONTACTS_PATH": "./config/approved-contacts.json",
        "AUDIT_LOG_PATH": "./Logs/email-audit.log",
        "DRY_RUN": "false"
      },
      "disabled": false,
      "autoApprove": [
        "email.search",
        "email.draft"
      ]
    }
  }
}
```

## MCP Tools

### email.send

**Purpose**: Send email via Gmail

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "to": {
      "type": "string",
      "description": "Recipient email address",
      "format": "email"
    },
    "subject": {
      "type": "string",
      "description": "Email subject line"
    },
    "body": {
      "type": "string",
      "description": "Email body (plain text or HTML)"
    },
    "cc": {
      "type": "array",
      "items": {"type": "string", "format": "email"},
      "description": "CC recipients (optional)"
    },
    "bcc": {
      "type": "array",
      "items": {"type": "string", "format": "email"},
      "description": "BCC recipients (optional)"
    },
    "attachments": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "filename": {"type": "string"},
          "path": {"type": "string"},
          "mimeType": {"type": "string"}
        }
      },
      "description": "File attachments (optional)"
    },
    "dry_run": {
      "type": "boolean",
      "description": "If true, simulate without sending",
      "default": false
    }
  },
  "required": ["to", "subject", "body"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "message_id": {"type": "string"},
    "sent_at": {"type": "string", "format": "date-time"},
    "approval_required": {"type": "boolean"},
    "approval_request_id": {"type": "string"},
    "dry_run": {"type": "boolean"},
    "audit_log_id": {"type": "string"}
  }
}
```

**Behavior**:
1. Check if recipient is in approved contacts
2. If new contact → Create approval request
3. If approved contact → Send immediately
4. If dry_run=true → Simulate only
5. Log all operations to audit trail
6. Return result with message ID

**Example Call**:
```json
{
  "tool": "email.send",
  "arguments": {
    "to": "client@example.com",
    "subject": "Project Update",
    "body": "Hi, here's the latest update on the project...",
    "dry_run": false
  }
}
```

**Example Response (New Contact)**:
```json
{
  "success": false,
  "approval_required": true,
  "approval_request_id": "email_20260215_104500",
  "approval_file": "/Pending_Approval/contacts/email_20260215_104500.md",
  "message": "Approval required for new contact: client@example.com",
  "audit_log_id": "audit_20260215_104500"
}
```

**Example Response (Approved Contact)**:
```json
{
  "success": true,
  "message_id": "18d4f2a3b5c6e7f8",
  "sent_at": "2026-02-15T10:45:00Z",
  "approval_required": false,
  "dry_run": false,
  "audit_log_id": "audit_20260215_104500"
}
```

**Example Response (Dry Run)**:
```json
{
  "success": true,
  "message_id": "DRY_RUN_18d4f2a3b5c6e7f8",
  "sent_at": "2026-02-15T10:45:00Z",
  "approval_required": false,
  "dry_run": true,
  "message": "DRY RUN: Email would be sent to client@example.com",
  "audit_log_id": "audit_20260215_104500"
}
```


### email.draft

**Purpose**: Create draft email (no sending)

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "to": {
      "type": "string",
      "description": "Recipient email address",
      "format": "email"
    },
    "subject": {
      "type": "string",
      "description": "Email subject line"
    },
    "body": {
      "type": "string",
      "description": "Email body (plain text or HTML)"
    },
    "cc": {
      "type": "array",
      "items": {"type": "string", "format": "email"}
    },
    "bcc": {
      "type": "array",
      "items": {"type": "string", "format": "email"}
    }
  },
  "required": ["to", "subject", "body"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "draft_id": {"type": "string"},
    "created_at": {"type": "string", "format": "date-time"},
    "draft_url": {"type": "string"},
    "audit_log_id": {"type": "string"}
  }
}
```

**Behavior**:
1. Create draft in Gmail
2. No approval required (not sending)
3. Log draft creation
4. Return draft ID and URL

**Example Call**:
```json
{
  "tool": "email.draft",
  "arguments": {
    "to": "client@example.com",
    "subject": "Project Update",
    "body": "Hi, here's the latest update..."
  }
}
```

**Example Response**:
```json
{
  "success": true,
  "draft_id": "r-1234567890",
  "created_at": "2026-02-15T10:45:00Z",
  "draft_url": "https://mail.google.com/mail/u/0/#drafts/r-1234567890",
  "audit_log_id": "audit_20260215_104500"
}
```

### email.search

**Purpose**: Search emails and contacts

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Gmail search query (e.g., 'from:user@example.com')"
    },
    "max_results": {
      "type": "integer",
      "description": "Maximum results to return",
      "default": 10,
      "minimum": 1,
      "maximum": 100
    },
    "include_body": {
      "type": "boolean",
      "description": "Include email body in results",
      "default": false
    }
  },
  "required": ["query"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "string"},
          "thread_id": {"type": "string"},
          "from": {"type": "string"},
          "to": {"type": "string"},
          "subject": {"type": "string"},
          "snippet": {"type": "string"},
          "date": {"type": "string", "format": "date-time"},
          "labels": {"type": "array", "items": {"type": "string"}},
          "body": {"type": "string"}
        }
      }
    },
    "total_count": {"type": "integer"},
    "audit_log_id": {"type": "string"}
  }
}
```

**Behavior**:
1. Execute Gmail search query
2. Return matching emails
3. Log search query (for audit)
4. No approval required (read-only)

**Example Call**:
```json
{
  "tool": "email.search",
  "arguments": {
    "query": "from:client@example.com subject:project",
    "max_results": 5,
    "include_body": false
  }
}
```

**Example Response**:
```json
{
  "success": true,
  "results": [
    {
      "id": "18d4f2a3b5c6e7f8",
      "thread_id": "18d4f2a3b5c6e7f8",
      "from": "client@example.com",
      "to": "me@example.com",
      "subject": "Project Update Request",
      "snippet": "Hi, can you send me an update on the project?",
      "date": "2026-02-15T09:30:00Z",
      "labels": ["INBOX", "UNREAD"]
    }
  ],
  "total_count": 1,
  "audit_log_id": "audit_20260215_104500"
}
```

### email.reply

**Purpose**: Reply to existing email

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "message_id": {
      "type": "string",
      "description": "ID of message to reply to"
    },
    "body": {
      "type": "string",
      "description": "Reply body"
    },
    "reply_all": {
      "type": "boolean",
      "description": "Reply to all recipients",
      "default": false
    },
    "dry_run": {
      "type": "boolean",
      "default": false
    }
  },
  "required": ["message_id", "body"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "message_id": {"type": "string"},
    "sent_at": {"type": "string", "format": "date-time"},
    "approval_required": {"type": "boolean"},
    "dry_run": {"type": "boolean"},
    "audit_log_id": {"type": "string"}
  }
}
```

**Behavior**:
1. Get original message
2. Check if sender is approved contact
3. If approved → Send reply
4. If new → Require approval
5. Log operation

### email.get_contacts

**Purpose**: Get approved contacts list

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "filter": {
      "type": "string",
      "description": "Filter contacts by email or name"
    }
  }
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "contacts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "email": {"type": "string"},
          "name": {"type": "string"},
          "added_at": {"type": "string", "format": "date-time"},
          "email_count": {"type": "integer"}
        }
      }
    },
    "total_count": {"type": "integer"}
  }
}
```

**Behavior**:
1. Read approved contacts file
2. Filter if requested
3. Return contact list
4. No approval required (read-only)

### email.add_contact

**Purpose**: Add contact to approved list

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "email": {
      "type": "string",
      "format": "email"
    },
    "name": {
      "type": "string"
    }
  },
  "required": ["email"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "contact": {
      "type": "object",
      "properties": {
        "email": {"type": "string"},
        "name": {"type": "string"},
        "added_at": {"type": "string", "format": "date-time"}
      }
    },
    "audit_log_id": {"type": "string"}
  }
}
```

**Behavior**:
1. Add email to approved contacts
2. Save to contacts file
3. Log addition
4. Return confirmation

## Approval Workflow

### Approval Decision Logic

```python
def requires_approval(recipient: str) -> bool:
    """Check if email requires approval"""
    
    # Load approved contacts
    approved = load_approved_contacts()
    
    # Check if recipient is approved
    if recipient in approved:
        return False  # Auto-approve
    
    # New contact requires approval
    return True

def create_approval_request(email_data: dict) -> str:
    """Create approval request file"""
    
    request_id = generate_request_id()
    
    # Create approval request markdown
    request = f"""---
type: email_approval
request_id: {request_id}
recipient: {email_data['to']}
contact_status: new
created: {datetime.now().isoformat()}
---

# Email Approval: {email_data['subject']}

## Recipient
**Email**: {email_data['to']}
**Status**: ⚠️ NEW CONTACT

## Draft Email

**Subject**: {email_data['subject']}

**Body**:
{email_data['body']}

## How to Approve

✅ **Approve**: Move to `/Approved/contacts/`
❌ **Reject**: Move to `/Rejected/contacts/`
✏️ **Edit**: Modify and keep in `/Pending_Approval/contacts/`
"""
    
    # Save to Pending_Approval
    filepath = f"/Pending_Approval/contacts/{request_id}.md"
    save_file(filepath, request)
    
    return request_id
```

### Approval Detection

```python
def watch_approval_folders():
    """Watch for approval decisions"""
    
    watcher = FileSystemWatcher()
    
    @watcher.on_file_moved
    def handle_move(event):
        source = event.source_path
        dest = event.dest_path
        
        if "Pending_Approval" in source:
            if "Approved" in dest:
                # Execute approved action
                request = parse_request(dest)
                execute_email_send(request)
                log_approval(request, "approved")
                
            elif "Rejected" in dest:
                # Cancel action
                request = parse_request(dest)
                log_approval(request, "rejected")
    
    watcher.start()
```

## Audit Logging

### Log Format

**JSON Log** (`/Logs/email-audit.log`):
```json
{
  "timestamp": "2026-02-15T10:45:00Z",
  "log_id": "audit_20260215_104500",
  "action": "email.send",
  "user": "ai_employee",
  "recipient": "client@example.com",
  "subject": "Project Update",
  "approval_required": true,
  "approval_status": "pending",
  "approval_request_id": "email_20260215_104500",
  "dry_run": false,
  "success": false,
  "message": "Approval required for new contact",
  "metadata": {
    "cc": [],
    "bcc": [],
    "attachments": 0,
    "body_length": 245
  }
}
```

**Markdown Log** (`/Logs/email-audit-YYYYMMDD.md`):
```markdown
## 2026-02-15 10:45:00 - Email Send Attempt

**Action**: email.send  
**Recipient**: client@example.com  
**Subject**: Project Update  
**Approval Required**: Yes (new contact)  
**Status**: Pending approval  
**Request ID**: email_20260215_104500  
**Dry Run**: No

### Details
- Body length: 245 characters
- Attachments: 0
- CC: None
- BCC: None

### Outcome
Approval request created at `/Pending_Approval/contacts/email_20260215_104500.md`
```

### Log Levels

1. **INFO**: Successful operations
2. **WARN**: Approval required, rate limits
3. **ERROR**: Failed operations, exceptions
4. **AUDIT**: All write operations (send, draft)

### Log Retention

- **JSON logs**: Append-only, permanent
- **Markdown logs**: Daily files, permanent
- **Rotation**: None (keep all logs)
- **Export**: JSON format for compliance


## Dry Run Mode

### Purpose

Test email operations without actually sending emails. Useful for:
- Testing email templates
- Validating approval workflows
- Debugging email logic
- Training and demonstrations

### Activation

**Method 1: Environment Variable**
```bash
export DRY_RUN=true
node mcp-servers/gmail-action-server.js
```

**Method 2: Per-Request**
```json
{
  "tool": "email.send",
  "arguments": {
    "to": "test@example.com",
    "subject": "Test",
    "body": "This is a test",
    "dry_run": true
  }
}
```

**Method 3: Configuration File**
```json
{
  "mcpServers": {
    "gmail-action-server": {
      "env": {
        "DRY_RUN": "true"
      }
    }
  }
}
```

### Behavior in Dry Run Mode

**email.send**:
- ✅ Validates input parameters
- ✅ Checks approval requirements
- ✅ Creates approval requests (if needed)
- ✅ Logs operation
- ❌ Does NOT send actual email
- ✅ Returns simulated message ID
- ✅ Returns success response

**email.draft**:
- ✅ Validates input parameters
- ✅ Logs operation
- ❌ Does NOT create actual draft
- ✅ Returns simulated draft ID

**email.reply**:
- ✅ Validates message ID exists
- ✅ Checks approval requirements
- ✅ Logs operation
- ❌ Does NOT send actual reply
- ✅ Returns simulated message ID

**email.search**:
- ✅ Executes actual search (read-only)
- ✅ Returns real results
- ✅ Logs operation

**email.get_contacts**:
- ✅ Returns actual contacts (read-only)
- ✅ Logs operation

**email.add_contact**:
- ✅ Validates input
- ✅ Logs operation
- ❌ Does NOT modify contacts file
- ✅ Returns simulated success

### Dry Run Indicators

All dry run responses include:
```json
{
  "dry_run": true,
  "message": "DRY RUN: [description of what would happen]"
}
```

Message IDs in dry run mode:
- Prefixed with `DRY_RUN_`
- Example: `DRY_RUN_18d4f2a3b5c6e7f8`

### Dry Run Logging

Logs clearly indicate dry run mode:
```json
{
  "timestamp": "2026-02-15T10:45:00Z",
  "action": "email.send",
  "dry_run": true,
  "message": "DRY RUN: Would send email to client@example.com",
  "simulated_message_id": "DRY_RUN_18d4f2a3b5c6e7f8"
}
```

## Implementation

### Server Structure

```javascript
// gmail-action-server.js

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

class GmailActionServer {
  constructor() {
    this.server = new Server({
      name: 'gmail-action-server',
      version: '1.0.0'
    }, {
      capabilities: {
        tools: {}
      }
    });
    
    this.dryRun = process.env.DRY_RUN === 'true';
    this.approvedContacts = this.loadApprovedContacts();
    this.auditLogger = new AuditLogger();
    
    this.setupTools();
  }
  
  loadApprovedContacts() {
    const contactsPath = process.env.APPROVED_CONTACTS_PATH;
    if (fs.existsSync(contactsPath)) {
      return JSON.parse(fs.readFileSync(contactsPath, 'utf8'));
    }
    return [];
  }
  
  setupTools() {
    // Register email.send tool
    this.server.setRequestHandler('tools/call', async (request) => {
      const { name, arguments: args } = request.params;
      
      switch (name) {
        case 'email.send':
          return await this.handleSend(args);
        case 'email.draft':
          return await this.handleDraft(args);
        case 'email.search':
          return await this.handleSearch(args);
        case 'email.reply':
          return await this.handleReply(args);
        case 'email.get_contacts':
          return await this.handleGetContacts(args);
        case 'email.add_contact':
          return await this.handleAddContact(args);
        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    });
    
    // Register tool list
    this.server.setRequestHandler('tools/list', async () => {
      return {
        tools: [
          {
            name: 'email.send',
            description: 'Send email via Gmail',
            inputSchema: { /* schema */ }
          },
          {
            name: 'email.draft',
            description: 'Create draft email',
            inputSchema: { /* schema */ }
          },
          {
            name: 'email.search',
            description: 'Search emails',
            inputSchema: { /* schema */ }
          },
          {
            name: 'email.reply',
            description: 'Reply to email',
            inputSchema: { /* schema */ }
          },
          {
            name: 'email.get_contacts',
            description: 'Get approved contacts',
            inputSchema: { /* schema */ }
          },
          {
            name: 'email.add_contact',
            description: 'Add approved contact',
            inputSchema: { /* schema */ }
          }
        ]
      };
    });
  }
  
  async handleSend(args) {
    const { to, subject, body, cc, bcc, attachments, dry_run } = args;
    const isDryRun = dry_run || this.dryRun;
    
    // Check approval requirement
    const requiresApproval = !this.approvedContacts.includes(to);
    
    if (requiresApproval) {
      // Create approval request
      const requestId = this.createApprovalRequest({
        to, subject, body, cc, bcc, attachments
      });
      
      // Log
      this.auditLogger.log({
        action: 'email.send',
        recipient: to,
        subject,
        approval_required: true,
        approval_request_id: requestId,
        dry_run: isDryRun
      });
      
      return {
        success: false,
        approval_required: true,
        approval_request_id: requestId,
        approval_file: `/Pending_Approval/contacts/${requestId}.md`,
        message: `Approval required for new contact: ${to}`
      };
    }
    
    // Send email (or simulate)
    let messageId;
    if (isDryRun) {
      messageId = `DRY_RUN_${Date.now()}`;
      this.auditLogger.log({
        action: 'email.send',
        recipient: to,
        subject,
        dry_run: true,
        simulated_message_id: messageId,
        message: `DRY RUN: Would send email to ${to}`
      });
    } else {
      messageId = await this.sendEmailViaGmail({
        to, subject, body, cc, bcc, attachments
      });
      this.auditLogger.log({
        action: 'email.send',
        recipient: to,
        subject,
        message_id: messageId,
        success: true
      });
    }
    
    return {
      success: true,
      message_id: messageId,
      sent_at: new Date().toISOString(),
      approval_required: false,
      dry_run: isDryRun
    };
  }
  
  async handleDraft(args) {
    const { to, subject, body, cc, bcc } = args;
    
    let draftId;
    if (this.dryRun) {
      draftId = `DRY_RUN_DRAFT_${Date.now()}`;
      this.auditLogger.log({
        action: 'email.draft',
        recipient: to,
        subject,
        dry_run: true,
        simulated_draft_id: draftId
      });
    } else {
      draftId = await this.createDraftViaGmail({
        to, subject, body, cc, bcc
      });
      this.auditLogger.log({
        action: 'email.draft',
        recipient: to,
        subject,
        draft_id: draftId,
        success: true
      });
    }
    
    return {
      success: true,
      draft_id: draftId,
      created_at: new Date().toISOString(),
      draft_url: `https://mail.google.com/mail/u/0/#drafts/${draftId}`
    };
  }
  
  async handleSearch(args) {
    const { query, max_results, include_body } = args;
    
    // Execute search (always real, even in dry run)
    const results = await this.searchViaGmail(query, max_results, include_body);
    
    this.auditLogger.log({
      action: 'email.search',
      query,
      results_count: results.length,
      success: true
    });
    
    return {
      success: true,
      results,
      total_count: results.length
    };
  }
  
  createApprovalRequest(emailData) {
    const requestId = `email_${Date.now()}`;
    const content = `---
type: email_approval
request_id: ${requestId}
recipient: ${emailData.to}
contact_status: new
created: ${new Date().toISOString()}
---

# Email Approval: ${emailData.subject}

## Recipient
**Email**: ${emailData.to}
**Status**: ⚠️ NEW CONTACT

## Draft Email

**Subject**: ${emailData.subject}

**Body**:
${emailData.body}

## How to Approve

✅ **Approve**: Move to \`/Approved/contacts/\`
❌ **Reject**: Move to \`/Rejected/contacts/\`
✏️ **Edit**: Modify and keep in \`/Pending_Approval/contacts/\`
`;
    
    const filepath = path.join(
      process.cwd(),
      'Pending_Approval',
      'contacts',
      `${requestId}.md`
    );
    
    fs.mkdirSync(path.dirname(filepath), { recursive: true });
    fs.writeFileSync(filepath, content);
    
    return requestId;
  }
  
  async sendEmailViaGmail(emailData) {
    // Actual Gmail API implementation
    const gmail = google.gmail({ version: 'v1', auth: this.auth });
    
    const message = this.createMimeMessage(emailData);
    const result = await gmail.users.messages.send({
      userId: 'me',
      requestBody: {
        raw: Buffer.from(message).toString('base64')
      }
    });
    
    return result.data.id;
  }
  
  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Gmail Action MCP Server running on stdio');
  }
}

// Start server
const server = new GmailActionServer();
server.run().catch(console.error);
```

### Audit Logger

```javascript
class AuditLogger {
  constructor() {
    this.logPath = process.env.AUDIT_LOG_PATH || './Logs/email-audit.log';
    this.ensureLogDirectory();
  }
  
  ensureLogDirectory() {
    const dir = path.dirname(this.logPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }
  
  log(entry) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      log_id: `audit_${Date.now()}`,
      ...entry
    };
    
    // Append to JSON log
    fs.appendFileSync(
      this.logPath,
      JSON.stringify(logEntry) + '\n'
    );
    
    // Also write to daily markdown log
    this.writeMarkdownLog(logEntry);
  }
  
  writeMarkdownLog(entry) {
    const date = new Date().toISOString().split('T')[0];
    const mdPath = `./Logs/email-audit-${date}.md`;
    
    const mdEntry = `
## ${entry.timestamp} - ${entry.action}

**Action**: ${entry.action}
**Recipient**: ${entry.recipient || 'N/A'}
**Subject**: ${entry.subject || 'N/A'}
**Success**: ${entry.success ? 'Yes' : 'No'}
**Dry Run**: ${entry.dry_run ? 'Yes' : 'No'}
${entry.approval_required ? `**Approval Required**: Yes\n**Request ID**: ${entry.approval_request_id}` : ''}

${entry.message ? `### Message\n${entry.message}\n` : ''}
---
`;
    
    fs.appendFileSync(mdPath, mdEntry);
  }
}
```

## Security and Safety

### Authentication
- OAuth 2.0 with Gmail API
- Credentials stored locally
- Token refresh automatic
- No password storage

### Authorization
- Approval required for new contacts
- File-based approval workflow
- Human-in-the-loop enforcement
- Complete audit trail

### Data Privacy
- All data stays local
- No external logging services
- Emails not stored by server
- Audit logs encrypted (optional)

### Rate Limiting
- Respect Gmail API quotas
- Exponential backoff on errors
- Max 100 emails per hour (configurable)
- Dry run mode for testing

## Testing

### Unit Tests
- Tool input validation
- Approval logic
- Dry run simulation
- Audit logging

### Integration Tests
- Gmail API authentication
- Email sending
- Draft creation
- Search functionality
- Approval workflow

### End-to-End Tests
- Complete send workflow
- Approval and execution
- Error handling
- Dry run mode

## Deployment

### Prerequisites
1. Gmail API enabled
2. OAuth credentials downloaded
3. Node.js 18+ installed
4. MCP SDK installed

### Installation
```bash
npm install @modelcontextprotocol/sdk googleapis
```

### Configuration
1. Place credentials in `config/gmail-credentials.json`
2. Run initial OAuth flow
3. Configure approved contacts
4. Set up audit log directory

### Running
```bash
# Production mode
node mcp-servers/gmail-action-server.js

# Dry run mode
DRY_RUN=true node mcp-servers/gmail-action-server.js
```

## Monitoring

### Health Checks
- Server responsiveness
- Gmail API connectivity
- Audit log writing
- Approval folder access

### Metrics
- Emails sent per hour
- Approval rate
- Dry run usage
- Error rate
- Response time

### Alerts
- Authentication failures
- Rate limit exceeded
- Audit log write failures
- Approval queue buildup

---

**Status**: DRAFT  
**Next Steps**:
1. Review specification
2. Approve MCP server design
3. Implement server
4. Test with dry run mode
5. Deploy with monitoring

