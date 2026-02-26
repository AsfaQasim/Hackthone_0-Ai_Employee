# 📡 How MCP Server Works with Gmail Watcher

## 🏗️ Complete Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   PERCEPTION LAYER                           │
│                                                              │
│  Gmail Watcher                                               │
│  - Monitors Gmail API                                        │
│  - Fetches unread emails                                     │
│  - Creates markdown files in Inbox/                          │
│  - Detects priority (High/Medium/Low)                        │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ Creates .md files
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   STORAGE LAYER (Vault)                      │
│                                                              │
│  Inbox/                                                      │
│  ├── email_001.md (task from Gmail)                         │
│  ├── email_002.md                                           │
│  └── email_003.md                                           │
│                                                              │
│  Each file contains:                                         │
│  - Email metadata (sender, subject, priority)               │
│  - Email content                                            │
│  - Action items                                             │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ Files to process
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   REASONING LAYER (AI)                       │
│                                                              │
│  Agent Skills:                                               │
│  - summarize_task() - Creates summary                        │
│  - create_plan() - Creates action plan                       │
│  - draft_reply() - Drafts email response                     │
│                                                              │
│  Output:                                                     │
│  - Task summary                                              │
│  - Execution plan                                            │
│  - Draft reply                                               │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ Decision to send email
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   ACTION LAYER (MCP Server)                  │
│                                                              │
│  Email MCP Server                                            │
│  - Tool: send_email                                          │
│  - Connects to Gmail API                                     │
│  - Sends actual email                                        │
│  - Returns success/failure                                   │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ API call
                     ▼
                  Gmail API
                  (Sends email)
```

---

## 📋 Step-by-Step Workflow

### **Step 1: Gmail Watcher - Perception**

```bash
# Run Gmail Watcher
python Skills/gmail_watcher.py poll
```

**What happens:**
1. Connects to Gmail API
2. Fetches unread emails
3. Filters important ones
4. Creates markdown files

**Output file:** `Inbox/email_20260226_meeting.md`

```markdown
---
type: email_task
sender: "boss@company.com"
subject: "Team Meeting"
priority: "high"
---

# Email: Team Meeting

**From**: boss@company.com
**Priority**: 🔴 High

## Content
Please schedule a team meeting for next week...

## Action Items
- [ ] Schedule meeting
- [ ] Send invites
```

---

### **Step 2: Agent Skills - Reasoning**

```python
from Skills.agent_skills import summarize_task, create_plan, draft_reply

# Read and summarize
summary = summarize_task("Inbox/email_20260226_meeting.md")
# Output: "Boss requests team meeting scheduling for next week. High priority."

# Create plan
plan_path = create_plan("Inbox/email_20260226_meeting.md")
# Output: Plans/plan_20260226.md with steps

# Draft reply
reply = draft_reply("Inbox/email_20260226_meeting.md")
# Output: "Hi, I'll schedule the meeting for Tuesday..."
```

---

### **Step 3: MCP Server - Action**

```python
from Skills.mcp_servers.email_mcp_server import EmailMCPServer
import asyncio

# Create MCP server
server = EmailMCPServer()

# Send email using MCP tool
result = await server.execute_tool(
    "send_email",
    {
        "to": "boss@company.com",
        "subject": "Re: Team Meeting",
        "body": "Hi, I've scheduled the meeting for Tuesday at 2 PM...",
        "cc": ["team@company.com"]
    }
)

print(result.text)
# Output: "Email sent successfully to boss@company.com"
```

---

## 🔧 MCP Server Explained

### What is MCP Server?

**MCP (Model Context Protocol) Server** is a standardized way to:
- Expose tools/actions to AI
- Handle authentication
- Execute external API calls
- Return structured results

### Email MCP Server Structure

```python
class EmailMCPServer:
    """
    MCP Server for sending emails
    """
    
    # 1. Define tools
    def register_tools(self):
        return [
            {
                "name": "send_email",
                "description": "Send an email via Gmail API",
                "parameters": {
                    "to": "recipient email",
                    "subject": "email subject",
                    "body": "email body"
                }
            }
        ]
    
    # 2. Execute tool
    async def handle_tool_call(self, name, arguments):
        if name == "send_email":
            # Call Gmail API
            # Return result
            return "Email sent successfully"
```

---

## 🎯 Complete Working Example

### File: `auto_respond_to_gmail.py`

```python
import asyncio
from Skills.agent_skills import summarize_task, draft_reply
from Skills.mcp_servers.email_mcp_server import EmailMCPServer

async def auto_respond():
    # 1. Get email tasks
    from pathlib import Path
    inbox = list(Path("Inbox").glob("*.md"))
    
    for email_file in inbox:
        # 2. AI processes
        summary = summarize_task(str(email_file))
        reply = draft_reply(str(email_file))
        
        # 3. MCP Server sends
        server = EmailMCPServer()
        result = await server.execute_tool(
            "send_email",
            {
                "to": "extracted_from_email",
                "subject": "Re: " + subject,
                "body": reply
            }
        )
        
        print(f"Sent: {result.text}")

asyncio.run(auto_respond())
```

---

## 📊 Data Flow

```
User sends email
    ↓
Gmail receives it
    ↓
Gmail Watcher fetches it
    ↓
Creates Inbox/email.md
    ↓
AI reads and processes
    ↓
AI drafts reply
    ↓
Human approves (optional)
    ↓
MCP Server sends via Gmail API
    ↓
Email sent! ✅
```

---

## ✅ Key Points

### Gmail Watcher (Perception)
- ✅ **Reads** emails from Gmail
- ✅ **Creates** task files
- ✅ **Does NOT send** emails

### Agent Skills (Reasoning)
- ✅ **Analyzes** email content
- ✅ **Generates** summaries, plans, drafts
- ✅ **Does NOT send** emails

### MCP Server (Action)
- ✅ **Sends** emails via Gmail API
- ✅ **Handles** authentication
- ✅ **Returns** success/failure

---

## 🚀 For Your Hackathon Demo

```bash
# 1. Show Gmail Watcher creating tasks
python Skills/gmail_watcher.py poll
dir Inbox

# 2. Show AI processing
python -c "from Skills.agent_skills import summarize_task; print(summarize_task('Inbox/*.md'))"

# 3. Show MCP Server ready to send
python -c "from Skills.mcp_servers.email_mcp_server import EmailMCPServer; print('MCP Server ready!')"

# 4. Explain the flow
# Gmail Watcher → AI Processing → MCP Server → Send Email
```

---

**MCP Server is the "hands" that actually sends emails!** ✉️
