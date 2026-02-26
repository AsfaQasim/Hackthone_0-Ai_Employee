# WhatsApp Watcher Test Guide

## Overview
The WhatsApp Watcher monitors WhatsApp Web for important messages and creates markdown files in your vault.

## Prerequisites

### 1. Install Playwright
```bash
pip install playwright
playwright install chromium
```

### 2. Verify Installation
Check if playwright is installed:
```bash
python -c "from playwright.sync_api import sync_playwright; print('Playwright OK')"
```

## How WhatsApp Watcher Works

1. **Authentication**: Opens WhatsApp Web in a browser
   - First run: You scan QR code
   - Subsequent runs: Uses saved session

2. **Monitoring**: Checks for unread chats with important keywords
   - Default keywords: 'urgent', 'asap', 'invoice', 'payment', 'help', 'important'

3. **Processing**: Creates markdown files for important messages
   - High priority → Needs_Action folder
   - Low priority → Inbox folder

## Testing Steps

### Step 1: Authenticate
```bash
python Skills/whatsapp_watcher.py auth
```

This will:
- Open a browser window
- Show WhatsApp Web QR code
- Wait for you to scan (5 minutes timeout)
- Save session to `.whatsapp_session` folder

### Step 2: Test Poll (Dry Run)
```bash
python Skills/whatsapp_watcher.py poll --dry-run
```

This will:
- Check for unread messages
- Filter by keywords
- Show what files would be created
- NOT actually create files

### Step 3: Real Poll
```bash
python Skills/whatsapp_watcher.py poll
```

This will:
- Check for unread messages
- Create markdown files for important ones
- Save to Inbox or Needs_Action folders

### Step 4: Continuous Monitoring
```bash
python Skills/whatsapp_watcher.py start
```

This will:
- Run continuously
- Check every 30 seconds (default)
- Process new messages automatically

## Configuration

You can customize the watcher:

```python
config = WhatsAppWatcherConfig(
    session_path=".whatsapp_session",
    keywords=['urgent', 'asap', 'invoice', 'payment', 'help', 'important'],
    polling_interval_ms=30000,  # 30 seconds
    vault_path=".",
    dry_run=False
)
```

## Expected Output

### Successful Authentication
```
✓ Authentication successful
Session saved to: .whatsapp_session
```

### Poll Results
```
Poll Results:
  Retrieved: 5
  Processed: 2
  Filtered: 3
  Created: 2
  Errors: 0
```

## Markdown File Format

Created files look like:

```markdown
---
type: whatsapp_message
chat_name: "John Doe"
timestamp: "2026-02-21T15:30:00Z"
priority: "high"
status: "pending"
source: "whatsapp"
---

# WhatsApp: John Doe

**Priority**: 🔴 High
**Received**: 2026-02-21T15:30:00Z
**Source**: WhatsApp Web

## Recent Messages

> Hey, this is urgent!
> Need your help ASAP

---

## Action Items

- [ ] Review and respond to this message
- [ ] Check if any follow-up is needed
```

## Troubleshooting

### Playwright Not Installed
```
Error: Playwright not installed
Solution: pip install playwright && playwright install chromium
```

### QR Code Timeout
```
Error: Timeout waiting for QR code scan
Solution: Run 'auth' command again and scan within 5 minutes
```

### Session Expired
```
Error: Authentication failed
Solution: Delete .whatsapp_session folder and run 'auth' again
```

### No Messages Found
- Check if you have unread messages in WhatsApp
- Verify messages contain your keywords
- Try with --dry-run to see what's being filtered

## Important Notes

⚠️ **WhatsApp Terms of Service**: This uses browser automation which may violate WhatsApp's terms. Use at your own risk.

⚠️ **Session Security**: The `.whatsapp_session` folder contains your login session. Keep it secure!

⚠️ **Rate Limiting**: Don't poll too frequently to avoid being flagged by WhatsApp.

## Next Steps

After testing WhatsApp watcher, you can:
1. Integrate it with the scheduler
2. Add it to the main loop
3. Customize keywords for your needs
4. Set up approval workflow
