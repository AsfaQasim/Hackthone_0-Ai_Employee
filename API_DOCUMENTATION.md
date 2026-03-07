# 📡 API Documentation: Personal AI Employee

## Overview

This document provides comprehensive API documentation for all components of the Personal AI Employee system.

## Table of Contents

1. [Watchers API](#watchers-api)
2. [Agent Skills API](#agent-skills-api)
3. [MCP Servers API](#mcp-servers-api)
4. [Utility Functions](#utility-functions)
5. [Data Schemas](#data-schemas)

---

## Watchers API

### BaseWatcher

Base class for all watchers. Provides common functionality for monitoring external systems.

**Location**: `Skills/base_watcher.py`

#### Constructor

```python
BaseWatcher(vault_path: str, check_interval: int = 60)
```

**Parameters**:
- `vault_path` (str): Path to Obsidian vault
- `check_interval` (int): Polling interval in seconds (default: 60)

**Attributes**:
- `vault_path` (Path): Vault directory path
- `needs_action` (Path): Needs_Action folder path
- `check_interval` (int): Polling frequency
- `logger` (Logger): Python logger instance

#### Methods

##### check_for_updates()

```python
@abstractmethod
def check_for_updates(self) -> list:
    """Return list of new items to process"""
    pass
```

**Returns**: List of new items detected

**Raises**: `NotImplementedError` if not overridden

##### create_action_file()

```python
@abstractmethod
def create_action_file(self, item) -> Path:
    """Create .md file in Needs_Action folder"""
    pass
```

**Parameters**:
- `item`: Item to process (type varies by watcher)

**Returns**: Path to created file

**Raises**: `NotImplementedError` if not overridden


##### run()

```python
def run(self):
    """Main watcher loop"""
```

Continuously polls for updates at `check_interval` frequency.

**Behavior**:
1. Calls `check_for_updates()`
2. For each item, calls `create_action_file()`
3. Logs errors without crashing
4. Sleeps for `check_interval` seconds
5. Repeats indefinitely

---

### GmailWatcher

Monitors Gmail for important emails.

**Location**: `Skills/gmail_watcher.py`

#### Constructor

```python
GmailWatcher(vault_path: str, credentials_path: str)
```

**Parameters**:
- `vault_path` (str): Path to Obsidian vault
- `credentials_path` (str): Path to Gmail credentials JSON

#### Methods

##### authenticate()

```python
def authenticate(self) -> Credentials:
    """Perform OAuth authentication"""
```

**Returns**: Google OAuth credentials

**Side Effects**: Creates `config/gmail-token.json`

##### check_for_updates()

```python
def check_for_updates(self) -> list:
    """Check for new important emails"""
```

**Returns**: List of message dictionaries

**Query**: `is:unread is:important`

##### create_action_file()

```python
def create_action_file(self, message) -> Path:
    """Create email task file"""
```

**Parameters**:
- `message` (dict): Gmail message object

**Returns**: Path to created markdown file

**File Format**:
```markdown
---
type: email
from: sender@example.com
subject: Email Subject
received: 2026-03-04T10:30:00Z
priority: high
status: pending
---

## Email Content
[Email snippet]

## Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
```


---

### WhatsAppWatcher

Monitors WhatsApp Web for urgent messages.

**Location**: `Skills/whatsapp_watcher.py`

#### Constructor

```python
WhatsAppWatcher(vault_path: str, session_path: str)
```

**Parameters**:
- `vault_path` (str): Path to Obsidian vault
- `session_path` (str): Path to browser session directory

**Attributes**:
- `keywords` (list): Urgent keywords to detect

#### Methods

##### check_for_updates()

```python
def check_for_updates(self) -> list:
    """Check for new urgent WhatsApp messages"""
```

**Returns**: List of message dictionaries

**Detection**: Messages containing keywords: `urgent`, `asap`, `invoice`, `payment`, `help`

##### create_action_file()

```python
def create_action_file(self, message) -> Path:
    """Create WhatsApp task file"""
```

**Parameters**:
- `message` (dict): WhatsApp message object

**Returns**: Path to created markdown file

---

### LinkedInWatcher

Monitors LinkedIn for business opportunities.

**Location**: `Skills/linkedin_watcher_simple.py`

#### Constructor

```python
LinkedInWatcher(vault_path: str, session_path: str)
```

**Parameters**:
- `vault_path` (str): Path to Obsidian vault
- `session_path` (str): Path to browser session directory

#### Methods

##### check_for_updates()

```python
def check_for_updates(self) -> list:
    """Check for new LinkedIn notifications"""
```

**Returns**: List of notification dictionaries

##### create_action_file()

```python
def create_action_file(self, notification) -> Path:
    """Create LinkedIn task file"""
```

**Parameters**:
- `notification` (dict): LinkedIn notification object

**Returns**: Path to created markdown file


---

## Agent Skills API

### Base Skill

Base class for all agent skills.

**Location**: `Skills/agent_skills/base_skill.py`

#### Constructor

```python
BaseSkill(name: str, description: str)
```

**Parameters**:
- `name` (str): Skill name
- `description` (str): Skill description

#### Methods

##### execute()

```python
@abstractmethod
def execute(self, context: dict) -> dict:
    """Execute the skill"""
    pass
```

**Parameters**:
- `context` (dict): Execution context

**Returns**: Result dictionary

---

### Draft Reply Skill

Drafts email or message replies.

**Location**: `Skills/agent_skills/draft_reply.py`

#### execute()

```python
def execute(self, context: dict) -> dict:
    """Draft a reply to email or message"""
```

**Parameters**:
- `context` (dict):
  - `message_type` (str): "email" or "whatsapp"
  - `original_message` (str): Original message content
  - `sender` (str): Sender name/email
  - `tone` (str): Reply tone (optional, default: "professional")

**Returns**:
- `draft` (str): Drafted reply
- `confidence` (float): Confidence score (0-1)
- `requires_approval` (bool): Whether approval needed

**Example**:
```python
result = draft_reply.execute({
    "message_type": "email",
    "original_message": "Can you send the invoice?",
    "sender": "client@example.com",
    "tone": "professional"
})
# Returns: {"draft": "...", "confidence": 0.95, "requires_approval": False}
```


---

### Summarize Task Skill

Summarizes tasks and messages.

**Location**: `Skills/agent_skills/summarize_task.py`

#### execute()

```python
def execute(self, context: dict) -> dict:
    """Summarize a task or message"""
```

**Parameters**:
- `context` (dict):
  - `content` (str): Content to summarize
  - `max_length` (int): Maximum summary length (optional, default: 200)

**Returns**:
- `summary` (str): Generated summary
- `key_points` (list): List of key points
- `action_items` (list): Extracted action items

---

### Create Plan Skill

Creates execution plans for multi-step tasks.

**Location**: `Skills/agent_skills/create_plan.py`

#### execute()

```python
def execute(self, context: dict) -> dict:
    """Create execution plan for task"""
```

**Parameters**:
- `context` (dict):
  - `task_description` (str): Task description
  - `constraints` (list): Constraints (optional)
  - `deadline` (str): Deadline (optional)

**Returns**:
- `plan` (str): Markdown formatted plan
- `steps` (list): List of step dictionaries
- `estimated_time` (int): Estimated completion time (minutes)

**Plan Format**:
```markdown
# Execution Plan: [Task Name]

## Objective
[Task description]

## Steps
1. [ ] Step 1 - Estimated: 10 minutes
2. [ ] Step 2 - Estimated: 15 minutes
3. [ ] Step 3 - Estimated: 5 minutes

## Total Estimated Time
30 minutes

## Dependencies
- Dependency 1
- Dependency 2

## Risks
- Risk 1: Mitigation strategy
- Risk 2: Mitigation strategy
```


---

## MCP Servers API

### Base MCP Server

Base framework for all MCP servers.

**Location**: `Skills/mcp_servers/base_mcp_server.py`

#### start_server()

```python
def start_server(port: int = 3000):
    """Start MCP server"""
```

**Parameters**:
- `port` (int): Server port (default: 3000)

**Behavior**: Starts HTTP server listening for MCP requests

---

### Email MCP Server

Handles email sending and drafting.

**Location**: `Skills/mcp_servers/email_mcp_server.py`

#### send_email()

```python
def send_email(to: str, subject: str, body: str, cc: list = None) -> dict:
    """Send email via Gmail"""
```

**Parameters**:
- `to` (str): Recipient email
- `subject` (str): Email subject
- `body` (str): Email body (HTML or plain text)
- `cc` (list): CC recipients (optional)

**Returns**:
- `success` (bool): Whether email sent successfully
- `message_id` (str): Gmail message ID
- `error` (str): Error message if failed

**Example**:
```python
result = send_email(
    to="client@example.com",
    subject="Invoice #123",
    body="Please find attached invoice.",
    cc=["manager@example.com"]
)
# Returns: {"success": True, "message_id": "abc123", "error": None}
```

#### draft_email()

```python
def draft_email(to: str, subject: str, body: str) -> dict:
    """Create email draft"""
```

**Parameters**: Same as `send_email()`

**Returns**:
- `success` (bool): Whether draft created
- `draft_id` (str): Gmail draft ID
- `error` (str): Error message if failed


---

### Social Media MCP Server

Handles social media posting.

**Location**: `Skills/mcp_servers/social_media_mcp_server.py`

#### post_to_linkedin()

```python
def post_to_linkedin(content: str, image_url: str = None) -> dict:
    """Post to LinkedIn"""
```

**Parameters**:
- `content` (str): Post content
- `image_url` (str): Image URL (optional)

**Returns**:
- `success` (bool): Whether post succeeded
- `post_id` (str): LinkedIn post ID
- `url` (str): Post URL
- `error` (str): Error message if failed

#### post_to_twitter()

```python
def post_to_twitter(content: str, image_url: str = None) -> dict:
    """Post to Twitter/X"""
```

**Parameters**: Same as `post_to_linkedin()`

**Returns**: Same as `post_to_linkedin()`

---

## Utility Functions

### Error Recovery

**Location**: `Skills/error_recovery.py`

#### with_retry()

```python
@with_retry(max_attempts=3, base_delay=1, max_delay=60)
def your_function():
    """Function with automatic retry"""
    pass
```

**Decorator Parameters**:
- `max_attempts` (int): Maximum retry attempts (default: 3)
- `base_delay` (int): Initial delay in seconds (default: 1)
- `max_delay` (int): Maximum delay in seconds (default: 60)

**Behavior**:
- Retries on transient errors
- Exponential backoff: delay = base_delay * (2 ** attempt)
- Caps delay at max_delay
- Raises exception after max_attempts

**Example**:
```python
@with_retry(max_attempts=5, base_delay=2, max_delay=120)
def fetch_data():
    response = requests.get("https://api.example.com/data")
    response.raise_for_status()
    return response.json()
```


---

### Audit Logger

**Location**: `Skills/audit_logger.py`

#### log_action()

```python
def log_action(
    action_type: str,
    actor: str,
    target: str,
    parameters: dict,
    result: str,
    approval_status: str = None
) -> None:
    """Log an action to audit trail"""
```

**Parameters**:
- `action_type` (str): Type of action (e.g., "email_send", "payment")
- `actor` (str): Who performed action (e.g., "claude_code", "human")
- `target` (str): Target of action (e.g., email address, account)
- `parameters` (dict): Action parameters
- `result` (str): "success" or "failure"
- `approval_status` (str): "approved", "rejected", or None

**Log Format**:
```json
{
  "timestamp": "2026-03-04T10:30:00Z",
  "action_type": "email_send",
  "actor": "claude_code",
  "target": "client@example.com",
  "parameters": {"subject": "Invoice #123"},
  "approval_status": "approved",
  "result": "success"
}
```

#### search_logs()

```python
def search_logs(
    start_date: str = None,
    end_date: str = None,
    action_type: str = None,
    actor: str = None
) -> list:
    """Search audit logs"""
```

**Parameters**:
- `start_date` (str): Start date (ISO format)
- `end_date` (str): End date (ISO format)
- `action_type` (str): Filter by action type
- `actor` (str): Filter by actor

**Returns**: List of matching log entries

---

### Approval Workflow

**Location**: `Skills/approval_workflow.py`

#### request_approval()

```python
def request_approval(
    action_type: str,
    details: dict,
    timeout_hours: int = 24
) -> str:
    """Request human approval for action"""
```

**Parameters**:
- `action_type` (str): Type of action requiring approval
- `details` (dict): Action details
- `timeout_hours` (int): Approval timeout (default: 24)

**Returns**: Approval request ID

**Side Effects**: Creates file in `/Pending_Approval/`

#### check_approval()

```python
def check_approval(request_id: str) -> str:
    """Check approval status"""
```

**Parameters**:
- `request_id` (str): Approval request ID

**Returns**: "approved", "rejected", "pending", or "expired"


---

## Data Schemas

### Task File Schema

All task files follow this frontmatter schema:

```yaml
---
type: email | whatsapp | linkedin | file_drop
from: sender_identifier
subject: task_subject (optional)
received: ISO_8601_timestamp
priority: low | medium | high | urgent
status: pending | in_progress | approved | done
---
```

### Email Task Schema

```yaml
---
type: email
from: sender@example.com
subject: Email Subject
received: 2026-03-04T10:30:00Z
priority: high
status: pending
message_id: gmail_message_id
---

## Email Content
[Email body or snippet]

## Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
```

### WhatsApp Task Schema

```yaml
---
type: whatsapp
from: Contact Name
received: 2026-03-04T10:30:00Z
priority: urgent
status: pending
keywords: [urgent, payment]
---

## Message Content
[WhatsApp message text]

## Suggested Actions
- [ ] Reply to sender
- [ ] Create task
- [ ] Forward to team
```

### Plan Schema

```yaml
---
type: plan
task_id: task_identifier
created: 2026-03-04T10:30:00Z
status: pending | in_progress | complete
estimated_time: 30 (minutes)
---

# Execution Plan: [Task Name]

## Objective
[Task description]

## Steps
1. [ ] Step 1 - Estimated: 10 minutes
2. [ ] Step 2 - Estimated: 15 minutes
3. [ ] Step 3 - Estimated: 5 minutes

## Dependencies
- Dependency 1

## Risks
- Risk 1: Mitigation
```


### Approval Request Schema

```yaml
---
type: approval_request
action: payment | email_send | social_post
amount: 500.00 (for payments)
recipient: target_identifier
reason: action_reason
created: 2026-03-04T10:30:00Z
expires: 2026-03-05T10:30:00Z
status: pending | approved | rejected | expired
---

## Action Details
[Detailed description of action]

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder.
```

### CEO Briefing Schema

```yaml
---
type: ceo_briefing
period_start: 2026-02-26
period_end: 2026-03-04
generated: 2026-03-04T07:00:00Z
---

# Monday Morning CEO Briefing

## Executive Summary
[High-level summary]

## Revenue
- This Week: $2,450
- MTD: $4,500 (45% of $10,000 target)
- Trend: On track

## Completed Tasks
- [x] Task 1
- [x] Task 2

## Bottlenecks
| Task | Expected | Actual | Delay |
|------|----------|--------|-------|
| Task | 2 days | 5 days | +3 days |

## Proactive Suggestions
- Suggestion 1
- Suggestion 2
```

---

## Error Codes

### Watcher Errors

| Code | Description | Resolution |
|------|-------------|------------|
| W001 | Authentication failed | Re-authenticate |
| W002 | Network timeout | Check internet connection |
| W003 | Rate limit exceeded | Wait and retry |
| W004 | Invalid credentials | Update credentials |

### MCP Server Errors

| Code | Description | Resolution |
|------|-------------|------------|
| M001 | Server not responding | Restart MCP server |
| M002 | Invalid parameters | Check API documentation |
| M003 | Permission denied | Check credentials |
| M004 | Resource not found | Verify resource exists |

### Skill Errors

| Code | Description | Resolution |
|------|-------------|------------|
| S001 | Invalid context | Provide required parameters |
| S002 | Execution failed | Check logs for details |
| S003 | Timeout | Increase timeout limit |
| S004 | Dependency missing | Install required dependencies |

---

## Rate Limits

### Gmail API
- Queries per day: 1,000,000,000
- Queries per 100 seconds: 250
- Queries per user per 100 seconds: 25

### WhatsApp Web
- No official limits
- Recommended: Max 50 messages/hour
- Risk of ban if exceeded

### LinkedIn API
- Posts per day: 100
- Requests per day: 500
- Requests per hour: 100

---

## Changelog

### v1.0.0 (2026-03-04)
- Initial Gold Tier release
- All core features implemented
- Complete API documentation

---

**Last Updated**: March 4, 2026  
**Version**: 1.0.0  
**Author**: Asfa Qasim  
**License**: MIT
