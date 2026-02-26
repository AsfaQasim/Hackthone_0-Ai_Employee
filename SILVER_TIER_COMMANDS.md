# 🥈 Silver Tier - Quick Command Reference

## Setup Commands

### Install Dependencies
```bash
pip install google-auth google-auth-oauthlib google-api-python-client
pip install playwright pyyaml html2text requests
playwright install chromium
```

### Authenticate Services
```bash
# Gmail
python Skills/gmail_watcher.py auth

# WhatsApp
python Skills/whatsapp_watcher.py auth

# LinkedIn (set token first)
set LINKEDIN_ACCESS_TOKEN=your_token_here
python Skills/linkedin_watcher.py auth
```

---

## Watcher Commands

### Gmail Watcher
```bash
# Authenticate
python Skills/gmail_watcher.py auth

# Poll once (check for new emails)
python Skills/gmail_watcher.py poll

# Start continuous monitoring (every 5 minutes)
python Skills/gmail_watcher.py start

# With config file
python Skills/gmail_watcher.py poll --config Skills/config/gmail_watcher_config.yaml

# Dry run (no modifications)
python Skills/gmail_watcher.py poll --dry-run
```

### WhatsApp Watcher
```bash
# Authenticate (scan QR code)
python Skills/whatsapp_watcher.py auth

# Check connection status
python Skills/whatsapp_watcher.py status

# Read messages from contact
python Skills/whatsapp_watcher.py read "Contact Name"

# Send message
python Skills/whatsapp_watcher.py send "Contact Name" "Your message here"

# Get unread chats
python Skills/whatsapp_watcher.py unread

# Start continuous monitoring
python Skills/whatsapp_watcher.py start
```

### LinkedIn Watcher
```bash
# Set access token (required)
set LINKEDIN_ACCESS_TOKEN=your_token_here

# Authenticate
python Skills/linkedin_watcher.py auth

# Poll once
python Skills/linkedin_watcher.py poll

# Start continuous monitoring
python Skills/linkedin_watcher.py start

# With custom vault path
python Skills/linkedin_watcher.py poll --vault-path "C:\MyVault"
```

---

## Agent Skills Commands

### Process WhatsApp Messages
```bash
# Process WhatsApp inbox
python Skills/agent_skills/process_whatsapp_messages.py

# Check results
dir WhatsApp_Outbox
```

### Process Gmail Messages
```bash
# Process Gmail (requires authentication)
python Skills/agent_skills/process_gmail_messages.py

# Check results
dir Inbox
```

### Auto-Post Social Media
```bash
# Test post (no approval)
python Skills/agent_skills/auto_post_social_media.py

# Approve and post
python Skills/agent_skills/auto_post_social_media.py --approve Social_Media_Tracking/social_media_approval_*.md
```

### Process All Channels
```bash
# Process all enabled channels
python Skills/agent_skills/process_all_channels.py

# Disable Gmail
python Skills/agent_skills/process_all_channels.py --no-gmail

# Disable WhatsApp
python Skills/agent_skills/process_all_channels.py --no-whatsapp

# Enable LinkedIn
python Skills/agent_skills/process_all_channels.py --linkedin

# Enable auto-respond (no approval)
python Skills/agent_skills/process_all_channels.py --auto

# Disable approval workflow
python Skills/agent_skills/process_all_channels.py --no-approval
```

---

## Test Commands

### Test All Skills
```bash
# Run skills test suite
python test_silver_tier_skills.py
```

### Test All Watchers
```bash
# Run watcher test suite
python test_watchers.py
```

---

## Python API Usage

### Import All Skills
```python
from Skills.agent_skills import (
    # Core Skills
    summarize_task,
    create_plan,
    draft_reply,
    generate_linkedin_post,
    
    # Integration Skills
    process_whatsapp_messages,
    process_gmail_messages,
    auto_post_social_media,
    approve_and_post,
    
    # Coordination Skills
    process_all_channels
)
```

### Process All Channels
```python
from Skills.agent_skills import process_all_channels

# Full processing with approval
results = process_all_channels(
    gmail_enabled=True,
    whatsapp_enabled=True,
    linkedin_enabled=False,
    auto_respond=False,
    require_approval=True
)

print(f"Tasks: {results['tasks_created']}")
print(f"Responses: {results['responses_generated']}")
```

### Use MCP Servers
```python
from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer
import asyncio

async def test():
    server = WhatsAppMCPServer()
    
    # Check status
    status = await server.execute_tool("check_whatsapp_status", {})
    print(status.text)
    
    # Read messages
    messages = await server.execute_tool(
        "read_whatsapp_messages",
        {"contact": "Anisa", "count": 5}
    )
    print(messages.text)
    
    # Send message
    result = await server.execute_tool(
        "send_whatsapp_message",
        {"recipient": "Anisa", "message": "Hello!"}
    )
    print(result.text)
    
    await server.cleanup()

asyncio.run(test())
```

### Use Watchers Directly
```python
from Skills.gmail_watcher import GmailWatcher, GmailWatcherConfig

# Create config
config = GmailWatcherConfig(
    polling_interval_ms=60000,  # 1 minute
    mark_as_read=True
)

# Create watcher
watcher = GmailWatcher(config)

# Authenticate
if watcher.authenticate():
    # Poll once
    stats = watcher.poll_once()
    print(f"Processed: {stats['processed']} emails")
```

---

## File Operations

### Check Inbox
```bash
# Gmail inbox
dir Inbox

# WhatsApp inbox
dir WhatsApp_Inbox

# Needs Action
dir Needs_Action

# Pending Approval
dir Pending_Approval
```

### Check Tracking
```bash
# Sent WhatsApp messages
dir WhatsApp_Sent

# Social media posts
dir Social_Media_Tracking

# Processed index
type .index\gmail-watcher-processed.json
```

---

## Configuration

### Gmail Config
```bash
# View config
type Skills/config/gmail_watcher_config.yaml

# Edit config
notepad Skills/config/gmail_watcher_config.yaml
```

### Environment Variables
```bash
# Set API keys
set OPENAI_API_KEY=your-api-key-here
set LINKEDIN_ACCESS_TOKEN=your-token-here

# View current vars
set | findstr API_KEY
set | findstr TOKEN
```

---

## Troubleshooting

### Check Dependencies
```bash
# List installed packages
pip list | findstr google
pip list | findstr playwright
pip list | findstr requests
```

### Re-authenticate
```bash
# Gmail (delete token first)
del config\gmail-token.json
python Skills/gmail_watcher.py auth

# WhatsApp (delete session first)
rmdir /s /q .whatsapp_session
python Skills/whatsapp_watcher.py auth
```

### Check Logs
```bash
# Gmail logs
type Logs\gmail_watcher\gmail-watcher.log

# WhatsApp logs
type Logs\whatsappwatcher\whatsapp_watcher.log

# LinkedIn logs
type Logs\linkedinwatcher\linkedin_watcher.log
```

---

## Quick Status Check

```bash
# Run all tests
python test_silver_tier_skills.py && python test_watchers.py

# Check all directories
dir Inbox && dir Needs_Action && dir WhatsApp_Inbox

# Check authentication
python Skills/gmail_watcher.py auth && python Skills/whatsapp_watcher.py status
```

---

**Silver Tier Quick Command Reference**  
*Version: 2.0.0-silver | Date: February 25, 2026*
