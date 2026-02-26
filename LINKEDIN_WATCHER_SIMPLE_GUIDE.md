# 🔗 LinkedIn Watcher - Simple Setup Guide

## Quick Start (3 Steps)

### Step 1: Get LinkedIn Access Token

**Option A: Use Token Helper Script** (Recommended)

```bash
# 1. Edit get_linkedin_token.py and add your credentials
#    - CLIENT_ID = "your_client_id"
#    - CLIENT_SECRET = "your_client_secret"

# 2. Run the script
python get_linkedin_token.py

# 3. Follow browser prompts and copy the token
```

**Option B: Manual Setup** (If you already have a token)

```bash
# Set token directly
set LINKEDIN_ACCESS_TOKEN=your_token_here
```

**Option C: No API Access** (For hackathon demo)

Manually create LinkedIn inbox files (see "Manual Mode" below).

---

### Step 2: Set Environment Variable

**Windows (Command Prompt)**:
```bash
set LINKEDIN_ACCESS_TOKEN=your_token_here
```

**Windows (PowerShell)**:
```powershell
$env:LINKEDIN_ACCESS_TOKEN="your_token_here"
```

**Permanent (Windows)**:
1. Press `Win + R`
2. Type `sysdm.cpl` and press Enter
3. Click "Environment Variables"
4. Under "User variables", click "New"
5. Name: `LINKEDIN_ACCESS_TOKEN`
6. Value: `your_token_here`
7. Click OK

---

### Step 3: Test LinkedIn Watcher

```bash
# Test setup
python test_linkedin_setup.py

# Authenticate
python Skills/linkedin_watcher.py auth

# Poll once (check for new activity)
python Skills/linkedin_watcher.py poll

# Start continuous monitoring (every 5 minutes)
python Skills/linkedin_watcher.py start
```

---

## Detailed Setup Instructions

### Getting LinkedIn API Credentials

#### 1. Create LinkedIn Developer Account

1. Go to https://www.linkedin.com/developers/
2. Sign in with your LinkedIn account
3. Accept the terms

#### 2. Create LinkedIn App

1. Click "Create app" button
2. Fill in the form:
   - **App Name**: `AI Employee` (or any name)
   - **LinkedIn Page**: Choose a page (or create one)
   - **Logo**: Optional
   - **Website**: `https://localhost`
   - **Redirect URL**: `http://localhost:8080`
   - **Description**: `AI Employee integration`
3. Click "Create app"

#### 3. Get Credentials

1. Go to "Auth" tab
2. Copy **Client ID**
3. Click "Generate" next to **Client Secret**
4. Copy **Client Secret**
5. Save both somewhere safe

#### 4. Configure Token Helper

Edit `get_linkedin_token.py`:

```python
# Replace these lines:
CLIENT_ID = "YOUR_CLIENT_ID_HERE"
CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"

# With your actual credentials:
CLIENT_ID = "1234567890abcdef"
CLIENT_SECRET = "AbCdEfGhIjKlMnOp"
```

#### 5. Get Access Token

```bash
python get_linkedin_token.py
```

This will:
1. Open your browser
2. Ask you to sign in to LinkedIn
3. Ask you to authorize the app
4. Display your access token in the terminal

**Copy the token!**

---

## Using LinkedIn Watcher

### Basic Commands

```bash
# Check authentication
python Skills/linkedin_watcher.py auth

# Check for new LinkedIn activity
python Skills/linkedin_watcher.py poll

# Start monitoring (runs continuously)
python Skills/linkedin_watcher.py start

# Stop monitoring
# Press Ctrl+C
```

### Advanced Commands

```bash
# Custom vault path
python Skills/linkedin_watcher.py poll --vault-path "C:\MyVault"

# Dry run (no file creation)
python Skills/linkedin_watcher.py poll --dry-run

# Use token directly (without environment variable)
python Skills/linkedin_watcher.py poll --access-token "your_token_here"
```

---

## Manual Mode (No API Required)

For hackathon demo, you can manually create LinkedIn inbox files:

### Step 1: Create LinkedIn Inbox File

Create file: `Inbox/linkedin_message_from_JohnDoe.md`

```markdown
---
type: linkedin_message
sender: "John Doe"
sender_headline: "CEO at Tech Corp"
subject: "Partnership Opportunity"
timestamp: "2026-02-25T12:00:00Z"
priority: "high"
status: "pending"
source: "linkedin_manual"
---

# LinkedIn Message: Partnership Opportunity

**From**: John Doe, CEO at Tech Corp
**Priority**: 🔴 High

## Message

Hi, I saw your AI automation project and would like to discuss a partnership...

---

## Action Items

- [ ] Review partnership opportunity
- [ ] Check sender's profile
- [ ] Draft response

---

*Manually created from LinkedIn*
```

### Step 2: Process with AI

