# Personal AI Employee System Specification

## Overview

This document defines the architecture, capabilities, and operational model for a Personal AI Employee that operates locally-first within an Obsidian vault, using the Ralph Loop (Perception → Reasoning → Action) architecture with human approval gates.

## System Purpose

The Personal AI Employee is an autonomous agent system designed to:
- Operate entirely within your local Obsidian vault (local-first, privacy-preserving)
- Monitor vault changes through file watchers
- Execute actions via Model Context Protocol (MCP)
- Maintain human oversight through approval workflows
- Follow the Ralph Loop: Perception → Reasoning → Action

## Design Principles

1. **Local First**: All data stays on your machine, no cloud dependencies
2. **Obsidian Native**: Uses markdown files, follows vault conventions
3. **Human in the Loop**: Critical actions require explicit approval
4. **Observable**: All reasoning and actions are logged transparently
5. **Extensible**: MCP enables integration with external tools

## Core Architecture: The Ralph Loop

```
┌─────────────────────────────────────────────────────────┐
│                  Personal AI Employee                    │
│                                                          │
│  ┌──────────────┐      ┌──────────────┐      ┌────────┐│
│  │  PERCEPTION  │ ───> │  REASONING   │ ───> │ ACTION ││
│  └──────────────┘      └──────────────┘      └────────┘│
│         │                     │                    │    │
│         │                     │                    │    │
│    [Watchers]           [Spec Engine]        [MCP Tools]│
│    [Vault Read]         [Task Planner]       [Vault Write]│
│         │                     │                    │    │
│         └─────────────────────┴────────────────────┘    │
│                          │                              │
│                   [Approval Gateway]                    │
│                          │                              │
│                   [Obsidian Vault]                      │
└─────────────────────────────────────────────────────────┘
```

### Ralph Loop Components

#### 1. PERCEPTION Layer

**Purpose**: Observe and understand the current state of the vault

**Capabilities**:
- **File Watchers**: Monitor vault for changes (new files, edits, deletions)
- **Vault Scanner**: Read and parse markdown files, frontmatter, tags
- **Context Builder**: Aggregate relevant information for decision-making
- **Event Queue**: Buffer and prioritize incoming events

**Inputs**:
- File system events (create, modify, delete)
- Scheduled triggers (time-based checks)
- User commands (manual invocations)
- MCP server notifications

**Outputs**:
- Structured observations (what changed, when, where)
- Context snapshots (current vault state)
- Event metadata (priority, type, source)

#### 2. REASONING Layer

**Purpose**: Analyze observations and decide what actions to take

**Capabilities**:
- **Spec Engine**: Transform ideas into formal specifications
- **Task Planner**: Break down goals into actionable tasks
- **Decision Engine**: Evaluate options and select best course
- **Dependency Resolver**: Determine task ordering and prerequisites
- **Risk Assessor**: Identify actions requiring approval

**Inputs**:
- Observations from Perception layer
- Existing specs, plans, and tasks
- Skills library (available capabilities)
- System constraints and policies

**Outputs**:
- Action plans (what to do)
- Task lists (step-by-step instructions)
- Approval requests (for high-risk actions)
- Reasoning traces (why decisions were made)

#### 3. ACTION Layer

**Purpose**: Execute decisions through MCP tools and vault operations

**Capabilities**:
- **MCP Client**: Invoke external tools via Model Context Protocol
- **Vault Writer**: Create, update, and organize markdown files
- **Task Executor**: Run tasks from specifications
- **Status Tracker**: Update task and spec status
- **Result Logger**: Record outcomes and metrics

**Inputs**:
- Action plans from Reasoning layer
- Approved requests from Approval Gateway
- MCP tool configurations
- Execution context

**Outputs**:
- Modified vault files (new specs, updated tasks)
- MCP tool results (external actions performed)
- Execution logs (what happened)
- Status updates (progress tracking)

