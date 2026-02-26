# Gmail Authentication Guide (Urdu/English)

## Problem: Browser open hoti hai lekin emails show nahi ho rahi

Yeh OAuth authentication ka issue hai. Aapko pehle properly authenticate karna hoga.

---

## Solution: Step-by-Step Authentication

### Step 1: Check Credentials File

```bash
# Check if credentials file exists
dir config\gmail-credentials.json
```

**Agar file nahi hai**, toh pehle credentials download karo:

1. Go to: https://console.cloud.google.com/
2. Create new project (ya existing select karo)
3. Enable "Gmail API"
4. Create "OAuth 2.0 Client ID" credentials
5. Download as `gmail-credentials.json`
6. Save to: `config/gmail-credentials.json`

### Step 2: Run Simple Authentication

```bash
python gmail_auth_simple.py
```

Yeh script:
- ✅ Credentials check karega
- ✅ Browser automatically open karega
- ✅ Step-by-step guide dega
- ✅ Token save karega

### Step 3: Test Gmail Watcher

```bash
python Skills/gmail_watcher.py poll
```

---

## Detailed Steps (Agar credentials nahi hai)

### A. Google Cloud Console Setup

1. **Go to Google Cloud Console**
   - https://console.cloud.google.com/

2. **Create Project**
   - Click "Select a project" → "New Project"
   - Name: "AI Employee"
   - Click "Create"

3. **Enable Gmail API**
   - Go to "APIs & Services" → "Library"
   - Search "Gmail API"
   - Click "Enable"

4. **Configure OAuth Consent Screen**
   - Go to "APIs & Services" → "OAuth consent screen"
   - Select "External" (for personal use)
   - Fill in:
     - App name: "AI Employee"
     - User support email: Your email
     - Developer contact: Your email
   - Click "Save and Continue"
   - Skip "Scopes" (click "Save and Continue")
   - Add test users: Your Gmail address
   - Click "Save and Continue"

5. **Create Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "AI Employee Desktop"
   - Click "Create"
   - Click "Download JSON"
   - Save as: `config/gmail-credentials.json`

### B. Authenticate

```bash
# Run authentication
python gmail_auth_simple.py
```

Browser khulega:
1. Select your Google account
2. Click "Continue" (ignore warning if app is not verified)
3. Click "Allow" to grant permissions
4. Browser will show "Authentication successful"

### C. Test

```bash
# Test if working
python Skills/gmail_watcher.py poll
```

---

## Troubleshooting

### Issue 1: "Credentials file not found"

**Solution:**
```bash
# Create config folder
mkdir config

# Download credentials from Google Cloud Console
# Save as config/gmail-credentials.json
```

### Issue 2: "Browser opens but nothing happens"

**Solution:**
1. Close all browser windows
2. Run authentication again
3. Use a different browser (Chrome recommended)

### Issue 3: "Access blocked: This app isn't verified"

**Solution:**
1. Click "Advanced"
2. Click "Go to AI Employee (unsafe)"
3. Click "Allow"

This is normal for personal apps.

### Issue 4: "Token expired"

**Solution:**
```bash
# Delete old token
del config\gmail-token.json

# Re-authenticate
python gmail_auth_simple.py
```

### Issue 5: "No emails showing"

**Possible reasons:**
1. No unread emails in inbox
2. All emails already processed
3. Emails don't match importance criteria

**Check:**
```bash
# Check if any unread emails exist
python -c "from googleapiclient.discovery import build; from google.oauth2.credentials import Credentials; creds = Credentials.from_authorized_user_file('config/gmail-token.json'); service = build('gmail', 'v1', credentials=creds); print(service.users().messages().list(userId='me', q='is:unread').execute())"
```

---

## Quick Test Script

Create `test_gmail.py`:

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load credentials
creds = Credentials.from_authorized_user_file('config/gmail-token.json')
service = build('gmail', 'v1', credentials=creds)

# Get profile
profile = service.users().getProfile(userId='me').execute()
print(f"Email: {profile['emailAddress']}")
print(f"Total messages: {profile['messagesTotal']}")

# Get unread count
unread = service.users().messages().list(userId='me', q='is:unread').execute()
print(f"Unread messages: {len(unread.get('messages', []))}")
```

Run:
```bash
python test_gmail.py
```

---

## Current Status Check

Run this to check your current status:

```bash
# Check if credentials exist
dir config\gmail-credentials.json

# Check if token exists
dir config\gmail-token.json

# If both exist, test authentication
python gmail_auth_simple.py
```

---

## Summary

**Problem**: OAuth flow starts but emails don't show

**Solution**:
1. ✅ Get credentials from Google Cloud Console
2. ✅ Save as `config/gmail-credentials.json`
3. ✅ Run `python gmail_auth_simple.py`
4. ✅ Allow permissions in browser
5. ✅ Test with `python Skills/gmail_watcher.py poll`

**Next Steps**:
1. Complete authentication
2. Test Gmail watcher
3. Your Bronze Tier is already complete!

---

**Need Help?**
- Check if `config/gmail-credentials.json` exists
- Run `python gmail_auth_simple.py` for guided setup
- Check logs in `Logs/gmail_watcher/`