```python
from Skills.agent_skills import summarize_task, create_plan, draft_reply

# Summarize
summary = summarize_task("Inbox/linkedin_message_from_JohnDoe.md")
print(f"Summary: {summary}")

# Create plan
plan_path = create_plan("Inbox/linkedin_message_from_JohnDoe.md")
print(f"Plan created: {plan_path}")

# Draft reply
reply = draft_reply("Inbox/linkedin_message_from_JohnDoe.md", tone="professional")
print(f"Draft reply:\n{reply}")
```

---

## Integration with AI Agent

### Process All Channels (Including LinkedIn)

```python
from Skills.agent_skills import process_all_channels

# Process Gmail, WhatsApp, and LinkedIn together
results = process_all_channels(
    gmail_enabled=True,
    whatsapp_enabled=True,
    linkedin_enabled=True,
    require_approval=True
)

print(f"Tasks created: {results['tasks_created']}")
```

### Process LinkedIn Only

```python
from Skills.linkedin_watcher import LinkedInWatcher, LinkedInWatcherConfig
import os

# Get token from environment
token = os.getenv("LINKEDIN_ACCESS_TOKEN")

# Create config
config = LinkedInWatcherConfig(
    access_token=token,
    vault_path=".",
    polling_interval_ms=300000,  # 5 minutes
    monitor_messages=True,
    monitor_connections=True,
    monitor_engagement=True
)

# Create and run watcher
watcher = LinkedInWatcher(config)

if watcher.authenticate():
    stats = watcher.poll_once()
    print(f"LinkedIn stats: {stats}")
```

---

## Troubleshooting

### Problem: "LINKEDIN_ACCESS_TOKEN not set"

**Solution**:
```bash
# Set the token
set LINKEDIN_ACCESS_TOKEN=your_token_here

# Verify
echo %LINKEDIN_ACCESS_TOKEN%
```

### Problem: "Authentication failed: 401"

**Causes**:
- Token is invalid
- Token has expired
- Wrong credentials

**Solution**:
1. Get new token: `python get_linkedin_token.py`
2. Verify credentials in LinkedIn Developer Portal
3. Check app permissions

### Problem: "API not approved"

LinkedIn requires app verification for some endpoints.

**Solution**:
- Use manual mode for hackathon demo
- Or complete LinkedIn app verification process
- Or use basic profile endpoints only

### Problem: "Rate limit exceeded"

**Solution**:
- Wait 5-10 minutes
- LinkedIn has daily limits (100-500 requests/day)
- Increase polling interval

---

## Testing

### Run Test Suite

```bash
# Quick setup test
python test_linkedin_setup.py

# Full watcher test
python test_watchers.py
```

### Expected Output

```
[TEST 1] Checking LINKEDIN_ACCESS_TOKEN...
  [OK] Token found: abc123...xyz

[TEST 2] Importing LinkedIn Watcher...
  [OK] Import successful

[TEST 3] Creating configuration...
  [OK] Configuration created

[TEST 4] Creating watcher instance...
  [OK] Watcher created

[TEST 5] Checking watcher methods...
  [OK] authenticate()
  [OK] check_for_new_items()
  [OK] get_item_content()
  [OK] is_important()
  [OK] detect_priority()
  [OK] generate_markdown()
  [OK] poll_once()
  [OK] start()

[SUCCESS] LinkedIn Watcher is ready!
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `Skills/linkedin_watcher.py` | Main watcher implementation |
| `get_linkedin_token.py` | Token helper script |
| `test_linkedin_setup.py` | Setup test script |
| `LINKEDIN_WATCHER_SETUP.md` | Detailed documentation |
| `Logs/linkedinwatcher/` | Log files |

---

## Quick Command Reference

```bash
# Get token
python get_linkedin_token.py

# Set token
set LINKEDIN_ACCESS_TOKEN=your_token

# Test setup
python test_linkedin_setup.py

# Authenticate
python Skills/linkedin_watcher.py auth

# Poll once
python Skills/linkedin_watcher.py poll

# Start monitoring
python Skills/linkedin_watcher.py start

# Process all channels
python Skills/agent_skills/process_all_channels.py
```

---

## Next Steps

1. ✅ Get LinkedIn API credentials
2. ✅ Run `python get_linkedin_token.py`
3. ✅ Set `LINKEDIN_ACCESS_TOKEN` environment variable
4. ✅ Test: `python test_linkedin_setup.py`
5. ✅ Poll: `python Skills/linkedin_watcher.py poll`
6. ✅ Integrate: Use with `process_all_channels`

---

**LinkedIn Watcher - Simple Setup Guide**  
*Version: 1.0.0 | Date: February 25, 2026*

**Need Help?**  
- Check logs: `type Logs\linkedinwatcher\linkedin_watcher.log`
- Read full docs: `LINKEDIN_WATCHER_SETUP.md`
- Run tests: `python test_linkedin_setup.py`