### Cross-Cutting Components

#### Approval Gateway

**Purpose**: Ensure human oversight for critical decisions

**Approval Triggers**:
- Creating new specifications
- Executing high-risk MCP actions
- Modifying approved documents
- Deleting files or data
- External API calls

**Approval Mechanism**:
- Creates approval request in `/Pending_Approval/`
- Waits for human review (file move to `/Approved/`)
- Proceeds only after explicit approval
- Logs approval decision and timestamp

#### Obsidian Vault Structure

**Purpose**: Organize all AI Employee data in markdown

**Vault Layout**:
```
/Specs/              # Active specifications
/Skills/             # Reusable capabilities
/Plans/              # Strategic roadmaps
/Needs_Action/       # Requires human input
/Pending_Approval/   # Awaiting review
/Approved/           # Ready for execution
/Done/               # Completed work
/Logs/               # Execution history
/Dashboard/          # Status overviews
```

**File Conventions**:
- All files are markdown (`.md`)
- Frontmatter for metadata (YAML)
- Wikilinks for cross-references (`[[link]]`)
- Tags for categorization (`#tag`)
- Checkboxes for tasks (`- [ ]`)

## Ralph Loop Execution Flow

### Complete Cycle

```
1. PERCEPTION: Watcher detects file change in /Specs/
   ↓
2. PERCEPTION: Read file, extract context, identify trigger
   ↓
3. REASONING: Analyze change, determine if action needed
   ↓
4. REASONING: Generate action plan (e.g., "create tasks.md")
   ↓
5. REASONING: Check if approval required
   ↓
6. [IF APPROVAL NEEDED] → Create request in /Pending_Approval/
   ↓
7. [WAIT FOR HUMAN] → File moved to /Approved/
   ↓
8. ACTION: Execute plan via MCP tools or vault operations
   ↓
9. ACTION: Log results to /Logs/
   ↓
10. ACTION: Update status, move files to appropriate folders
    ↓
11. [LOOP] → Return to PERCEPTION
```

### Operational States

Specifications flow through vault folders representing states:

```
/Specs/ (DRAFT)
    ↓
/Needs_Action/ (BLOCKED) ⟷ /Pending_Approval/ (REVIEW)
    ↓                              ↓
    └──────────────────────→ /Approved/ (READY)
                                   ↓
                            [Execution Phase]
                                   ↓
                              /Done/ (COMPLETE)
```

**State Definitions**:
- **DRAFT** (`/Specs/`): Active development
- **BLOCKED** (`/Needs_Action/`): Requires human decision
- **REVIEW** (`/Pending_Approval/`): Awaiting approval
- **READY** (`/Approved/`): Approved for execution
- **COMPLETE** (`/Done/`): Finished and validated

## Watchers: Perception Triggers

### File System Watchers

**Purpose**: Detect changes in the Obsidian vault to trigger Ralph Loop

**Watched Locations**:
- `/Specs/**/*.md` - New or modified specifications
- `/Approved/**/*.md` - Approved items ready for execution
- `/Needs_Action/**/*.md` - Items requiring attention
- `/Skills/**/*.md` - New capabilities added
- `/Plans/**/*.md` - Strategic changes

**Event Types**:
- `FILE_CREATED` - New file added
- `FILE_MODIFIED` - Existing file changed
- `FILE_DELETED` - File removed
- `FILE_MOVED` - File relocated (state transition)

**Watcher Behavior**:
- Debounce rapid changes (wait 2s after last change)
- Ignore temp files and system files
- Queue events for sequential processing
- Log all detected events

### Trigger Conditions

**Automatic Triggers**:
- New spec created → Generate requirements template
- Spec moved to `/Approved/` → Begin task execution
- Task marked complete → Update status, check dependencies
- File moved to `/Needs_Action/` → Notify human

**Manual Triggers**:
- Frontmatter flag: `trigger: manual`
- Command palette invocation
- Scheduled cron expressions

