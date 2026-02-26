# 🔧 Gmail Watcher - Token Expired Fix

## Problem

Your Gmail refresh token has expired. This is normal - tokens expire after some time.

## ✅ Solution - Re-authenticate

### Step 1: Delete Old Token

```bash
del config\gmail-token.json
```

### Step 2: Run Authentication

```bash
python gmail_auth_simple.py
```

### Step 3: Authorize in Browser

1. Browser will open automatically
2. Sign in to your Gmail account
3. Click **"Allow"** to grant permissions
4. Browser will redirect to localhost (might show error - that's OK!)
5. Token is saved automatically

### Step 4: Verify

```bash
python Skills/gmail_watcher.py poll
```

---

## 🚀 Quick Commands

```bash
# Re-authenticate
del config\gmail-token.json
python gmail_auth_simple.py

# Test Gmail Watcher
python Skills/gmail_watcher.py poll

# Start monitoring
python Skills/gmail_watcher.py start
```

---

## ⚠️ If Browser Doesn't Open

Manual steps:

1. Open this URL in browser (replace CLIENT_ID with yours from config):
```
https://accounts.google.com/o/oauth2/auth?client_id=YOUR_CLIENT_ID&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://www.googleapis.com/auth/gmail.readonly+https://www.googleapis.com/auth/gmail.modify&response_type=code
```

2. Sign in and allow access
3. Copy the authorization code
4. Run the script with the code

---

## ✅ Current Status

| Component | Status |
|-----------|--------|
| Gmail Credentials | ✅ Exist |
| Gmail Token | ❌ Expired |
| WhatsApp | ✅ Working |
| LinkedIn Auto-Post | ✅ Working |
| Agent Skills | ✅ Working |

---

**Next: Run the authentication commands above!**
