# Gmail Authentication Fix (Urdu)

## Problem
Browser open hoti hai lekin authentication complete nahi hota aur emails show nahi hoti.

## Solution

### Quick Fix (Recommended)

```bash
python gmail_auth_fix.py
```

Yeh script:
1. ✅ Purana token delete karega (agar hai)
2. ✅ Browser automatically open karega
3. ✅ Step-by-step guide dega
4. ✅ Authentication complete karega
5. ✅ Token save karega
6. ✅ Test karega ke sab kaam kar raha hai

### Steps

1. **Run authentication script**
   ```bash
   python gmail_auth_fix.py
   ```

2. **Browser mein:**
   - Google account select karo
   - "Continue" click karo (warning ignore karo)
   - "Allow" click karo permissions ke liye
   - "Authentication successful" message dikhe ga

3. **Test karo**
   ```bash
   python Skills/gmail_watcher.py poll
   ```

---

## Agar Browser Nahi Khulta

Agar browser automatically nahi khulta, toh:

1. Script URL show karega
2. URL copy karo
3. Manually browser mein paste karo
4. Authentication complete karo

---

## Common Issues

### Issue 1: "This app isn't verified"

**Normal hai!** Yeh aapka personal app hai.

**Solution:**
1. Click "Advanced"
2. Click "Go to [App Name] (unsafe)"
3. Click "Allow"

### Issue 2: "Access blocked"

**Reason:** OAuth consent screen properly configured nahi hai.

**Solution:**
1. Go to: https://console.cloud.google.com/
2. APIs & Services → OAuth consent screen
3. Add your email as "Test user"
4. Try authentication again

### Issue 3: "Port already in use"

**Solution:**
```bash
# Kill process on port 8080
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Try again
python gmail_auth_fix.py
```

---

## Verification

Authentication successful hai ya nahi check karne ke liye:

```bash
# Check if token exists
dir config\gmail-token.json

# If exists, test it
python -c "from google.oauth2.credentials import Credentials; from googleapiclient.discovery import build; creds = Credentials.from_authorized_user_file('config/gmail-token.json'); service = build('gmail', 'v1', credentials=creds); profile = service.users().getProfile(userId='me').execute(); print(f'Email: {profile[\"emailAddress\"]}')"
```

---

## After Authentication

Jab authentication complete ho jaye:

1. **Test Gmail Watcher**
   ```bash
   python Skills/gmail_watcher.py poll
   ```

2. **Check Inbox folder**
   ```bash
   dir Inbox
   ```

3. **Your Bronze Tier is complete!** ✅

---

## Summary

**Current Issue:** Browser opens but authentication doesn't complete

**Solution:** Run `python gmail_auth_fix.py`

**Expected Result:**
- ✅ Browser opens
- ✅ You login and allow permissions
- ✅ Token saved to `config/gmail-token.json`
- ✅ Gmail Watcher works

**Next:** Test with `python Skills/gmail_watcher.py poll`

---

**Aapka Bronze Tier already complete hai!** Gmail authentication sirf testing ke liye hai.