## MCP Actions: Execution Layer

### Model Context Protocol Integration

**Purpose**: Enable AI Employee to interact with external tools and services

**MCP Architecture**:
```
AI Employee (MCP Client)
    ↓
MCP Protocol (JSON-RPC)
    ↓
MCP Servers (Tool Providers)
    ↓
External Systems (APIs, CLIs, Services)
```

**Core MCP Actions**:

1. **Vault Operations**
   - `vault.read(path)` - Read file content
   - `vault.write(path, content)` - Create/update file
   - `vault.move(from, to)` - Move file (state transition)
   - `vault.delete(path)` - Remove file
   - `vault.search(query)` - Find files by content

2. **Task Management**
   - `task.create(spec, description)` - Add new task
   - `task.update(id, status)` - Change task status
   - `task.complete(id)` - Mark task done
   - `task.list(spec)` - Get all tasks for spec

3. **Spec Operations**
   - `spec.create(name, idea)` - Generate new spec
   - `spec.validate(path)` - Check completeness
   - `spec.approve(path)` - Request approval
   - `spec.execute(path)` - Run tasks

4. **External Integrations** (via MCP servers)
   - `git.commit(message)` - Version control
   - `api.call(endpoint, params)` - HTTP requests
   - `shell.exec(command)` - Run CLI commands
   - `calendar.schedule(event)` - Time management

**MCP Configuration**:
- Defined in `mcp.json` in vault root
- Each server specifies command, args, env
- Auto-approval list for trusted actions
- Timeout and retry policies

## Human Approval Workflow

### Approval Philosophy

**When to Require Approval**:
- Creating new specifications (high-level decisions)
- Executing external MCP actions (side effects)
- Modifying approved documents (change control)
- Deleting files or data (irreversible actions)
- High-risk operations (security, privacy)

**When to Auto-Approve**:
- Reading vault files (safe, read-only)
- Logging and status updates (observability)
- Internal reasoning and planning (no side effects)
- Low-risk MCP actions (in auto-approve list)

### Approval Process

1. **Request Creation**:
   - AI Employee creates approval request file
   - File placed in `/Pending_Approval/`
   - Contains: action description, reasoning, risks, alternatives

2. **Human Review**:
   - Human reads request in Obsidian
   - Evaluates reasoning and risks
   - Makes decision: approve, reject, or modify

3. **Approval Signaling**:
   - **Approve**: Move file to `/Approved/`
   - **Reject**: Move file to `/Needs_Action/` with feedback
   - **Modify**: Edit request, keep in `/Pending_Approval/`

4. **Execution**:
   - Watcher detects file move to `/Approved/`
   - AI Employee proceeds with action
   - Results logged to `/Logs/`
   - Original request moved to `/Done/`

### Approval Request Format

```markdown
---
type: approval_request
action: create_spec
risk_level: medium
requested_at: 2026-02-14T10:30:00Z
---

# Approval Request: Create User Authentication Spec

## Proposed Action
Create a new specification for user authentication feature

## Reasoning
User requested authentication capability for the application

## Risks
- May require external dependencies
- Security implications if implemented incorrectly

## Alternatives
- Use existing authentication library
- Implement OAuth instead of custom auth

## Approval Decision
- [ ] Approve (move to /Approved/)
- [ ] Reject (move to /Needs_Action/ with feedback)
- [ ] Modify (edit this file)
```

## Correctness Properties

### Ralph Loop Invariants

1. **Perception Completeness**
   - All vault changes are detected by watchers
   - Events are queued and processed in order
   - No events are lost or duplicated

2. **Reasoning Soundness**
   - Decisions are based on complete context
   - Reasoning traces are logged and auditable
   - Risk assessment is performed for all actions

3. **Action Safety**
   - High-risk actions require approval
   - Approved actions are executed exactly once
   - Failed actions are logged and can be retried

