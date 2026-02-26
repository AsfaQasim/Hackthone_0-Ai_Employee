# Skills Directory

This directory contains all the AI Employee's skills and capabilities.

## Running Scripts

**Important**: Most scripts should be run from the **root directory** (`F:\hackthone_0\`), not from the Skills directory.

### If you're in the Skills directory:

```cmd
# Go back to root
cd ..

# Then run commands
python setup.py
python main_loop.py
python setup_scheduler.py
```

### Or use relative paths:

```cmd
# From Skills directory
python ..\setup.py
python ..\main_loop.py
```

## Directory Structure

```
Skills/
├── agent_skills/          # Agent Skills (4 skills)
│   ├── base_skill.py
│   ├── summarize_task.py
│   ├── create_plan.py
│   ├── draft_reply.py
│   └── generate_linkedin_post.py
├── mcp_servers/           # MCP Servers
│   ├── base_mcp_server.py
│   ├── email_mcp_server.py
│   └── social_media_mcp_server.py
├── tests/                 # Unit tests
├── approval_workflow.py   # Approval system
├── gmail_watcher.py       # Gmail monitoring
├── plan_reasoning_loop.py # Plan creation
└── scheduler.py           # Task scheduling
```

## Quick Commands

### Setup (from root)
```cmd
cd ..
python setup.py
```

### Run Gmail Watcher
```cmd
cd ..
python Skills\gmail_watcher.py
```

### Setup Scheduler
```cmd
cd ..
python setup_scheduler.py
```

### Run Main Loop
```cmd
cd ..
python main_loop.py
```

## Current Location Check

To see where you are:
```cmd
cd
```

To go to root:
```cmd
cd F:\hackthone_0
```

Or:
```cmd
cd ..
```
