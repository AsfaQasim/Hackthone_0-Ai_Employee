# 🏗️ Gold Tier System Architecture

## Overview

This Personal AI Employee is a fully autonomous, local-first system that manages personal and business affairs 24/7. It achieves Gold Tier status with cross-domain integration, multiple watchers, MCP servers, error recovery, audit logging, and autonomous task execution.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERSONAL AI EMPLOYEE                         │
│                   GOLD TIER ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      PERCEPTION LAYER                           │
│                        (Watchers)                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │    Gmail     │  │   WhatsApp   │  │   LinkedIn   │        │
│  │   Watcher    │  │   Watcher    │  │   Watcher    │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
│         │                  │                  │                 │
│         └──────────────────┴──────────────────┘                │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE BASE LAYER                         │
│                      (Obsidian Vault)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  /Inbox/              ← New tasks from watchers                │
│  /Needs_Action/       ← Tasks requiring processing             │
│  /In_Progress/        ← Currently being worked on              │
│  /Pending_Approval/   ← Awaiting human approval                │
│  /Approved/           ← Approved for execution                 │
│  /Done/               ← Completed tasks                        │
│  /Plans/              ← Execution plans                        │
│  /Briefings/          ← CEO briefings                          │
│  /Logs/               ← Audit logs (90+ day retention)         │
│                                                                 │
│  Dashboard.md         ← Real-time status                       │
│  Company_Handbook.md  ← Rules and guidelines                   │
│                                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     REASONING LAYER                             │
│                    (Claude Code + Skills)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Unified Task Processor (Cross-Domain Integration)     │   │
│  └────────────────────────────────────────────────────────┘   │
│                            │                                    │
│  ┌─────────────────┬──────┴──────┬─────────────────┐          │
│  │                 │             │                 │          │
│  ▼                 ▼             ▼                 ▼          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  Plan    │  │  Draft   │  │ Summarize│  │  Create  │     │
│  │ Reasoning│  │  Reply   │  │   Task   │  │  Plan    │     │
│  │   Loop   │  │  Skill   │  │   Skill  │  │  Skill   │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Ralph Wiggum Loop (Autonomous Multi-Step Execution)   │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Error Recovery (Retry + Exponential Backoff)          │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ACTION LAYER                               │
│                     (MCP Servers)                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │    Email     │  │ Social Media │  │   Browser    │        │
│  │ MCP Server   │  │  MCP Server  │  │  MCP Server  │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
│         │                  │                  │                 │
│         └──────────────────┴──────────────────┘                │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SUPPORTING SYSTEMS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Audit Logger (90+ day retention, search, reporting)   │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Approval Workflow (Human-in-the-Loop)                 │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Scheduler (Cron/Task Scheduler)                       │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  CEO Briefing Generator (Weekly Business Audit)        │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Perception Layer (Watchers)

**Purpose**: Monitor external systems and create actionable tasks

**Components**:
- `Skills/gmail_watcher.py` - Monitors Gmail for important emails
- `Skills/whatsapp_watcher.py` - Monitors WhatsApp for urgent messages
- `Skills/linkedin_watcher.py` - Monitors LinkedIn for business opportunities
- `Skills/base_watcher.py` - Base class for all watchers

**How it works**:
1. Watchers run continuously in background
2. Poll external systems at regular intervals (30-120 seconds)
3. Detect new items (emails, messages, posts)
4. Create markdown files in `/Needs_Action/` folder
5. Include metadata (priority, type, timestamp)

### 2. Knowledge Base Layer (Obsidian Vault)

**Purpose**: Central repository for all data, tasks, and state

**Folder Structure**:
- `/Inbox/` - New tasks from watchers
- `/Needs_Action/` - Tasks requiring processing
- `/In_Progress/` - Currently being worked on
- `/Pending_Approval/` - Awaiting human approval
- `/Approved/` - Approved for execution
- `/Done/` - Completed tasks
- `/Plans/` - Execution plans
- `/Briefings/` - CEO briefings
- `/Logs/` - Audit logs

**Key Files**:
- `Dashboard.md` - Real-time system status
- `Company_Handbook.md` - Rules and guidelines

### 3. Reasoning Layer (Claude Code + Agent Skills)

**Purpose**: Process tasks, make decisions, create plans

**Core Skills**:
- `unified_task_processor.py` - Cross-domain task routing
- `plan_reasoning_loop.py` - Multi-step planning
- `agent_skills/draft_reply.py` - Draft email/message replies
- `agent_skills/summarize_task.py` - Summarize tasks
- `agent_skills/create_plan.py` - Create execution plans

