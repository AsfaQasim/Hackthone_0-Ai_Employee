# 🔗 LinkedIn Watcher - Complete Setup Guide

## Overview

The LinkedIn Watcher monitors your LinkedIn account for:
- Direct messages
- Connection requests
- Post engagement (likes, comments, shares)

It creates markdown files in your vault for important activities.

---

## ⚠️ Important: LinkedIn API Access

**Note**: LinkedIn API access requires approval from LinkedIn. The current implementation uses LinkedIn API v2.

### Option 1: Use LinkedIn API (Recommended for Production)

### Option 2: Manual Monitoring (For Testing/Demo)

For hackathon purposes, you can manually create LinkedIn inbox files similar to WhatsApp.

---

## Step 1: Get LinkedIn API Credentials

### 1.1 Create LinkedIn Developer Account

1. Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
2. Sign in with your LinkedIn account
3. Click "Create App" in the top right

### 1.2 Create LinkedIn App

Fill in the app details:
- **App Name**: AI Employee Watcher (or your choice)
- **LinkedIn Page**: Select a company page (or create one)
- **App Logo**: Upload optional logo
- **Website**: `https://localhost` (for testing)
- **Redirect URL**: `https://localhost:8080` (for OAuth)
- **App Description**: AI Employee integration for monitoring LinkedIn

### 1.3 Get OAuth 2.0 Credentials

After creating the app:
1. Go to "Auth" tab
2. Note your **Client ID**
3. Click "Generate" to create **Client Secret**
4. Save both credentials securely

### 1.4 Request API Permissions

For LinkedIn Watcher, you need these scopes:
- `r_liteprofile` - Basic profile information
- `r_emailaddress` - Email address
- `w_member_social` - Post and manage content
- `r_basicprofile` - Basic profile details

**Important**: Some permissions require LinkedIn verification and approval.

---

## Step 2: Get Access Token

### Method 1: OAuth 2.0 Authorization Code Flow (Recommended)

```bash
# Step 1: Authorization URL
# Open in browser:
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=https://localhost:8080&scope=r_liteprofile%20w_member_social

# Step 2: After authorization, you'll be redirected to:
# https://localhost:8080?code=AUTHORIZATION_CODE

# Step 3: Exchange code for access token
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -d "grant_type=authorization_code" \
  -d "code=AUTHORIZATION_CODE" \
  -d "redirect_uri=https://localhost:8080" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

### Method 2: Use Python Script (Easier)

Create a file `get_linkedin_token.py`:

```python
"""
Get LinkedIn Access Token
"""
import requests
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import threading

# Your app credentials
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8080"
SCOPES = "r_liteprofile w_member_social"

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        code = query_components.get("code", [None])[0]
        
        if code:
            # Exchange code for token
            response = requests.post(
                "https://www.linkedin.com/oauth/v2/accessToken",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": REDIRECT_URI,
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET
                }
            )
            
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get("access_token")
                
                print("\n" + "="*60)
                print("✅ SUCCESS! Your LinkedIn Access Token:")
                print("="*60)
                print(f"\n{access_token}\n")
                print("="*60)
                print("\nSave this token and set it as LINKEDIN_ACCESS_TOKEN")
                print("Example: set LINKEDIN_ACCESS_TOKEN=" + access_token)
            else:
                print(f"Error: {response.text}")
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Authorization Complete!</h1><p>You can close this window.</p></body></html>")

def start_server():
    server = HTTPServer(("localhost", 8080), CallbackHandler)
    server.handle_request()

# Open authorization URL
auth_url = (
    f"https://www.linkedin.com/oauth/v2/authorization?"
    f"response_type=code&client_id={CLIENT_ID}&"
    f"redirect_uri={REDIRECT_URI}&scope={SCOPES}"
)

print("Opening LinkedIn authorization page...")
webbrowser.open(auth_url)

