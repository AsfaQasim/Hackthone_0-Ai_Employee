# 🥉 Bronze Tier Architecture

Simple, local-first AI Employee foundation.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     BRONZE TIER SYSTEM                      │
│                  (Local, Single Watcher)                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL SOURCE                          │
│                                                             │
│                    📧 Gmail Inbox                           │
│                   (Unread Emails)                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Gmail API
                         │ (OAuth 2.0)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   PERCEPTION LAYER                          │
│                                                             │
│              📡 Gmail Watcher (Python)                      │
│                                                             │
│  • Polls every 5 minutes                                    │
│  • Filters by importance criteria                           │
│  • Detects priority (High/Medium/Low)                       │
│  • Checks for duplicates                                    │
│                                                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Creates .md files
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  OBSIDIAN VAULT (Local)                     │
│                   "The Brain & Memory"                      │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Dashboard.md          │  Company_Handbook.md       │   │
│  │  (Status Overview)     │  (Rules & Guidelines)      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  /Needs_Action/                                     │   │
│  │  ├── 20260216_urgent_client_email.md               │   │
│  │  ├── 20260216_invoice_request.md                   │   │
│  │  └── 20260216_meeting_reminder.md                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  /Done/          /Logs/          /Plans/           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Reads & Writes
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   REASONING LAYER                           │
│                                                             │
│                  🤖 Claude Code (You!)                      │
│                                                             │
│  • Reads tasks from /Needs_Action                           │
│  • Analyzes email content                                   │
│  • Drafts responses                                         │
│  • Updates Dashboard                                        │
│  • Creates Plans for multi-step tasks                       │
│  • Moves completed items to /Done                           │
│                                                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Human reviews
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  HUMAN-IN-THE-LOOP                          │
│                                                             │
│                    👤 You (The Boss)                        │
│                                                             │
│  • Review tasks in Needs_Action/                            │
│  • Approve/reject Claude's suggestions                      │
│  • Move files to Done/ when complete                        │
│  • Update Company_Handbook.md rules                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Email Arrives

```
Gmail Inbox
    ↓
[New unread email from client@example.com]
Subject: "Urgent: Invoice needed ASAP"
```

### 2. Watcher Detects

```
Gmail Watcher (polling)
    ↓
• Fetches unread emails via Gmail API
• Checks importance criteria:
  ✓ Contains keyword "urgent"
  ✓ Contains keyword "invoice"
• Detects priority: HIGH (contains "urgent", "asap")
• Not a duplicate (not in processed index)
```

### 3. Markdown Created

```
/Needs_Action/20260216_103045_urgent-invoice-needed-asap.md
    ↓
---
email_id: "abc123xyz"
sender: "Client Name <client@example.com>"
priority: "high"
status: "pending"
---

# Email: Urgent: Invoice needed ASAP

**From**: Client Name <client@example.com>
**Priority**: 🔴 High

## Email Content
[Email body here...]

## Action Items
- [ ] Review and respond to this email
```

### 4. Claude Processes

```
You ask: "Check Needs_Action and summarize"
    ↓
Claude reads the markdown file
    ↓
Claude responds:
"You have 1 high-priority task:
- Client needs invoice ASAP
- Suggested action: Draft invoice and send"
```

### 5. Task Completed

```
You: "Move to Done after I send the invoice"
    ↓
File moved: Needs_Action/ → Done/
    ↓
Dashboard.md updated with completion
```

---

## File Structure

```
your-workspace/
│
├── 📊 Dashboard.md              # Real-time status
├── 📖 Company_Handbook.md       # Your rules
│
├── 📁 Needs_Action/             # Pending tasks
│   ├── email_task_1.md
│   └── email_task_2.md
│
├── 📁 Done/                     # Completed
│   └── email_task_completed.md
│
├── 📁 Logs/                     # Activity logs
│   └── gmail_watcher/
│       └── gmail-watcher.log
│
├── 📁 Skills/                   # Agent capabilities
│   ├── gmail_watcher.py         # The watcher script
│   └── config/
│       └── gmail_watcher_config.yaml
│
├── 📁 config/                   # Credentials (gitignored)
│   ├── gmail-credentials.json
│   └── gmail-token.json
│
└── 📁 .index/                   # Processed tracking
    └── gmail-watcher-processed.json
```

---

## Component Responsibilities

### Gmail Watcher (Python)
- **Input**: Gmail API (unread emails)
- **Output**: Markdown files in Needs_Action/
- **Runs**: Continuously (every 5 min) or on-demand
- **State**: Maintains processed index to avoid duplicates

### Obsidian Vault
- **Purpose**: Central knowledge base and task queue
- **Format**: Plain markdown files
- **Benefits**: Human-readable, version-controllable, portable

### Claude Code
- **Input**: Markdown files from vault
- **Output**: Summaries, drafts, plans, updates
- **Runs**: On-demand (when you ask)
- **Capabilities**: Read, write, analyze, generate

### Human (You)
- **Role**: Final decision maker
- **Tasks**: Review, approve, execute sensitive actions
- **Tools**: File system, Obsidian, terminal

---

## Security Model

```
┌─────────────────────────────────────────┐
│         SECURITY BOUNDARIES             │
└─────────────────────────────────────────┘

🔒 Credentials (Never in vault)
   ├── config/gmail-credentials.json
   └── config/gmail-token.json
   
📝 Vault (Safe to sync/backup)
   ├── All markdown files
   ├── Dashboard.md
   └── Company_Handbook.md
   
🚫 Gitignored
   ├── .env
   ├── config/*.json
   ├── .index/
   └── Logs/
```

---

## Scaling Path

### Bronze → Silver
- Add more watchers (WhatsApp, LinkedIn)
- Add MCP server for actions (send emails)
- Add approval workflow
- Add scheduling (cron)

### Silver → Gold
- Multi-domain integration
- Accounting system (Odoo)
- Social media posting
- Weekly CEO briefing

### Gold → Platinum
- Cloud deployment (24/7)
- Work-zone specialization
- Agent-to-agent communication
- Production monitoring

---

## Key Concepts

### Perception → Reasoning → Action

1. **Perception**: Watcher detects important emails
2. **Reasoning**: Claude analyzes and plans
3. **Action**: Human executes (Bronze) or MCP executes (Silver+)

### File-Based Workflow

- Tasks flow through folders: Needs_Action → Done
- State persists in markdown files
- Human-readable audit trail
- No database needed

### Human-in-the-Loop

- AI suggests, human decides
- All sensitive actions require approval
- Gradual trust building
- Safety by design

---

**This is your Bronze Tier foundation. Build on it! 🚀**