**Ralph Wiggum Loop**:
- Autonomous multi-step task execution
- Continues until task is complete
- Moves task to `/Done/` when finished
- Implemented in `Skills/ralph_loop.py`

**Error Recovery**:
- Automatic retry with exponential backoff
- Graceful degradation on failures
- Comprehensive error logging
- Implemented in `Skills/error_recovery.py`

### 4. Action Layer (MCP Servers)

**Purpose**: Execute actions on external systems

**MCP Servers**:
- `base_mcp_server.py` - Base framework for all MCP servers
- `email_mcp_server.py` - Send emails, draft replies
- `social_media_mcp_server.py` - Post to LinkedIn, Twitter

**Human-in-the-Loop**:
- Sensitive actions require approval
- System writes to `/Pending_Approval/`
- Human moves to `/Approved/` to authorize
- Implemented in `Skills/approval_workflow.py`

### 5. Supporting Systems

**Audit Logger**:
- Logs all actions with timestamps
- 90+ day retention
- Search and reporting capabilities
- Implemented in `Skills/audit_logger.py`

**Scheduler**:
- Runs periodic tasks (daily briefings, weekly audits)
- Uses cron (Linux/Mac) or Task Scheduler (Windows)
- Implemented in `Skills/scheduler.py`

**CEO Briefing Generator**:
- Weekly business audit
- Revenue tracking
- Bottleneck identification
- Proactive suggestions
- Implemented in `Skills/ceo_briefing_generator.py`

## Data Flow

### Example: Email Processing

1. **Detection**: Gmail Watcher detects new important email
2. **Ingestion**: Creates `/Needs_Action/EMAIL_12345.md`
3. **Processing**: Unified Task Processor reads file
4. **Reasoning**: Claude analyzes email, determines action needed
5. **Planning**: Creates plan in `/Plans/plan_20260304.md`
6. **Drafting**: Draft Reply skill creates response
7. **Approval**: Writes to `/Pending_Approval/REPLY_12345.md`
8. **Human Review**: User moves to `/Approved/`
9. **Execution**: Email MCP Server sends reply
10. **Logging**: Audit Logger records action
11. **Completion**: Task moved to `/Done/`

## Security Architecture

### Credential Management
- Environment variables for API keys
- `.env` file (never committed to git)
- Secrets stored in OS keychain
- Monthly credential rotation

### Sandboxing
- Development mode flag prevents real actions
- Dry-run mode for testing
- Separate test accounts
- Rate limiting (max 10 emails/hour, max 3 payments/hour)

### Audit Trail
- All actions logged with timestamps
- 90+ day retention
- Searchable logs
- Compliance reporting

## Scalability

### Current Capacity
- Handles 100+ emails/day
- Processes 50+ WhatsApp messages/day
- Creates 10+ LinkedIn posts/week
- Generates weekly CEO briefings

### Performance
- Watcher polling: 30-120 second intervals
- Task processing: 1-5 minutes per task
- MCP actions: 2-10 seconds per action
- End-to-end latency: 2-10 minutes

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Knowledge Base | Obsidian (Markdown) | Local-first data storage |
| Reasoning Engine | Claude Code | AI decision making |
| Watchers | Python 3.13+ | System monitoring |
| MCP Servers | Node.js 24+ | External actions |
| Scheduler | Cron / Task Scheduler | Periodic tasks |
| Version Control | Git | Code and vault versioning |

## Deployment

### Local Deployment
- Runs on user's laptop/desktop
- Always-on when machine is running
- No cloud dependencies
- Full privacy and control

### Requirements
- 8GB RAM minimum (16GB recommended)
- 4-core CPU minimum (8-core recommended)
- 20GB free disk space
- Stable internet connection (10+ Mbps)

## Future Enhancements

### Platinum Tier (Optional)
- Cloud deployment for 24/7 operation
- Multi-agent coordination
- Advanced analytics dashboard
- Mobile app integration

### Optional Integrations
- Odoo accounting system
- Facebook/Instagram posting
- Twitter/X integration
- Banking automation

## Conclusion

This Gold Tier architecture provides a robust, scalable, and secure foundation for an autonomous AI Employee. It successfully integrates multiple domains (email, messaging, social media), implements human-in-the-loop approval, provides comprehensive audit logging, and enables autonomous multi-step task execution.

The system is production-ready for personal and small business use, with clear paths for scaling to Platinum Tier for enterprise deployment.