4. **Loop Continuity**
   - After action, perception resumes
   - System never deadlocks or hangs
   - Errors are handled gracefully

### Vault Integrity

1. **File System Consistency**
   - Files are in exactly one folder (state)
   - State transitions follow defined paths
   - No orphaned or lost files

2. **Markdown Validity**
   - All files are valid markdown
   - Frontmatter is valid YAML
   - Links and references are resolvable

3. **Approval Integrity**
   - Approved actions are immutable
   - Approval history is preserved
   - Rejected actions cannot auto-execute

## Skills System

### Skill Definition

Skills are reusable capabilities stored as markdown files in `/Skills/`

**Skill File Format**:
```markdown
---
skill_name: file_watcher
category: perception
inputs: [path, event_types]
outputs: [events]
mcp_tools: [vault.read, vault.search]
risk_level: low
---

# File Watcher Skill

## Purpose
Monitor vault files for changes and trigger Ralph Loop

## Preconditions
- Valid vault path
- Read permissions

## Execution
1. Set up file system watcher
2. Filter events by type
3. Queue events for processing

## Postconditions
- Events are queued
- No events are lost

## Properties
- All file changes are detected
- Events are processed in order
```

### Skill Categories

1. **Perception Skills**
   - File watching and monitoring
   - Content parsing and extraction
   - Context building and aggregation

2. **Reasoning Skills**
   - Spec generation and validation
   - Task planning and decomposition
   - Risk assessment and decision-making

3. **Action Skills**
   - Vault file operations
   - MCP tool invocation
   - Status tracking and logging

### Skill Composition

Skills can be chained to create workflows:

```
watch_file → parse_content → generate_tasks → request_approval → execute_tasks
```

Composition rules:
- Skills are executed sequentially
- Output of one skill feeds into next
- Failure stops the chain
- Results are logged at each step

## Local-First Architecture

### Privacy and Data Sovereignty

**Core Principles**:
- All data stays on your local machine
- No cloud services or external dependencies
- You own and control all files
- Obsidian vault is the single source of truth
- Portable and backup-friendly

**Data Storage**:
- Everything is markdown files
- Human-readable and editable
- Version control friendly (Git)
- No proprietary formats or databases
- Easy to migrate or export

**Offline Operation**:
- Works without internet connection
- No API keys or authentication required
- Fast and responsive (local file system)
- No rate limits or quotas

### Obsidian Integration

**Why Obsidian**:
- Markdown-native knowledge base
- Powerful linking and graph view
- Extensible with plugins
- Cross-platform (Windows, Mac, Linux, Mobile)
- Active community and ecosystem

**Obsidian Features Used**:
- File system as database
- Frontmatter for metadata
- Wikilinks for relationships
- Tags for categorization
- Graph view for visualization
- Search and query capabilities

**Obsidian Plugins** (optional enhancements):
- Dataview: Query and display data
- Templater: Template automation
- Tasks: Advanced task management
- Calendar: Time-based views
- Kanban: Visual task boards

## Logging and Observability

### Log Files in `/Logs/`

All logs are markdown files for transparency and searchability

**Log Types**:

1. **Ralph Loop Logs** (`ralph_loop_YYYYMMDD.md`)
   ```markdown
   ## 2026-02-14 10:30:15 - Perception
   - Event: FILE_MODIFIED
   - Path: /Specs/auth_feature.md
   - Trigger: Watcher detected change
   
   ## 2026-02-14 10:30:16 - Reasoning
   - Analysis: Spec updated, needs task generation
   - Decision: Create tasks.md
   - Risk: Low (read-only analysis)
   
   ## 2026-02-14 10:30:17 - Action
   - MCP Call: spec.generate_tasks(auth_feature)
   - Result: Success
   - Output: /Specs/auth_feature/tasks.md created
   ```

2. **Approval Logs** (`approvals_YYYYMMDD.md`)
   - Approval requests created
   - Human decisions (approve/reject)
   - Execution results