# Start callback server
print("Waiting for authorization...")
server_thread = threading.Thread(target=start_server)
server_thread.start()
server_thread.join()
```

**Run the script**:
```bash
python get_linkedin_token.py
```

### Method 3: Use Online Tool (Quickest for Testing)

1. Go to [LinkedIn OAuth Tester](https://linkedin-oauth-tester.com/) (or similar tool)
2. Enter your Client ID and Secret
3. Get access token
4. Copy the token

---

## Step 3: Configure LinkedIn Watcher

### 3.1 Set Environment Variable

**Windows**:
```bash
set LINKEDIN_ACCESS_TOKEN=your_access_token_here
```

**Permanent (Windows)**:
1. Right-click "This PC" → Properties
2. Advanced System Settings → Environment Variables
3. Add new user variable:
   - Name: `LINKEDIN_ACCESS_TOKEN`
   - Value: `your_access_token_here`

**Linux/Mac**:
```bash
export LINKEDIN_ACCESS_TOKEN="your_access_token_here"
# Add to ~/.bashrc or ~/.zshrc for permanent
```

### 3.2 Verify Token

```bash
# Test authentication
cd F:\hackthone_0
python Skills/linkedin_watcher.py auth
```

Expected output:
```
✓ Authentication successful
Authenticated as: Your Name
```

---

## Step 4: Use LinkedIn Watcher

### 4.1 Check Status

```bash
# Authenticate and check connection
python Skills/linkedin_watcher.py auth
```

### 4.2 Poll Once

```bash
# Check for new LinkedIn activity
python Skills/linkedin_watcher.py poll
```

Expected output:
```
[LinkedInWatcher] INFO: Polling cycle initiated
[LinkedInWatcher] INFO: Found 3 new items
[LinkedInWatcher] INFO: Processing item: message_123 (Priority: high)
[LinkedInWatcher] INFO: Created inbox file: Inbox/20260225_12345_linkedin_message.md
[LinkedInWatcher] INFO: Polling cycle completed in 2.34s
```

### 4.3 Start Continuous Monitoring

```bash
# Monitor LinkedIn every 5 minutes
python Skills/linkedin_watcher.py start
```

To stop: Press `Ctrl+C`

### 4.4 Advanced Options

```bash
# Custom vault path
python Skills/linkedin_watcher.py poll --vault-path "C:\MyVault"

# Dry run (no file creation)
python Skills/linkedin_watcher.py poll --dry-run

# With access token directly
python Skills/linkedin_watcher.py poll --access-token "your_token_here"
```

---

## Step 5: Check Results

### 5.1 View Created Files

```bash
# Check Inbox
dir Inbox

# Check Needs_Action (high priority items)
dir Needs_Action

# View specific file
type Inbox\20260225_12345_linkedin_message.md
```

### 5.2 Example Output File

```markdown
---
type: linkedin_message
sender: "John Doe"
subject: "Re: Project Collaboration"
timestamp: "2026-02-25T12:34:56Z"
priority: "high"
status: "pending"
source: "linkedin"
item_id: "message_123"
---

# LinkedIn Message: Re: Project Collaboration

**From**: John Doe
**Priority**: 🔴 High
**Received**: 2026-02-25T12:34:56Z

## Message Content

Hi, I'd love to discuss the AI project opportunity...

---

## Action Items

- [ ] Review and respond to this message
- [ ] Check sender's profile

---

*Processed by LinkedIn Watcher v1.0.0*
```

---

## Step 6: Integration with AI Agent

### 6.1 Process LinkedIn with Other Channels

```python
from Skills.agent_skills import process_all_channels

# Process Gmail, WhatsApp, and LinkedIn together
results = process_all_channels(
    gmail_enabled=True,
    whatsapp_enabled=True,
    linkedin_enabled=True,  # Enable LinkedIn
    require_approval=True
)

