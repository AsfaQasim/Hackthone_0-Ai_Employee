# Design Document: AI Employee System Implementation

## Overview

This document defines the technical design for a complete Personal AI Employee System based on the Ralph Loop architecture. The system implements a continuous Perception → Reasoning → Action cycle, operates locally-first within an Obsidian vault, uses Python for core implementation, integrates with Model Context Protocol (MCP) for external actions, and enforces human-in-the-loop approval for high-risk operations.

The system is designed to be:
- **Minimal**: Only essential components for a working system
- **Complete**: All key capabilities demonstrated
- **Local-first**: All data in Obsidian vault, no cloud dependencies
- **Observable**: Complete logging and transparency
- **Approval-gated**: Human control over high-risk actions

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  AI EMPLOYEE SYSTEM                          │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  PERCEPTION LAYER                                       │ │
│  │  - File Watchers (vault changes)                       │ │
│  │  - Email Watcher (Gmail monitoring)                    │ │
│  │  - Business Data Scanner (daily review)                │ │
│  │  - Event Queue (observation buffering)                 │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  REASONING LAYER                                        │ │
│  │  - Context Analyzer (build complete picture)           │ │
│  │  - Decision Engine (evaluate options)                  │ │
│  │  - Plan Generator (create execution plans)             │ │
│  │  - Risk Assessor (determine approval needs)            │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  APPROVAL GATEWAY                                       │ │
│  │  - Request Generator (create approval files)           │ │
│  │  - Decision Detector (watch for human decisions)       │ │
│  │  - Approval Enforcer (block high-risk actions)         │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  ACTION LAYER                                           │ │
│  │  - Vault Writer (create/update markdown files)         │ │
│  │  - MCP Client (call external tools)                    │ │
│  │  - Task Executor (run autonomous loops)                │ │
│  │  - State Manager (persist execution state)             │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  CROSS-CUTTING CONCERNS                                 │ │
│  │  - Logging (markdown + JSON audit trail)               │ │
│  │  - Error Handling (retry, rollback, escalate)          │ │
│  │  - Configuration (YAML-based settings)                 │ │
│  │  - State Persistence (JSON state files)                │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Language**: Python 3.10+
- **File Watching**: watchdog library
- **Email**: Gmail API via google-api-python-client
- **MCP**: Model Context Protocol SDK
- **Configuration**: PyYAML
- **Logging**: Python logging + custom markdown formatter
- **Testing**: pytest + hypothesis (property-based testing)