3. **Error Logs** (`errors_YYYYMMDD.md`)
   - Exceptions and failures
   - Stack traces and context
   - Recovery actions taken

4. **Performance Logs** (`performance_YYYYMMDD.md`)
   - Execution times per stage
   - Resource usage (CPU, memory)
   - Bottleneck identification

### Dashboard Views

**Daily Summary** (`/Dashboard/daily_YYYYMMDD.md`):
- Ralph Loop cycles completed
- Specs created/updated
- Tasks executed
- Approvals pending/completed
- Errors encountered

**Metrics** (`/Dashboard/metrics.md`):
- Perception: Events detected per day
- Reasoning: Decisions made per day
- Action: MCP calls executed per day
- Approval: Average approval time
- Success rate: % of successful executions

## MCP Server Configuration

### Example `mcp.json`

```json
{
  "mcpServers": {
    "vault-operations": {
      "command": "node",
      "args": ["./mcp-servers/vault-server.js"],
      "env": {
        "VAULT_PATH": "/path/to/obsidian/vault"
      },
      "disabled": false,
      "autoApprove": [
        "vault.read",
        "vault.search",
        "task.list"
      ]
    },
    "spec-engine": {
      "command": "node",
      "args": ["./mcp-servers/spec-server.js"],
      "disabled": false,
      "autoApprove": [
        "spec.validate"
      ]
    },
    "git-integration": {
      "command": "node",
      "args": ["./mcp-servers/git-server.js"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### MCP Server Responsibilities

**vault-operations**:
- Read/write markdown files
- Search vault content
- Move files between folders
- Parse frontmatter and links

**spec-engine**:
- Generate requirements from ideas
- Create design documents
- Generate task lists
- Validate spec completeness

**git-integration** (optional):
- Commit changes
- Create branches
- Push to remote
- View history

## Security and Safety

### Local-First Security

**Threat Model**:
- No network attacks (offline operation)
- No unauthorized access (local file system)
- Primary risk: Accidental data loss or corruption

**Safety Mechanisms**:

1. **Approval Gates**
   - High-risk actions require human approval
   - Destructive operations are logged
   - Rollback capability via Git

2. **Vault Isolation**
   - AI Employee only accesses designated vault
   - No access to system files or other directories
   - File operations are scoped to vault root

3. **MCP Sandboxing**
   - MCP servers run in separate processes
   - Limited permissions and capabilities
   - Timeout and resource limits

4. **Audit Trail**
   - All actions logged to `/Logs/`
   - Immutable log files (append-only)
   - Reasoning traces for accountability

5. **Graceful Degradation**
   - Errors don't crash the system
   - Failed actions are logged and retried
   - Human can intervene at any point

### Backup and Recovery

**Recommended Practices**:
- Use Git for version control
- Regular vault backups (Obsidian Sync, Dropbox, etc.)
- Test restore procedures
- Keep logs for debugging

**Recovery Scenarios**:
- Accidental file deletion → Restore from Git
- Corrupted spec → Revert to previous version
- Failed execution → Review logs, retry manually

## Extension Points

### Plugin Architecture

The system supports extensions through:
- Custom skill implementations
- Additional validation rules
- New approval workflows
- Enhanced logging strategies
- Integration adapters

### Configuration

System behavior is configurable:
- Approval thresholds
- Execution parallelism
- Retry policies
- Timeout values
- Logging verbosity

## Future Considerations

### Planned Enhancements

1. **Learning System**: Improve from past executions
2. **Parallel Execution**: Run independent tasks concurrently
3. **Distributed Operation**: Scale across multiple agents
4. **Advanced Reasoning**: Multi-step planning and optimization
5. **Self-Improvement**: Identify and fix own inefficiencies

### Research Areas

- Formal verification of specifications
- Automated property discovery
- Adaptive skill composition
- Predictive failure detection
- Collaborative multi-agent workflows

## Compliance

This system adheres to:
- Spec Driven Development methodology
- Property-Based Testing principles
- Formal correctness validation
- Human-in-the-loop oversight
- Transparent decision-making

## Version History

- **v1.0**: Initial system specification
- Date: 2026-02-14
- Status: DRAFT

---

**Next Steps:**
1. Review and approve this system specification
2. Create feature specs that align with this architecture
3. Implement core components with property-based tests
4. Validate system-level invariants
5. Deploy with monitoring and logging


## Extension Points

### Custom Skills

Add new capabilities by creating skill files in `/Skills/`:

```markdown
---
skill_name: custom_analyzer
category: reasoning
inputs: [text, criteria]
outputs: [analysis]
mcp_tools: [vault.read]
risk_level: low
---

