# 🥈 Silver Tier Skills - Quick Reference

## Import All Skills

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

---

## Core Skills (Bronze/Silver)

### summarize_task
```python
summary = summarize_task(
    task_filepath="Inbox/email_20260225.md",
    max_length=200,
    model_name="gpt-4"
)
```

### create_plan
```python
plan_path = create_plan(
    task_filepath="Inbox/email_20260225.md",
    output_dir="Plans",
    model_name="gpt-4"
)
```

### draft_reply
```python
reply = draft_reply(
    task_filepath="Inbox/email_20260225.md",
    tone="professional",  # professional, friendly, formal, casual
    model_name="gpt-4"
)
```

### generate_linkedin_post
```python
post = generate_linkedin_post(
    topic="AI automation in business",
    style="thought-leadership",  # professional, casual, thought-leadership, storytelling
    include_hashtags=True,
    max_length=3000,
    model_name="gpt-4"
)
```

---

## Integration Skills (Silver)

### process_whatsapp_messages
```python
results = process_whatsapp_messages(
    inbox_dir="WhatsApp_Inbox",
    outbox_dir="WhatsApp_Outbox",
    model_name="gpt-4"
)

for result in results:
    print(f"Contact: {result['contact']}")
    print(f"Response: {result['output_file']}")
```

### process_gmail_messages
```python
results = process_gmail_messages(
    credentials_path="config/gmail-credentials.json",
    token_path="config/gmail-token.json",
    output_dir="Inbox",
    max_results=10,
    model_name="gpt-4"
)

for result in results:
    print(f"[{result['priority'].upper()}] {result['subject']}")
    print(f"Task file: {result['task_file']}")
```

### auto_post_social_media
```python
# Direct posting (no approval)
result = auto_post_social_media(
    content="Excited to share our AI breakthrough! 🚀",
    platforms=['linkedin', 'twitter'],
    schedule=False,
    require_approval=False,
    vault_path="."
)

# With approval workflow
result = auto_post_social_media(
    content="Product launch announcement",
    platforms=['linkedin', 'facebook', 'instagram'],
    require_approval=True  # Creates approval file
)

if result['status'] == 'pending_approval':
    print(f"Approval file: {result['approval_file']}")
    # Review file, set status to 'approved', then:
    approve_and_post(result['approval_file'])
```

### process_all_channels
```python
# Process all enabled channels
results = process_all_channels(
    gmail_enabled=True,
    whatsapp_enabled=True,
    linkedin_enabled=False,
    auto_respond=False,
    require_approval=True,
    vault_path="."
)

print(f"Tasks created: {results['tasks_created']}")
print(f"Responses generated: {results['responses_generated']}")

# Check channel status
for channel, data in results['channels'].items():
    print(f"{channel}: {data['status']}")
```

---

## MCP Servers (Action Layer)

### WhatsApp MCP Server
```python
from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer
import asyncio

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
    {"recipient": "Anisa", "message": "Hello from AI!"}
)
print(result.text)

await server.cleanup()
```

### Email MCP Server
```python
from Skills.mcp_servers.email_mcp_server import EmailMCPServer
import asyncio

server = EmailMCPServer()

result = await server.execute_tool(
    "send_email",
    {
        "to": "recipient@example.com",
        "subject": "Test Email",
        "body": "This is a test email from MCP Server",
        "cc": ["cc@example.com"],
        "html": False
    }
)
print(result.text)
```

### Social Media MCP Server
```python
from Skills.mcp_servers.social_media_mcp_server import SocialMediaMCPServer
import asyncio

server = SocialMediaMCPServer()

# LinkedIn
result = await server.execute_tool(
    "post_to_linkedin",
    {
        "content": "Professional update 🚀",
        "visibility": "public",
        "media_url": "https://example.com/image.jpg"
    }
)
print(result.text)

# Facebook
result = await server.execute_tool(
    "post_to_facebook",
    {
        "content": "Casual update",
        "visibility": "friends"
    }
)

# Instagram
result = await server.execute_tool(
    "post_to_instagram",
    {
        "caption": "Instagram caption",
        "media_url": "https://example.com/photo.jpg",
        "location": "New York"
    }
)

# Twitter
result = await server.execute_tool(
    "post_to_twitter",
    {
        "content": "Tweet content (max 280 chars)",
        "media_url": "https://example.com/image.jpg"
    }
)
```