print(f"LinkedIn items processed: {results['channels'].get('linkedin', {})}")
```

### 6.2 Process LinkedIn Messages Only

```python
from Skills.linkedin_watcher import LinkedInWatcher, LinkedInWatcherConfig

# Create config
config = LinkedInWatcherConfig(
    access_token="your_token_here",
    vault_path=".",
    polling_interval_ms=300000,  # 5 minutes
    monitor_messages=True,
    monitor_connections=True,
    monitor_engagement=True
)

# Create watcher
watcher = LinkedInWatcher(config)

# Authenticate
if watcher.authenticate():
    # Poll once
    stats = watcher.poll_once()
    print(f"LinkedIn stats: {stats}")
```

---

## Troubleshooting

### Issue 1: "No access token provided"

**Solution**:
```bash
# Set the token
set LINKEDIN_ACCESS_TOKEN=your_token_here

# Verify it's set
echo %LINKEDIN_ACCESS_TOKEN%
```

### Issue 2: "Authentication failed: 401"

**Causes**:
- Token expired
- Invalid token
- Wrong permissions

**Solution**:
1. Get new access token (they expire after 60 days)
2. Verify token is correct
3. Check app permissions in LinkedIn Developer Portal

### Issue 3: "Rate limit exceeded"

**Solution**:
- Wait 5-10 minutes before polling again
- LinkedIn has strict rate limits (100 requests/day for most endpoints)
- Increase polling interval in config

### Issue 4: "API not approved"

Some LinkedIn APIs require business verification:

**Solution**:
1. Complete LinkedIn app verification
2. Or use manual monitoring for hackathon demo
3. Or use alternative: manually create inbox files

---

## Alternative: Manual LinkedIn Monitoring (For Hackathon Demo)

If API access is not available, use manual monitoring:

### Create LinkedIn Inbox Files Manually

1. **Open LinkedIn** → Go to Messaging
2. **Copy message** from a connection
3. **Create file**: `Inbox/linkedin_message_from_JohnDoe.md`

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

4. **Process with AI**:
```python
from Skills.agent_skills import summarize_task, create_plan, draft_reply

# Summarize
summary = summarize_task("Inbox/linkedin_message_from_JohnDoe.md")

# Create plan
plan_path = create_plan("Inbox/linkedin_message_from_JohnDoe.md")

# Draft reply
reply = draft_reply("Inbox/linkedin_message_from_JohnDoe.md", tone="professional")
```

---

## Quick Reference

### Commands
```bash
# Set token
set LINKEDIN_ACCESS_TOKEN=your_token

# Authenticate
python Skills/linkedin_watcher.py auth

# Poll once
python Skills/linkedin_watcher.py poll

# Start monitoring
python Skills/linkedin_watcher.py start

# With options
python Skills/linkedin_watcher.py poll --vault-path "." --dry-run
```

### Environment
```bash
# Windows (temporary)
set LINKEDIN_ACCESS_TOKEN=your_token

# Windows (permanent)
System Properties → Environment Variables → Add LINKEDIN_ACCESS_TOKEN

# Linux/Mac
export LINKEDIN_ACCESS_TOKEN=your_token
# Add to ~/.bashrc for permanent
```

### Files
- **Script**: `Skills/linkedin_watcher.py`
- **Config**: Built-in (LinkedInWatcherConfig)
- **Logs**: `Logs/linkedinwatcher/linkedin_watcher.log`
- **Output**: `Inbox/` or `Needs_Action/`

---

## Next Steps

1. ✅ Get LinkedIn API credentials
2. ✅ Obtain access token
3. ✅ Set environment variable
4. ✅ Test authentication
5. ✅ Run poll command
6. ✅ Check created files
7. ✅ Integrate with AI agent

---

**LinkedIn Watcher Setup Guide**  
*Version: 1.0.0 | Date: February 25, 2026*

**Need Help?**  
Check logs: `type Logs\linkedinwatcher\linkedin_watcher.log`