# Custom Analyzer Skill

## Purpose
Analyze text against custom criteria

## Implementation
[Your implementation details]
```

### Custom MCP Servers

Extend functionality by adding MCP servers:
1. Create server implementation
2. Add to `mcp.json` configuration
3. Define auto-approve list
4. Test with sample calls

### Obsidian Plugins

Enhance vault experience:
- Dataview: Query specs and tasks
- Templater: Automate file creation
- Tasks: Advanced task management
- Kanban: Visual workflow boards

## Future Enhancements

### Planned Features

1. **Proactive Monitoring**
   - Detect patterns in vault usage
   - Suggest optimizations
   - Identify stale specs

2. **Learning from History**
   - Analyze past executions
   - Improve decision-making
   - Predict approval outcomes

3. **Multi-Agent Collaboration**
   - Specialized agents for different domains
   - Coordinated task execution
   - Shared skills library

4. **Advanced Reasoning**
   - Multi-step planning
   - Constraint satisfaction
   - Optimization algorithms

5. **Mobile Support**
   - Obsidian mobile integration
   - Offline sync
   - Push notifications for approvals

### Research Areas

- Formal verification of Ralph Loop properties
- Automated skill discovery and composition
- Predictive approval modeling
- Natural language spec generation
- Visual workflow editors

## Getting Started

### Initial Setup

1. **Create Vault Structure**
   - Set up folders: Specs, Skills, Plans, etc.
   - Add README.md with documentation
   - Initialize Git repository (optional)

2. **Configure MCP Servers**
   - Create `mcp.json` in vault root
   - Define vault-operations server
   - Define spec-engine server
   - Test server connections

3. **Set Up Watchers**
   - Configure file system monitoring
   - Define trigger conditions
   - Test event detection

4. **Create First Spec**
   - Add rough idea to `/Specs/`
   - Let Ralph Loop generate requirements
   - Review and approve
   - Execute tasks

### Daily Workflow

1. **Morning**: Check `/Dashboard/` for overnight activity
2. **Throughout Day**: Review `/Pending_Approval/` for requests
3. **As Needed**: Add new ideas to `/Specs/`
4. **Evening**: Review `/Logs/` for issues or insights

## Compliance and Standards

This system adheres to:
- **Local-First Principles**: Data sovereignty and privacy
- **Spec Driven Development**: Formal specifications before code
- **Property-Based Testing**: Universal correctness validation
- **Human-in-the-Loop**: Oversight for critical decisions
- **Transparent Operations**: All reasoning and actions logged

## Version History

- **v2.0**: Personal AI Employee with Ralph Loop architecture
- **v1.0**: Initial system specification
- Date: 2026-02-14
- Status: DRAFT

---

## Next Steps

1. **Review this specification** - Ensure it meets your needs
2. **Set up Obsidian vault** - Create folder structure
3. **Configure MCP servers** - Enable vault operations
4. **Implement watchers** - Start perception layer
5. **Test Ralph Loop** - Run end-to-end cycle
6. **Create first spec** - Build a real feature
7. **Iterate and improve** - Refine based on experience