---

## Command Line Usage

### Process WhatsApp Messages
```bash
python Skills/agent_skills/process_whatsapp_messages.py
```

### Process Gmail Messages
```bash
python Skills/agent_skills/process_gmail_messages.py
```

### Auto-Post Social Media
```bash
# Test post
python Skills/agent_skills/auto_post_social_media.py

# Approve and post
python Skills/agent_skills/auto_post_social_media.py --approve Social_Media_Tracking/social_media_approval_*.md
```

### Process All Channels
```bash
# Default (all enabled, approval required)
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

## Workflow Examples

### Workflow 1: Email → Task → Plan → Reply
```python
from Skills.agent_skills import (
    process_gmail_messages,
    summarize_task,
    create_plan,
    draft_reply
)

# 1. Process Gmail
results = process_gmail_messages()

# 2. For each task, create summary and plan
for result in results:
    if result['status'] == 'success':
        task_file = result['task_file']
        
        # Summarize
        summary = summarize_task(task_file)
        print(f"Summary: {summary}")
        
        # Create plan
        plan_path = create_plan(task_file)
        print(f"Plan: {plan_path}")
        
        # Draft reply
        reply = draft_reply(task_file, tone="professional")
        print(f"Reply drafted")
```

### Workflow 2: WhatsApp → AI Response → Send
```python
from Skills.agent_skills import (
    process_whatsapp_messages,
    process_all_channels
)

# Option 1: Process WhatsApp only
results = process_whatsapp_messages()

# Option 2: Full coordination with auto-respond
results = process_all_channels(
    gmail_enabled=False,
    whatsapp_enabled=True,
    auto_respond=True,
    require_approval=False
)
```

### Workflow 3: Multi-Channel → Approval → Post
```python
from Skills.agent_skills import auto_post_social_media

# Create content
content = "Major product announcement coming soon! 🚀"

# Post with approval
result = auto_post_social_media(
    content=content,
    platforms=['linkedin', 'twitter', 'facebook'],
    require_approval=True
)

# Check approval status
if result['status'] == 'pending_approval':
    print(f"Review: {result['approval_file']}")
    # Manually review and approve the file
    # Then run:
    # approve_and_post(result['approval_file'])
```

---

## Configuration

### Environment Variables
```bash
# AI Model API
export OPENAI_API_KEY="your-api-key-here"

# Gmail OAuth (automatic via auth flow)
# LinkedIn API
export LINKEDIN_ACCESS_TOKEN="your-token-here"

# Facebook API
export FACEBOOK_ACCESS_TOKEN="your-token-here"

# Twitter API
export TWITTER_API_KEY="your-api-key-here"
export TWITTER_API_SECRET="your-api-secret-here"
export TWITTER_ACCESS_TOKEN="your-access-token-here"
```

### File Structure
```
F:\hackthone_0\
├── config/
│   ├── gmail-credentials.json
│   └── gmail-token.json
├── WhatsApp_Inbox/
├── WhatsApp_Outbox/
├── WhatsApp_Sent/
├── Inbox/
├── Needs_Action/
├── Plans/
├── Social_Media_Tracking/
└── Skills/
    ├── agent_skills/
    └── mcp_servers/
```

---

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Gmail auth failed | `python Skills/gmail_watcher.py auth` |
| WhatsApp session expired | `python Skills/whatsapp_watcher.py auth` |
| Module not found | Ensure in `F:\hackthone_0\` directory |
| API key missing | Set `OPENAI_API_KEY` environment variable |
| Import error | Check `PYTHONPATH` includes `Skills/` |

---

## Testing Commands

```bash
# Test all skills
python -c "from Skills.agent_skills import *; print('All skills imported successfully')"

# Test WhatsApp processing
python Skills/agent_skills/process_whatsapp_messages.py

# Test Gmail processing
python Skills/agent_skills/process_gmail_messages.py

# Test social media posting
python Skills/agent_skills/auto_post_social_media.py

# Test full coordination
python Skills/agent_skills/process_all_channels.py
```

---

**Silver Tier Skills - Quick Reference**  
*Version: 2.0.0-silver | Date: February 25, 2026*
